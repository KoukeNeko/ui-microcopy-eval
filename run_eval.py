#!/usr/bin/env python3
"""Control-group harness for UI microcopy.

Sends the same probes to the same model with different amounts of guidance and
scores every answer with the linter from the `ui-microcopy` skill:

  control  the task alone — what the model does unprompted
  rules    the task plus the canonical doctrine (~/.claude/rules/ui-microcopy.md)
  skill    the task plus the ui-microcopy skill's references
  patched  the task with the fixture's revised field contract, when it has one

A probe fails when a required string is missing, a forbidden pattern appears,
or the linter raises an error on the answer.

  python3 run_eval.py --channel ollama:glm-5.3:cloud --arms control,skill

Channels: ``codex``, ``ollama:<model>``, ``cloakgpt:<session-id>``, ``dry``
(writes the prompts and scores nothing, for a channel driven by hand),
``subagent`` (writes prompts to ``<out>/pending`` for an agent to fill, then
``--ingest`` reads its answers back).

  python3 run_eval.py --score <out-dir>     aggregate a run into report.md
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent / "ui-microcopy"
DOCTRINE = Path.home() / ".claude" / "rules" / "ui-microcopy.md"
sys.path.insert(0, str(SKILL / "scripts"))
from microcopy_lint import lint_text  # noqa: E402

ARMS = ("control", "rules", "skill", "patched")
SKILL_FILES = (
    "SKILL.md",
    "references/roles.md",
    "references/failure-modes.md",
    "references/zh-tw-lexicon.md",
)
RUNTIME_FILE = "assets/runtime-prompt-block.zh-TW.md"

ANSI = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]|\x1b\][^\x07]*\x07")
FENCE = re.compile(r"```(?:json)?", re.I)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def extract_json(text: str) -> dict | None:
    """The answer's JSON object, braces balanced so a trailing sentence does
    not break it.

    A model that thinks out loud usually echoes the requested shape as
    ``{"s1": "..."}`` before answering, so placeholder objects are dropped and
    the last real one wins — the answer is written after the reasoning, never
    before it.
    """
    text = FENCE.sub("", text)
    found: list[dict] = []
    cursor = 0
    while True:
        start = text.find("{", cursor)
        if start == -1:
            break
        end = _matching_brace(text, start)
        if end is None:
            cursor = start + 1
            continue
        try:
            found.append(json.loads(text[start : end + 1]))
        except json.JSONDecodeError:
            pass
        # Skip the object whole, so its nested objects are not read as
        # answers in their own right.
        cursor = end + 1
    real = [obj for obj in found if not _is_placeholder(obj)]
    return (real or found or [None])[-1]


def _matching_brace(text: str, start: int) -> int | None:
    depth = 0
    in_string = False
    escaped = False
    for i in range(start, len(text)):
        char = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return i
    return None


def _is_placeholder(obj: dict) -> bool:
    values = [v for v in obj.values() if isinstance(v, str)]
    return bool(values) and all(v.strip("...… 　") == "" for v in values)


def build_prompt(fixture: dict, arm: str) -> str:
    """The whole instruction a channel receives: the probe, then whatever
    guidance the arm adds."""
    if arm == "patched":
        return fixture.get("task_patched") or fixture["task"]
    task = fixture["task"]
    if arm == "control":
        return task
    if arm == "rules":
        return f"{task}\n\n---\n以下是這個專案既有的介面文字規則，請遵守：\n\n{read(DOCTRINE)}"
    parts = [read(SKILL / name) for name in SKILL_FILES]
    if fixture.get("kind") == "runtime":
        parts.append(read(SKILL / RUNTIME_FILE))
    return f"{task}\n\n---\n以下是 ui-microcopy skill 的規則與案例，請遵守：\n\n" + "\n\n".join(parts)


# --------------------------------------------------------------------------
# Channels


def run_codex(prompt: str) -> str:
    """Codex with a throwaway CODEX_HOME, so the user's own AGENTS.md and
    config cannot leak into an arm. The home holds a copy of the login, so it
    lives in a temporary directory that is removed after the call, never
    under results."""
    with tempfile.TemporaryDirectory(prefix="microcopy-codex-") as tmp:
        home = Path(tmp) / "codex-home"
        home.mkdir()
        auth = Path.home() / ".codex" / "auth.json"
        if auth.exists():
            shutil.copy(auth, home / "auth.json")
        env = {**os.environ, "CODEX_HOME": str(home)}
        proc = subprocess.run(
            [
                "codex",
                "exec",
                "--skip-git-repo-check",
                "-s",
                "read-only",
                "-C",
                tmp,
                prompt,
            ],
            capture_output=True,
            text=True,
            env=env,
            timeout=900,
        )
    if proc.returncode != 0 and not proc.stdout:
        raise RuntimeError(f"codex failed: {proc.stderr.strip()[:400]}")
    return proc.stdout


def run_ollama(prompt: str, model: str) -> str:
    """Through the local HTTP API rather than the CLI: the CLI rewraps lines to
    the terminal width, which breaks a JSON string mid-word."""
    import urllib.error
    import urllib.request

    body = json.dumps(
        {"model": model, "prompt": prompt, "stream": False, "think": False}
    ).encode()
    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=900) as response:
            payload = json.loads(response.read())
    except urllib.error.URLError as exc:
        raise RuntimeError(f"ollama api unreachable: {exc}") from exc
    if payload.get("error"):
        raise RuntimeError(f"ollama error: {payload['error']}")
    # A thinking model returns its reasoning in the same field.
    return re.sub(r"<think(?:ing)?>.*?</think(?:ing)?>", "", payload.get("response", ""), flags=re.S)


def run_cloakgpt(prompt: str, session: str) -> str:
    """``cloakgpt:new`` asks each probe in its own conversation, so one answer
    cannot set the style for the next. ``cloakgpt:auto`` opens a persistent
    session for each probe instead, which survives a signed-in profile where
    repeated one-shot pages do not."""
    if session == "auto":
        opened = subprocess.run(
            ["cloakgpt", "session", "open"], capture_output=True, text=True, timeout=600
        )
        lines = [line for line in opened.stdout.splitlines() if line.strip()]
        if not lines:
            raise RuntimeError(f"cloakgpt session open failed: {opened.stderr[:200]}")
        session = lines[-1].strip()
    argv = ["cloakgpt", "ask", prompt]
    if session != "new":
        argv += ["--session", session]
    proc = subprocess.run(
        argv + ["--output", "jsonl"],
        capture_output=True,
        text=True,
        timeout=3600,
    )
    answer = ""
    for line in proc.stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "result":
            answer = event.get("answer", "")
    if not answer:
        raise RuntimeError(f"cloakgpt returned no answer (rc={proc.returncode})")
    return answer


def call(channel: str, prompt: str) -> str:
    kind, _, arg = channel.partition(":")
    if kind == "codex":
        return run_codex(prompt)
    if kind == "ollama":
        return run_ollama(prompt, arg)
    if kind == "cloakgpt":
        return run_cloakgpt(prompt, arg)
    raise RuntimeError(f"channel {channel} has to be driven by hand")


# --------------------------------------------------------------------------
# Scoring


def score(fixture: dict, parsed: dict | None, raw: str) -> dict:
    result = {"probe": fixture["id"], "kind": fixture.get("kind", "strings")}
    problems: list[str] = []
    findings: list[dict] = []

    if parsed is None:
        result.update(ok=False, problems=["答案裡找不到 JSON"], findings=[])
        return result

    if result["kind"] == "runtime":
        notes = parsed.get("notes")
        text = "；".join(str(n) for n in notes) if isinstance(notes, list) else ""
        if not isinstance(notes, list):
            problems.append("notes 不是陣列")
        check = fixture["checks"]["notes"]
        for pattern in check.get("require", []):
            if not re.search(pattern, text):
                problems.append(f"缺少必要內容 /{pattern}/")
        for pattern in check.get("forbid", []):
            if re.search(pattern, text):
                problems.append(f"出現禁止樣式 /{pattern}/")
        findings = [f.as_dict() for f in lint_text("ai-note", text)]
        extra = fixture.get("extra", {})
        items = parsed.get("items")
        if extra.get("items_name_contains"):
            names = " ".join(
                str(item.get("name", "")) for item in items if isinstance(item, dict)
            ) if isinstance(items, list) else ""
            if extra["items_name_contains"] not in names:
                problems.append(f"item 名稱缺少 {extra['items_name_contains']}")
        if extra.get("items_kcal_number"):
            first = items[0] if isinstance(items, list) and items else {}
            if not isinstance(first, dict) or not isinstance(first.get("kcal"), (int, float)):
                problems.append("kcal 不是數字")
        result["text"] = text
    else:
        texts = {}
        for item in fixture["items"]:
            key, role = item["key"], item["role"]
            value = parsed.get(key)
            if not isinstance(value, str) or not value.strip():
                problems.append(f"{key} 沒有文字（role={role}）")
                continue
            texts[key] = value
            check = fixture["checks"].get(key, {})
            for pattern in check.get("require", []):
                if not re.search(pattern, value):
                    problems.append(f"{key} 缺少必要內容 /{pattern}/：{value!r}")
            for pattern in check.get("forbid", []):
                if re.search(pattern, value):
                    problems.append(f"{key} 出現禁止樣式 /{pattern}/：{value!r}")
            findings.extend(f.as_dict() for f in lint_text(role, value))
        result["text"] = "\n".join(texts.values())

    errors = [f for f in findings if f["severity"] == "error"]
    result["ok"] = not problems and not errors
    result["problems"] = problems
    result["findings"] = findings
    result["error_rules"] = sorted({f["rule"] for f in errors})
    return result


def rescore(out: Path) -> None:
    """Re-score the saved answers, for when a rule or a parser changed and the
    models should not be asked again."""
    fixtures = {f["id"]: f for f in json.loads(read(HERE / "fixtures.json"))}
    for channel in sorted(
        p for p in out.iterdir() if p.is_dir() and p.name not in {"pending", "work"}
    ):
        for arm_dir in sorted(p for p in channel.iterdir() if p.is_dir()):
            for raw_file in sorted(arm_dir.glob("*.txt")):
                if raw_file.stem not in fixtures:
                    continue
                raw = raw_file.read_text(encoding="utf-8")
                (arm_dir / f"{raw_file.stem}.json").write_text(
                    json.dumps(
                        {
                            **score(
                                fixtures[raw_file.stem], extract_json(raw), raw
                            ),
                            "raw": raw,
                        },
                        ensure_ascii=False,
                        indent=2,
                    ),
                    encoding="utf-8",
                )
    print(report(out))


def ingest(out: Path, channel_label: str) -> None:
    """Score the answers a hand-driven channel wrote into ``pending``."""
    fixtures = {f["id"]: f for f in json.loads(read(HERE / "fixtures.json"))}
    pending = out / "pending"
    done = 0
    for arm_dir in sorted(pending.glob("*")):
        for answer in sorted(arm_dir.glob("*.txt")):
            # ``P3.prompt.txt`` is the question, not the answer.
            if "." in answer.stem:
                continue
            probe = answer.stem
            if probe not in fixtures:
                continue
            target = out / channel_label / arm_dir.name / f"{probe}.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            raw = answer.read_text(encoding="utf-8")
            target.write_text(
                json.dumps(
                    {**score(fixtures[probe], extract_json(raw), raw), "raw": raw},
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            done += 1
    print(f"scored {done} answers into {out / channel_label}")


# --------------------------------------------------------------------------
# Report


def report(out: Path) -> str:
    channels = sorted(
        p for p in out.iterdir() if p.is_dir() and p.name not in {"pending", "work"}
    )
    lines = ["# ui-microcopy 對照組結果", ""]
    lines.append(f"執行時間：{time.strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    lines.append("| 模型 / 管道 | 組別 | 通過 probe | 禁止樣式命中 | linter error 筆數 |")
    lines.append("| --- | --- | --- | --- | --- |")
    totals: dict[str, dict[str, int]] = {}
    for channel in channels:
        for arm_dir in sorted(channel.iterdir()):
            arm = arm_dir.name
            files = sorted(arm_dir.glob("*.json"))
            if not files:
                continue
            passed = banned = errors = 0
            for path in files:
                data = json.loads(path.read_text(encoding="utf-8"))
                passed += 1 if data.get("ok") else 0
                banned += sum(
                    1 for p in data.get("problems", []) if "禁止樣式" in p
                )
                errors += len(data.get("error_rules", []))
            totals.setdefault(channel.name, {})[arm] = passed
            lines.append(
                f"| {channel.name} | {arm} | {passed}/{len(files)} | {banned} | {errors} |"
            )
    lines.append("")
    lines.append("## 逐題結果")
    lines.append("")
    order = {"control": "C", "rules": "R", "skill": "S", "patched": "P"}
    probes = sorted(
        {p.stem for channel in channels for arm in channel.iterdir() for p in arm.glob("*.json")}
    )
    names = [c.name for c in channels]
    lines.append("| probe | " + " | ".join(names) + " |")
    lines.append("| --- | " + " | ".join("---" for _ in names) + " |")
    for probe in probes:
        row = []
        for channel in channels:
            marks = []
            for arm in ("patched", "control", "rules", "skill"):
                path = channel / arm / f"{probe}.json"
                if path.exists():
                    ok = json.loads(path.read_text(encoding="utf-8")).get("ok")
                    marks.append(f"{order[arm]}{'✓' if ok else '✗'}")
            row.append(" ".join(marks) if marks else "—")
        lines.append(f"| {probe} | " + " | ".join(row) + " |")
    lines.append("")
    lines.append("C = control（只給任務）、R = rules（專案既有規則）、"
                 "S = skill（ui-microcopy）、P = patched（修訂後的 app 內 prompt）。")
    text = "\n".join(lines) + "\n"
    (out / "report.md").write_text(text, encoding="utf-8")
    return text


# --------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--channel", default="dry")
    parser.add_argument("--arms", default="control,rules,skill")
    parser.add_argument("--probes", default="")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--score", type=Path, default=None)
    parser.add_argument("--rescore", type=Path, default=None)
    parser.add_argument("--ingest", action="store_true")
    parser.add_argument("--label", default="")
    args = parser.parse_args(argv)

    if args.score:
        print(report(args.score))
        return 0
    if args.rescore:
        rescore(args.rescore)
        return 0

    fixtures = json.loads(read(HERE / "fixtures.json"))
    wanted = args.probes.split(",") if args.probes else None
    arms = [a for a in args.arms.split(",") if a]
    unknown = [a for a in arms if a not in ARMS]
    if unknown:
        parser.error(f"unknown arm(s): {unknown}")

    stamp = time.strftime("%Y%m%d-%H%M")
    label = args.label or args.channel.replace(":", "-").replace("/", "-")
    out = args.out or (HERE / "results" / f"{stamp}-{label}")
    out.mkdir(parents=True, exist_ok=True)
    (out / "meta.json").write_text(
        json.dumps(
            {"channel": args.channel, "arms": arms, "probes": wanted, "started": stamp},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    if args.ingest:
        ingest(out, label)
        print(report(out))
        return 0

    for fixture in fixtures:
        if wanted and fixture["id"] not in wanted:
            continue
        for arm in arms:
            if arm == "patched" and not fixture.get("task_patched"):
                continue
            prompt = build_prompt(fixture, arm)
            target = out / label / arm
            target.mkdir(parents=True, exist_ok=True)
            stem = f"{fixture['id']}"
            if args.channel == "dry":
                pending = out / "pending" / arm
                pending.mkdir(parents=True, exist_ok=True)
                (pending / f"{stem}.prompt.txt").write_text(prompt, encoding="utf-8")
                print(f"prepared {fixture['id']} {arm}")
                continue
            print(f"[{time.strftime('%H:%M:%S')}] {fixture['id']} {arm} …", flush=True)
            try:
                raw = ANSI.sub("", call(args.channel, prompt))
            except Exception as exc:  # a channel failure is data too, not a crash
                raw = ""
                print(f"    channel error: {exc}", flush=True)
            (target / f"{stem}.txt").write_text(raw, encoding="utf-8")
            scored = {**score(fixture, extract_json(raw), raw), "raw": raw}
            (target / f"{stem}.json").write_text(
                json.dumps(scored, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            print(f"    {'ok' if scored['ok'] else 'FAIL'}", flush=True)

    if args.channel != "dry":
        print(report(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
