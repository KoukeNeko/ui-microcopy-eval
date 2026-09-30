<h1 align="center">ui-microcopy-eval</h1>

<p align="center">
  <strong>The measurement behind the <a href="https://github.com/KoukeNeko/ui-microcopy">ui-microcopy</a> skill.</strong><br>
  Held-out briefs from two authors, seven model channels, judges from other model families, paired analysis — and every generation and verdict, checked in.
</p>

<p align="center">
  <img alt="Held-out briefs" src="https://img.shields.io/badge/HELD--OUT-32_BRIEFS-2196F3?style=for-the-badge">
  <img alt="Records" src="https://img.shields.io/badge/RECORDS-2%2C016_GEN_·_2%2C746_VERDICTS-4CAF50?style=for-the-badge">
  <img alt="Python 3, no dependencies" src="https://img.shields.io/badge/PYTHON_3-NO_DEPS-00A5A5?style=for-the-badge&logo=python&logoColor=white">
</p>

<p align="center">
  <strong>English</strong> · <a href="README.zh-TW.md">繁體中文</a>
</p>

<p align="center">
  <a href="#what-is-measured">What is measured</a>
  · <a href="#results">Results</a>
  · <a href="#running-it">Running it</a>
  · <a href="#reading-a-result-honestly">Reading a result</a>
  · <a href="#repository-layout">Layout</a>
</p>

```sh
python3 v2/eval_v2.py contamination --skill-dir ~/.claude/skills/ui-microcopy          # both ways
python3 v2/eval_v2.py generate --channel ollama:gemma4:31b-cloud --arms control,skill --samples 2
python3 v2/eval_v2.py judge --judge ollama:nemotron-3-super:cloud
python3 v2/eval_v2.py report
```

```text
| judge    | author | arm      | pairs | b  | c  | net Δ | clustered 95% CI | Δ facts |
| gemma    | all    | skill v2 | 504   | 80 | 42 | +8%   | +1% … +15%       | −3.4%   |
| nemotron | all    | skill v2 | 271   | 36 | 14 | +8%   | +1% … +15%       | +1.1%   |
```

The first version of the skill was written, probed and graded by one model in one session, and it
looked excellent — until an audit showed that three quarters of the grader's forbidden strings were
sitting in the skill text and two probes quoted the skill's own sentences. A skill that grades
itself measures obedience, not generalisation. This repository is the harness built to replace that
number with one that can be wrong.

**Nothing here has seen the skill.** The 32 briefs were written by two authors from different model
families, neither shown the skill or its strings; a two-way grep confirms no string crosses from
skill to probe or back. The judges are models from families that wrote none of the skill, scoring
two axes from a rubric that names the element and the required facts but never the doctrine.

**Every number is paired.** An arm is compared with control on the same model, the same brief, the
same sample and the same field, with McNemar's b/c counts and a bootstrap confidence interval
clustered by brief. The absolute pass rates are in the report too, but they are not the claim.

## What is measured

### Held-out evaluation (`v2/`)

