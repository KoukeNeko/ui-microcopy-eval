# UI microcopy control groups

A harness that answers "does this model actually avoid the assistant-voice
failure, or does it only sound like it does?" — by putting the same probes to
the same model with different amounts of guidance and scoring every answer
mechanically.

## Design

**Probes** (`fixtures.json`) — nine tasks shaped like real work, each aimed at
one failure mode:

| Probe | Task | Targets |
| --- | --- | --- |
| P1 | installer buttons, completion, write error, blank disk | register drift, affect |
| P2 | rewrite a boot-disk message that reads 「這台機器正從它開機，不能裝」 | assistant voice in a system message |
| P3 | the notes field of a photo nutrition estimate | defensive disclosure |
| P4 | the source label under an AI estimate | provenance meta-commentary |
| P5 | value lines with targets and a range | duplicated hedging |
| P6 | an empty state | coaching, affect, questions |
| P7 | delete-confirmation dialog | question-form titles, affect |
| P8 | a line shown when the calorie target is exceeded | affect, praise |
| P9 | settings button, saved state, upload explanation | zh-TW vocabulary |

Each probe declares its role per string, the patterns it must contain, and the
patterns it must not. P3 is `kind: runtime`: it is answered as the app's own
model would answer it, and it also carries a `task_patched` — the same prompt
with the note-field contract replaced by
`../ui-microcopy/assets/runtime-prompt-block.zh-TW.md`.

**Arms** — the independent variable:

| Arm | What the model receives |
| --- | --- |
| `control` | the task alone |
| `rules` | the task plus `~/.claude/rules/ui-microcopy.md` |
| `skill` | the task plus this machine's `ui-microcopy` skill |
| `patched` | the task with the revised field contract baked in (runtime probes only) |

**Scoring** — `../ui-microcopy/scripts/microcopy_lint.py` plus the probe's own
require/forbid patterns. No LLM judge: judges carry the same length bias that
produced the problem, so "friendlier" would win on appeal
(`../ui-microcopy/references/why.md`).

## Running

```sh
# one model through the local HTTP API (any pulled or cloud model)
python3 run_eval.py --channel ollama:glm-5.3:cloud --arms control,rules,skill

# a GPT-family model through Codex, in an isolated CODEX_HOME
python3 run_eval.py --channel codex --arms control,rules,skill,patched

# ChatGPT through the user's own browser session, one conversation per probe
python3 run_eval.py --channel cloakgpt:auto --arms control,skill --probes P1,P3,P7

# a channel driven by hand (an agent, a person, a model with no CLI)
python3 run_eval.py --channel dry --arms control,skill --out results/run-x
#   ... write each answer into results/run-x/pending/<arm>/<probe>.txt ...
python3 run_eval.py --ingest --out results/run-x --label claude

# re-score saved answers after a rule or parser change — no model calls
python3 run_eval.py --rescore results/run-x
python3 run_eval.py --score results/final
```

Results land in `results/<stamp>-<label>/<label>/<arm>/<probe>.{txt,json}`;
`--score` writes `report.md` beside them. `results/final/` is the merged
view used for the 2026-09-30 run.

## Adding a channel

Add a branch to `call()` returning the model's raw answer; keep everything a
channel prints about itself out of the answer, and keep the arm's config
isolated (`CODEX_HOME`, `CLAUDE_CONFIG_DIR`, a fresh conversation) so a
treatment cannot leak into a control.

## Reading a result honestly

- A probe fails on a missing required string, a forbidden pattern, or a linter
  error — not on style taste.
- Within a channel, `control → skill` is the effect of the skill. `rules →
  skill` is the effect of the skill over the doctrine this machine already
  had, which is usually the more interesting comparison.
- `patched` measures the fix at the layer that actually produced the text: the
  app's own prompt.
- A single run is a sample. Nine probes per arm detects a large effect, not a
  subtle one; re-run before drawing a fine-grained conclusion.
