<h1 align="center">ui-microcopy-eval</h1>

<p align="center">
  <strong>The evaluation harness and measurement record for the <a href="https://github.com/KoukeNeko/ui-microcopy">ui-microcopy</a> skill.</strong><br>
  Held-out briefs from two authors, seven model channels, judges from other model families, paired analysis; every generation and verdict is checked in.
</p>

<p align="center">
  <img alt="Held-out briefs" src="https://img.shields.io/badge/HELD--OUT-32_BRIEFS-2196F3?style=for-the-badge">
  <img alt="Records" src="https://img.shields.io/badge/RECORDS-2%2C016_GEN_·_2%2C746_VERDICTS-4CAF50?style=for-the-badge">
  <img alt="Python 3, no dependencies" src="https://img.shields.io/badge/PYTHON_3-NO_DEPS-00A5A5?style=for-the-badge&logo=python&logoColor=white">
</p>

<p align="center">
  <a href="README.md">繁體中文</a> · <strong>English</strong>
</p>

<p align="center">
  <a href="#design">Design</a>
  · <a href="#results">Results</a>
  · <a href="#running">Running</a>
  · <a href="#interpretation">Interpretation</a>
  · <a href="#repository-layout">Layout</a>
</p>

```sh
python3 v2/eval_v2.py contamination --skill-dir ~/.claude/skills/ui-microcopy          # both directions
python3 v2/eval_v2.py generate --channel ollama:gemma4:31b-cloud --arms control,skill --samples 2
python3 v2/eval_v2.py judge --judge ollama:nemotron-3-super:cloud
python3 v2/eval_v2.py report
```

```text
| judge    | author | arm      | pairs | b  | c  | net Δ | clustered 95% CI | Δ facts |
| gemma    | all    | skill v2 | 504   | 80 | 42 | +8%   | +1% … +15%       | −3.4%   |
| nemotron | all    | skill v2 | 271   | 36 | 14 | +8%   | +1% … +15%       | +1.1%   |
```

## Overview

The first version of the skill was written, probed and graded by one model in one session. An
audit found three quarters of the grader's forbidden strings in the skill body and two probes
quoting the skill's sentences. Such an evaluation measures compliance, not generalisation. This
repository is the harness built to replace it, on two principles.

- **Neither the briefs nor the judges have seen the skill.** The 32 briefs were written by authors
  from two model families, neither given the skill or its strings; a two-way grep confirms that no
  string crosses between skill and briefs. The judges are models from families that did not write
  the skill, scoring from a rubric that names the element and the required facts and omits the
  doctrine.
- **Every figure is a paired comparison.** An arm is compared with control on the same model,
  brief, sample and field, with McNemar's b/c counts and a brief-clustered bootstrap confidence
  interval. Absolute pass rates appear in the report for description only.

## Design

### Held-out evaluation (`v2/`)

