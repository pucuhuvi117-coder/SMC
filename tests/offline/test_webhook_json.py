#!/usr/bin/env python3
"""Offline check of the webhook envelope (src/50_webhook.pine, docs §12).

Pine cannot be executed offline, so this file mirrors the JSON assembly of 50_webhook
helper by helper (f_esc, f_q, f_kv, f_obj, f_jn, f_jp, f_jSetup, f_jPlan, f_jEvent,
f_whMessage) and checks that the result parses with json.loads and has the §12.2 fields.
It guards the structure (commas, brackets, quoting, null for na), not Pine semantics:
keep it in sync with 50_webhook when the envelope changes.

Run: python3 tests/offline/test_webhook_json.py
"""
import json
import math

NA = float("nan")


def na(v):
    return v is None or (isinstance(v, float) and math.isnan(v))


def f_esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def f_q(s):
    return '"' + f_esc(s) + '"'


def f_kv(k, v):
    return '"' + k + '":' + v


def f_obj(parts):
    return "{" + ",".join(parts) + "}"


def f_jn(v):  # str.tostring(v, "0.0###")
    if na(v):
        return "null"
    s = f"{v:.4f}".rstrip("0")
    return s + "0" if s.endswith(".") else s


def f_jp(v, mintick=0.01):  # str.tostring(v, format.mintick)
    if na(v):
        return "null"
    dec = max(0, -int(math.floor(math.log10(mintick))))
    return f"{round(v / mintick) * mintick:.{dec}f}"


def f_setKey(s):
    return "SETUP|" + s["model"] + "|" + str(s["dir"]) + "|CHART|" + str(s["bornT"])


def f_jSetup(s):
    a = [f_kv("model", f_q(s["model"])), f_kv("state", f_q(s["state"])),
         f_kv("grade", "null" if s["readyBar"] is None else f_q(s["grade"])),
         f_kv("score", f_jn(s["score"])), f_kv("chain", f_q(s["chain"])),
         f_kv("factors", f_q(s["factors"])), f_kv("r_real", f_jn(s["rReal"])),
         f_kv("reason", "null" if s["reason"] == "" else f_q(s["reason"]))]
    return f_obj(a)


def f_jPlan(s, req_kz):
    risk = (s["entry"] - s["sl"]) * s["dir"]
    tp = []
    for n, (p, tag, alloc) in enumerate(s["tps"], 1):
        rr = (p - s["entry"]) * s["dir"] / risk
        tp.append(f_obj([f_kv("n", str(n)), f_kv("price", f_jp(p)), f_kv("rr", f_jn(rr)), f_kv("src", f_q(tag)), f_kv("alloc", f_jn(alloc))]))
    a = [f_kv("id", f_q("PLAN|" + f_setKey(s) + "|r1")), f_kv("rev", "1"),
         f_kv("side", f_q("LONG" if s["dir"] == 1 else "SHORT")),
         f_kv("entry", f_obj([f_kv("type", f_q("LIMIT")), f_kv("mode", f_q("CE")), f_kv("price", f_jp(s["entry"])), f_kv("zone", "[" + f_jp(s["bot"]) + "," + f_jp(s["top"]) + "]")])),
         f_kv("sl", f_obj([f_kv("mode", f_q("BEYOND_SWEEP")), f_kv("price", f_jp(s["sl"]))])),
         f_kv("tp", "[" + ",".join(tp) + "]"), f_kv("rr_final", f_jn(s["rrFinal"])),
         f_kv("invalidation", f_jp(s["inv"])), f_kv("valid_until_t", str(s["readyT"] + 30 * 900000)),
         f_kv("cancel", '["INVALIDATION_CLOSE","OPP_CHOCH","POI_BROKEN","TP1_BEFORE_ENTRY","EXPIRY"' + (',"SESSION_END"' if req_kz else "") + "]"),
         f_kv("risk", f_obj([f_kv("sl_atr", f_jn(risk / 12.5)), f_kv("sl_ticks", str(round(risk / 0.01))), f_kv("risk_pct", "null"), f_kv("qty", "null")]))]
    return f_obj(a)


def f_jEvent(e, s, seq, base, req_kz):
    a = [f_kv("seq", str(seq)), f_kv("key", f_q(base + "|" + e["type"] + "|" + str(seq))),
         f_kv("type", f_q(e["type"])), f_kv("dir", str(e["dir"])), f_kv("price", f_jp(e["price"])),
         f_kv("tf", f_q(e["tf"])), f_kv("tier", str(e["tier"])),
         f_kv("ref", "null" if s is None else f_q(f_setKey(s))), f_kv("cause", "null"),
         f_kv("data", f_obj([f_kv("v1", f_jn(e["v1"])), f_kv("v2", f_jn(e["v2"])), f_kv("v3", f_jn(e["v3"])), f_kv("s1", f_q(e["s1"]))]))]
    if s is not None:
        a.append(f_kv("setup", f_jSetup(s)))
        if s["readyBar"] is not None:
            a.append(f_kv("plan", f_jPlan(s, req_kz)))
    return f_obj(a)


