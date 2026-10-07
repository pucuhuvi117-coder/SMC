#!/usr/bin/env python3
"""Assemble SMC Visualizer Pro from modular sources into a single Pine Script file.

Pine Script has no include mechanism and the published script must be a single
file (docs/02-architecture.md §4.11, ADR-04). Sources live in src/ as ordered
fragments; this script concatenates them, stamps the version and build date,
runs project lint rules and, when available, a syntax check with pynescript.

Two indicators are built from the same sources (ADR-13): `core` (SMC Visualizer Pro) and
`setups` (SMC Pro · Setups). Code that belongs to one of them only is fenced in the modules:

    //#if setups        (or //#if core)
    ...
    //#else             (optional)
    ...
    //#endif

Flags come from build/targets.json; blocks do not nest.

Usage:
    python3 build/build.py                 # build every target
    python3 build/build.py --check         # build + syntax check (needs pynescript, ~3 min per target)
    python3 build/build.py --target NAME   # build one target from targets.json

Environment:
    PINE_PARSER_PYTHON  Python interpreter that has `pynescript` installed
                        (defaults to the current interpreter).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
TARGETS = ROOT / "build" / "targets.json"

# Compile budget per target (risk T-01, ADR-13). Measured in TradingView: ~30k tokens
# compile in about a minute, ~40k tokens hit "Pine compilation was timed out" (2 min).
# Compile time grows faster than linearly with size, so each indicator stays well below.
WARN_LINES = 4000
WARN_TOKENS = 34000

TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_.]*|\d+\.?\d*|==|!=|<=|>=|:=|=>|[^\s\w]")


def read_version() -> str:
    return (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def strip_comment(line: str) -> str:
    """Drop a trailing // comment, ignoring // inside string literals."""
    out = []
    quote = None
    i = 0
    while i < len(line):
        ch = line[i]
        if quote:
            out.append(ch)
            if ch == "\\" and i + 1 < len(line):
                out.append(line[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
        else:
            if ch in ('"', "'"):
                quote = ch
            elif line.startswith("//", i):
                break
            out.append(ch)
        i += 1
    return "".join(out)


RESERVED = "text|line|label|box|table|color|array|map|matrix|polyline|linefill|string|int|float|bool|const|simple|series"
DIRECTIVE_RE = re.compile(r"^\s*//#(if|else|endif)\b\s*(!?\w*)\s*$")


def preprocess(name: str, text: str, flags: set[str]) -> tuple[str, list[str]]:
    """Keep the lines of `//#if flag` blocks whose flag is set for the target; drop the directives."""
    out, issues = [], []
    state = None  # None outside a block, else [keep_if_branch, in_else]
    for n, raw in enumerate(text.splitlines(), 1):
        m = DIRECTIVE_RE.match(raw)
        if m:
            kind, arg = m.group(1), m.group(2)
            if kind == "if":
                if state is not None:
                    issues.append(f"{name}:{n}: nested //#if is not supported")
                neg = arg.startswith("!")
                flag = arg.lstrip("!")
                if not flag:
                    issues.append(f"{name}:{n}: //#if needs a flag")
                state = [(flag in flags) != neg, False]
            elif kind == "else":
                if state is None or state[1]:
                    issues.append(f"{name}:{n}: //#else without //#if")
                else:
                    state[1] = True
            else:
                if state is None:
                    issues.append(f"{name}:{n}: //#endif without //#if")
                state = None
            continue
        if state is None or state[0] != state[1]:
            out.append(raw)
    if state is not None:
        issues.append(f"{name}: //#if is not closed")
    return "\n".join(out) + "\n", issues


def has_open_quote(line: str) -> bool:
    """True if a string literal is still open at the end of the line."""
    quote = None
    i = 0
    while i < len(line):
        ch = line[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in ('"', "'"):
            quote = ch
        i += 1
    return quote is not None


DECL_TYPES = r"(?:int|float|bool|string|color|line|box|label|table|array<[^>]+>|map<[^>]+>|[A-Z]\w*)"


def lint_shadowing(body: str) -> list[str]:
    """A local variable named like a global one triggers CW10013 in TradingView (caught in v0.4: `body`)."""
    lines = body.splitlines()
    glob: set[str] = set()
    for raw in lines:
        code = strip_comment(raw)
        if not code or code[0] in " \t" or code.startswith(("enum ", "type ", "//")):
            continue
        m = re.match(r"^(?:var\s+)?(?:" + DECL_TYPES + r"\s+)?([A-Za-z_]\w*)\s*=(?!=|>)", code)
        if m:
            glob.add(m.group(1))
        m = re.match(r"^\[([^\]]+)\]\s*=", code)
        if m:
            glob.update(x.strip() for x in m.group(1).split(","))
    issues = []
    skip_block = False  # indented members of `type` / `enum` are fields, not variables
    fn = "<global block>"
    for n, raw in enumerate(lines, 1):
        code = strip_comment(raw)
        if not code.strip():
            continue
        if code[0] not in " \t":
            skip_block = code.startswith(("enum ", "type "))
            mm = re.match(r"^([A-Za-z_]\w*)\s*\(.*\)\s*=>", code)
            fn = mm.group(1) if mm else "<global block>"
            continue
        if skip_block:
            continue
        names = []
        m = re.match(r"^\s+(?:var\s+)?(?:" + DECL_TYPES + r"\s+)?([A-Za-z_]\w*)\s*=(?!=|>)", code)
        if m:
            names.append(m.group(1))
        m = re.match(r"^\s+\[([^\]]+)\]\s*=", code)
        if m:
            names += [x.strip() for x in m.group(1).split(",")]
        for nm in names:
            if nm in glob:
                issues.append(f"dist:{n}: local `{nm}` in {fn} shadows a global of the same name (CW10013); rename it")
    return issues


def lint_inputs(body: str) -> list[str]:
    """Settings dialog order: one `inline` row and one `group` must be declared without gaps
    (v0.8.1: the Setup panel position sat below the alert inputs)."""
    issues = []
    prev_inline = prev_group = None
    seen_inline: set[str] = set()
    seen_group: set[str] = set()
    for n, raw in enumerate(body.splitlines(), 1):
        code = strip_comment(raw)
        if not re.match(r"^\w+\s*=\s*input\.\w+\(", code):
            continue
        il = re.search(r"\binline\s*=\s*\"([^\"]*)\"", code)
        gr = re.search(r"\bgroup\s*=\s*(\w+|\"[^\"]*\")", code)
        il = il.group(1) if il else None
        gr = gr.group(1) if gr else None
        if il is not None and il != prev_inline and il in seen_inline:
            issues.append(f"dist:{n}: input row inline=\"{il}\" is split by other inputs; declare its inputs one after another")
        if gr is not None and gr != prev_group and gr in seen_group:
            issues.append(f"dist:{n}: input group {gr} is split by other groups; declare its inputs one after another")
        if il is not None:
            seen_inline.add(il)
        if gr is not None:
            seen_group.add(gr)
        prev_inline, prev_group = il, gr
    return issues


def lint(name: str, text: str) -> list[str]:
    """Project rules from docs/02-architecture.md §20.8 and docs/09-master-checklist.md."""
    issues = []
    for n, raw in enumerate(text.splitlines(), 1):
        code = strip_comment(raw)
        where = f"{name}:{n}"
        if "\t" in raw:
            issues.append(f"{where}: tab character (use 4 spaces)")
        if re.search(r"\bvarip\b", code):
            issues.append(f"{where}: varip is forbidden in logic (ADR-10)")
        if re.search(r"\btimenow\b", code):
            issues.append(f"{where}: timenow is forbidden in logic (§20.8)")
        # Reading the visible range makes TradingView re-run the whole script on every scroll / zoom (v0.6)
        if re.search(r"\bchart\.(left|right)_visible_bar_time\b", code):
            issues.append(f"{where}: chart.left/right_visible_bar_time re-runs the script on every scroll and zoom (v0.6, ADR-14)")
        # The [1] offset may live inside the requested function; such lines must say so explicitly
        if "lookahead_on" in code and "[1]" not in code and "no-repaint:" not in raw:
            issues.append(f"{where}: lookahead_on without [1] offset or a `// no-repaint:` note (repaint, §4.7)")
        # A string literal cannot span lines in Pine (caught in v0.4: a tooltip broken after `"`)
        if has_open_quote(code):
            issues.append(f"{where}: string literal is not closed on this line (use \\n for a line break)")
        stripped = code.rstrip()
        if stripped and not stripped.lstrip().startswith("//"):
            indent = len(code) - len(code.lstrip(" "))
            if indent % 4 != 0:
                issues.append(f"{where}: indentation {indent} is not a multiple of 4 (line wrapping is not used in this project)")
        # Pine keywords cannot be identifiers (caught in v0.4: a parameter named `to`)
        kw = re.search(r"\b(?:int|float|bool|string|color|line|box|label|table|array<[^>]+>|map<[^>]+>|[A-Z]\w*)\s+(to|by|in|or|and|not|if|else|for|while|var|switch|import|export|method|type|enum|true|false|na)\b\s*(?:[,)=]|$)", code)
        if kw:
            issues.append(f"{where}: `{kw.group(1)}` is a Pine keyword and cannot be used as a name")
        # Built-in type / namespace names are reserved (caught in v0.5: an enum member named `text`, CE10150)
        rs = re.match(r"^\s*(?:var\s+)?(?:[\w<>.]+\s+)?(" + RESERVED + r")\s*(?:=(?!=)|$)", code)
        if rs and not re.match(r"^\s*(?:type|enum)\b", code):
            issues.append(f"{where}: `{rs.group(1)}` is a reserved Pine name and cannot be used as a variable, field or enum member")
        m = re.search(r"for\s+\w+\s*=\s*0\s+to\s+(.+?)\s*-\s*1\s*$", code)
        if m and "size()" in m.group(1):
            issues.append(f"{where}: ascending loop to size()-1 iterates twice on empty arrays; guard it with `if n > 0`")
    return issues


def assemble(target: str) -> tuple[Path, str, list[str]]:
    cfg = json.loads(TARGETS.read_text(encoding="utf-8"))[target]
    flags = set(cfg.get("flags", []))
    version = read_version()
    date = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    parts = []
    issues = []
    for mod in cfg["modules"]:
        path = SRC / mod
        text, pp_issues = preprocess(mod, path.read_text(encoding="utf-8").rstrip() + "\n", flags)
        issues += pp_issues
        issues += lint(mod, text)
        parts.append(text.rstrip() + "\n")
    body = "\n".join(parts)
    body = body.replace("{{VERSION}}", version).replace("{{DATE}}", date)
    issues += lint_shadowing(body)
    issues += lint_inputs(body)
    if not body.startswith("//@version=6"):
        issues.append("00_header.pine must start with //@version=6")
    out = ROOT / cfg["output"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return out, body, issues


def syntax_check(path: Path) -> tuple[bool, str]:
    python = os.environ.get("PINE_PARSER_PYTHON", sys.executable)
    proc = subprocess.run(
        [python, "-m", "pynescript", "parse-and-dump", str(path)],
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        return True, "syntax OK (pynescript)"
    tail = "\n".join(proc.stderr.strip().splitlines()[-6:])
    return False, tail or "pynescript failed"


def build_target(target: str, check: bool) -> bool:
    out, body, issues = assemble(target)
    lines = body.count("\n")
    tokens = sum(len(TOKEN_RE.findall(strip_comment(l))) for l in body.splitlines())
    print(f"[{target}] built {out.relative_to(ROOT)}  v{read_version()}  lines={lines}  ~tokens={tokens}")
    if lines > WARN_LINES or tokens > WARN_TOKENS:
        print(f"[{target}] WARNING: above the compile budget (lines>{WARN_LINES} or tokens>{WARN_TOKENS}): TradingView may time out (risk T-01, ADR-13)")

    ok = True
    for msg in issues:
        print(f"[{target}] LINT {msg}")
    if issues:
        ok = False

    if check:
        passed, msg = syntax_check(out)
        print(f"[{target}] {msg}")
        ok = ok and passed
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default="all", help="target name from targets.json, or all")
    ap.add_argument("--check", action="store_true", help="run pynescript syntax check")
    args = ap.parse_args()

    names = list(json.loads(TARGETS.read_text(encoding="utf-8"))) if args.target == "all" else [args.target]
    ok = True
    for name in names:
        ok = build_target(name, args.check) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
