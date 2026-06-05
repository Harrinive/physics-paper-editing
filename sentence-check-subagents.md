# Sentence-level checks via Task subagents

**SUBAGENTS mode only.** Obey [SKILL.md](SKILL.md) § Gate first: 2+ sentences, **not** a major rewrite (Q2), and a **feasible** split (Q3) → use this file; Q3 not feasible → AskQuestion in the gate, then return here only if the user chose **Proceed with subagents anyway**.

**Main agent keeps:** narrative ([narrative-checks.md](narrative-checks.md)) and math ([math-checks.md](math-checks.md)) after synthesis.

**Read this file with the Read tool** before splitting the passage or launching Tasks.

---

## 1. When this file applies

| Gate mode | Use this file? |
|-----------|----------------|
| **INLINE** | No — run [sentence-checks.md](sentence-checks.md) inline |
| **SUBAGENTS** | Yes — required |
| **ASK USER** → user chose proceed anyway | Yes — coarser split; note partial coverage |
| **ASK USER** → user chose skip | No — inline sentence checks instead |

Do not AskQuestion when the gate already selected **SUBAGENTS**.

---

## 2. Split into numbered sentences

1. Strip `[square-bracket user comments]` from the working copy; keep as editing instructions.
2. Split on sentence boundaries; **do not break** inside `\(...\)`, `$...$`, `\begin{equation}...\end{equation}`, `\cite{...}`, `\ref{...}`, etc.
3. Label **S1, S2, …** for assignment.

If ambiguous, note in the prompt and include the preceding sentence as context.

---

## 3. Batch sentences across subagents

Choose the split (no fixed chunk size):

- **One sentence per Task** when long, dense, or math-heavy.
- **2–4 short related sentences** when one logical beat (e.g. consecutive proof steps).
- **Do not** assign a whole paragraph unless it is one sentence.

Keep list items or proof steps together when splitting would lose referents (“the second term”, “type~2”).

Launch Tasks **in parallel** when practical; batch waves if many. **`run_in_background: false`** — wait before synthesizing.

---

## 4. Passage summary, then launch Tasks

**Before any Task**, write one **passage summary** for the full S1…Sn scope (same bullets as SKILL.md § Response — passage summary):

- Passage role and logical flow.
- Placement (section, `.tex` path, neighbors).
- Physics and math at graduate level.

Paste the **identical** block into every subagent prompt under `## Passage summary (shared)`.

```text
Task(
  subagent_type: "generalPurpose",
  readonly: true,
  model: <highest-capability model in Task tool allowed list this session>,
  description: "Sentence check: <brief scope>",
  prompt: <template §5>
)
```

Set `model` from the **current** Task allowed list each session. **Do not** hardcode model names in skill files or prompts.

---

## 5. Subagent prompt template

Replace placeholders. Reuse the same `## Passage summary (shared)` in every Task.

```text
You are a sentence-level scientific editor for a physics paper.

## Passage summary (shared)
<identical block in every Task — from §4>

## Local context (read-only)
- Paper topic: <if not clear from summary>
- Section / file: <title and .tex path>
- Adjacent excerpt (1–3 sentences before/after if helpful): <or omit>

## Your assignment
Check ONLY the following sentence(s). Use the given labels.

### Sentence <label>
<exact LaTeX/text>

User inline comments: <[bracket comments] or "none">

## Sentence-level check rules
Read and apply every objective in order from:
sentence-checks.md
(same directory as this skill — use the Read tool if you do not have the file)

Run all 11 checks per assigned sentence. Do not skip.

## Apply corrections yourself (do not report these)

**Fix silently (obvious):** Clear from the sentence alone — unambiguous pronoun, SVO mismatch, mandatory “For A, it does B” → “A does B”, obvious non-standard term → standard equivalent, clear “if X then” → “because X,” when X is stated as fact in that sentence.

**Fix silently (minor):** Typos, punctuation, trivial grammar, polish that does not change meaning.

Respect objective 8 (minimal changes).

## Report only what you did not fix

Report when wording needs passage-level judgment: ambiguous “it/this/which”, intentional terminology, physics-story vs rigor tradeoff, or risk of changing technical meaning.

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
7. Rigor vs narrative:
8. Minimal changes:
9. Active voice:
10. "For A, it does B":
11. Physics story:

**Needs user / main-agent judgment:** <items or "none">
---
```

---

## 6. Synthesize subagent reports

1. **Assemble** from each **Edited** line (S1, S2, …). Resolve boundary conflicts minimally; note conflicts.
2. **Collect** only unresolved **Checks** and **Needs user / main-agent judgment** → focused questions (SKILL.md § Response — Clarify).
3. **Run** [narrative-checks.md](narrative-checks.md) and [math-checks.md](math-checks.md) on the full draft when loaded.
4. In the response, **summarize sentence-level** from subagent reports; do not re-run all 11 inline unless a subagent failed or you override.
5. Finish SKILL.md workflow (respond → self-check → apply in Agent mode).

On timeout or incomplete report: run sentence checks manually for that chunk and note the gap.
