#!/usr/bin/env python3
import json, re, sys, math, random
from pathlib import Path
from collections import defaultdict
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path.home() / ".claude/skills/ui-microcopy/scripts"))
import microcopy_lint as L
probes = {p["id"]: p for p in json.loads((HERE / "probes.json").read_text())}
rules = [(sev, re.compile(pat), fix) for sev, pat, fix in L.CN_TERMS]
ARMS = ("control", "instruct", "relevant", "table", "bigtable")
S = defaultdict(lambda: defaultdict(list))  # (model)->(arm)->list of per-string dicts
for f in sorted((HERE / "gen").glob("*.json")):
    g = json.loads(f.read_text()); p = probes[g["probe"]]
    if not isinstance(g.get("parsed"), dict):
        S[g["model"]][g["arm"]].append(dict(probe=g["probe"], bad=None, hit=None, expect=None)); continue
    for k in ("s1", "s2", "s3"):
        s = g["parsed"].get(k)
        if not isinstance(s, str): continue
        masked = s
        for t in L.TW_WHITELIST: masked = masked.replace(t, "＿" * len(t))
        hits = [rx.pattern for sev, rx, fix in rules if rx.search(masked)]
        S[g["model"]][g["arm"]].append(dict(probe=g["probe"], bad=bool(hits), hit=hits,
                                            target=any(d in s for d in p["drift"]), expect=any(e in s for e in p["expect"]),
                                            simplified=bool(re.search(r"[国会从学说时这为个们来对开关发电应该约记录数据设视频网络请输确认删储项页转账币传连线无败错误试处编辑显图选择检软级统计邮权读写务询问题闭号亿万几点让实现]", s))))
def ci(xs):
    ps = [x for x in xs if x is not None]
    if not ps: return (0, 0, 0)
    n = len(ps); p = sum(ps) / n; z = 1.96
    d = 1 + z*z/n; c = (p + z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return p, c-h, c+h
print("| model | arm | strings | parse fail | any mainland term | 95% CI | target drift term | expected TW term | simplified char |")
print("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
tot = defaultdict(list)
for model in sorted(S):
    for arm in ARMS:
        rows = S[model][arm]
        if not rows: continue
        fails = sum(1 for r in rows if r["bad"] is None); ok = [r for r in rows if r["bad"] is not None]
        p, lo, hi = ci([r["bad"] for r in ok])
        tot[arm].extend(ok)
        print(f"| {model} | {arm} | {len(ok)} | {fails} | {p:.1%} | {lo:.0%}–{hi:.0%} | {sum(r['target'] for r in ok)/max(1,len(ok)):.1%} | {sum(r['expect'] for r in ok)/max(1,len(ok)):.1%} | {sum(r['simplified'] for r in ok)/max(1,len(ok)):.1%} |")
print()
print("| arm (all models) | strings | any mainland term | 95% CI | target drift term | expected TW term |")
print("| --- | --- | --- | --- | --- | --- |")
for arm in ARMS:
    ok = tot[arm]
    if not ok: continue
    p, lo, hi = ci([r["bad"] for r in ok])
    print(f"| {arm} | {len(ok)} | {p:.1%} | {lo:.0%}–{hi:.0%} | {sum(r['target'] for r in ok)/len(ok):.1%} | {sum(r['expect'] for r in ok)/len(ok):.1%} |")
# which terms leak under control
from collections import Counter
c = Counter(h for r in tot["control"] for h in (r["hit"] or []))
print("\ncontrol leaks:", c.most_common(12))
c2 = Counter((r["probe"]) for r in tot["control"] if r["bad"])
print("control leaks by probe:", c2.most_common())
