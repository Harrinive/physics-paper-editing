# Sentence-level checks via Task subagents

Use when [sentence-checks.md](sentence-checks.md) is loaded and the passage has **two or more** complete sentences.

**Main agent keeps:** narrative ([narrative-checks.md](narrative-checks.md)) and math ([math-checks.md](math-checks.md)) after synthesis.

**Read this file before** splitting the passage or launching Tasks.

---

## 1. Subagents vs AskQuestion vs inline

| Situation | AskQuestion? | Sentence checks |
|-----------|--------------|-----------------|
| Single sentence or fragment | No | Inline [sentence-checks.md](sentence-checks.md) |
| ≥2 sentences, **feasible** scope (below) | No | **Task subagents** (required — do not skip) |
| ≥2 sentences, **impractical** scope (below) | **Yes** | Per user choice |
| User asked for no subagents / quick inline | No | Inline |
| User already chose skip vs proceed **this passage, this chat** | No | Honor prior choice |
| `sentence-checks.md` not loaded | No | Other checklists only |

### 1.1 Feasible — run subagents without asking

All must hold:

- Roughly **≤12** complete sentences.
- Each chunk is short enough for rigorous per-objective checking.
- Mostly checkable prose (not display equations, tables, or bare lists).
- Sentences can be split without losing essential cross-references.

→ Split (§2), launch Tasks (§4–5), synthesize (§6). **Do not AskQuestion** for routine edits in this range.

### 1.2 Impractical — AskQuestion required

Examples: full paper or section, **~15+** sentences, mostly equations/tables, inseparable cross-references, or an unwieldy number of Tasks.

**AskQuestion** title *Sentence-level checking*, options:

| Option | Effect |
|--------|--------|
| **Skip sentence-level subagents** | Main agent runs narrative/math; fixes obvious sentence issues inline |
| **Proceed with subagents anyway** | Coarser split (§3); note partial coverage in synthesis |
| **Narrow the scope** | User gives a shorter passage; if still ≥2 feasible sentences, run subagents |

Briefly say why (e.g. “~40 sentences”). If user skips, do **not** launch Tasks; run sentence checks inline, then narrative/math.

### 1.3 Tie-break

Modest count → feasible (subagents). Large count or non-sentential prose → AskQuestion.

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

**Before any Task**, write one **passage summary** for the full S1…Sn scope (same bullets as SKILL.md Response §1):

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

Run all 10 checks per assigned sentence. Do not skip.

## Apply corrections yourself (do not report these)

**Fix silently (obvious):** Clear from the sentence alone — unambiguous pronoun, SVO mismatch, mandatory “For A, it does B” → “A does B”, obvious non-standard term → standard equivalent, clear “if X then” → “because X,” when X is stated as fact in that sentence.

**Fix silently (minor):** Typos, punctuation, trivial grammar, polish that does not change meaning.

Respect objective 7 (minimal changes).

## Report only what you did not fix

Report when wording needs passage-level judgment: ambiguous “it/this/which”, intentional terminology, physics-story vs rigor tradeoff, or risk of changing technical meaning.

## Output format
One block per assigned sentence:

---
### Sentence <label>
**Edited:** <final LaTeX after silent fixes; if unchanged, repeat original>

**Checks — unresolved only** (if all fixed: "All checks addressed in **Edited** (none to report)."):
1. Clarify references:
2. Define/replace terminology:
3. Subject–verb–object:
4. Streamline narrative:
5. Polish wording:
6. Rigor vs narrative:
7. Minimal changes:
8. Active voice:
9. "For A, it does B":
10. Physics story:

**Needs user / main-agent judgment:** <items or "none">
---
```

---

## 6. Synthesize subagent reports

1. **Assemble** from each **Edited** line (S1, S2, …). Resolve boundary conflicts minimally; note conflicts.
2. **Collect** only unresolved **Checks** and **Needs user / main-agent judgment** → focused questions (SKILL.md Response §3).
3. **Run** [narrative-checks.md](narrative-checks.md) and [math-checks.md](math-checks.md) on the full draft when loaded.
4. In the response, **summarize sentence-level** from subagent reports; do not re-run all 10 inline unless a subagent failed or you override.
5. Finish SKILL.md workflow (clarify → deliver → self-check).

On timeout or incomplete report: run sentence checks manually for that chunk and note the gap.
