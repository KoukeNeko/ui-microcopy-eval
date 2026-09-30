#!/usr/bin/env python3
"""The tables the report quotes, computed on matched records so v1 and v2 are
compared on the same models, probes and samples.

Prints markdown. `python3 final_numbers.py > eval_v2/final_tables.md`.
"""
import json
import math
import random
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
probes = {p["id"]: p for p in json.loads((HERE / "probes_v2/probes_claude.json").read_text())
          + json.loads((HERE / "probes_v2/probes_gpt.json").read_text())}

rows = []
for path in sorted((HERE / "eval_v2/judge").rglob("*.json")):
    d = json.loads(path.read_text())
    items = (d.get("verdict") or {}).get("items") or {}
    judge, channel, arm = path.parts[-4], path.parts[-3], path.parts[-2]
    pid, sm = path.stem.split(".")
    for key, it in items.items():
        if isinstance(it, dict):
            rows.append(dict(judge=judge, channel=channel, arm=arm, probe=pid, sample=sm, key=key,
                             author=probes[pid]["author"], lang=probes[pid]["lang"],
                             role=next(i["role"] for i in probes[pid]["items"] if i["key"] == key),
                             facts=int(it.get("facts_present", 0) or 0),
                             surplus=int(it.get("surplus", 0) or 0)))
idx = {(r["judge"], r["channel"], r["probe"], r["sample"], r["key"], r["arm"]): r for r in rows}
FAMILY = {"ollama-gemma4-31b-cloud": "gemma", "ollama-nemotron-3-super-cloud": "nemotron",
          "ollama-deepseek-v4.1-flash-cloud": "deepseek", "ollama-glm-5.3-flash-cloud": "glm",
          "codex": "gpt", "claude-haiku-rules-in-context": "claude", "claude-sonnet-rules-in-context": "claude"}
JUDGE_FAMILY = {"ollama-gemma4-31b-cloud": "gemma", "ollama-nemotron-3-super-cloud": "nemotron"}


def wilson(k, n, z=1.96):
    if not n:
        return (0, 0, 0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, c - h, c + h)


def paired(judge, arm, base="control", channels=None, author=None, cross_family_only=True):
    pairs = []
    for (j, ch, pr, sm, key, a), r in idx.items():
        if j != judge or a != arm:
            continue
        if channels and ch not in channels:
            continue
        if author and r["author"] != author:
            continue
        if cross_family_only and FAMILY.get(ch) == JUDGE_FAMILY.get(j):
            continue
        c = idx.get((j, ch, pr, sm, key, base))
        if not c:
            continue
        pairs.append((pr, (c["facts"] == 1 and c["surplus"] == 0), (r["facts"] == 1 and r["surplus"] == 0),
                      c["facts"], r["facts"], c["surplus"], r["surplus"]))
    if not pairs:
        return None
    n = len(pairs)
    b = sum(1 for _, cp, ap, *_ in pairs if not cp and ap)
    c = sum(1 for _, cp, ap, *_ in pairs if cp and not ap)
    by_probe = defaultdict(list)
    for pr, cp, ap, *_ in pairs:
        by_probe[pr].append(int(ap) - int(cp))
    rng = random.Random(3)
    keys = list(by_probe)
    boots = []
    for _ in range(1000):
        s = [rng.choice(keys) for _ in keys]
        vals = [v for k in s for v in by_probe[k]]
        boots.append(sum(vals) / len(vals))
    boots.sort()
    return dict(n=n, b=b, c=c, net=(b - c) / n, lo=boots[25], hi=boots[974],
                dfacts=sum(af - cf for *_, cf, af, _, _ in pairs) / n,
                dsurplus=sum(as_ - cs for *_, cs, as_ in pairs) / n,
                probes=len(keys))


def fmt(p):
    if not p:
        return "| — | | | | | | |"
    return (f"| {p['n']} ({p['probes']} 題) | {p['b']} | {p['c']} | {p['net']:+.0%} | {p['lo']:+.0%}…{p['hi']:+.0%} | "
            f"{p['dfacts']:+.1%} | {p['dsurplus']:+.1%} |")


