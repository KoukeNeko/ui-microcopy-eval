#!/usr/bin/env python3
"""Held-out evaluation, v2: generation, independent judging, human sampling.

  eval_v2.py contamination                 # probe text vs skill / v1 fixtures
  eval_v2.py generate --channel C [--arms ...] [--samples 2] [--probes C01,G03]
  eval_v2.py judge --judge J [--channels ...]    # J is a channel spec too
  eval_v2.py sample-for-human --n 40
  eval_v2.py report

Channels are the same specs as ui-microcopy-eval/run_eval.py (codex,
ollama:<model>, cloakgpt:auto). Arms:

  control   the brief alone
  rules     brief + arms/rules_only.md        (negative list)
  exemplar  brief + arms/exemplar_only.md     (role → form → examples, no "don't")
  skill     brief + the ui-microcopy skill files (+ runtime block for runtime)
  schema    brief + a per-field length/emptiness contract, no wording advice

`postfilter` is derived at report time from `control` on runtime probes by
passing free-text fields through the v1 linter's apparatus/absence/provenance
patterns — the app-side filter, measured without a second generation.

Layout: eval_v2/gen/<channel>/<arm>/<probe>.<k>.json and
eval_v2/judge/<judge>/<channel>/<arm>/<probe>.<k>.json.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBES = HERE / "probes_v2"
OUT = HERE / "eval_v2"
SKILL = Path.home() / ".claude" / "skills" / "ui-microcopy"
V1 = Path.home() / ".claude" / "skills" / "ui-microcopy-eval"
sys.path.insert(0, str(V1))
sys.path.insert(0, str(SKILL / "scripts"))
import run_eval as v1  # noqa: E402  channels, extract_json, ANSI
from microcopy_lint import RULES as LINT_RULES  # noqa: E402

ARMS = ("control", "rules", "exemplar", "skill", "schema", "skill2", "skill2b")
SKILL_FILES = ("SKILL.md", "references/roles.md", "references/failure-modes.md",
               "references/zh-tw-lexicon.md")
RUNTIME_FILE = "assets/runtime-prompt-block.zh-TW.md"
# v2 of the skill, staged beside this script until it ships. Only its
# instruction files go into the prompt; evidence and evaluation pages are
# documentation and would carry test-derived strings.
# the research folder keeps the v2 skill beside the harness; the checked-in
# harness reads the installed skill instead
SKILL2 = HERE / "skill_v2"
if not SKILL2.exists():
    SKILL2 = Path.home() / ".claude" / "skills" / "ui-microcopy"
SKILL2_FILES = ("SKILL.md", "references/roles.md", "references/uncertainty.md",
                "references/zh-tw-lexicon.md")
LENGTH_CAP = {"button": 8, "dialog-title": 16, "dialog-body": 96, "title": 16,
              "label": 12, "status": 24, "error": 64, "empty": 24, "value": 32,
              "note": 32}
FILTER_RULES = {"apparatus-disclaimer", "absence-disclaimer", "provenance-meta",
                "boilerplate-disclaimer"}


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def load_probes(wanted: list[str] | None = None) -> list[dict]:
    probes = []
    for name in ("probes_claude.json", "probes_gpt.json"):
        path = PROBES / name
        if path.exists():
            probes.extend(json.loads(read(path)))
    if wanted:
        probes = [p for p in probes if p["id"] in wanted]
    return probes


def label_of(channel: str) -> str:
    return channel.replace(":", "-").replace("/", "-")


# --------------------------------------------------------------------------
# arms


def schema_block(probe: dict) -> str:
    lines = ["每個欄位的限制（回傳前逐一確認）："]
    for item in probe["items"]:
        cap = LENGTH_CAP.get(item["role"], 48)
        if item["role"] == "note" and not item["must_convey"]:
            lines.append(f"- {item['key']}：字串，可以是空字串；最多 {cap} 個字元")
        elif item["key"] in ("action_items", "ingredients"):
            lines.append(f"- {item['key']}：字串陣列，每個元素最多 {cap * 2} 個字元")
        else:
            lines.append(f"- {item['key']}：字串，最多 {cap} 個字元")
    return "\n".join(lines)


def build_prompt(probe: dict, arm: str) -> str:
    task = probe["task"]
    if arm == "control":
        return task
    if arm == "rules":
        return f"{task}\n\n---\n{read(PROBES / 'arms' / 'rules_only.md')}"
    if arm == "exemplar":
        return f"{task}\n\n---\n{read(PROBES / 'arms' / 'exemplar_only.md')}"
    if arm == "skill":
        parts = [read(SKILL / f) for f in SKILL_FILES]
        if probe["kind"] == "runtime":
            parts.append(read(SKILL / RUNTIME_FILE))
        return f"{task}\n\n---\n以下是介面文字的規則與案例，請遵守：\n\n" + "\n\n".join(parts)
    if arm == "schema":
        return f"{task}\n\n---\n{schema_block(probe)}"
    if arm == "skill2":
        # draft 1 of v2, frozen in skill_v2_draft1 after the first measurement
        d1 = HERE / "skill_v2_draft1"
        parts = [read(d1 / f) for f in SKILL2_FILES]
        if probe["kind"] == "runtime":
            parts.append(read(d1 / RUNTIME_FILE))
        return f"{task}\n\n---\n以下是介面文字的規則與案例，請遵守：\n\n" + "\n\n".join(parts)
    if arm == "skill2b":
        # v2 after the language fix; the wrapper is language-neutral because
        # in real use the skill is loaded as a document, not introduced in
        # Chinese
        parts = [read(SKILL2 / f) for f in SKILL2_FILES]
        if probe["kind"] == "runtime":
            parts.append(read(SKILL2 / RUNTIME_FILE))
        return f"{task}\n\n---\nSkill (applies to the brief above):\n\n" + "\n\n".join(parts)
    raise ValueError(arm)


# --------------------------------------------------------------------------
# contamination


def quoted_strings(text: str) -> set[str]:
    out = set(re.findall(r"「([^」]{2,40})」", text))
    out |= set(re.findall(r"[\"“]([^\"”]{4,60})[\"”]", text))
    return out


def cmd_contamination(args: argparse.Namespace) -> int:
    skill_dir = Path(args.skill_dir) if getattr(args, "skill_dir", None) else SKILL
    skill = "".join(read(p) for p in skill_dir.rglob("*.md"))
    lint = skill_dir / "scripts" / "microcopy_lint.py"
    if lint.exists():
        skill += read(lint)
    if getattr(args, "reverse", False):
        # The other direction: probe answers' required facts and briefs must
        # not have been written into the skill after the fact.
        banned = set()
        for probe in load_probes():
            banned |= quoted_strings(probe["task"])
            for it in probe["items"]:
                for fact in it["must_convey"]:
                    if len(fact) >= 12:
                        banned.add(fact)
            for m in re.finditer(r"[㐀-鿿]{4,}", probe["task"]):
                banned.add(m.group(0))
        common = {"只回傳", "繁體中文", "台灣", "使用者", "請寫出", "回傳"}
        hits = sorted({b for b in banned if b in skill and b not in common and len(b) >= 4})
        print(f"{len(banned)} probe strings checked against {skill_dir}")
        for h in hits[:40]:
            print(f"  LEAK(skill<-probe) {h!r}")
        print("clean" if not hits else f"{len(hits)} hits")
        return 1 if hits else 0
    v1fx = json.loads(read(V1 / "fixtures.json"))
    banned = quoted_strings(skill)
    # examples are often unquoted: figures with units, and the ✓/✗ lines
    for m in re.finditer(r"[\$NT€¥]?\s?\d[\d,]*(?:\.\d+)?\s?(?:%|g|kcal|mg|ml|USD|shares|分|秒|片|克|元)?", skill):
        tok = m.group(0).strip()
        if len(re.sub(r"\D", "", tok)) >= 3:
            banned.add(tok)
    for line in skill.splitlines():
        if line.strip().startswith(("- ✓", "- ✗")):
            for ex in re.split(r"／|/", line.strip()[3:]):
                ex = ex.strip(" ✓✗（）()")
                if len(ex) >= 6:
                    banned.add(ex)
    for f in v1fx:
        banned |= quoted_strings(f["task"] + f.get("task_patched", ""))
        for c in f["checks"].values():
            for pat in c.get("forbid", []):
                for alt in pat.split("|"):
                    alt = re.sub(r"[\\()\[\]?*+.{}^$]", "", alt).strip()
                    if len(alt) >= 2:
                        banned.add(alt)
    # Ordinary words that any brief would contain are not leakage, and neither
    # are schema vocabulary (role names, JSON placeholders) shared by design.
    common = {"取消", "刪除", "儲存", "完成", "設定", "錯誤", "今天", "目前", "資料",
              "重新開機", "安裝完成", "無法", "搜尋", "關閉", "更多選項", "允許",
              "Cancel", "Save", "Delete", "取消安裝", "已儲存", "同步中",
              "button", "dialog-title", "dialog-body", "status", "error", "empty",
              "label", "value", "note", "ai-note", "title", "items", "notes", "name",
              "amount", "kcal", "summary"}
    banned = {b for b in banned if b not in common and len(b) >= 3
              and not re.fullmatch(r"[.…\s]+", b)
              and (re.search(r"[㐀-鿿]", b) or len(b) >= 8)}
    hits = []
    for probe in load_probes():
        for b in banned:
            if b in probe["task"]:
                hits.append((probe["id"], b))
    print(f"{len(banned)} strings from skill+v1 checked against {len(load_probes())} probes")
    for pid, b in hits:
        print(f"  LEAK {pid}: {b!r}")
    print("clean" if not hits else f"{len(hits)} hits")
    return 1 if hits else 0


# --------------------------------------------------------------------------
# generate


def cmd_generate(args: argparse.Namespace) -> int:
    probes = load_probes(args.probes.split(",") if args.probes else None)
    arms = args.arms.split(",")
    label = label_of(args.channel)
    for probe in probes:
        for arm in arms:
            for k in range(args.samples):
                target = OUT / "gen" / label / arm / f"{probe['id']}.{k}.json"
                if target.exists() and not args.redo:
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                prompt = build_prompt(probe, arm)
                t0 = time.time()
                try:
                    raw = v1.ANSI.sub("", v1.call(args.channel, prompt))
                    err = ""
                except Exception as exc:  # the failure is data
                    raw, err = "", str(exc)[:300]
                parsed = v1.extract_json(raw) if raw else None
                target.write_text(json.dumps({
                    "probe": probe["id"], "arm": arm, "channel": label, "sample": k,
                    "prompt_chars": len(prompt), "seconds": round(time.time() - t0, 1),
                    "raw": raw, "parsed": parsed, "error": err,
                }, ensure_ascii=False, indent=1), encoding="utf-8")
                print(f"[{time.strftime('%H:%M:%S')}] {label} {arm} {probe['id']}.{k} "
                      f"{'ok' if parsed else 'NO-JSON'}{' ' + err if err else ''}", flush=True)
    return 0


def cmd_human(args: argparse.Namespace) -> int:
    """Agreement between a rated human sample and each judge, plus the
    human's surplus rate per arm (the arm was hidden from the rater)."""
    ratings = {}
    for line in Path(args.rated).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|[^|]*\|[^|]*\|.*\|\s*([01])\s*\|(?:\s*[01]?\s*\|)?\s*$", line)
        if m:
            ratings[int(m.group(1))] = int(m.group(2))
    key = {k["n"]: k for k in json.loads(read(Path(args.key)))}
    by_arm = defaultdict(list)
    for n, r in ratings.items():
        if n in key:
            by_arm[key[n]["arm"]].append(r)
    print(f"{len(ratings)} rated")
    for arm, rs in sorted(by_arm.items()):
        print(f"  {arm:10} n={len(rs):3} human surplus {sum(rs) / len(rs):.0%}")
    for jdir in sorted(p for p in (OUT / "judge").iterdir() if p.is_dir()):
        pairs = []
        for n, r in ratings.items():
            k = key.get(n)
            if not k:
                continue
            p = jdir / k["channel"] / k["arm"] / f"{k['probe']}.{k['sample']}.json"
            if not p.exists():
                continue
            it = ((json.loads(read(p)).get("verdict") or {}).get("items") or {}).get(k["key"])
            if isinstance(it, dict):
                pairs.append((r, int(it.get("surplus", 0) or 0)))
        if not pairs:
            continue
        n = len(pairs)
        po = sum(1 for a, b in pairs if a == b) / n
        pa = sum(a for a, _ in pairs) / n
        pb = sum(b for _, b in pairs) / n
        pe = pa * pb + (1 - pa) * (1 - pb)
        kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0
        print(f"  {jdir.name}: n={n} agreement {po:.0%} κ={kappa:.2f} "
              f"(h1/j0={sum(1 for a, b in pairs if a == 1 and b == 0)}, h0/j1={sum(1 for a, b in pairs if a == 0 and b == 1)})")
    return 0