| | |
| --- | --- |
| **Briefs** | 32 in `v2/probes_v2/`: 16 Claude-written, 16 GPT-written; ten product scenarios, ten element types; zh-TW 20, en 6, ja 6. Each string's required facts (`must_convey`) are listed by the brief's author. |
| **Arms** | `control` (brief only) · `rules` (a negative list, each item with its replacement) · `exemplar` (element → form → example, no prohibitions) · `schema` (per-field length and emptiness only) · `skill` (v1) · `skill2` / `skill2b` (v2 drafts) · `postfilter` (control output through the linter's patterns, runtime briefs only) |
| **Channels** | `ollama:<model>` (deepseek, gemma4, nemotron, glm), `codex` (GPT-6 in an isolated `CODEX_HOME`), `cloakgpt:<session>`, `dry` + `ingest` for a hand-driven agent. Claude results come from subagents carrying the user's rule file and are labelled *rules-in-context*, not control. |
| **Judges** | gemma4 and nemotron. Each string receives `facts_present` and `surplus` (0/1); records are shuffled across arms and judged in batches with the arm label removed; headline figures exclude a judge's verdicts on its own family. |
| **Human calibration** | 108 strings blind-rated by the person who raised the issue: one random stratified batch, one stratified by judge verdict. |
| **Objective measures** | Language leak (CJK in an English answer, a Simplified-only character in a zh-TW answer, kanji only in a Japanese one), note emptiness, string length; computed from the generations directly. |

### Lexicon delivery (`v2/drift/`)

Sixteen zh-TW briefs describing a screen without naming the target term (「app 為了加快載入而暫存在
裝置上的資料」, not 快取); five ways of supplying the term table, four models, two samples each,
640 generations; scored by the skill's linter rules only.

### The first harness (`run_eval.py`, `fixtures.json`, `results/`)

Nine probes, four arms, scored by the linter and each probe's require/forbid patterns. Retained as
the record of the first measurement; its probes and grader share text with the skill under test,
so its results are development evidence and the tables below do not rest on them.

## Results

### Skill against control, matched channels

Net pass Δ = (b − c)/n, where pass means no surplus and every required fact present; CI is a
brief-clustered bootstrap. Only channels present in both v1 and v2 are counted (Claude Haiku and
Sonnet, deepseek, gemma, nemotron); a judge never scores its own family.

| judge | briefs | rules | exemplar | schema | skill v1 | skill v2 |
| --- | --- | --- | --- | --- | --- | --- |
| gemma | all 32 | +12 [+2, +21] | +7 [−4, +18] | 0 [−6, +8] | +8 [0, +15] | **+8 [+1, +15]** |
| gemma | Claude-written | +18 [+6, +31] | +12 [−3, +28] | +2 [−7, +13] | +16 [+8, +25] | +13 [+3, +23] |
| gemma | GPT-written | +4 [−9, +15] | −1 [−11, +8] | −3 [−12, +5] | −5 [−16, +3] | 0 [−8, +8] |
| nemotron | all 32 | −2 [−14, +11] | −1 [−12, +8] | −8 [−17, +3] | −2 [−12, +7] | **+8 [+1, +15]** |
| nemotron | Claude-written | +9 [−13, +29] | +4 [−11, +19] | −4 [−19, +14] | +2 [−11, +14] | +14 [+5, +21] |
| nemotron | GPT-written | −12 [−26, −1] | −7 [−23, +6] | −11 [−24, +1] | −8 [−22, +5] | +1 [−8, +9] |

Δ required facts (gemma): rules −6.5, exemplar −8.3, schema −11.6, skill v1 −6.5, skill v2 −3.4;
nemotron: −9.7, −2.2, −11.6, −7.9, **+1.1**. On the GPT-written half, v1 lost 15.7 points of
required facts; v2 lost 8.8 (gemma) and 1.7 (nemotron). Every deletion-first intervention lost
facts; v2 places facts and language before deletion.

Objective measures: answers to English briefs containing Chinese, deepseek 53% → 15%, gemma
41% → 0%, nemotron 82% → 0% (v1 → v2); notes whose brief listed no facts, filled 88% by control,
12% by v1, 0% by v2; the linter as a post-filter, −1 pp [−3, 0] with Δ facts −4.0. Judge agreement
on surplus (gemma vs nemotron): κ 0.45, n = 1,276.

### Human calibration

108 blind ratings: 4 strings marked surplus (3.7%), 0 marked missing information; all 25 control
strings clean. Of 27 strings flagged by the judge, the rater agreed with one; judge precision 5%,
κ ≈ 0. The rater's flags were an invented claim (「不會儲存**或追蹤**」 where the brief stated only
"not stored") and one surplus instruction; items flagged by the judge and not by the rater were
"successfully", a purpose clause, an onboarding benefit clause, an example inside an error and an
exclamation mark on a confirmation. The judge measures strict compliance with the doctrine, which
differs from the criterion the person who requested it applies. Details in
[`v2/eval_v2/human_calibration.md`](v2/eval_v2/human_calibration.md).

### Lexicon delivery

| arm | strings | any China term | 95% CI | canonical Taiwan term |
| --- | --- | --- | --- | --- |
| control (brief only) | 315 | **0.0%** | 0–1% | 42.9% |
| one negative line (不用中國用語) | 333 | **2.4%** | 1–5% | 45.3% |
| the 1–3 rows relevant to the screen | 366 | 0.0% | 0–1% | **65.6%** |
| the whole 40-row table | 354 | 0.0% | 0–1% | 51.1% |
| the table plus 60 noise rows | 360 | 0.3% | 0–2% | 51.9% |

Under control, four models produced no China terms; the only condition with leaks was the single
negative line (on one brief deepseek wrote 「解除安裝」 six times under control and 「卸載」 six times with
the line). The rise in canonical-term use comes from the rows relevant to the screen; the whole
table achieves about half the effect. Per-model and per-brief tables in
[`v2/drift/results.md`](v2/drift/results.md).

## Running

Requirements: Python 3, no dependencies. Generation needs a model channel: an Ollama daemon on
`localhost:11434` for `ollama:<model>`, the Codex CLI for `codex`, a CloakGPT session for
`cloakgpt:<id>`. The skill under test is read from `~/.claude/skills/ui-microcopy` (or a
`skill_v2/` folder beside the script).