def f_whMessage(events, setups, snap, tok, req_kz, max_len=4000):
    base = "BINANCE:ETHUSDT.P|240|1759734000000"
    ev, length, trunc = [], 0, False
    for seq, (e, s) in enumerate(events, 1):
        j = f_jEvent(e, s, seq, base, req_kz)
        if length + len(j) <= max_len:
            ev.append(j)
            length += len(j) + 1
        else:
            trunc = True
    a = [f_kv("schema", f_q("smcvp.event")), f_kv("v", f_q("1.0")), f_kv("msg_id", f_q("SMCVP|" + base)),
         f_kv("build", f_q("0.5.0")), f_kv("cfg", f_q("483921"))]
    if tok:
        a.append(f_kv("tok", f_q(tok)))
    a.append(f_kv("inst", f_obj([f_kv("tickerid", f_q("BINANCE:ETHUSDT.P")), f_kv("tf", f_q("240")), f_kv("mintick", "0.01")])))
    a.append(f_kv("bar", f_obj([f_kv("t", "1759734000000"), f_kv("o", f_jp(2690.86)), f_kv("h", f_jp(2693.44)), f_kv("l", f_jp(2689.77)), f_kv("c", f_jp(2692.64))])))
    ctx = f_obj([f_kv("htf", f_q("D")), f_kv("htf_bias", f_q("BULL")), f_kv("structure", f_q("BULL")), f_kv("session", "null"), f_kv("pd", f_q("DISCOUNT")), f_kv("pd_pct", f_jn(0.39)), f_kv("regime", f_q("TRENDING"))])
    a.append(f_kv("ctx", ctx))
    a.append(f_kv("events", "[" + ",".join(ev) + "]"))
    if trunc:
        a.append(f_kv("truncated", "true"))
    if snap:
        sn = [f_obj([f_kv("ref", f_q(f_setKey(s))), f_kv("setup", f_jSetup(s)), f_kv("plan", f_jPlan(s, req_kz))]) for s in setups]
        a.append(f_kv("snapshot", "[" + ",".join(sn) + "]"))
    return f_obj(a)


SETUP = dict(model="SWEEP_REVERSAL", dir=1, bornT=1759700700000, state="READY", readyBar=5900, grade="A+",
             score=8.4, chain="Sweep → CHoCH → FVG+OB → OTE",
             factors='+ HTF D BULLISH  +1.5\n+ SSL "EQL" swept (major)  +2.0\n− D zone against before TP1  −1.0\n',
             rReal=NA, reason="", entry=2650.25, sl=2638.4, bot=2645.1, top=2655.4, inv=2641.0,
             tps=[(2690.0, "BSL", 0.5), (2737.61, "◆D PDH", 0.3), (2780.0, "Range high", 0.2)],
             rrFinal=10.98, readyT=1759730400000)
EVENTS = [
    (dict(type="LIQ_SWEPT", dir=1, price=2645.0, tf="CHART", tier=1, v1=0.18, v2=1, v3=1.0, s1='SSL "EQL" \\ back'), None),
    (dict(type="CHOCH", dir=1, price=2660.0, tf="HTF1", tier=1, v1=1, v2=1.8, v3=NA, s1=""), None),
    (dict(type="SETUP_READY", dir=1, price=2650.25, tf="CHART", tier=1, v1=8.4, v2=10.98, v3=3, s1=SETUP["chain"]), SETUP),
]


def check(msg):
    doc = json.loads(msg)
    for k in ("schema", "v", "msg_id", "build", "cfg", "inst", "bar", "ctx", "events"):
        assert k in doc, k
    seqs = [e["seq"] for e in doc["events"]]
    assert seqs == sorted(seqs) and (not seqs or seqs[0] == 1), seqs
    return doc


if __name__ == "__main__":
    doc = check(f_whMessage(EVENTS, [SETUP], snap=False, tok="", req_kz=False))
    assert doc["events"][2]["plan"]["tp"][1]["src"] == "◆D PDH"
    assert doc["events"][0]["data"]["s1"] == 'SSL "EQL" \\ back'
    assert doc["events"][1]["data"]["v3"] is None
    check(f_whMessage(EVENTS, [SETUP], snap=True, tok='id"1', req_kz=True))
    small = check(f_whMessage(EVENTS, [SETUP], snap=False, tok="", req_kz=False, max_len=600))
    assert small.get("truncated") is True and len(small["events"]) < 3
    check(f_whMessage([], [SETUP], snap=True, tok="", req_kz=False))
    print("webhook JSON: 4 envelopes parse, fields and escaping OK")
