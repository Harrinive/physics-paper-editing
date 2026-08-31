# Fast polish scope (standalone micro only)

**For agents:** Start with [SKILL.md](SKILL.md) § Agent read order. **Read with the Read tool** before step 6 when `edit_gate: polish`, `pace: fast`, `caller: micro`.

**Applies only when all three hold:** `edit_gate: polish` **and** `pace: fast` **and** `caller: micro` (standalone quote — not a macro chunk). If any is false, this file does not apply — run [phase2-verify-subagents.md](phase2-verify-subagents.md), [narrative-checks.md](narrative-checks.md), and [math-checks.md](math-checks.md) exactly as written, full whole-passage-vs-manuscript audit, no exceptions.

Macro chunks always pass `caller: section-orchestrator` ([chunk-contract.md](../physics-paper-editing-section/chunk-contract.md)) — this file's exceptions **never** apply to chunks, regardless of pace.

This file changes **what Phase 2 asks and whether the math Task launches**. It does not change who may set `OVERALL` (synthesizer only), does not skip the synthesizer, and does not skip sentence Tasks for changed sentences.

---

## 1. Equation-detection test (run once; mechanical)

Run against the **quoted source** before the Task plan, and again against the **producer's draft** after step 5 — if the draft adds math the quote lacked, re-run and re-emit the Task plan.

**Launch the math Task** (skip nothing) if the quote **or** the draft contains any of:

- `$`, `$$`, `\(...\)`, `\[...\]`
- an `equation`, `align`, `gather`, `eqnarray`, `multline`, `split`, or `cases` environment, or `\ensuremath`
- a numbered `definition`, `lemma`, `theorem`, `proposition`, `corollary`, `claim`, or `condition`
- a cross-reference to math elsewhere (`\eqref`, `Eq.~\ref{...}`, `Lemma~\ref{...}` or equivalent prose pointer)
- a Unicode math operator (∀ ∃ ≤ ≥ ⟨ ⟩ ħ φ and similar)

**Skip the math Task** only when none of the above appear anywhere in the quote or the draft. Record the outcome in the Task plan field `phase2_math_task: launched | skipped (no equations)` ([compliance-monitoring.md](compliance-monitoring.md) § Task plan block).

Do **not** add "the passage contains a prose definition" as its own trigger — a defined term stated in words, with no math notation, does not launch math on this test. That case is covered by § 2 below, inside the narrative Task.

## 2. Delta scope (narrative Task always; math Task too, when it runs)

The question narrows from "is this passage correct against the whole paper" to: **did the producer's edit change what the sentence claims, relative to the user's own quoted source?**

- **In scope:** the edit invents a relation the source didn't state; reverses an implication; strengthens or weakens a hedge, quantifier, or scope word; or drops a stated limitation.
- **Out of scope for a BLOCKER:** a defect that was **already present, unedited, in the user's quoted source**. Report it as `SUGGEST — pre-existing in source (not introduced by this edit)`, name the sentence, and stop — do not chase it against later definitions, lemmas, or theorems elsewhere in the manuscript.

**Closed word-delta class** (BLOCKER-eligible on its own, no manuscript lookup required): the edit changes any of *only / all / any / uniform / iff / equivalent / necessary / sufficient / always* ↔ *may / can / does* (or the symmetric reverse) relative to the source wording for the same claim. This is in addition to — not a replacement for — the closed BLOCKER lists already in [narrative-checks.md](narrative-checks.md) and [math-checks.md](math-checks.md); those lists still apply to what the **edit** does.

Full pace and rewrite are unaffected by this section — they keep the standard whole-passage-vs-manuscript audit in narrative-checks.md and math-checks.md.

## 3. No manuscript search

Do not `Grep` or `Read` beyond: the supplied passage, the immediate neighbor sentences already in the prompt, and any formal excerpt already pasted in under "Referenced formal excerpt." That excerpt field is for terms **already defined earlier** in the manuscript than the quote — never for a term the quote itself only **promises to define later** (a roadmap sentence naming a concept its own section will formalize next is not a trigger; do not pull the later definition in to "check ahead"). If settling a claim would require more manuscript context than that, do not go hunting for it — report:

```
PACKET_GAP: <one line — what context would be needed and why>
```

`PACKET_GAP` is not a BLOCKER and not silently dropped — the synthesizer surfaces it in CHECKS (`packet_gap: <count>`) and the producer discloses it to the user in plain language: "This fast check compared your edit to your quoted source, not the rest of the paper."

## 4. Compliance mirror (math skip is not a violation)

On `pace: fast` + `polish` + `caller: micro`:

- `phase2_math_task: skipped (no equations)` is a **valid, compliant** plan when § 1's test finds no math in quote or draft. The math worker Step 0 in [compliance-monitoring.md](compliance-monitoring.md) does not apply — there is no math Task to grade.
- `COMPLIANCE: FAIL` only if the plan **disagrees** with the mechanical test: math launched with no equations present (compliance violation: unnecessary Task, but not a content defect), or math skipped while equations are present in quote or draft (this is the real violation — never ship on this).
- The synthesizer accepts `### Math report: skipped — no equations per Task plan` in place of a math verifier report; CHECKS records `math_step0: N/A (skipped)`. This is **not** a procedural FAIL.

## 5. Model recommendation (fast pace only)

At `pace: fast`, recommend a capable **medium-effort** flagship (not an "xhigh" / "thinking-high" reasoning variant, and not a coding-specialist slug) as the **first** option for the narrative/math (Q2) and synthesizer (Q3) roles in the single intake. Note on the form: "a high-reasoning-effort model adds several minutes at fast pace." The user may still pick a thinking-high model — this changes the recommended default only, never a silent substitution. At `pace: full` (or `rewrite`), keep the existing flagship / thinking-high recommendation unchanged.

---

## What does not change

- Sentence Tasks: still one Task per **changed** label, same 13 objectives, same fast-tier model, unaffected by this file.
- Synthesizer: still the sole `OVERALL` authority; still fresh Tasks every iteration; still fails on any unresolved BLOCKER.
- Narrative Task: still runs all four groups, full passage — this file only narrows classes 1–5 relative to the **edit**, and adds § 2's word-delta class; it does not remove any check.
- `caller: section-orchestrator` (macro chunks): none of this applies. Chunks always get the math Task when applicable and the full whole-passage audit, at either pace.