def cmd_dry(args: argparse.Namespace) -> int:
    """Write the prompts a hand-driven channel (an agent, a person) must
    answer, one file per probe × arm; `ingest` reads the answers back."""
    probes = load_probes(args.probes.split(",") if args.probes else None)
    pending = OUT / "pending" / args.channel_label
    n = 0
    for probe in probes:
        for arm in args.arms.split(","):
            d = pending / arm
            d.mkdir(parents=True, exist_ok=True)
            (d / f"{probe['id']}.prompt.txt").write_text(build_prompt(probe, arm), encoding="utf-8")
            n += 1
    print(f"wrote {n} prompts under {pending}")
    return 0


def cmd_ingest(args: argparse.Namespace) -> int:
    probes = {p["id"]: p for p in load_probes()}
    pending = OUT / "pending" / args.channel_label
    n = 0
    for answer in sorted(pending.rglob("*.txt")):
        if answer.name.endswith(".prompt.txt"):
            continue
        probe_id, k = answer.stem.split(".")
        if probe_id not in probes:
            continue
        arm = answer.parent.name
        raw = answer.read_text(encoding="utf-8")
        target = OUT / "gen" / args.channel_label / arm / f"{probe_id}.{k}.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps({
            "probe": probe_id, "arm": arm, "channel": args.channel_label, "sample": int(k),
            "prompt_chars": len(build_prompt(probes[probe_id], arm)), "seconds": None,
            "raw": raw, "parsed": v1.extract_json(raw), "error": "",
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        n += 1
    print(f"ingested {n} answers for {args.channel_label}")
    return 0


