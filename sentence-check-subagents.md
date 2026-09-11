# Sentence checks via Task subagents

**For agents:** Start with [SKILL.md](SKILL.md) § Agent read order. **Read with the Read tool** before splitting the snapshot or launching sentence Tasks.

Background checkers grade **changed sentences only** ([phase2-verify-subagents.md](phase2-verify-subagents.md)). There is no Phase 1 source-audit wave. Narrative + math are separate Tasks on the full snapshot. The synthesizer sets job-round `OVERALL` after the round.

Sentence-count thresholds: [gate.md](gate.md).

**Compliance:** Every sentence Task runs **Step 0 assignment compliance** before specialist work — see [compliance-monitoring.md](compliance-monitoring.md). Batched prompts (S1–S3 in one Task) when N ≤ 10 → `COMPLIANCE: FAIL`. Specialist work is **artifact-first** ([sentence.md](../physics-paper-principles/sentence.md) Detect names); do not walk 1–14 as the primary loop.

---

## 1. When this file applies

| Context | Use this file? |
|---------|----------------|
| Producer drafting | No — producer uses [sentence.md](../physics-paper-principles/sentence.md) as **principles** |
| Background verify | Yes — **changed labels only** |
| ASK USER → proceed anyway | Yes — splittable sentences; note partial coverage |

Model choice: inherit or defaults ([gate.md](gate.md) · [phase2-verify-subagents.md](phase2-verify-subagents.md)). `section-brief.md` / `manifest.json` alone are not enough without `session.md` `user_confirmed: true`.

---

## 2. Split into numbered sentences

1. Strip `[square-bracket user comments]` from the working copy; keep as editing instructions.
2. Split mechanically at terminal `.`, `?`, or `!` followed by whitespace or
   end of text. Do not split at a decimal, abbreviation, initials, ellipsis, or
   inside `\(...\)`, `$...$`, `\begin{equation}...\end{equation}`,
   `\cite{...}`, `\ref{...}`, braces, or brackets.
3. Label **S1, S2, …** for assignment.

If a boundary is genuinely ambiguous, keep the span together, record the
decision once in the Task plan, and use the same labels every wave.

After labeling, identify changed labels per [phase2-verify-subagents.md](phase2-verify-subagents.md) § Changed sentences. Only changed labels get Tasks.

---

## 3. Task assignment

**Default:** one Task per changed sentence — each subagent runs the artifact-first workflow, then reports unresolved items against all 14 sentence principles.

1. Launch **one Task per assigned sentence** (or per §3.1 batch).
2. Launch Tasks **in parallel** with `run_in_background: true`. Do not wait before ending the turn.
3. **M** in the Mode line = number of sentence Tasks launched (must equal C).

**Anti-patterns:** See [compliance-monitoring.md](compliance-monitoring.md). Launching one Task for multiple labels when N ≤ 10 is a **compliance violation**.

### 3.1 Batching (11–12 sentences, or user chose proceed on longer quote)

When the assigned set has **>10** sentences (typically 11–12 under the ≤12 gate limit), you may assign **2+ sentences per Task**. If user chose **Proceed with subagents anyway** on a longer quote, scale batch size accordingly. Note batching in the Mode line (e.g. `· 6 Tasks (2 sentences each)`). **Never** batch when ≤10 sentences unless user explicitly requests it.

---

## 4. Model choice

Inherit the sentence-checker slug or use the recommended fast-tier default
([phase2-verify-subagents.md](phase2-verify-subagents.md)). Do not ask a
separate model question.

Use a fast-tier model for this high-volume, wording-only role.

Build options from the **current session Task allowed model list**. Prefer a **fast Composer** model when available; otherwise offer one flagship per provider with the **exact slug in each label**:

| Provider | Pick |
|----------|------|
| Cursor | Fast Composer model if in the allowed list; else highest-tier Composer |
| OpenAI | Highest-tier GPT model in the allowed list |
| Anthropic | Highest-tier Claude model in the allowed list |

Use the chosen slug on **every** sentence Task. If unavailable, pick the closest fast-tier slug in the session list and mention once.

---

## 5. Passage summary

**Before any Task**, write one **passage summary** for the full S1…Sn scope (keep it for prompts; do not put the itinerary in the user narrative):

- Passage role and logical flow.
- Placement (section, `.tex` path, neighbors).
- Physics and math at graduate level.

Paste the **identical** block into every subagent prompt under `## Passage summary (shared)`.

```text
Task(
  subagent_type: "generalPurpose",
  readonly: true,
  model: <sentence-checker slug — fast tier from §4>,
  run_in_background: true,
  description: "background sentence: S<k>",
  prompt: <template §6>
)
```

