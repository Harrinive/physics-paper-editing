# Sentence checks via verifier subagents

**For agents:** Start with [SKILL.md](SKILL.md) § Agent read order. **Read with the Read tool** before splitting the snapshot or scheduling sentence verifiers.

Verifiers grade **changed sentences only** ([phase2-verify-subagents.md](phase2-verify-subagents.md)). There is no Phase 1 source-audit wave. Narrative + math are separate verifier assignments on the full snapshot. The synthesizer sets job-round `OVERALL` after the round.

Sentence-count thresholds: [gate.md](gate.md).

**Compliance:** Every sentence verifier runs **Step 0 assignment compliance** before specialist work — see [compliance-monitoring.md](compliance-monitoring.md). Batched prompts (S1–S3 in one assignment) when N ≤ 10 → `COMPLIANCE: FAIL`. Specialist work is **artifact-first** ([sentence.md](../physics-paper-principles/sentence.md) Detect names); do not walk 1–15 as the primary loop.

---

## 1. When this file applies

| Context | Use this file? |
|---------|----------------|
| Producer drafting | No — producer uses [sentence.md](../physics-paper-principles/sentence.md) as **principles** |
| Background verify | Yes — **changed labels only** |
| ASK USER → proceed anyway | Yes — splittable sentences; note partial coverage |

Model choice: use the recorded profile ([gate.md](gate.md) · [phase2-verify-subagents.md](phase2-verify-subagents.md)). `section-brief.md` / `manifest.json` alone are not enough without the matching `session.md` profile; a no-interaction fallback remains valid with `user_confirmed: false`.

---

## 2. Split into numbered sentences

1. Strip `[square-bracket user comments]` from the working copy; keep as editing instructions.
2. Split mechanically at terminal `.`, `?`, or `!` followed by whitespace or
   end of text. Do not split at a decimal, abbreviation, initials, ellipsis, or
   inside `\(...\)`, `$...$`, `\begin{equation}...\end{equation}`,
   `\cite{...}`, `\ref{...}`, braces, or brackets.
3. Label **S1, S2, …** for assignment.

If a boundary is genuinely ambiguous, keep the span together, record the
decision once in the worker plan, and use the same labels every wave.

After labeling, identify changed labels per [phase2-verify-subagents.md](phase2-verify-subagents.md) § Changed sentences. Only changed labels get verifier assignments.

---

## 3. Verifier assignment

**Default:** one verifier assignment per changed sentence — each subagent runs the artifact-first workflow, then reports unresolved items against all 15 sentence principles.

1. Schedule **one verifier assignment per sentence** (or per §3.1 batch).
2. Use the runtime scheduler for parallel waves. Continue asynchronously when available; otherwise harvest foreground waves without withholding the draft.
3. **M** in the Mode line = number of sentence assignments launched (must equal C).

**Anti-patterns:** See [compliance-monitoring.md](compliance-monitoring.md). Assigning one verifier to multiple labels when N ≤ 10 is a **compliance violation**.

### 3.1 Batching (11–12 sentences, or user chose proceed on longer quote)

When the assigned set has **>10** sentences (typically 11–12 under the ≤12 gate limit), you may assign **2+ sentences per verifier**. If the user chose **Proceed with partial coverage** on a longer quote, scale batch size accordingly. Note batching in the Mode line. **Never** batch when ≤10 sentences unless the user explicitly requests it.

---

## 4. Model choice

Use the confirmed `sentence` role from [runtime-contract.md](runtime-contract.md); do not ask a second question. The adapter resolves this fast-tier role to an available model and records an explicit fallback or `unknown` identifier when necessary.

---

## 5. Passage summary

**Before any verifier assignment**, write one **passage summary** for the full S1…Sn scope (keep it for prompts; do not put the itinerary in the user narrative):

- Passage role and logical flow.
- Placement (section, `.tex` path, neighbors).
- Physics and math at graduate level.

Paste the **identical** block into every verifier prompt under `## Passage summary (shared)`.