# --------------------------------------------------------------------------
# postfilter (derived arm)

_FILTER = [r.pattern for r in LINT_RULES if r.id in FILTER_RULES]


def postfilter(parsed: dict | None, probe: dict) -> dict | None:
    if not parsed:
        return parsed
    out = dict(parsed)
    for item in probe["items"]:
        if item["role"] != "note":
            continue
        v = out.get(item["key"])
        if isinstance(v, str) and any(p.search(v) for p in _FILTER):
            out[item["key"]] = ""
        elif isinstance(v, list):
            out[item["key"]] = [s for s in v if not any(p.search(str(s)) for p in _FILTER)]
    return out


# --------------------------------------------------------------------------
# judge


def strings_of(parsed: dict | None, probe: dict) -> dict:
    out = {}
    for item in probe["items"]:
        v = (parsed or {}).get(item["key"])
        if isinstance(v, list):
            v = " ／ ".join(str(x) for x in v)
        out[item["key"]] = "" if v is None else str(v)
    return out


def gen_records(channels: list[str] | None) -> list[dict]:
    recs = []
    for path in sorted((OUT / "gen").rglob("*.json")):
        d = json.loads(read(path))
        if channels and d["channel"] not in channels:
            continue
        recs.append(d)
    # derived arm
    probes = {p["id"]: p for p in load_probes()}
    for d in [r for r in recs if r["arm"] == "control" and probes[r["probe"]]["kind"] == "runtime"]:
        recs.append({**d, "arm": "postfilter", "parsed": postfilter(d["parsed"], probes[d["probe"]])})
    return recs