| | |
| --- | --- |
| **Briefs** | 32 in `v2/probes_v2/` — 16 Claude-written, 16 GPT-written; ten product scenarios, ten element types; zh-TW 20, en 6, ja 6. Each string's required facts (`must_convey`) come from the brief's author. |
| **Arms** | `control` (brief only) · `rules` (a negative list, each "don't" with its replacement) · `exemplar` (element → form → example, no prohibitions) · `schema` (per-field length and emptiness only) · `skill` (v1) · `skill2` / `skill2b` (v2 drafts) · `postfilter` (control output through the linter's patterns, runtime briefs only) |
| **Channels** | `ollama:<model>` (deepseek, gemma4, nemotron, glm), `codex` (GPT-6 in an isolated `CODEX_HOME`), `cloakgpt:<session>`, `dry` + `ingest` for a hand-driven agent. Claude runs come from subagents that carry the user's rule file and are labelled *rules-in-context*, never control. |
| **Judges** | gemma4 and nemotron. Each string gets `facts_present` and `surplus`, 0/1; records are shuffled across arms and judged in batches with the arm label removed; a judge never scores its own family in the headline numbers. |
| **Human calibration** | 108 strings blind-rated by the person who raised the complaint — one random stratified batch, one stratified by judge verdict. |
| **Objective measures** | Language leak (CJK in an English answer, a Simplified-only character in a zh-TW answer, kanji-only in a Japanese one), note emptiness, string length — read straight from the generations, no judge. |

### Lexicon delivery (`v2/drift/`)

Sixteen zh-TW briefs written to invite China terms without naming them (「app 為了加快載入而暫存在
裝置上的資料」, not 快取), five ways of handing the model the term table, four models, two samples
each, 640 generations, scored by the skill's linter rules alone.

### The first harness (`run_eval.py`, `fixtures.json`, `results/`)

Nine probes, four arms, scored by the linter plus each probe's require/forbid patterns. Kept as the
record of what was measured first and why it did not count: the probes and the grader share text
with the skill they were grading. Its results are development evidence; the tables below do not
rest on them.

## Results

### Skill against control, matched channels

Net pass Δ = (b − c)/n where pass is *no surplus and every required fact present*; CI is a
brief-clustered bootstrap. Channels present in both v1 and v2 (Claude Haiku and Sonnet, deepseek,
gemma, nemotron); judges never score their own family.

| judge | briefs | rules | exemplar | schema | skill v1 | skill v2 |
| --- | --- | --- | --- | --- | --- | --- |
| gemma | all 32 | +12 [+2, +21] | +7 [−4, +18] | 0 [−6, +8] | +8 [0, +15] | **+8 [+1, +15]** |
| gemma | Claude-written | +18 [+6, +31] | +12 [−3, +28] | +2 [−7, +13] | +16 [+8, +25] | +13 [+3, +23] |
| gemma | GPT-written | +4 [−9, +15] | −1 [−11, +8] | −3 [−12, +5] | −5 [−16, +3] | 0 [−8, +8] |
| nemotron | all 32 | −2 [−14, +11] | −1 [−12, +8] | −8 [−17, +3] | −2 [−12, +7] | **+8 [+1, +15]** |
| nemotron | Claude-written | +9 [−13, +29] | +4 [−11, +19] | −4 [−19, +14] | +2 [−11, +14] | +14 [+5, +21] |
| nemotron | GPT-written | −12 [−26, −1] | −7 [−23, +6] | −11 [−24, +1] | −8 [−22, +5] | +1 [−8, +9] |

Δ required-facts (gemma): rules −6.5, exemplar −8.3, schema −11.6, skill v1 −6.5, skill v2 −3.4;
under nemotron −9.7, −2.2, −11.6, −7.9, **+1.1**. On the GPT-written half, v1 lost 15.7 points of
required facts; v2 lost 8.8 (gemma) and 1.7 (nemotron). Every intervention that taught deletion
deleted facts; v2 is the one that put facts and language ahead of deletion.

Objective measures: strings containing Chinese on English briefs — deepseek 53% → 15%, gemma
41% → 0%, nemotron 82% → 0% (v1 → v2); notes whose brief listed no facts filled 88% by control,
12% by v1, 0% by v2; the linter as a post-filter −1 pp [−3, 0] with Δ facts −4.0. Judge agreement
on surplus, gemma vs nemotron: κ 0.45 on 1,276 shared strings.

### What the human saw

108 blind ratings: 4 strings marked surplus (3.7%), 0 marked missing information; all 25 control
strings clean. Of 27 strings the judge had flagged, the rater agreed with one — judge precision 5%,
κ ≈ 0. What the rater objected to was an invented claim (「不會儲存**或追蹤**」 where the brief said
only *not stored*) and one over-instruction; what the judge flagged and the rater let pass was
"successfully", a purpose clause, an onboarding benefit clause, an example inside an error and an
exclamation mark on a confirmation. The judge measures strict compliance with the doctrine; the
person who asked for the doctrine does not apply it that strictly. Details in
[`v2/eval_v2/human_calibration.md`](v2/eval_v2/human_calibration.md).

### Lexicon delivery

| arm | strings | any China term | 95% CI | canonical Taiwan term |
| --- | --- | --- | --- | --- |
| control (brief only) | 315 | **0.0%** | 0–1% | 42.9% |
| one negative line 「不用中國大陸用語」 | 333 | **2.4%** | 1–5% | 45.3% |
| the 1–3 rows relevant to the screen | 366 | 0.0% | 0–1% | **65.6%** |
| the whole 40-row table | 354 | 0.0% | 0–1% | 51.1% |
| the table plus 60 noise rows | 360 | 0.3% | 0–2% | 51.9% |

Four models leak no China terms on their own; the only condition that leaked was the lone negative
line (deepseek wrote 卸載 six times where control wrote 解除安裝 six times); the rows relevant to the
screen are what raise use of the canonical term, and the whole table does about half as well.
Per-model and per-brief tables in [`v2/drift/results.md`](v2/drift/results.md).

## Running it

Python 3, no dependencies. Generation needs a model channel: an Ollama daemon on `localhost:11434`
for `ollama:<model>`, the Codex CLI for `codex`, a CloakGPT session for `cloakgpt:<id>`. The skill
under test is read from `~/.claude/skills/ui-microcopy` (or a `skill_v2/` folder beside the script).

```sh
# 1. prove the briefs and the skill share no strings, in both directions
python3 v2/eval_v2.py contamination --skill-dir ~/.claude/skills/ui-microcopy
python3 v2/eval_v2.py contamination --skill-dir ~/.claude/skills/ui-microcopy --reverse

# 2. generate — one channel at a time, two samples per brief × arm
python3 v2/eval_v2.py generate --channel ollama:deepseek-v4.1-flash:cloud --arms control,rules,exemplar,schema,skill,skill2b --samples 2
python3 v2/eval_v2.py generate --channel codex --arms control,skill --samples 2

# 3. judge with a model from another family than the subjects it scores
python3 v2/eval_v2.py judge --judge ollama:gemma4:31b-cloud
python3 v2/eval_v2.py judge --judge ollama:nemotron-3-super:cloud

# 4. calibrate against a person, then report
python3 v2/eval_v2.py sample-for-human --n 40          # writes a blind sheet + a key
python3 v2/eval_v2.py human --rated human_sample.rated.md --key human_sample.key.json
python3 v2/eval_v2.py report                            # paired tables, leak, emptiness, κ

# a channel driven by hand (an agent, a person)
python3 v2/eval_v2.py dry --channel-label claude-sonnet-rules-in-context --arms control,skill2b
#   ... fill eval_v2/pending/<channel>/<arm>/<probe>.<k>.txt ...
python3 v2/eval_v2.py ingest --channel-label claude-sonnet-rules-in-context

# lexicon delivery
python3 v2/drift/run.py                 # 16 briefs × 5 arms × 4 models × 2 samples
python3 v2/drift/score.py > v2/drift/results.md

# the first harness
python3 run_eval.py --channel ollama:glm-5.3:cloud --arms control,rules,skill
python3 run_eval.py --score results/final
```

Records land in `v2/eval_v2/gen/<channel>/<arm>/<probe>.<k>.json` and
`v2/eval_v2/judge/<judge>/<channel>/<arm>/<probe>.<k>.json`; `report` reads whatever is there.
Anything that changes the skill's examples is followed by the contamination check; anything that
changes the rubric is followed by a new human sample.

## Reading a result honestly

- **Pair within a channel.** `control → skill` on the same model, brief, sample and field is the
  effect of the skill. Absolute pass rates mix channels with different coverage and are descriptive
  only.
- **Two judges, or none.** gemma and nemotron disagreed about v1 (+8 versus −2) and agreed about v2.
  A number from one judge is a number from one judge.
- **The judge is stricter than the user.** κ with the human was near zero in both batches. Between-arm
  differences say how closely an arm follows the strict reading of the doctrine, not how much a
  person would mind.
- **Watch the facts axis.** An arm that raises "no surplus" while lowering "facts present" has taught
  deletion. The pass definition requires both.
- **Claude channels are not controls.** Subagents on this machine carry the user's rule file; their
  rows answer "does the skill add anything over the rules already in context?"
- **Development, not confirmatory.** The v2 language fix was made after seeing draft-1 results on
  these briefs, and the shipped skill has two later edits (example scrub, note slots) that were not
  re-measured. A confirmatory run needs a frozen skill and briefs nobody has seen.

## Repository layout

```text
v2/
  eval_v2.py                       held-out harness: contamination, generate, judge, human, report
  probes_v2/
    probes_claude.json             16 briefs, Claude-written
    probes_gpt.json                16 briefs, GPT-written
    SCHEMA.md                      brief format
    judge_rubric.md                the two-axis rubric the judges see
    arms/rules_only.md             the negative-list arm
    arms/exemplar_only.md          the positive-example arm
  eval_v2/
    gen/<channel>/<arm>/           2,016 generations
    judge/<judge>/<channel>/<arm>/ 2,746 verdicts
    report.md                      the full tables the README summarises
    human_calibration.md           both blind batches, with κ
    human_sample1.rated.md, human_sample2.rated.md
  drift/
    probes.json, run.py, score.py  lexicon-delivery experiment
    gen/                           640 generations
    results.md
run_eval.py, fixtures.json, results/   the first harness and its runs
```

## Limits

- 32 briefs, two samples each, 32 cluster units: effects of ten points or more are visible, finer ones
  are not. A confirmatory design needs on the order of 120–390 briefs.
- One human rater, who is also the complainant; this is calibration, not inter-rater reliability.
- GPT-6 has no v2 run (Codex quota exhausted mid-run); glm ran only the Claude-written half.
- The judges' surplus criterion and the skill's doctrine share a taxonomy; a pass rate is not a
  measure of interface quality.
- The drift experiment covers four open models and 16 briefs; "canonical Taiwan term" is a narrow
  definition (「暫存資料」 for 快取 counts as neither a hit nor an error).
