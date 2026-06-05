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
| **ASK USER** → user chose proceed anyway | Yes — one Task per splittable sentence when possible; note partial coverage |
| **ASK USER** → user chose skip | No — inline sentence checks instead |

Do not re-AskQuestion for *Sentence-level checking* when Q3 was already feasible. **Always** run the *Subagent model* AskQuestion (§4) before launching Tasks, unless the user already chose a model for **this same quote in this chat**.

---

## 2. Split into numbered sentences

1. Strip `[square-bracket user comments]` from the working copy; keep as editing instructions.
2. Split on sentence boundaries; **do not break** inside `\(...\)`, `$...$`, `\begin{equation}...\end{equation}`, `\cite{...}`, `\ref{...}`, etc.
3. Label **S1, S2, …** for assignment.

If ambiguous, note in the prompt and include the preceding sentence as context.

---

## 3. One sentence per Task (default)

**Purpose:** each subagent audits **one** sentence against all 13 checks. This is the normal assignment rule.

1. After labeling **S1, S2, …**, launch **one Task per sentence**: S1 → Task 1, S2 → Task 2, etc.
2. **Do not** put multiple sentences in one Task unless §3.1 applies.
3. Launch Tasks **in parallel** when practical; use waves if the platform limits concurrency. **`run_in_background: false`** — wait before synthesizing.
4. State the plan in the Mode line: `· <M> Tasks` where **M = number of sentences** (when using the default rule).

### 3.1 Exception: more than 10 sentences

When the passage has **>10** complete sentences, you may assign **2 or more sentences per Task** to keep the run manageable (typical under the gate: 11–12 sentences → e.g. 2 per Task). If the user chose **Proceed with subagents anyway** on a longer quote, scale batch size accordingly. Briefly note the batching choice in the Mode line (e.g. `· 6 Tasks (2 sentences each)`). **Never** batch when **≤10** sentences unless the user explicitly requests it for this quote.

---

## 4. AskQuestion — subagent model

**After** §2–§3 assignment planning and **before** writing the passage summary or launching Tasks, call **AskQuestion**.

**Title:** *Subagent model*

Build options from the **current session Task allowed model list** (do not hardcode slugs in skill files). Offer **one flagship per provider**, with the **exact model slug in each option label**:

| Provider | Pick |
|----------|------|
| **Cursor** | Highest-tier Composer model in the allowed list |
| **OpenAI** | Highest-tier GPT model in the allowed list |
| **Anthropic** | Highest-tier Claude model in the allowed list |

Example option labels (slugs change — derive from the live list):

- `Cursor — composer-2.5`
- `OpenAI — gpt-5.3-codex`
- `Anthropic — claude-opus-4-8-thinking-medium`

Use the chosen slug as the `model` argument on **every** sentence-check Task in this round. If a slug is unavailable when launching, say so and re-AskQuestion with valid options.

**Skip** this AskQuestion only when the user already selected a subagent model for **this same quote in this chat**.

---

## 5. Passage summary, then launch Tasks

**Before any Task**, write one **passage summary** for the full S1…Sn scope (same bullets as SKILL.md § Response — passage summary):

- Passage role and logical flow.
- Placement (section, `.tex` path, neighbors).
- Physics and math at graduate level.

Paste the **identical** block into every subagent prompt under `## Passage summary (shared)`.

```text
Task(
  subagent_type: "generalPurpose",
  readonly: true,
  model: <slug from §4 AskQuestion>,
  description: "Sentence check: S<k>",
  prompt: <template §6>
)
```

Set `model` to the user’s §4 choice. **Do not** hardcode model slugs in skill files; **do** show current slugs in the AskQuestion option labels.

---

## 6. Subagent prompt template

Replace placeholders. Reuse the same `## Passage summary (shared)` in every Task.

```text
You are a sentence-level scientific editor for a physics paper.

## Passage summary (shared)
<identical block in every Task — from §5>

## Local context (read-only)
- Paper topic: <if not clear from summary>
- Section / file: <title and .tex path>
- Adjacent excerpt (1–3 sentences before/after if helpful): <or omit>

## Your assignment
Check ONLY the sentence(s) listed below—**default: one sentence** (§3); if §3.1 batched, list each label separately.

### Sentence <label>
<exact LaTeX/text>

(repeat `### Sentence <label>` blocks only when §3.1 assigned multiple sentences to this Task)

User inline comments: <[bracket comments] or "none">

## Sentence-level check rules
Read and apply every objective in order from:
sentence-checks.md
(same directory as this skill — use the Read tool if you do not have the file)

Run all 13 checks per assigned sentence. Do not skip.

## Apply corrections yourself (do not report these)

**Fix silently (obvious):** Clear from the sentence alone — unambiguous pronoun, SVO mismatch, mandatory “For A, it does B” → “A does B”, obvious non-standard term → standard equivalent, clear “if X then” → “because X,” when X is stated as fact in that sentence.

**Fix silently (minor):** Typos, punctuation, trivial grammar, polish that does not change meaning.

Respect objective 8 (minimal changes).

## Report only what you did not fix

Report when wording needs passage-level judgment: ambiguous “it/this/which”, intentional terminology, physics-story vs rigor tradeoff, prose-vs-math relocation (objective 12), confusion-on-first-read ordering that depends on neighboring sentences (objective 13), or risk of changing technical meaning.

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
12. Use math for math:
13. Confusion-on-first-read ordering:

**Needs user / main-agent judgment:** <items or "none">
---
```

---

## 7. Synthesize subagent reports

1. **Assemble** from each **Edited** line (S1, S2, …). Resolve boundary conflicts minimally; note conflicts.
2. **Collect** only unresolved **Checks** and **Needs user / main-agent judgment** → focused questions (SKILL.md § Response — Clarify).
3. **Run** [narrative-checks.md](narrative-checks.md) and [math-checks.md](math-checks.md) on the full draft when loaded.
4. In the response, **summarize sentence-level** from subagent reports; do not re-run all 13 inline unless a subagent failed or you override.
5. Finish SKILL.md workflow (respond → self-check → apply in Agent mode).

On timeout or incomplete report: run sentence checks manually for that chunk and note the gap.