```sh
# 1. contamination check: no shared strings between briefs and skill, both directions
python3 v2/eval_v2.py contamination --skill-dir ~/.claude/skills/ui-microcopy
python3 v2/eval_v2.py contamination --skill-dir ~/.claude/skills/ui-microcopy --reverse

# 2. generation: one channel per run, two samples per brief × arm
python3 v2/eval_v2.py generate --channel ollama:deepseek-v4.1-flash:cloud --arms control,rules,exemplar,schema,skill,skill2b --samples 2
python3 v2/eval_v2.py generate --channel codex --arms control,skill --samples 2

# 3. judging: a judge from a model family other than the subjects
python3 v2/eval_v2.py judge --judge ollama:gemma4:31b-cloud
python3 v2/eval_v2.py judge --judge ollama:nemotron-3-super:cloud

# 4. human calibration and report
python3 v2/eval_v2.py sample-for-human --n 40          # writes a blind sheet and a key
python3 v2/eval_v2.py human --rated human_sample.rated.md --key human_sample.key.json
python3 v2/eval_v2.py report                            # paired tables, leak, emptiness, κ
python3 v2/final_numbers.py > v2/final_tables.md        # matched-channel Tables A–D

# a hand-driven channel (an agent or a person)
python3 v2/eval_v2.py dry --channel-label claude-sonnet-rules-in-context --arms control,skill2b
#   fill eval_v2/pending/<channel>/<arm>/<probe>.<k>.txt
python3 v2/eval_v2.py ingest --channel-label claude-sonnet-rules-in-context

# lexicon delivery
python3 v2/drift/run.py                 # 16 briefs × 5 arms × 4 models × 2 samples
python3 v2/drift/score.py > v2/drift/results.md

# the first harness
python3 run_eval.py --channel ollama:glm-5.3:cloud --arms control,rules,skill
python3 run_eval.py --score results/final
```

Record paths: `v2/eval_v2/gen/<channel>/<arm>/<probe>.<k>.json` and
`v2/eval_v2/judge/<judge>/<channel>/<arm>/<probe>.<k>.json`; `report` reads all existing records.
A change to the skill's examples requires a new contamination check; a change to the rubric
requires a new human sample.

## Interpretation

- **Pair within a channel.** The skill's effect is the `control → skill` difference on the same
  model, brief, sample and field. Absolute pass rates mix channels with different coverage and are
  descriptive.
- **Two judges.** gemma and nemotron disagreed on v1 (+8 and −2) and agreed on v2. A figure from
  one judge is not a conclusion.
- **The judge's criterion is stricter than the user's.** κ with the human rater was near zero in
  both batches. Between-arm differences reflect compliance with the strict reading of the doctrine,
  not user acceptance.
- **Read the facts axis.** An arm that raises "no surplus" while lowering "facts present" has the
  effect of deletion. The pass definition requires both.
- **Claude channels are not controls.** Subagents on this machine carry the user's rule file; their
  rows answer whether the skill adds anything over the rules already in context.
- **Development evidence.** The v2 language fix followed the first draft's results on these briefs;
  the shipped skill has two later edits (example scrub, note slots) that were not re-measured. A
  confirmatory run requires a frozen skill and unused briefs.

## Repository layout

```text
v2/
  eval_v2.py                       held-out harness: contamination, generate, judge, human, report
  probes_v2/
    probes_claude.json             16 briefs, Claude-written
    probes_gpt.json                16 briefs, GPT-written
    SCHEMA.md                      brief format
    judge_rubric.md                the two-axis rubric given to the judges
    arms/rules_only.md             the negative-list arm
    arms/exemplar_only.md          the positive-example arm
  eval_v2/
    gen/<channel>/<arm>/           2,016 generations
    judge/<judge>/<channel>/<arm>/ 2,746 verdicts
    report.md                      full tables
  final_numbers.py                 matched-channel tables for v1 vs v2 (Tables A–D)
  final_tables.md                  its output
    human_calibration.md           both blind batches, with κ
    human_sample1.rated.md, human_sample2.rated.md
  drift/
    probes.json, run.py, score.py  lexicon-delivery experiment
    gen/                           640 generations
    results.md
run_eval.py, fixtures.json, results/   the first harness and its runs
```

## Limits

- 32 briefs, two samples each, 32 cluster units: effects of ten points or more are detectable; a
  confirmatory design needs on the order of 120–390 briefs.
- One human rater, who is the person who raised the issue; this is calibration, not inter-rater
  reliability.
- GPT-6 has no v2 run (the Codex quota was exhausted during the run); glm ran only the
  Claude-written half.
- The judges' surplus criterion and the skill's doctrine share a taxonomy; a pass rate is not a
  measure of interface quality.
- The lexicon experiment covers four open models and 16 briefs; "canonical Taiwan term" is a narrow
  definition (「暫存資料」 counts neither as 快取 nor as an error).