def judge_prompt(batch: list[tuple[str, dict, dict]]) -> str:
    rubric = read(PROBES / "judge_rubric.md")
    blocks = []
    for rid, probe, rec in batch:
        items = "\n".join(
            f"  - {it['key']} (element: {it['role']}; must convey: {json.dumps(it['must_convey'], ensure_ascii=False)})"
            for it in probe["items"])
        strings = json.dumps(strings_of(rec["parsed"], probe), ensure_ascii=False)
        blocks.append(f"### record {rid}\nBrief ({probe['lang']}):\n{probe['task']}\n\nElements:\n{items}\n\nStrings returned:\n{strings}")
    return rubric + "\n\n" + "\n\n".join(blocks) + "\n\nReturn the JSON array now."


def cmd_judge(args: argparse.Namespace) -> int:
    probes = {p["id"]: p for p in load_probes()}
    recs = gen_records(args.channels.split(",") if args.channels else None)
    jlabel = label_of(args.judge)
    todo = []
    for rec in recs:
        rid = f"{rec['channel']}|{rec['arm']}|{rec['probe']}.{rec['sample']}"
        target = OUT / "judge" / jlabel / rec["channel"] / rec["arm"] / f"{rec['probe']}.{rec['sample']}.json"
        if target.exists() and not args.redo:
            continue
        todo.append((rid, probes[rec["probe"]], rec, target))
    random.Random(args.seed).shuffle(todo)  # arms interleaved, never grouped
    print(f"{len(todo)} records to judge with {args.judge}", flush=True)
    for i in range(0, len(todo), args.batch):
        chunk = todo[i:i + args.batch]
        prompt = judge_prompt([(rid, p, r) for rid, p, r, _ in chunk])
        try:
            raw = v1.ANSI.sub("", v1.call(args.judge, prompt))
        except Exception as exc:
            print(f"  judge error: {exc}", flush=True)
            continue
        m = re.search(r"\[.*\]", re.sub(r"```(?:json)?", "", raw), re.S)
        try:
            verdicts = json.loads(m.group(0)) if m else []
        except json.JSONDecodeError:
            verdicts = []
        by_rid = {v.get("record"): v for v in verdicts if isinstance(v, dict)}
        for rid, probe, rec, target in chunk:
            v = by_rid.get(rid)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps({
                "record": rid, "judge": jlabel, "verdict": v, "raw_missing": v is None,
                "strings": strings_of(rec["parsed"], probe),
            }, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[{time.strftime('%H:%M:%S')}] judged {i + len(chunk)}/{len(todo)} "
              f"({sum(1 for r in chunk if r[0] in by_rid)} parsed)", flush=True)
    return 0


