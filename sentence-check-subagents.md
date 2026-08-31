# Sentence checks via Task subagents

**For agents:** Start with [SKILL.md](SKILL.md) § Agent read order. **Read with the Read tool** before splitting the passage or launching sentence Tasks.

| Phase | Sentence scope | Narrative + math |
|-------|----------------|------------------|
| **Phase 1 full pace** | All sentences ([gate.md](gate.md) → SUBAGENTS) | Main agent after sentence merge ([verification-loop.md](verification-loop.md)) |
| **Phase 1 fast pace** | No Tasks; producer checks all sentences INLINE | Main agent |
| **Phase 2** | **Changed sentences only** ([phase2-verify-subagents.md](phase2-verify-subagents.md)) | Verifier Tasks on full passage; synthesizer decides OVERALL |

Sentence-count thresholds (Phase 1 gates): [gate.md](gate.md) § Sentence-count thresholds.

**Compliance:** Every sentence Task runs **Step 0 assignment compliance** before the 13 objectives — see [compliance-monitoring.md](compliance-monitoring.md). Batched prompts (S1–S3 in one Task) → `COMPLIANCE: FAIL`.

---

## 1. When this file applies

| Context | Use this file? |
|---------|----------------|
| INLINE | No — run [sentence-checks.md](sentence-checks.md) inline |
| Phase 1 SUBAGENTS | Yes — all sentences |
| Phase 2 output verify | Yes — **changed labels only** |
| ASK USER → proceed anyway | Yes — splittable sentences; note partial coverage |
| ASK USER → skip | No — inline instead |

Model choice comes from the single editing intake (§4). A confirmed section
`session.md` may supply it; `section-brief.md` or `manifest.json` alone may not.

---

## 2. Split into numbered sentences

1. Strip `[square-bracket user comments]` from the working copy; keep as editing instructions.
2. Split mechanically at terminal `.`, `?`, or `!` followed by whitespace or
   end of text. Do not split at a decimal, abbreviation, initials, ellipsis, or
   inside `\(...\)`, `$...$`, `\begin{equation}...\end{equation}`,
   `\cite{...}`, `\ref{...}`, braces, or brackets.
3. Label **S1, S2, …** for assignment.

If a boundary is genuinely ambiguous, keep the span together, record the
decision once in the Task plan, and use the same labels in every phase.

**Phase 2:** after labeling, identify changed labels per [phase2-verify-subagents.md](phase2-verify-subagents.md) § Changed sentences. Only changed labels get Tasks.

---

## 3. Task assignment

**Default:** one Task per sentence — each subagent audits one sentence against all 13 checks.

| Phase | Which sentences get Tasks |
|-------|---------------------------|
| Phase 1 full pace | All labels S1…Sn |
| Phase 1 fast pace | No Tasks (`phase1_sentence_tasks: INLINE`) |
| Phase 2 | Changed labels only |

1. Launch **one Task per assigned sentence** (or per §3.1 batch).
2. Launch Tasks **in parallel** when practical; `run_in_background: false` — wait before next step.
3. **M** in the Mode line = number of sentence Tasks launched (must equal N in
   Phase 1 full-pace polish, or C in Phase 2).

**Anti-patterns:** See [compliance-monitoring.md](compliance-monitoring.md) § Anti-patterns. Launching one Task for multiple labels when N ≤ 10 is a **compliance violation** — workers will FAIL and synthesizer will block ship.

### 3.1 Batching (11–12 sentences, or user chose proceed on longer quote)

When the assigned set has **>10** sentences (typically 11–12 under the ≤12 gate limit), you may assign **2+ sentences per Task**. If user chose **Proceed with subagents anyway** on a longer quote, scale batch size accordingly. Note batching in the Mode line (e.g. `· 6 Tasks (2 sentences each)`). **Never** batch when ≤10 sentences unless user explicitly requests it.

---

## 4. Model choice