```text
role: sentence
labels: [S<k>]
model_role: sentence
write_policy: result-shard-only
completion: asynchronous-when-supported
prompt: template §6
```

The assignment label must be explicit (`S2`), never an opaque identifier or `all sentences`.

---

## 6. Subagent prompt template

```text
You are a sentence-level wording editor for a physics paper. You are not the
physics, mathematics, scope, theorem, or evidence adjudicator.

## Worker plan (verify in Step 0 — read-only)
<paste identical block from producer — compliance-monitoring.md § Worker plan block>

## Passage summary (shared)
<identical block in every verifier prompt — from §5>

## Local context (read-only; never edit)
- Paper topic: <if not clear from summary>
- Section / file: <title and .tex path>
- Previous sentence: <exact text or NONE>
- Next sentence: <exact text or NONE>
- Referenced formal excerpt: <every labeled definition/lemma/theorem whose
  label or defined term is used and already established **earlier** in the
  manuscript; otherwise NONE. A sentence that only promises to define a term
  **later** (a roadmap/forward reference) does not trigger this — pulling in
  the not-yet-reached definition is manuscript-wide reconstruction, not local
  context. On fast polish, standalone micro, this stays NONE unless the term
  was already defined before the quote's location — see [fast-polish.md](fast-polish.md) § 3>

Always supply both immediate neighbors when they exist. Do not choose the
excerpt subjectively. Include a formal block only by the mechanical reference
rule above, never because the orchestrator expects a particular answer.

## Step 0 — Assignment compliance (run FIRST)

You monitor the orchestrator, not just the prose. Read `pace` from the plan.

Expected: exactly ONE target label S<k>, listed in `phase2_changed_labels`.
`phase1_sentence_tasks` must be `0`. Also append findings to `result_path`
as you go (job-state.md).

If the prompt lists multiple sentences, a range (S1–S3), or "all sentences", or your label is missing from the worker plan:

### Assignment compliance
COMPLIANCE: FAIL
Role: sentence
Label: S<k>
Reason: <one line — e.g. batched assignment; expected one label per verifier>

(Do not run specialist checks below.)

Otherwise emit COMPLIANCE: PASS and continue.

## Your assignment
Check ONLY **one** sentence — label S<k>:

### Sentence <label>
<exact LaTeX/text>

User inline comments: <[bracket comments] or "none">

## Incremental ledger
Append each finding and a terminal completion record for S<k> to `result_path` from the
worker plan as JSON lines the moment you have them (job-state.md). Do not edit
the .tex. On a supported stop request: flush then stop.

## Role boundary and sentence-level rules
Read ../physics-paper-principles/sentence.md (Detect column) and
physics-paper-editing/severity.md § Sentence workers (Read tool if needed).
Do **not** walk principles 1–15 as the primary loop. Run the workflow below.

Use neighboring sentences only to judge flow and references. Do not edit them.
Do not introduce a discourse connective (`however`, `conversely`, `therefore`,
`thus`, `even though`, and similar) unless that logical relation is explicit in
the source or immediate context. If uncertain, use no connective. Do not invent
a mechanism, assumption, operator declaration, equivalence claim, or other
scientific content.

## Workflow (run in this order; do not skip an artifact)

1. Produce artifacts (tests named in sentence.md Detect column). One line each.
2. Under each artifact, check only the listed principles.
3. Silent-fix only what those checks force. Cite the artifact that forced each
   silent fix. Principle 8 last.
4. Then fill **Checks — unresolved only** (existing 1–15 list).

### Artifacts → principles
**Kernel** (drop modifiers; one SVO per clause; head must survive; Coinage test; Standard-meaning substitution)
  Then: 4 SVO, 6 wording, 9 voice, 10 "For A, it", 3 coined heads, 15 standard meaning
**Antecedent map** (substitution; distant labels get a content reminder + number)
  Then: 1 local refs, 2 cross-boundary
**Topic / stress** (old at start, new at end; first-read pause)
  Then: 5 streamline, 9 voice, 13 ordering
**Clause-claim list** (one claim per clause or DELETE)
  Then: 12 math-for-math, 14 clause-must-claim
**Speech-act** (setup | hypothesis | proof-strategy | N/A)
  Then: 7 declare setup
**Physical meaning and definition choice** (role, category, operational option, chosen name/form; or N/A; scientific uncertainty → ESCALATE_TO math)
  Then: 11 physical meaning, category, and definition choice
**Principle 8** after the rest: change only what the artifacts forced

Empty Diagnostics field → stop specialist work; incomplete homework (synthesizer
marks this label open / OVERALL PARTIAL). Fast polish does not skip Diagnostics.

## Apply corrections yourself (do not report these)

**Fix silently (obvious):** Unambiguous pronoun, SVO mismatch, "For A, it does
B" → "A does B", and obvious non-standard wording → standard wording, provided
the edit does not add a scientific claim or shift a field-standard term
(principle 15).

**Fix silently (minor):** Typos, punctuation, trivial grammar, polish that does not change meaning.

**Do not silent-fix:** tautological or type-gloss clauses (principle 14). Deleting a clause whose claim is already in an adjacent clause is allowed as a silent minor fix. Supplying the missing contrast or consequence is passage-level judgment — report it as `SUGGEST` with a proposed `Edited:` line; do not invent a scientific point. Unclear physical role on a newly named object (principle 11 / physical-lead.md): suggest supported clarification; do not invent meaning. Shifted field-standard meaning (principle 15): do not silent-rename or silently broaden the term; report it. Escalate scientific uncertainty to math (or narrative if no math verifier); a non-operational definition alone is not a defect.

Respect principle 8 (minimal changes).

## Report only what you did not fix

Report when wording needs passage-level judgment. Classify grammar or reference
failure that makes the target unreadable or reverses/materially changes the
supplied meaning as `BLOCKER`. Classify every physics, mathematics, scope,
theorem, evidence, or scientific-correctness concern as `SUGGEST` and add
`ESCALATE_TO: narrative` or `ESCALATE_TO: math`; never state it as a confident
physics conclusion.

## Output format

### Assignment compliance
COMPLIANCE: PASS | FAIL
Role: sentence
Label: S<k>
Reason: <one line>

(Omit specialist section below if COMPLIANCE: FAIL.)

---
### Sentence <label>
**Edited:** <final LaTeX after silent fixes; if unchanged, repeat original>
**Silent fixes cited:** <artifact → what changed; or "none">

**Diagnostics** (required; empty field → incomplete homework):
- Kernel: <one SVO per clause; no modifiers; coined or shifted terms or none>
- Antecedent map: <pronoun → noun, or none>
- Topic / stress: <old → new; pause + tier or none>
- Clause-claim list: <one claim per clause, or DELETE>
- Speech-act: setup | hypothesis | proof-strategy | N/A
- Physical meaning and definition choice: <role; category; operational option; chosen name/form and reason> | N/A | ESCALATE

**Checks — unresolved only** (if all fixed: "All checks addressed in **Edited** (none to report)."):
1. Clarify local references:
2. Clarify cross-boundary references:
3. Define/replace terminology:
4. Subject–verb–object:
5. Streamline narrative:
6. Polish wording:
7. Declare setup; do not hypothesize:
8. Minimal changes:
9. Active voice:
10. "For A, it does B":
11. Physics story:
12. Use math for math:
13. Confusion-on-first-read ordering:
14. Every clause must carry a claim:
15. Preserve standard meaning:

**Needs user / main-agent judgment:** <items or "none">
**Severity:** BLOCKER | SUGGEST | none
**Escalate to:** narrative | math | none
---
```

---

## 7. After sentence verifiers complete (or after a stop request)

1. Harvest deterministic result shards ([job-state.md](job-state.md)). Keep stale lines.
2. Pass harvest + any final reports to the **round synthesizer** with changed/skipped label lists.
3. Producer does **not** run narrative/math inline or grade OVERALL. Apply [merge-policy.md](merge-policy.md).

On timeout or incomplete report: treat that label as `open`; do not grade inline.