out = []
# channels where both skill (v1) and skill2b (v2) exist with the same samples
both = sorted({ch for (_, ch, *_r, a) in idx if a == "skill2b"} & {ch for (_, ch, *_r, a) in idx if a == "skill"})
out.append("## 表 A — v1 與 v2 在相同模型、相同題、相同抽樣上的配對結果（對 control）")
out.append("")
out.append(f"模型：{', '.join(sorted(set(FAMILY[c] for c in both)))}（claude 為 haiku 與 sonnet，規則檔在 context）；judge 不評自家族輸出。")
out.append("")
out.append("| judge | 出題者 | arm | 配對數 | b | c | 淨通過差 | 叢集 95% CI | Δ事實齊全 | Δ多餘 |")
out.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
for judge in sorted(JUDGE_FAMILY):
    for author in ("all", "claude", "gpt"):
        for arm in ("rules", "exemplar", "schema", "skill", "skill2b"):
            p = paired(judge, arm, channels=both, author=None if author == "all" else author)
            out.append(f"| {JUDGE_FAMILY[judge]} | {author} | {arm} | " + fmt(p)[2:])
out.append("")
out.append("## 表 B — v2 直接對 v1 的配對（skill2b vs skill，同模型同題同抽樣）")
out.append("")
out.append("| judge | 出題者 | 配對數 | v1 過→v2 不過 (c) | v1 不過→v2 過 (b) | 淨差 | 叢集 95% CI | Δ事實齊全 | Δ多餘 |")
out.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
for judge in sorted(JUDGE_FAMILY):
    for author in ("all", "claude", "gpt"):
        p = paired(judge, "skill2b", base="skill", channels=both, author=None if author == "all" else author)
        if p:
            out.append(f"| {JUDGE_FAMILY[judge]} | {author} | {p['n']} ({p['probes']} 題) | {p['c']} | {p['b']} | {p['net']:+.0%} | {p['lo']:+.0%}…{p['hi']:+.0%} | {p['dfacts']:+.1%} | {p['dsurplus']:+.1%} |")
out.append("")
out.append("## 表 C — 各 arm 的絕對通過率（gemma judge，全部可用模型，異家族）")
out.append("")
out.append("| arm | 字串數 | 無多餘 | 事實齊全 | 通過 | 95% CI |")
out.append("| --- | --- | --- | --- | --- | --- |")
for arm in ("control", "rules", "exemplar", "schema", "postfilter", "skill", "skill2", "skill2b"):
    rs = [r for r in rows if r["arm"] == arm and r["judge"] == "ollama-gemma4-31b-cloud" and FAMILY.get(r["channel"]) != "gemma"]
    if not rs:
        continue
    n = len(rs)
    ok = sum(1 for r in rs if r["facts"] == 1 and r["surplus"] == 0)
    p, lo, hi = wilson(ok, n)
    out.append(f"| {arm} | {n} | {sum(1 for r in rs if r['surplus'] == 0) / n:.0%} | {sum(r['facts'] for r in rs) / n:.0%} | {ok / n:.0%} | {lo:.0%}–{hi:.0%} |")
out.append("")
# per-channel skill2b vs control, both judges
out.append("## 表 D — 各模型的 v2 效果（skill2b vs control）")
out.append("")
out.append("| 模型 | judge | 配對數 | 淨通過差 | 叢集 95% CI | Δ事實齊全 |")
out.append("| --- | --- | --- | --- | --- | --- |")
for ch in both:
    for judge in sorted(JUDGE_FAMILY):
        p = paired(judge, "skill2b", channels=[ch])
        if p:
            label = {"claude-haiku-rules-in-context": "claude haiku (rules-in-context)", "claude-sonnet-rules-in-context": "claude sonnet (rules-in-context)"}.get(ch, FAMILY[ch])
            out.append(f"| {label} | {JUDGE_FAMILY[judge]} | {p['n']} | {p['net']:+.0%} | {p['lo']:+.0%}…{p['hi']:+.0%} | {p['dfacts']:+.1%} |")
out.append("")
print("\n".join(out))