# --------------------------------------------------------------------------
# human sample


def cmd_sample(args: argparse.Namespace) -> int:
    probes = {p["id"]: p for p in load_probes()}
    recs = gen_records(None)
    rng = random.Random(args.seed)
    by_arm = defaultdict(list)
    for r in recs:
        if r["parsed"]:
            by_arm[r["arm"]].append(r)
    per_arm = max(1, args.n // max(1, len(by_arm)))
    picked = []
    for arm, rs in by_arm.items():
        picked += rng.sample(rs, min(per_arm, len(rs)))
    rng.shuffle(picked)
    key, lines = [], ["# 人工盲評", "",
                      "每一列是一條介面字串。請只判斷一件事：**有沒有多餘或不像介面的內容**"
                      "（多餘的解釋、口語回話、安慰、免責、對數字的辯護、描述沒看到的東西、"
                      "問句當按鈕）。有 → 1，沒有 → 0。不用管字串好不好看，只看有沒有多餘。", "",
                      "| # | 元件 | 情境 | 字串 | 多餘 (0/1) |", "| --- | --- | --- | --- | --- |"]
    n = 0
    for r in picked:
        probe = probes[r["probe"]]
        for it in probe["items"]:
            s = strings_of(r["parsed"], probe)[it["key"]]
            if not s and it["role"] != "note":
                continue
            n += 1
            key.append({"n": n, "channel": r["channel"], "arm": r["arm"], "probe": r["probe"],
                        "sample": r["sample"], "key": it["key"]})
            lines.append(f"| {n} | {it['role']} | {probe['scenario']} / {probe['lang']} | "
                         f"{s.replace('|', '｜').replace(chr(10), ' ')} | |")
    (OUT / "human_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "human_sample.key.json").write_text(json.dumps(key, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {n} strings to eval_v2/human_sample.md (key hidden in human_sample.key.json)")
    return 0


# --------------------------------------------------------------------------
# report


def judges_primary(rows: list[dict]) -> str:
    """The judge with the most verdicts, used for single-judge tables."""
    counts = defaultdict(int)
    for r in rows:
        counts[r["judge"]] += 1
    return max(counts, key=counts.get)


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, c - h, c + h)


