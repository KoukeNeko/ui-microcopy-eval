You are grading user-interface strings that a writer produced from a brief. You will see several records. For each record you get: the brief the writer received, the element type of each string, the facts each string must convey, and the strings the writer returned. You do not know who or what wrote them. Grade each string on two independent axes.

Axis A — facts_present (0 or 1): every listed fact is recoverable from the string. Paraphrase is fine; a missing or contradicted fact is 0. If the fact list is empty, facts_present is 1 when the string is empty or says nothing beyond the brief, and 0 when it introduces a claim the brief does not support.

Axis B — surplus (0 or 1): 1 if the string contains ANY of the following; 0 otherwise.
  1. A clause that does not change what a reader understands about the current state, the consequence, or what they can do next.
  2. Wording that reads as a reply between two people rather than as an element of the interface: a spoken-register answer used as a control label (the equivalent of "never mind", "okay then", "all done" in place of the conventional action or state name), an apology, a reassurance, praise, cheering, an exclamation mark or emoji in a routine, error or destructive state.
  3. A statement about how the writer or system produced the content, defended it, or hedged it, that the brief did not ask for (source disclaimers, "this is only an estimate", "please double-check", "this is not a guess", descriptions of the method used).
  4. An observation about what was NOT seen or NOT included, or about the container, apparatus, or setting rather than the content itself.
  5. A question where the element type is a button, title, or label.
  6. For a `note` element: any content when the fact list is empty (the correct note is empty), or content beyond the listed facts.

Element-type expectations (these describe the element; they are not the writer's instructions):
- button: names the action the control performs.
- dialog-title: names the decision or the act.
- dialog-body: the consequence or facts the reader needs to decide; onboarding bodies may carry a warmer tone, but every sentence must still map to a listed fact.
- status: the current or completed state.
- error: what happened, the cause if given, the next step if given.
- empty: the state (nothing here yet); the call to action lives on a button that the brief says already exists.
- label: a noun phrase naming the thing (for screen-reader labels: what the control does).
- value: the figure with its unit; a range, when given, stays with the figure.
- note: one fact that changes how the adjacent figure or list is read; empty when there is none.
- title: the name of the screen or step.

Also report, per string:
- surplus_quote: the exact substring that triggered surplus, or "" if none.
- register: one of "interface", "conversational", "mixed" — your judgement of the overall register.
- lang_ok (0/1): the string is in the brief's language and, for zh-TW, uses Taiwan vocabulary (e.g. 設定 not 設置, 資料 not 數據, 影片 not 視頻, 目前 not 當前); for ja, natural Japanese UI wording; for en, natural English.

Do not reward length. Do not reward friendliness. Do not penalise a short string for being short. A string that carries every fact with nothing else is the best possible answer.

Return ONLY a JSON array, one object per record, in the order given:
[{"record":"<record id>","items":{"<key>":{"facts_present":0|1,"missing":["..."],"surplus":0|1,"surplus_quote":"...","register":"interface|conversational|mixed","lang_ok":0|1}}}]
