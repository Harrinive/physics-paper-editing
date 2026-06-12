# Sentence checks via Task subagents

**Read with the Read tool** before splitting the passage or launching sentence Tasks.

| Phase | Sentence scope | Narrative + math |
|-------|----------------|------------------|
| **Phase 1** | All sentences ([gate.md](gate.md) → SUBAGENTS) | Main agent after sentence merge ([verification-loop.md](verification-loop.md)) |
| **Phase 2** | **Changed sentences only** ([phase2-verify-subagents.md](phase2-verify-subagents.md)) | Verifier Tasks on full passage; synthesizer decides OVERALL |

Sentence-count thresholds (Phase 1 gates): [SKILL.md](SKILL.md) § Roles and terms.

---

## 1. When this file applies

| Context | Use this file? |
|---------|----------------|
| INLINE | No — run [sentence-checks.md](sentence-checks.md) inline |
| Phase 1 SUBAGENTS | Yes — all sentences |
| Phase 2 output verify | Yes — **changed labels only** |
| ASK USER → proceed anyway | Yes — splittable sentences; note partial coverage |
| ASK USER → skip | No — inline instead |

Do not re-AskQuestion for *Sentence-level checking* when Q3 was already feasible. Run the sentence-checker AskQuestion (§4) before Phase 1 Tasks unless user already chose a model for **this same quote/draft scope in this chat**, or a macro **section brief** supplied `verifier_profile.sentence` (use that slug — do not re-ask).

---

## 2. Split into numbered sentences

1. Strip `[square-bracket user comments]` from the working copy; keep as editing instructions.
2. Split on sentence boundaries; **do not break** inside `\(...\)`, `$...$`, `\begin{equation}...\end{equation}`, `\cite{...}`, `\ref{...}`, etc.
3. Label **S1, S2, …** for assignment.

If ambiguous, note in the prompt and include the preceding sentence as context.

**Phase 2:** after labeling, identify changed labels per [phase2-verify-subagents.md](phase2-verify-subagents.md) § Changed sentences. Only changed labels get Tasks.

---

## 3. Task assignment

**Default:** one Task per sentence — each subagent audits one sentence against all 13 checks.

| Phase | Which sentences get Tasks |
|-------|---------------------------|
| Phase 1 | All labels S1…Sn |
| Phase 2 | Changed labels only |

1. Launch **one Task per assigned sentence** (or per §3.1 batch).
2. Launch Tasks **in parallel** when practical; `run_in_background: false` — wait before next step.
3. **M** in the Mode line = number of sentence Tasks launched.

### 3.1 Batching (11–12 sentences, or user chose proceed on longer quote)

When the assigned set has **>10** sentences (typically 11–12 under the ≤12 gate limit), you may assign **2+ sentences per Task**. If user chose **Proceed with subagents anyway** on a longer quote, scale batch size accordingly. Note batching in the Mode line (e.g. `· 6 Tasks (2 sentences each)`). **Never** batch when ≤10 sentences unless user explicitly requests it.

---

## 4. AskQuestion — sentence checker model (fast tier)

**After** §2–§3 planning and **before** passage summary or Tasks, call **AskQuestion** unless the user already chose a sentence-checker model for **this same quote/draft scope in this chat**, or macro `session.md` has `user_confirmed: true` with a Phase 1 sentence slug.

**Hard stop:** do not launch sentence `Task`s until `AskQuestion` returns. Skill recommendations (e.g. fast Composer) are **(Recommended)** options in the form — not silent defaults. Phase 2 uses the three-question *Verifier model profile* instead ([phase2-verify-subagents.md](phase2-verify-subagents.md) § Model selection gate).

| Phase | Title |
|-------|-------|
| Phase 1 SUBAGENTS | *Sentence checker model* |
| Phase 2 | Part of *Verifier model profile* — see [phase2-verify-subagents.md](phase2-verify-subagents.md) § AskQuestion (question 1 only) |

**Phase 1 SUBAGENTS:** ask for the **sentence checker** model only (fast tier — high volume, mechanical 13-objective pass).

Build options from the **current session Task allowed model list**. Prefer a **fast Composer** model when available; otherwise offer one flagship per provider with the **exact slug in each label**:

| Provider | Pick |
|----------|------|
| Cursor | Fast Composer model if in the allowed list; else highest-tier Composer |
| OpenAI | Highest-tier GPT model in the allowed list |
| Anthropic | Highest-tier Claude model in the allowed list |

Use the chosen slug on **every** sentence Task. If unavailable, re-AskQuestion with valid options.

**Phase 2:** do not run a separate sentence-model AskQuestion — use question 1 of the three-question *Verifier model profile* form in [phase2-verify-subagents.md](phase2-verify-subagents.md) § AskQuestion.

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
  description: "Sentence check: S<k>" | "Phase2 sentence verify: S<k>",
  prompt: <template §6>
)
```

---

## 6. Subagent prompt template

```text
You are a sentence-level scientific editor for a physics paper.

## Passage summary (shared)
<identical block in every Task — from §5>

## Local context (read-only)
- Paper topic: <if not clear from summary>
- Section / file: <title and .tex path>
- Adjacent excerpt (1–3 sentences before/after if helpful): <or omit>

## Your assignment
Check ONLY the sentence(s) listed below—default: one sentence (§3); if §3.1 batched, list each label separately.

### Sentence <label>
<exact LaTeX/text>

(repeat only when §3.1 batched multiple sentences into one Task)

User inline comments: <[bracket comments] or "none">

## Sentence-level check rules
Read and apply every objective in order from sentence-checks.md (Read tool if needed).
Run all 13 checks per assigned sentence. Do not skip.

## Apply corrections yourself (do not report these)

**Fix silently (obvious):** Unambiguous pronoun, SVO mismatch, "For A, it does B" → "A does B", obvious non-standard term → standard equivalent, clear "if X then" → "because X," when X is stated as fact, clear passive/tentative setup → active scope declaration when the sentence fixes the model.

**Fix silently (minor):** Typos, punctuation, trivial grammar, polish that does not change meaning.

Respect objective 8 (minimal changes).

## Report only what you did not fix

Report when wording needs passage-level judgment: ambiguous "it/this/which", intentional terminology, physics-story vs setup-declaration tradeoff (obj. 7), prose-vs-math relocation (obj. 12), confusion-on-first-read ordering depending on neighbors (obj. 13), or risk of changing technical meaning.

## Output format
One block per assigned sentence:

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