**Task description must include the label** (`background sentence: S2`) — not `sentence verify c11` or `all sentences`.

---

## 6. Subagent prompt template

```text
You are a sentence-level wording editor for a physics paper. You are not the
physics, mathematics, scope, theorem, or evidence adjudicator.

## Orchestrator task plan (verify in Step 0 — read-only)
<paste identical block from producer — compliance-monitoring.md § Task plan block>

## Passage summary (shared)
<identical block in every Task — from §5>

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
`phase1_sentence_tasks` must be `0`. Also append findings to `findings_path`
as you go (job-state.md).

If the prompt lists multiple sentences, a range (S1–S3), or "all sentences", or your label is missing from the task plan:

### Assignment compliance
COMPLIANCE: FAIL
Role: sentence
Label: S<k>
Reason: <one line — e.g. batched assignment; expected one label per Task>

(Do not run specialist checks below.)

Otherwise emit COMPLIANCE: PASS and continue.

## Your assignment
Check ONLY **one** sentence — label S<k>:

### Sentence <label>
<exact LaTeX/text>

User inline comments: <[bracket comments] or "none">

## Incremental ledger
Append each finding (and a `done` line for S<k>) to `findings_path` from the
Task plan as JSON lines the moment you have them (job-state.md). Do not edit
the .tex. On interrupt: flush then stop.

## Role boundary and sentence-level rules
Read ../physics-paper-principles/sentence.md (Detect column) and
physics-paper-editing/severity.md § Sentence workers (Read tool if needed).
Do **not** walk principles 1–14 as the primary loop. Run the workflow below.

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
4. Then fill **Checks — unresolved only** (existing 1–14 list).

### Artifacts → principles
**Kernel** (drop modifiers; one SVO per clause; head must survive)
  Then: 4 SVO, 6 wording, 9 voice, 10 "For A, it", 3 coined heads
**Antecedent map** (substitution; distant labels get a content reminder + number)
  Then: 1 local refs, 2 cross-boundary
**Topic / stress** (old at start, new at end; first-read pause)
  Then: 5 streamline, 9 voice, 13 ordering
**Clause-claim list** (one claim per clause or DELETE)
  Then: 12 math-for-math, 14 clause-must-claim
**Speech-act** (setup | hypothesis | proof-strategy | N/A)
  Then: 7 declare setup
**Membership without recipe** (or ESCALATE_TO math)
  Then: 11 physics story / physical lead
**Principle 8** after the rest: change only what the artifacts forced

Empty Diagnostics field → stop specialist work; incomplete homework (synthesizer
marks this label open / OVERALL PARTIAL). Fast polish does not skip Diagnostics.

## Apply corrections yourself (do not report these)

**Fix silently (obvious):** Unambiguous pronoun, SVO mismatch, "For A, it does
B" → "A does B", and obvious non-standard wording → standard wording, provided
the edit does not add a scientific claim.

**Fix silently (minor):** Typos, punctuation, trivial grammar, polish that does not change meaning.

**Do not silent-fix:** tautological or type-gloss clauses (principle 14). Deleting a clause whose claim is already in an adjacent clause is allowed as a silent minor fix. Supplying the missing contrast or consequence is passage-level judgment — report it as `SUGGEST` with a proposed `Edited:` line; do not invent a scientific point. Missing physical lead on a newly named object (principle 11 / physical-lead.md): do not invent the criterion; `ESCALATE_TO: math` (or narrative if no math Task) and `Needs user / main-agent judgment`.

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
- Kernel: <one SVO per clause; no modifiers>
- Antecedent map: <pronoun → noun, or none>
- Topic / stress: <old → new; pause + tier or none>
- Clause-claim list: <one claim per clause, or DELETE>
- Speech-act: setup | hypothesis | proof-strategy | N/A
- Membership without recipe: <one clause> | N/A | ESCALATE

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

**Needs user / main-agent judgment:** <items or "none">
**Severity:** BLOCKER | SUGGEST | none
**Escalate to:** narrative | math | none
---
```

---

## 7. After sentence Tasks complete (or on interrupt)

1. Harvest `findings.jsonl` ([job-state.md](job-state.md)). Keep stale lines.
2. Pass harvest + any final reports to the **round synthesizer** with changed/skipped label lists.
3. Producer does **not** run narrative/math inline or grade OVERALL. Apply [merge-policy.md](merge-policy.md).

On timeout or incomplete report: treat that label as `open`; do not grade inline.
