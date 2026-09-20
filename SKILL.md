---
name: physics-paper-editing
description: >-
  Draft-first coworker loop for LaTeX physics passages (≤12 sentences): write
  marked working text, background-verify a snapshot, interrupt-safe harvest,
  three-way merge. Canon is physics-paper-principles. Routes >12 sentences to
  parent skill physics-paper-editing-section.
compatibility: >-
  Requires filesystem access for drafting. Full verification requires subagent
  delegation; adapters are provided for Cursor, Codex, and Claude Code.
---

# Physics Paper Editing (micro)

**Process** for editing a short LaTeX physics/mathematics passage. Canon — what the prose should be — is **`physics-paper-principles`**. This skill does not restate those principles. Verifier workers use the **inverted** Detect lookup: artifact first, then the principles listed under it ([sentence-check-subagents.md](sentence-check-subagents.md), [phase2-verify-subagents.md](phase2-verify-subagents.md)).

**Standalone** for passages **≤12 sentences**. Parent: **`physics-paper-editing-section`** for whole `\section{...}` or **>12 sentences**.

## When to use

- Run the coworker loop: draft into the `.tex` immediately, check in the background, merge on each round
- User gives a short quote, paragraph fragment, or caption block within micro scope

**Route elsewhere:** passages **>12 sentences** or whole `\section{...}` → **`physics-paper-editing-section`** ([Scope overflow](#scope-overflow)). Writing without the loop → **`physics-paper-principles`** only.

## Agent read order

| Situation | Read |
|-----------|------|
| **Standalone micro job (≤12 sentences)** | This file → [user-communication.md](user-communication.md) → [coworker-loop.md](coworker-loop.md) → step 2 table |
| **Scope overflow (>12 sentences)** | § Scope overflow below — route to the parent skill; do **not** read [cross-skill.md](../physics-paper-editing-section/cross-skill.md) |
| **Invoked from macro Stage D** | This file + [Invoked by section macro](#invoked-by-section-macro-optional) + parent [cross-skill.md](../physics-paper-editing-section/cross-skill.md) § Verifier model profile |
| **Every resume / wake** | [job-state.md](job-state.md) for the live job, then [coworker-loop.md](coworker-loop.md) § Wake |

**Use this skill alone** (plus **`physics-paper-principles`**) when the user gives a passage of **≤12 sentences**. No parent skill, no `cross-skill.md` on that path. Standalone jobs still write `.physics-edit/micro/<job_id>/` ([job-state.md](job-state.md)).

**First reply:** count typographic sentences. If ≤12, ask polish versus rewrite only if unclear; resolve one confirmed model profile for this top-level session ([runtime-contract.md](runtime-contract.md) and [gate.md](gate.md)). If the passage introduces or rewrites a named physical object, run the physical-lead diagnostic ([physical-lead.md](../physics-paper-principles/physical-lead.md)); **halt and ask** only when an essential scientific ambiguity prevents faithful drafting ([coworker-loop.md](coworker-loop.md) § Definition halt). Otherwise draft from principles, mark, delegate verification under the selected runtime, and return control whenever the runtime permits. User-facing copy: [user-communication.md](user-communication.md).

## Invoked by section macro (optional)

Read this section only when Stage D passes `chunk_text` + `edit_gate` + `pace` +
`session.md` via [chunk-contract.md](../physics-paper-editing-section/chunk-contract.md).

- Run the coworker loop on `chunk_text` only.
- Use supplied `edit_gate` and `pace`; do not re-ask.
- **Verifier models:** inherit only the confirmed profile from `session.md`. Handoff: [cross-skill.md](../physics-paper-editing-section/cross-skill.md) § Verifier model profile.
- Set `caller: section-orchestrator` in the worker plan ([compliance-monitoring.md](compliance-monitoring.md)).
- Wrap that chunk’s `tex_anchor` span; one job per chunk.

## Purpose

Edit LaTeX prose as a **coworker**, not a blocking pipeline:

1. **Draft first** — producer writes using **`physics-paper-principles`** as canon.
2. **Mark** a construction area and leave the text in the `.tex`.
3. **Verify** a frozen snapshot against those principles; workers persist findings to disk.
4. **Merge** once per round; request a stop when supported, then harvest if the user changed related text.

The producer writes the draft and applies merge actions. It **must not** grade its own draft or set `OVERALL` — only the per-round **verifier synthesizer** may do that. `OVERALL` is a job-round status (`PASS` | `CONFLICTS` | `PARTIAL`), not a gate that blocks the first `.tex` write.

Canonical loop: [coworker-loop.md](coworker-loop.md).

---

## Unit of work

| | |
|--|--|
| **Scope** | One passage, **≤12 sentences** |
| **Input** | Passage + optional context (neighbors, section title, brief) |
| **Output (first turn)** | Marked draft in `.tex`; verification dispatched; first-turn orientation |
| **Output (later wake)** | Receipt and/or one decision; marks updated or removed |

Passages **>12 sentences** are out of scope — see [Scope overflow](#scope-overflow).

---

## Standalone quick start

1. **Scope** — confirm ≤12 sentences ([Scope overflow](#scope-overflow) if not).
2. **Read** — [user-communication.md](user-communication.md), [coworker-loop.md](coworker-loop.md), step 2 table.
3. **Intake** — polish versus rewrite if unclear; confirm the session model profile once ([runtime-contract.md](runtime-contract.md)). Definition halt if needed ([coworker-loop.md](coworker-loop.md)).
4. **Draft** — **`physics-paper-principles`**; no blocking source-audit phase. Named physical objects: [physical-lead.md](../physics-paper-principles/physical-lead.md).
5. **Mark + write** — [job-state.md](job-state.md); snapshot; dispatch verification ([phase2-verify-subagents.md](phase2-verify-subagents.md)).
6. **Continue or return control** — follow the runtime's asynchronous or foreground mode.
7. **On completion or wake** — stop stale work if supported; harvest; one merge ([merge-policy.md](merge-policy.md)); relaunch dirty labels or unmark.

---

## Scope overflow

When the target has **>12 sentences** or the user asks for a whole `\section{...}`:

1. Do **not** run the coworker loop on the full text in one turn.
2. Tell the user the passage exceeds a short-passage edit — copy in [user-communication.md](user-communication.md).
3. Offer: attach [physics-paper-editing-section](../physics-paper-editing-section/SKILL.md), **or** narrow to ≤12 sentences.

That is the **only** parent-skill awareness required on a standalone micro job. Do not read [cross-skill.md](../physics-paper-editing-section/cross-skill.md) unless you are routing overflow or were invoked from macro Stage D.

---

## Roles and terms

| Term | Meaning |
|------|---------|
| **Producer** | Main agent — drafts, marks, applies merge; never sets `OVERALL` |
| **Sentence verifier** | Independent subagent — assigned sentence scope; artifact-first then unresolved 1–15; writes its own result shard |
| **Narrative verifier** | Independent subagent — full snapshot; four narrative groups |
| **Math verifier** | Independent subagent — full snapshot when math or logical argument is present |
| **Verifier synthesizer** | Per **round** — sole `OVERALL` authority (`PASS` \| `CONFLICTS` \| `PARTIAL`) |
| **Worker plan** | Required before any verifier delegation ([compliance-monitoring.md](compliance-monitoring.md)) |
| **Construction area** | `% PPE-BEGIN` / `% PPE-END` pair ([job-state.md](job-state.md)) |
| **Round** | Full wave completion **or** interrupt harvest, then one merge write |
| **Edit gate** | `polish` \| `rewrite` — how the draft is produced |
| **Fast / full** | Background-check scope only — never whether the user waits ([fast-polish.md](fast-polish.md)) |
| **BLOCKER** | Must-fix on untouched text (auto-apply) or serious vs user (report). Unresolved physical meaning (class 6) never auto-applies ([severity.md](severity.md)) |
| **SUGGEST** | Never auto-applies; never a decision |
| **Changed sentences** | Labels whose text differs from the prior snapshot / source |
| **CHECKS block** | Audit-drawer only; synthesizer is sole authority |
| **PACKET_GAP** | Fast-polish note that a finding needs more manuscript context — not a must-fix |
| **Definition halt** | Producer pauses the affected definition only when faithful drafting requires an essential scientific choice that supplied context cannot resolve |

**Sentence-count thresholds:** [gate.md](gate.md). **Scope:** ≤12 micro; >12 route to parent.

### Agent tiers

| Tier | Who | Writes prose? | Delegates workers? | Grades `OVERALL`? |
|------|-----|---------------|-------------------|-------------------|
| **Main agent** (Producer) | 1 agent | Yes (draft + merge) | Yes | **No** |
| **Verifier subagents** | sentence · narrative · math | No | No | No |
| **Verifier synthesizer** | 1 agent per round | No | No | **Yes (sole authority)** |

**Writer ≠ grader:** [compliance-monitoring.md](compliance-monitoring.md).

---

## Workflow checklist

**Hard rules:**

- Write the marked draft to `.tex` **before** checks finish. Do not wait for `OVERALL`. **Exception:** definition halt — do not invent the resolution of an essential scientific ambiguity ([coworker-loop.md](coworker-loop.md)).
- Producer must not grade its own draft or set `OVERALL`.
- Delegate checkers through the selected runtime. Continue asynchronously when available; otherwise use foreground waves without withholding the draft.
- On completion or wake, harvest result shards before merging. Do not drop stale findings.
- **Publish the worker plan** before any verifier delegation. Preserve one changed-sentence assignment for scopes of ten or fewer unless the user explicitly accepts partial coverage.
- User-facing turns follow [user-communication.md](user-communication.md) — no fake progress bars, no pipeline narration.

```
[ ] 1. Context — file, neighbors, [bracket comments] as editing instructions
[ ] 2. Read — user-communication.md, coworker-loop.md, principles + severity (table below)
[ ] 3. Intake — polish/rewrite if unclear; confirm or inherit the recorded session profile ([runtime-contract.md](runtime-contract.md)); consider physical meaning and definition choice; definition halt only for essential scientific ambiguity
[ ] 4. Draft — physics-paper-principles; no blocking source-audit phase
[ ] 5. Mark + snapshot — [job-state.md](job-state.md)
[ ] 6. Verification — [phase2-verify-subagents.md](phase2-verify-subagents.md)
      [ ] Worker plan; schedule changed-label, narrative, and math assignments as applicable
      [ ] Runtime capability resolution; workers write separate result shards
      [ ] Continue asynchronously when supported; otherwise harvest foreground waves
[ ] 7. On completion or wake — related hashes → stop if supported → harvest → merge ([merge-policy.md](merge-policy.md))
[ ] 8. Relaunch open/dirty labels or unmark; synthesizer CHECKS in the audit drawer
```

### Step 1 — Context

| Item | Source |
|------|--------|
| Topic and main claim | User or abstract / introduction |
| Section order | User or `main.tex` (or top-level `.tex`) |
| Files for this passage | User or paths around the selection |
| `[bracket comments]` | User inline editing instructions — strip from working copy, honor in edits |

### Step 2 — What to Read

| Condition | Read |
|-----------|------|
| Always | [user-communication.md](user-communication.md), [coworker-loop.md](coworker-loop.md), [sentence.md](../physics-paper-principles/sentence.md), [severity.md](severity.md) |
| 2+ sentences | + [narrative.md](../physics-paper-principles/narrative.md) |
| Math, equations, logical argument, or a named-object definition | + [math.md](../physics-paper-principles/math.md); named objects: [physical-lead.md](../physics-paper-principles/physical-lead.md) |
| Intake | + [gate.md](gate.md) |
| Mark / snapshot / interrupt | + [job-state.md](job-state.md) |
| Merge round | + [merge-policy.md](merge-policy.md) |
| Dispatch or harvest checkers | + [runtime-contract.md](runtime-contract.md), [phase2-verify-subagents.md](phase2-verify-subagents.md), [sentence-check-subagents.md](sentence-check-subagents.md), [compliance-monitoring.md](compliance-monitoring.md) |
| `polish` + `pace: fast` + standalone | + [fast-polish.md](fast-polish.md) |
| Before any verifier delegation | + [compliance-monitoring.md](compliance-monitoring.md) § Worker plan block |

When length is ambiguous, load sentence + narrative. When math or a named-object definition might appear, load math (and physical-lead) too.

---

## Response format

Follow [user-communication.md](user-communication.md) exactly — named state, receipt, optional decision, audit drawer. Do not use the old seven-section form or progress bars.

---

## File map

**Coworker loop**

| File | Role |
|------|------|
| [coworker-loop.md](coworker-loop.md) | Draft → mark → snapshot → verification → harvest → merge |
| [job-state.md](job-state.md) | PPE marks, snapshot, result shards, stop request |
| [runtime-contract.md](runtime-contract.md) | Capability contract, session profile, scheduler, storage schema |
| [runtime-cursor.md](runtime-cursor.md) | Cursor adapter |
| [runtime-codex.md](runtime-codex.md) | Codex adapter |
| [runtime-claude.md](runtime-claude.md) | Claude Code adapter |
| [merge-policy.md](merge-policy.md) | Three-way merge rubric |
| [user-communication.md](user-communication.md) | Workbench UX — every user-facing turn |
| [gate.md](gate.md) | Job × pace; inherit models; sentence-count thresholds |
| [severity.md](severity.md) | Closed BLOCKER lists; SUGGEST; unresolved physical meaning never auto-applies |
| [phase2-verify-subagents.md](phase2-verify-subagents.md) | Verifier prompts, artifact-first checks, per-round synthesizer |
| [sentence-check-subagents.md](sentence-check-subagents.md) | Sentence split, artifact-first sentence verifiers, incremental result writes |
| [compliance-monitoring.md](compliance-monitoring.md) | Worker plan, Step 0, Diagnostics homework, synthesizer procedural checks |
| [fast-polish.md](fast-polish.md) | Fast standalone polish: narrower question, possible math skip |

**Canon (sibling skill)** — [physics-paper-principles/SKILL.md](../physics-paper-principles/SKILL.md)

**Sibling sync:** this skill and **`physics-paper-principles`** are a paired split (harness vs canon). Changing a Detect test name or principle ID in the canon lookup requires the same name in this skill’s worker **artifact → principles** list, **same pass**. Changing a worker artifact, silent-fix list, or its principle list requires the canon Detect column still to point at that artifact. Grep the sibling for the old name before finishing. Drift is a bug. Do not copy Detect paragraphs into prompts — name the test; require the same artifact label. `physics-paper-editing-section` only if it duplicates prompt text; otherwise it already points here.

## Related skills

| Skill | When |
|-------|------|
| **physics-paper-principles** | Canon — always, as drafting and checker objectives |
| **physics-paper-editing-section** | Parent — passage **>12 sentences** or whole `\section{...}` |
| **sc-qubit-sim** | Scientific prose in simulation docs (`conventions/scientific-prose.md`) |

## Out of scope

- Passages **>12 sentences** or whole `\section{...}` — route to **`physics-paper-editing-section`**
- Restating sentence/narrative/math principles — those live in **`physics-paper-principles`**
- Waiting to write `.tex` until `OVERALL: PASS`
- Producer self-grading `OVERALL`
- BibTeX, figure files, or non-prose LaTeX (equations-only blocks with no prose claims)