def cmd_report(_: argparse.Namespace) -> int:
    probes = {p["id"]: p for p in load_probes()}
    rows = []  # one per (judge, channel, arm, probe, sample, key)
    for path in sorted((OUT / "judge").rglob("*.json")):
        d = json.loads(read(path))
        v = d.get("verdict") or {}
        items = v.get("items") or {}
        # OUT/judge/<judge>/<channel>/<arm>/<probe>.<k>.json
        judge, channel, arm = path.parts[-4], path.parts[-3], path.parts[-2]
        probe_id, sample = path.stem.split(".")
        for key, it in items.items():
            if not isinstance(it, dict):
                continue
            rows.append({"judge": judge, "channel": channel, "arm": arm, "probe": probe_id,
                         "sample": sample, "key": key,
                         "role": next((x["role"] for x in probes[probe_id]["items"] if x["key"] == key), "?"),
                         "lang": probes[probe_id]["lang"], "author": probes[probe_id]["author"],
                         "facts": int(it.get("facts_present", 0) or 0),
                         "surplus": int(it.get("surplus", 0) or 0),
                         "lang_ok": int(it.get("lang_ok", 1) if it.get("lang_ok") is not None else 1)})
    if not rows:
        print("no judged records")
        return 1
    out = ["# Held-out 結果 v2", "", f"{len(rows)} 條字串判定，{len({r['judge'] for r in rows})} 個 judge。", ""]

    def table(title, keyfn, label):
        out.append(f"## {title}")
        out.append("")
        out.append(f"| {label} | judge | 字串數 | 無多餘 | 事實齊全 | 兩者皆是（通過） | 通過率 95% CI |")
        out.append("| --- | --- | --- | --- | --- | --- | --- |")
        groups = defaultdict(list)
        for r in rows:
            groups[(keyfn(r), r["judge"])].append(r)
        for (g, j), rs in sorted(groups.items()):
            n = len(rs)
            ns = sum(1 for r in rs if r["surplus"] == 0)
            nf = sum(1 for r in rs if r["facts"] == 1)
            ok = sum(1 for r in rs if r["surplus"] == 0 and r["facts"] == 1)
            p, lo, hi = wilson(ok, n)
            out.append(f"| {g} | {j} | {n} | {ns / n:.0%} | {nf / n:.0%} | {ok / n:.0%} | {lo:.0%}–{hi:.0%} |")
        out.append("")

    table("依介入（全部模型）", lambda r: r["arm"], "arm")
    table("依模型 × 介入", lambda r: f"{r['channel']} / {r['arm']}", "model / arm")
    table("依語言 × 介入", lambda r: f"{r['lang']} / {r['arm']}", "lang / arm")
    table("依元件 × 介入", lambda r: f"{r['role']} / {r['arm']}", "role / arm")
    table("依出題者 × 介入（洩漏檢查：兩者應相近）", lambda r: f"{r['author']} / {r['arm']}", "author / arm")

    # paired analysis vs control: same judge, channel, probe, sample, key
    out.append("## 配對分析（各 arm 對 control；同 judge、模型、題、抽樣、欄位）")
    out.append("")
    out.append("pass = 無多餘且事實齊全。b = control 不過→arm 過，c = control 過→arm 不過；"
               "淨改善 = (b−c)/n；CI 以題目為叢集做 bootstrap（1,000 次）；McNemar 以 b、c 計算。")
    out.append("")
    out.append("| judge | 出題者 | arm | 配對數 | b | c | 淨改善 | 叢集 bootstrap 95% CI | McNemar χ² | 事實齊全差 |")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    idx = {}
    for r in rows:
        idx[(r["judge"], r["channel"], r["probe"], r["sample"], r["key"], r["arm"])] = r
    rng = random.Random(3)
    for judge in sorted({r["judge"] for r in rows}):
      for author in ("all", "claude", "gpt"):
        for arm in sorted({r["arm"] for r in rows if r["arm"] != "control"}):
            pairs = []  # (probe, control_pass, arm_pass, control_facts, arm_facts)
            for (j, ch, pr, sm, key, a), r in idx.items():
                if j != judge or a != arm:
                    continue
                if author != "all" and r["author"] != author:
                    continue
                c = idx.get((j, ch, pr, sm, key, "control"))
                if not c:
                    continue
                cp = c["surplus"] == 0 and c["facts"] == 1
                ap = r["surplus"] == 0 and r["facts"] == 1
                pairs.append((pr, cp, ap, c["facts"], r["facts"]))
            if not pairs:
                continue
            n = len(pairs)
            b = sum(1 for _, cp, ap, _, _ in pairs if not cp and ap)
            cc = sum(1 for _, cp, ap, _, _ in pairs if cp and not ap)
            net = (b - cc) / n
            dfacts = (sum(af for *_, af in pairs) - sum(cf for *_, cf, _ in pairs)) / n
            by_probe = defaultdict(list)
            for pr, cp, ap, _, _ in pairs:
                by_probe[pr].append(int(ap) - int(cp))
            probes_list = list(by_probe)
            boots = []
            for _ in range(1000):
                sample = [rng.choice(probes_list) for _ in probes_list]
                vals = [v for pr in sample for v in by_probe[pr]]
                boots.append(sum(vals) / len(vals))
            boots.sort()
            lo, hi = boots[int(0.025 * len(boots))], boots[int(0.975 * len(boots)) - 1]
            chi = ((b - cc) ** 2 / (b + cc)) if (b + cc) else 0.0
            out.append(f"| {judge} | {author} | {arm} | {n} | {b} | {cc} | {net:+.0%} | {lo:+.0%}…{hi:+.0%} | {chi:.1f} | {dfacts:+.1%} |")
    out.append("")
    out.append("（McNemar χ² > 3.84 對應 p < .05，未校正多重比較；事實齊全差為負表示 arm 掉了必要資訊。）")
    out.append("")

    # language: the judge's lang_ok flag (zh-TW vocabulary / script, natural ja/en)
    out.append("## 語言正確率（judge 的 lang_ok；zh-TW 題含簡體字或大陸用語即 0）")
    out.append("")
    out.append("| lang | channel | arm | n | lang_ok |")
    out.append("| --- | --- | --- | --- | --- |")
    lang_groups = defaultdict(list)
    for r in rows:
        if r["judge"] != judges_primary(rows):
            continue
        lang_groups[(r["lang"], r["channel"], r["arm"])].append(r["lang_ok"])
    for (lang, ch, arm), xs in sorted(lang_groups.items()):
        if lang == "zh-TW" and arm in ("control", "skill"):
            out.append(f"| {lang} | {ch} | {arm} | {len(xs)} | {sum(xs) / len(xs):.0%} |")
    out.append("")
    out.append("（只列 zh-TW 的 control 與 skill；其他組合在 judge 檔內。）")
    out.append("")

    gens = gen_records(None)
    # script leakage measured on the generations themselves: CJK in an English
    # answer, a simplified-only character in a zh-TW answer, a Chinese-only
    # term in a Japanese answer.
    simplified = set("国会从学说时这为个们来对开关发电应该约饭鸡记录数据设视频网络请输确认删储项页转账币传连线无败错误试处编辑显图选择检软级统计邮权读写务询问题闭号亿万几点让实现")
    zh_only_in_ja = ("設定", "儲存", "刪除", "確認", "訊息", "資料", "載入", "無法", "請", "已")
    leak = defaultdict(lambda: [0, 0])  # (lang, channel, arm) -> [leaks, n]
    for g in gens:
        probe = probes[g["probe"]]
        if not g["parsed"]:
            continue
        for it in probe["items"]:
            s = strings_of(g["parsed"], probe)[it["key"]]
            if not s.strip():
                continue
            bad = False
            if probe["lang"] == "en":
                bad = re.search(r"[㐀-鿿぀-ヿ]", s) is not None
            elif probe["lang"] == "zh-TW":
                bad = any(ch in simplified for ch in s)
            elif probe["lang"] == "ja":
                bad = any(t in s for t in zh_only_in_ja) and not re.search(r"[぀-ヿ]", s)
            k = (probe["lang"], g["channel"], g["arm"])
            leak[k][1] += 1
            leak[k][0] += 1 if bad else 0
    out.append("## 語言洩漏（生成檔直接偵測：英文題出現中日文、繁中題出現簡體字、日文題只有中文詞而無假名）")
    out.append("")
    out.append("| lang | channel | arm | n | 洩漏率 |")
    out.append("| --- | --- | --- | --- | --- |")
    for (lang, ch, arm), (b, n) in sorted(leak.items()):
        if n and (b or arm in ("control", "skill")):
            out.append(f"| {lang} | {ch} | {arm} | {n} | {b / n:.0%} |")
    out.append("")

    # objective measures straight from the generations: note emptiness (priming
    # side effect) and string length (conciseness without a judge)
    note_stats = defaultdict(lambda: [0, 0])  # (arm, expected) -> [nonempty, n]
    length = defaultdict(list)  # (arm, role) -> chars
    for g in gens:
        probe = probes[g["probe"]]
        if not g["parsed"]:
            continue
        strings = strings_of(g["parsed"], probe)
        for it in probe["items"]:
            s = strings[it["key"]]
            length[(g["arm"], it["role"])].append(len(s))
            if it["role"] == "note":
                key = (g["arm"], "應為空" if not it["must_convey"] else "應有內容")
                note_stats[key][1] += 1
                note_stats[key][0] += 1 if s.strip() else 0
    out.append("## note 元件：非空率（生成檔直接統計，不經 judge）")
    out.append("")
    out.append("| arm | 題目要求 | n | 非空率 |")
    out.append("| --- | --- | --- | --- |")
    for (arm, exp), (ne, n) in sorted(note_stats.items()):
        out.append(f"| {arm} | {exp} | {n} | {ne / n:.0%} |")
    out.append("")
    out.append("（「應為空」= must_convey 為空的備註欄位；非空即 priming 或多餘。「應有內容」= 有必要事實的備註；非空是正確的。）")
    out.append("")
    out.append("## 字串長度（字元數中位數，依元件 × arm）")
    out.append("")
    arms_all = sorted({a for a, _ in length})
    roles_all = sorted({r for _, r in length})
    out.append("| role | " + " | ".join(arms_all) + " |")
    out.append("| --- | " + " | ".join("---" for _ in arms_all) + " |")
    for role in roles_all:
        cells = []
        for arm in arms_all:
            xs = sorted(length.get((arm, role), []))
            cells.append(str(xs[len(xs) // 2]) if xs else "—")
        out.append(f"| {role} | " + " | ".join(cells) + " |")
    out.append("")

    # judge agreement on surplus
    judges = sorted({r["judge"] for r in rows})
    if len(judges) >= 2:
        out.append("## Judge 一致性（surplus，Cohen's κ）")
        out.append("")
        idx = defaultdict(dict)
        for r in rows:
            idx[(r["channel"], r["arm"], r["probe"], r["sample"], r["key"])][r["judge"]] = r["surplus"]
        for i in range(len(judges)):
            for j in range(i + 1, len(judges)):
                a, b = judges[i], judges[j]
                pairs = [(v[a], v[b]) for v in idx.values() if a in v and b in v]
                if not pairs:
                    continue
                n = len(pairs)
                po = sum(1 for x, y in pairs if x == y) / n
                pa = sum(x for x, _ in pairs) / n
                pb = sum(y for _, y in pairs) / n
                pe = pa * pb + (1 - pa) * (1 - pb)
                kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0
                out.append(f"- {a} vs {b}: n={n}, 觀察一致 {po:.0%}, κ={kappa:.2f}")
        out.append("")
    (OUT / "report.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("contamination")
    c.add_argument("--skill-dir", default="")
    c.add_argument("--reverse", action="store_true",
                   help="check probe briefs/facts against the skill text (skill written after probes)")
    g = sub.add_parser("generate")
    g.add_argument("--channel", required=True)
    g.add_argument("--arms", default=",".join(ARMS))
    g.add_argument("--samples", type=int, default=2)
    g.add_argument("--probes", default="")
    g.add_argument("--redo", action="store_true")
    j = sub.add_parser("judge")
    j.add_argument("--judge", required=True)
    j.add_argument("--channels", default="")
    j.add_argument("--batch", type=int, default=8)
    j.add_argument("--seed", type=int, default=7)
    j.add_argument("--redo", action="store_true")
    s = sub.add_parser("sample-for-human")
    s.add_argument("--n", type=int, default=40)
    s.add_argument("--seed", type=int, default=11)
    d = sub.add_parser("dry")
    d.add_argument("--channel-label", required=True)
    d.add_argument("--arms", default="control,skill")
    d.add_argument("--probes", default="")
    i = sub.add_parser("ingest")
    i.add_argument("--channel-label", required=True)
    h = sub.add_parser("human")
    h.add_argument("--rated", required=True)
    h.add_argument("--key", required=True)
    sub.add_parser("report")
    args = ap.parse_args(argv)
    return {"contamination": cmd_contamination, "generate": cmd_generate, "judge": cmd_judge,
            "sample-for-human": cmd_sample, "dry": cmd_dry, "ingest": cmd_ingest,
            "human": cmd_human, "report": cmd_report}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
