---
name: physics-paper-editing
description: >-
  Edits and proofreads LaTeX from physics papers. Every round: complete § Gate
  (count sentences, major-rewrite check, feasible split) before editing.
  Polish on 2+ splittable sentences → one Task subagent per sentence; AskQuestion
  for subagent model before launch. Major rewrite or not feasible → inline or
  AskQuestion. Loads checklists via Read tool.
---

# Physics Paper Editing

Expert scientific editor for physics and mathematics at graduate level.

## Gate (do this first)

**Do not edit `.tex` or run sentence-level work until the gate is done.**

1. **Count** complete sentences in the user’s quote or selection.
2. Answer **Q1**, then **Q2** (if 2+ sentences), then **Q3** (if Q2 is not a major rewrite).
3. Open the reply with: `Mode: <inline | subagents | asked-user> · <N> sentences` (add `· <M> Tasks · <model slug>` when **SUBAGENTS** runs).

### Q1: How many sentences?

```
Q1: How many sentences?
    │
    ├─ 1 (or fragment) ──────────────► INLINE
    │
    └─ 2+ ──► Q2
```

### Q2: Major rewrite?

**Major rewrite** means the deliverable should be **substantially new prose**, not a polish of the existing wording in place. Subagents audit fixed **S1, S2, …** against the source; that workflow fits line-edits, not wholesale replacement.

Treat as **yes** when the user (or implied task) asks to **recompose** the passage—for example: rewrite / redraft / start over; new structure or argument order; merge or split ideas into a fresh narrative; change voice or level so sentences would not read as tightened versions of the originals.

Treat as **no** when the task is **polish or fix**: grammar, clarity, notation, citations, tone, word choice, or light reordering **within** the same claims and sentence roles.

```
Q2: Major rewrite?
    │
    ├─ yes ─► INLINE — skip subagents (main agent drafts, then checklists)
    │
    └─ no ───► Q3
```

### Q3: Feasible to split for subagent sentence-level editing?

Judge whether you can split into **S1, S2, …** and run Tasks without losing meaning. **Feasible** when roughly all hold:

- About **≤12** complete sentences (not a full section or paper).
- Mostly checkable prose (not mostly display equations, tables, or bare lists).
- Splittable without breaking inside math, `\cite{}`, `\ref{}`, or essential cross-references.
- Reasonable Task count (**one Task per sentence** by default; see [sentence-check-subagents.md](sentence-check-subagents.md) §3).

```
Q3: Feasible split for subagents?
    │
    ├─ yes ─► SUBAGENTS — AskQuestion subagent model → one Task per sentence → merge
    │
    └─ no ───► ASK USER — then INLINE or SUBAGENTS per their answer
```

**Not feasible** examples: **>12** sentences, full section, mostly equations/tables, inseparable cross-references, unwieldy Task count. Briefly say why (e.g. “~40 sentences, mostly equations”).

**AskQuestion** (title: *Sentence-level checking*):

| Option | Then |
|--------|------|
| **Skip sentence-level subagents** | **INLINE** — all 12 sentence checks on the passage, then passage-level checklists |
| **Proceed with subagents anyway** | **SUBAGENTS** — one Task per splittable sentence when possible; note partial coverage when synthesizing |
| **Narrow the scope** | User gives a shorter quote; re-run the gate |

**Exceptions (skip the Q3 feasibility AskQuestion only):**

- **Q1 → 1 sentence:** always **INLINE**.
- **Q2 → major rewrite:** always **INLINE**; do not launch sentence-level subagents.
- **Q3 → feasible:** go straight to **SUBAGENTS** (no *Sentence-level checking* AskQuestion).
- User explicitly chose skip / proceed / narrow for **this same quote in this chat** — honor it.
- User explicitly says **inline / quick / no subagents** this turn — **INLINE**.

**SUBAGENTS always requires a model AskQuestion** before launching Tasks (see [sentence-check-subagents.md](sentence-check-subagents.md) §4), unless the user already picked a subagent model for **this same quote in this chat**.

| Mode | When |
|------|------|
| **INLINE** | 1 sentence; major rewrite; or Q3 not feasible and user skipped subagents; or explicit inline request |
| **SUBAGENTS** | 2+ sentences, polish (Q2 no), and feasible split |
| **ASK USER** | 2+ sentences, polish (Q2 no), and Q3 not feasible — AskQuestion before sentence-level work |