Resolve the sentence-checker model in the single editing intake defined by
[gate.md](gate.md). Do not ask separately before Phase 1 or Phase 2. Reuse a
choice for this scope, or inherit a section profile only when `session.md` has
`user_confirmed: true`.

**Hard stop:** do not launch sentence Tasks until the single intake returns.

| Phase | Title |
|-------|-------|
| Phase 1 full pace | Intake sentence-checker choice |
| Phase 2 | Same intake profile, question 1 |

Use a fast-tier model for this high-volume, wording-only role.

Build options from the **current session Task allowed model list**. Prefer a **fast Composer** model when available; otherwise offer one flagship per provider with the **exact slug in each label**:

| Provider | Pick |
|----------|------|
| Cursor | Fast Composer model if in the allowed list; else highest-tier Composer |
| OpenAI | Highest-tier GPT model in the allowed list |
| Anthropic | Highest-tier Claude model in the allowed list |

Use the chosen slug on **every** sentence Task. If unavailable, re-AskQuestion with valid options.

Both phases reuse the same slug.

---

## 5. Passage summary

**Before any Task**, write one **passage summary** for the full S1…Sn scope ([SKILL.md](SKILL.md) § Response — passage summary):

- Passage role and logical flow.
- Placement (section, `.tex` path, neighbors).
- Physics and math at graduate level.

Paste the **identical** block into every subagent prompt under `## Passage summary (shared)`.

```text
Task(
  subagent_type: "generalPurpose",
  readonly: true,
  model: <sentence-checker slug — fast tier from §4 or Phase 2 profile Q1>,
  description: "Phase1 sentence: S<k>" | "Phase2 sentence verify: S<k>",
  prompt: <template §6>
)
```

**Task description must include the label** (`Phase1 sentence: S2`) — not `sentence verify c11` or `all sentences`.

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

Expected: exactly ONE target label S<k>. Phase 1 sentence Tasks are legal only
for `pace: full`, and the label must appear in `phase1_sentence_tasks`. Phase 2:
the label must appear in `phase2_changed_labels`.

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

## Role boundary and sentence-level rules
Read and apply every objective in order from sentence-checks.md (Read tool if needed).
Run all 13 checks per assigned sentence. Do not skip.

Use neighboring sentences only to judge flow and references. Do not edit them.
Do not introduce a discourse connective (`however`, `conversely`, `therefore`,
`thus`, `even though`, and similar) unless that logical relation is explicit in
the source or immediate context. If uncertain, use no connective. Do not invent
a mechanism, assumption, operator declaration, equivalence claim, or other
scientific content.

## Apply corrections yourself (do not report these)

**Fix silently (obvious):** Unambiguous pronoun, SVO mismatch, "For A, it does
B" → "A does B", and obvious non-standard wording → standard wording, provided
the edit does not add a scientific claim.

**Fix silently (minor):** Typos, punctuation, trivial grammar, polish that does not change meaning.

Respect objective 8 (minimal changes).

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

**Needs user / main-agent judgment:** <items or "none">
**Severity:** BLOCKER | SUGGEST | none
**Escalate to:** narrative | math | none
---
```

---

## 7. After sentence Tasks complete

### Phase 1

1. **Assemble** from each **Edited** line (S1, S2, …). Resolve boundary conflicts minimally.
2. **Collect** unresolved **Checks** and **Needs user / main-agent judgment** → focused questions.
3. **Run** [narrative-checks.md](narrative-checks.md) and [math-checks.md](math-checks.md) on the full passage (main agent).
4. Summarize sentence-level from subagent reports; do not re-run all 13 inline unless a subagent failed.
5. → step 5 (produce draft).

### Phase 2

1. Pass changed-sentence outputs to the **verifier synthesizer** with changed/skipped label lists.
2. Producer does **not** run narrative/math inline or grade OVERALL.

On timeout or incomplete report: relaunch the Task; producer must not grade inline.
