# Sentence-Level Checks via Task Subagents

When the loaded checklist includes **`sentence-checks.md`** and the passage contains one or more sentences, **delegate sentence-level checking to Task subagents** instead of running those checks yourself inline — unless subagent delegation is infeasible (see §2) or the user opts out.

Narrative checks (`narrative-checks.md`) and math checks (`math-checks.md`) stay with the **main agent** after subagent reports are merged.

---

## 1. Decide whether subagent delegation is feasible

Before splitting or launching Tasks, judge whether sentence-level checking via subagents is **practical** for this request.

**Use subagents** when the passage has multiple complete sentences and each chunk you plan to assign is short enough for rigorous item-by-item checking (see §3).

**Ask the user before proceeding** when delegation is **obviously not feasible**, e.g.:

- The scope is an entire paper, a full section, or another very large block (dozens of sentences or more).
- The text is mostly display equations, tables, or list fragments with little checkable prose.
- Sentences are so tightly cross-referential that isolating them would strip essential context and produce unreliable reports.
- You expect an impractically large number of subagent calls for the value gained.

Use **`AskQuestion`** with options such as:

- **Skip sentence-level subagents** — main agent runs narrative/math checklists only; still fixes any sentence-level issues noticed inline.
- **Proceed with subagents anyway** — main agent chooses a coarser split (§3) and accepts partial coverage if needed.
- **Narrow the scope** — user specifies a shorter passage to edit.

If the user skips subagents, the main agent **may still edit** obvious sentence-level problems while running the other checklists. Do not block the edit round on subagents.

**Do not use AskQuestion** for small, routine passages where subagent delegation is clearly feasible (a paragraph, a proof, a subsection opening).

---

## 2. Split the passage into sentences

1. Strip `[square-bracket user comments]` from the working copy; keep them as separate editing instructions.
2. Split on sentence boundaries while **keeping LaTeX intact** (do not break inside `\(...\)`, `$...$`, `\begin{equation}...\end{equation}`, `\cite{...}`, `\ref{...}`, etc.).
3. Number each sentence **S1, S2, …** for assignment.

If splitting is ambiguous, note the ambiguity in the subagent prompt and include the preceding sentence as context.

---

## 3. Batch sentences across subagents *(main agent decides)*

**You choose the split.** There is no fixed agent count or fixed chunk size. Use judgment so each Task receives a **short, feasible** assignment: enough context to apply all 10 checks item-by-item, but not so much that the subagent rushes or skips checks.

**Rule of thumb:** one complete sentence per subagent when sentences are long, dense, or math-heavy; group 2–4 short, closely related sentences when they form one logical beat (e.g. a list-item heading + its follow-on clause, or two consecutive proof steps). Never assign a whole paragraph to one subagent unless it is genuinely a single sentence.

**Other guidance:**

- Keep adjacent list items or proof steps together when splitting them would lose the referent for “the second term”, “type~2”, etc.
- Prefer **fewer, well-scoped** subagents over many tiny ones when sentences are trivial (headings, “Fix **s** and define”).
- Launch subagents **in parallel** when practical (one message, multiple `Task` calls). If the split is large, batch launches (e.g. two waves) rather than one enormous wave.
- Do **not** set `run_in_background: true` — wait for reports before synthesizing.

---

## 4. Launch Task subagents

For each chunk:

```
Task(
  subagent_type: "generalPurpose",
  readonly: true,
  model: <Cursor flagship model — see below>,
  description: "Sentence check: <brief scope, e.g. 'intro ¶1' or 'proof S12–S14'>",
  prompt: <subagent prompt below>
)
```

**Model:** Always set the Task tool's `model` parameter to **Cursor's current flagship model** — the highest-capability general model in the Task tool's allowed list for this session. Read that list when you launch Tasks; do not hardcode model names or version numbers in skill files or in the subagent prompt text (they change over time).

Do **not** mention model names inside the prompt you send to the subagent.

---

## 5. Subagent prompt template

Paste this block into every subagent prompt. Replace bracketed placeholders.

```
You are a sentence-level scientific editor for a physics paper.

## Context (read-only)
- Paper topic: <topic or "see surrounding material">
- Section / file: <section title and .tex path if known>
- Surrounding material (for reference only):
<1–3 adjacent sentences or a short excerpt>

## Your assignment
Check ONLY the following sentence(s) from the passage. Number them as given.

<for each assigned sentence>
### Sentence <index>
<exact LaTeX/text of the sentence>
</for each>

User inline comments (apply as editing instructions):
<list [bracket comments] or "none">

## Sentence-level check rules
Read and apply every objective in order from:
/Users/harry/.cursor/skills/physics-paper-editing/sentence-checks.md

Run all 10 checks for each assigned sentence. Do not skip a check; if it does not apply, say "N/A" and why.

## Output format (concise — main agent will synthesize)
Return one block per assigned sentence:

---
### Sentence <index>
**Original:** <quote>

**Checks (one line each):**
1. Clarify references: <OK | issue + brief note>
2. Define/replace terminology: <OK | issue + brief note>
3. Subject–verb–object: <OK | issue + brief note>
4. Streamline narrative: <OK | issue + brief note>
5. Polish wording: <OK | issue + brief note>
6. Rigor vs narrative: <OK | issue + brief note>
7. Minimal changes: <OK | issue + brief note>
8. Active voice: <OK | issue + brief note>
9. "For A, it does B": <OK | issue + brief note>
10. Physics story: <OK | issue + brief note>

**Obvious corrections** (clear errors — main agent should apply without asking):
- <corrected sentence in LaTeX, or "none">

**Minor suggestions** (stylistic / judgment calls — main agent should ask the user):
- <suggestion + brief rationale, or "none">
---

Keep each sentence report under ~15 lines. No full paper summary. No narrative- or section-level commentary.
```

---

## 6. Main agent: synthesize subagent reports

After all subagents return:

1. **Merge obvious corrections** into a working draft (respect check 7 — minimal changes).
2. **Collect minor suggestions** from all reports; group duplicates; turn them into focused questions for the user (step 3 of Response Format).
3. **Run remaining checklists yourself** on the full passage:
   - `narrative-checks.md` when loaded
   - `math-checks.md` when loaded
4. In step 2 of Response Format, **summarize sentence-level findings** by referencing subagent reports (do not re-run all 10 checks inline unless a subagent failed or you disagree — then note the override).
5. Proceed with steps 3–6 of Response Format (clarify → edit → self-check).

If a subagent times out or returns an incomplete report, run sentence checks manually for that chunk and note the gap.

---

## 7. When NOT to use subagents *(no AskQuestion needed)*

- User explicitly asks for a quick inline pass with no subagents.
- Passage is a **single sentence** or **single sentence fragment** with no multi-sentence scope (main agent runs `sentence-checks.md` directly).
- `sentence-checks.md` is **not** in the loaded checklist (e.g. pure math-symbol audit with only `math-checks.md`).

In these cases the main agent still applies `sentence-checks.md` inline when that checklist is loaded.
