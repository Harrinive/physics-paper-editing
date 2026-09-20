# User communication (workbench)

**For agents:** Start with [SKILL.md](SKILL.md) § Agent read order. Read on **every turn** when editing for a user — micro or section.

Level 1 (the message) answers three anxieties only: *will it overwrite me, is it stuck, what can I do now*. The itinerary lives in the **Audit log** drawer at the end. Do not narrate the harness.

**Hard rule:** Never drop or rewrite the verbatim `Mode:` line or `<!-- CHECKS -->` / `<!-- SECTION DONE -->` blocks — hooks and resume depend on them. Place them **only** in the Audit log at the **end**.

---

## Decision rule

If it is not a named state, a receipt of a file change, or a decision the user must make, it does not belong in the narrative.

---

## Level 1 — every turn

One named state, then a receipt, then at most one decision. No percents. No progress bars. No seven-section form.

### Named states (say these)

| State | Say |
|-------|-----|
| **Draft in the file** | Passage is between the `PPE` marks; I am still reading it |
| **Updated the marked passage** | A check pass finished; here is what I kept / changed |
| **Need your call** | One serious conflict; your text is still in the file. Also: a definition that says how to compute the object, not what it is — stop before rewriting it |
| **Done** | Marks removed |

### Receipt (1–3 bullets)

- Where: `{file}`, between `% PPE-BEGIN` / `% PPE-END`
- What changed in the **prose** (physics or wording), not which workers ran
- What happened to **their** edits: kept / auto-fixed an untouched sentence / asking

### Decision (omit if none)

Quote the one conflicting sentence. One clause for their version, one for the check. Ask which to keep. Never a queue of optional nits.

### You can (one line, not a command)

Keep editing inside the marks · say **stop** · say **next piece** on a section job.

On a **definition halt** before marks exist, ask the specific unresolved scientific question and explain why the answer changes the definition. Do not demand a membership test or confirmation of purely formal status merely because the author used a construction.

Do **not** say “reply continue” to unlock the next stage.

---

## Level 1 — first turn of a job only

After the draft is in the file, **three lines** (not a tutorial):

> The revised passage is already in `{file}`, between `% PPE-BEGIN` and `% PPE-END` (created `{timestamp}`). You can edit those lines while I keep reading. If we both change the same sentence I keep your wording unless it contradicts the physics — then I ask, and I only rewrite that block when a check pass finishes.

Show the draft in chat **this once**. Later wakes do not re-paste the passage (except a conflict quote).

Skip this orientation when **definition halt** fired before marks — there is no marked draft yet.

Do not repeat this orientation unless the marks were just created for a new job.

---

## Status copy formula

*Action + specific item + limit.* Never “Working…”, “Running verifiers…”, or “Loading…”.

- “I put the flux-jump definition in `{file}` and I am still reading it. You can edit inside the marks.”
- “I updated the marked block: kept your second sentence; fixed the sign in the lemma sentence (you had not touched it).”
- “I need your call on one sentence — your version says X; the check says Y. I left yours in the file.”
- “I need your call on the definition of X: the text leaves [specific scientific choice] unresolved, and the alternatives give different objects. I have left that definition unchanged.”

---

## Forbidden in the narrative

Phase, Stage, verifier, synthesizer, COMPLIANCE, BLOCKER, snapshot, hash, jsonl, stop request, `rev`, `job=`, worker counts, Producer, internal workflow names, chunk agent.

| Internal | Say only if needed |
|----------|-------------------|
| Construction area / PPE marks | “the marked lines” / “between `% PPE-BEGIN` and `% PPE-END`” |
| Job-round OVERALL PASS | “I finished reading this passage — marks are gone.” |
| OVERALL CONFLICTS | “I need your call on one sentence.” |
| OVERALL PARTIAL | “I am still reading the rest.” |
| polish / rewrite | “light polish” / “rewrite” — only at intake if unclear |
| fast / full | Do not teach pace. Inherit; mention once they can change checkers. |

If they ask “how did you check this?”, answer then — not before.

---

## Response skeleton

```markdown
**{Named state}.** {action + item + limit}

{first turn only: the three-line orientation}

{receipt, 1–3 bullets — omit on a pure “still reading” wake with no file write}

{Decision — omit if none}

You can keep editing inside the marks{, say **next piece**,} or say **stop**.

{first turn only: the draft}

---
### Audit log
Mode: …
<!-- CHECKS … -->   <!-- when a round has a synthesizer result -->
```

### Mode lines (audit drawer only)

```
Mode: draft-ready · verify:running · <N> sentences
Mode: verify-subagents · verify:running · <N> sentences · sentence:<slug> · deep:<slug> · synth:<slug>
Mode: verify-subagents · verify:partial · <N> sentences · …
Mode: verify-subagents · verify:complete · <N> sentences · …
Mode: section-edit · stage:<A|B|C|E> · <slug>
Mode: section-edit · chunk:<id> · verify:running · …
```

`OVERALL` in CHECKS is `PASS` | `CONFLICTS` | `PARTIAL` (job-round). Do not invent a percent from these.

---

## Intake (first reply)

1. Count typographic sentences. If >12, use the scope-overflow message below — do not start this loop on the full section.
2. Ask **polish vs rewrite** only when that is actually unclear.
3. **Do not** ask pace or three models every job. Inherit the last confirmed profile in this chat or `session.md`. If none, use the recommended slugs in [phase2-verify-subagents.md](phase2-verify-subagents.md) and mention once: “I’ll use the usual checkers; say if you want different models.”
4. If the quote **introduces or rewrites** a named physical/protocol object, run [physical-lead.md](../physics-paper-principles/physical-lead.md). Consider physical meaning and choose a suitable definition form. Use **Need your call** only for the essential scientific ambiguity described in [coworker-loop.md](coworker-loop.md) § Definition halt; otherwise draft with supported interpretation.
5. Otherwise draft, mark, schedule verification, and follow this file’s first-turn orientation.

---

## Section jobs

Do not babysit “piece 3 of 7, reply continue.”

Say how many pieces are **in the file**, which one is still being read, and that they can start the next piece or keep editing this one.

Structure review is one receipt: “I reordered X and left placeholders at Y — no new body prose.”

---

## Scope overflow

When the passage has **>12 sentences** or the user asked for a whole `\section{...}`:

> This selection is longer than a single short-passage edit (more than 12 sentences). I can either:
> 1. **Edit the whole section** — structure first, then piece-by-piece (recommended for long text), or
> 2. **Narrow the quote** — pick ≤12 sentences and I will edit that passage directly.
>
> Tell me which you prefer.

Do not say “micro scope”, “macro skill”, or the skill file names unless they ask how the skill works.

---

## What not to put on the bench

| Avoid | Use instead |
|-------|-------------|
| Fake `Progress: [■■■■□□□□] 50%` | A named state |
| “What to expect: pre-edit → check → ship” | First-turn three lines, then receipts |
| “Reply **continue** for piece 4” | “You can keep editing or say **next piece**.” |
| “4 of 11 sentence checks” | “I am still reading it.” |
| “Phase 2 verifier jobs launched” | “I put the draft in `{file}` and I am still reading it.” |
| Merge-algorithm / hash lecture | “I kept your definition sentence.” |
| A standing “don’t worry” paragraph | Orientation once; then silence |
