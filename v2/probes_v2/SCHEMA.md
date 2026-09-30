# Held-out probe set v2 — schema

Purpose: a probe set whose text, required facts and grading were not written by
the model that wrote the `ui-microcopy` skill, so a result on it can
disconfirm the skill. Half the probes are authored by Claude (this session),
half by GPT-6 through Codex in an isolated home; neither author is shown the
skill, the v1 fixtures, or any string from them. A contamination check greps
every quoted string in the skill and v1 fixtures against the probe text.

One probe:

```json
{
  "id": "C01",
  "author": "claude | gpt",
  "scenario": "finance | ecommerce | installer | settings | notifications | onboarding | forms | a11y | ai-summary | health",
  "lang": "zh-TW | en | ja",
  "kind": "strings | runtime",
  "task": "natural-language brief the model receives; ends with the exact JSON shape to return",
  "items": [
    {"key": "s1", "role": "button", "must_convey": ["the action cancels the transfer"]}
  ]
}
```

- `role` ∈ button, dialog-title, dialog-body, status, error, empty, label,
  value, note, title. Roles are element types, not writing rules.
- `must_convey` lists the facts a reader must still get from the string. The
  judge checks these are present; it is the only "required content" mechanism
  — no regexes authored by anyone who wrote a rule.
- `kind: runtime` probes are answered as an in-app model would answer them
  (JSON with a free-text field the UI renders).
- Task text must not quote example strings of the register under test, so the
  task itself cannot prime the answer either way.

Grading (see `judge_rubric.md`): an LLM judge from a family that did not write
the skill scores each string on two axes — required facts present (0/1) and
surplus/register (0/1) — with the role named and a role-specific definition of
surplus; pairwise comparisons swap position. A human (the user) blind-rates a
stratified sample to calibrate the judge.