**SUBAGENTS:** Follow [sentence-check-subagents.md](sentence-check-subagents.md): **one Task per sentence** (default), **AskQuestion** for subagent model, passage summary, parallel Tasks, merge. In Agent mode, do not apply `.tex` edits until subagent results are merged.

---

## Workflow

```
[ ] 1. Context — topic, file, quote; read neighbor .tex only if needed
[ ] 2. Gate — count sentences; Q1–Q3; set Mode line
[ ] 3. Read checklists — Read tool only (table below)
[ ] 4. Sentence-level — INLINE (12 checks) or SUBAGENTS (split → model AskQuestion → one Task/sentence → merge)
[ ] 5. Passage-level — narrative-checks.md / math-checks.md on full draft (main agent)
[ ] 6. Respond — § Response format; self-check all loaded checklists
[ ] 7. Apply — edit .tex in Agent mode; dual-format output in Ask mode
```

Honor `[square-bracket user comments]` as editing instructions.

### Context (step 1)

| Item | Source |
|------|--------|
| Topic and main claim | User or abstract / introduction |
| Section order | User or `main.tex` (or top-level `.tex`) |
| Files for this passage | User or paths around the selection |

### Which checklists to Read (step 3)

| Condition | Read |
|-----------|------|
| Always (sentence-level work) | [sentence-checks.md](sentence-checks.md) |
| 2+ sentences | + [narrative-checks.md](narrative-checks.md) |
| Math, equations, or logical argument | + [math-checks.md](math-checks.md) |
| **SUBAGENTS** mode | + [sentence-check-subagents.md](sentence-check-subagents.md) **before** split or Tasks |

When length is ambiguous, load sentence + narrative. When math might appear, load math too.

### Sentence-level (step 4)

| Mode | Method |
|------|--------|
| **INLINE** | All 12 objectives in [sentence-checks.md](sentence-checks.md) on the passage |
| **SUBAGENTS** | [sentence-check-subagents.md](sentence-check-subagents.md) — split, Tasks, synthesize |

Narrative and math stay with the **main agent** after sentence-level work (subagents do not run them).

---

## Response format

**1. Passage summary**

- What the text does and how it flows logically.
- Where it sits in the section and relation to neighbors.
- Underlying physics and mathematics.

**2. Check report**

- First line: `Mode: …` (from the gate).
- **Sentence-level:** If **SUBAGENTS** ran, name all **12 objectives** from `sentence-checks.md` and report only **unresolved** items (or “addressed in draft”). If **INLINE**, report all 12. Do not re-list fixes subagents already applied silently.
- **Narrative / math:** For each loaded file, go through every bullet or check **in file order**; if N/A, say why.
- Include explicit user editing directions.

**3. Clarify** — one focused question if guidance is ambiguous; do not finalize edits until resolved.

**4. Edited text**

- **Agent mode:** apply edits in the source `.tex` file.
- **Ask mode:** provide
  - **Rendered:** inline `\( … \)`, display `\[ … \]`.
  - **LaTeX source:** inline `\( … \)`, display `\begin{equation} … \end{equation}` in a fenced block for copy-paste.

**5. Self-check** — re-run every loaded checklist against the final draft; fix gaps before sending.

---

## Checklist files (reference)

| File | Scope |
|------|------|
| [sentence-checks.md](sentence-checks.md) | 12 sentence-level objectives |
| [sentence-check-subagents.md](sentence-check-subagents.md) | Split, Task prompts, synthesis (**SUBAGENTS** only) |
| [narrative-checks.md](narrative-checks.md) | Paragraph through full paper |
| [math-checks.md](math-checks.md) | Definitions, logic, notation, quantifiers |

---

## Project-specific context (optional)

When the manuscript is the Ancilla Optimization / QEC error-budgeting paper:

- **Topic:** decomposing logical infidelity into error-mechanism contributions for realistic QEC devices.
- **Typical skeleton:** Introduction → Background → full QEC evolution → logical evolution graph → Markov chain → error-budget analysis → example.
- **Main sources:** `main.tex`, `Sections/*.tex` (read only what the user points to or what surrounds the edit).

For other papers, use only the generic workflow above.
