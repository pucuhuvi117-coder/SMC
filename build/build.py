#!/usr/bin/env python3
"""Assemble SMC Visualizer Pro from modular sources into a single Pine Script file.

Pine Script has no include mechanism and the published script must be a single
file (docs/02-architecture.md §4.11, ADR-04). Sources live in src/ as ordered
fragments; this script concatenates them, stamps the version and build date,
runs project lint rules and, when available, a syntax check with pynescript.

Usage:
    python3 build/build.py                 # build the default target (indicator)
    python3 build/build.py --check         # build + syntax check (needs pynescript)
    python3 build/build.py --target NAME   # build another target from targets.json

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

# Soft limits used for the size report. TradingView enforces limits on the
# compiled script (tokens, variables, scopes) that cannot be computed exactly
# offline; these thresholds give early warning (risk T-01, spike S-7).
WARN_LINES = 6000
WARN_TOKENS = 60000

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
        # The [1] offset may live inside the requested function; such lines must say so explicitly
        if "lookahead_on" in code and "[1]" not in code and "no-repaint:" not in raw:
            issues.append(f"{where}: lookahead_on without [1] offset or a `// no-repaint:` note (repaint, §4.7)")
        stripped = code.rstrip()
        if stripped and not stripped.lstrip().startswith("//"):
            indent = len(code) - len(code.lstrip(" "))
            if indent % 4 != 0:
                issues.append(f"{where}: indentation {indent} is not a multiple of 4 (line wrapping is not used in this project)")
        # Pine keywords cannot be identifiers (caught in v0.4: a parameter named `to`)
        kw = re.search(r"\b(?:int|float|bool|string|color|line|box|label|table|array<[^>]+>|map<[^>]+>|[A-Z]\w*)\s+(to|by|in|or|and|not|if|else|for|while|var|switch|import|export|method|type|enum|true|false|na)\b\s*(?:[,)=]|$)", code)
        if kw:
            issues.append(f"{where}: `{kw.group(1)}` is a Pine keyword and cannot be used as a name")
        m = re.search(r"for\s+\w+\s*=\s*0\s+to\s+(.+?)\s*-\s*1\s*$", code)
        if m and "size()" in m.group(1):
            issues.append(f"{where}: ascending loop to size()-1 iterates twice on empty arrays; guard it with `if n > 0`")
    return issues


def assemble(target: str) -> tuple[Path, str, list[str]]:
    cfg = json.loads(TARGETS.read_text(encoding="utf-8"))[target]
    version = read_version()
    date = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    parts = []
    issues = []
    for mod in cfg["modules"]:
        path = SRC / mod
        text = path.read_text(encoding="utf-8").rstrip() + "\n"
        issues += lint(mod, text)
        parts.append(text)
    body = "\n".join(parts)
    body = body.replace("{{VERSION}}", version).replace("{{DATE}}", date)
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default="indicator")
    ap.add_argument("--check", action="store_true", help="run pynescript syntax check")
    args = ap.parse_args()

    out, body, issues = assemble(args.target)
    lines = body.count("\n")
    tokens = sum(len(TOKEN_RE.findall(strip_comment(l))) for l in body.splitlines())
    print(f"built {out.relative_to(ROOT)}  v{read_version()}  lines={lines}  ~tokens={tokens}")
    if lines > WARN_LINES or tokens > WARN_TOKENS:
        print(f"WARNING: size above soft limit (lines>{WARN_LINES} or tokens>{WARN_TOKENS}) — see risk T-01")

    ok = True
    for msg in issues:
        print(f"LINT {msg}")
    if issues:
        ok = False

    if args.check:
        passed, msg = syntax_check(out)
        print(msg)
        ok = ok and passed

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
