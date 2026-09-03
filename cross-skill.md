# Micro ↔ macro — shared rules

**For agents:** Start with the skill that matches scope — micro [SKILL.md](SKILL.md) § Agent read order for ≤12 sentences; macro [physics-paper-editing-section/SKILL.md](../physics-paper-editing-section/SKILL.md) § Agent read order for whole sections. Read this file only when routing, resuming, or handing off verifier models between macro and micro.

**Audience:** macro orchestrator · micro agents **invoked from macro Stage D** · skill maintainers.

**Do not read this file** for a standalone short-passage edit (≤12 sentences, only micro skill attached). That path is fully specified in [SKILL.md](SKILL.md) plus [coworker-loop.md](coworker-loop.md).

| Read cross-skill when… | Section |
|------------------------|---------|
| Micro scope is **>12** or user wants a whole section | § Routing |
| Macro Stages A–E or resume | § ON RESUME · § Verifier model profile |
| Micro chunk agent with `session.md` / chunk-contract inputs | § Verifier model profile |
| Maintaining skills — avoid duplicating canonical tables | § Canonical rules |

| Skill | Path | Scope |
|-------|------|-------|
| **Micro** | [physics-paper-editing/SKILL.md](SKILL.md) | One passage **≤12 sentences** — coworker loop |
| **Macro** | [physics-paper-editing-section/SKILL.md](../physics-paper-editing-section/SKILL.md) | Whole `\section{...}` or **>12 sentences** |

Standalone micro needs only one fact about macro: **if the quote exceeds 12 sentences, stop** and suggest the section skill or ask the user to narrow — [SKILL.md](SKILL.md) § Scope overflow.

---

## Routing

```
How many sentences in the target passage?
│
├─ ≤12 ──► micro skill
│           • Coworker loop in micro SKILL.md
│           • Intake: job if unclear; inherit pace + models
│           • No macro required
│
└─ >12 or whole section ──► macro skill
                            • Stages A–E; prose via micro per chunk
                            • Do not run micro on the full section in one turn
```

| Situation | Route |
|-----------|--------|
| User quotes ≤12 sentences | **Micro only** |
| User quotes >12 sentences | **Macro** (or ask user to narrow) |
| User asks to edit a whole `\section{...}` | **Macro** |
| Macro Stage D chunk | **Micro** coworker loop on that `chunk_text` only |
| Macro Stage E boundary fix | **Micro** on ≤12-sentence span |

**Micro gate canonical:** [gate.md](gate.md) § Sentence-count thresholds.

---

## Terminology map

| Concept | Micro | Macro |
|---------|-------|-------|
| Pipeline unit | Passage (≤12 sentences) | Section → chunks |
| Main agent role | **Producer** — drafts, marks, merges | **Section orchestrator** — structure only |
| Verification | Background snapshot check; per-round synthesizer | Same **inside Stage D** per chunk |
| Source-audit Phase 1 | **Does not run** | **Does not run** |
| Pace | Background-check scope only | Frozen in Stage A; passed to every chunk |
| Grades `OVERALL` | Synthesizer only — job-round `PASS` \| `CONFLICTS` \| `PARTIAL` | Same per chunk; orchestrator never grades |
| First `.tex` write | Before checks finish (marked) | Same per chunk |
| Section-scale review | N/A | Stages **B** and **E** (`Scope: section`) |
| Disk state | `.physics-edit/micro/<job_id>/` | `.physics-edit/<slug>/` + `jobs/<id>/` |
| Resume boot | Live marks + `jobs/` | Read **`session.md` first** — § ON RESUME |

**Chunk agent** = micro producer invoked by macro Stage D. Same coworker loop; extra inputs in [chunk-contract.md](../physics-paper-editing-section/chunk-contract.md).

---

## Verifier model profile

### Standalone micro (no macro)

1. Ask polish vs rewrite only if unclear.
2. Inherit pace + the three slugs from this chat, **or** use recommended defaults and mention once ([user-communication.md](user-communication.md)).
3. Reuse the profile for every wave of this draft scope.

### Macro (section edit)

1. **Stage A** — freeze `job_mode`; persist pace and slugs (inherit, disclosed defaults, or AskQuestion) in `session.md`, `section-brief.md`, `manifest.json`.
2. Set **`user_confirmed: true`** after inherit / disclosed defaults / AskQuestion — never from brief/manifest alone without that.
3. **Stages B, D, E** — inherit slugs when `user_confirmed: true`.
4. **Per chunk (Stage D)** — no re-ask when confirmed:

| Session row | Used for |
|-------------|----------|
| sentence | Background changed-sentence Tasks |
| deep | Narrative + math (Stages B/E and micro) |
| synth | Synthesizer only — never fast tier |

**Invalid skips:** `manifest.json` / `section-brief.md` slugs without `session.md` `user_confirmed: true`.

**Hard stop:** no editing Task until slugs are resolved (inherit or defaults). Do not block every job on AskQuestion.

---

## Canonical rules (single source per topic)

| Topic | Canonical file | Section |
|-------|----------------|---------|
| Coworker loop | [coworker-loop.md](coworker-loop.md) | Full file |
| Marks / snapshot / interrupt | [job-state.md](job-state.md) | Full file |
| Merge | [merge-policy.md](merge-policy.md) | Full file |
| User-facing UX | [user-communication.md](user-communication.md) | Full file |
| Job × pace | [gate.md](gate.md) | Decision tree · Sentence-count thresholds |
| Background verify | [phase2-verify-subagents.md](phase2-verify-subagents.md) | Full file |
| Task plan · COMPLIANCE | [compliance-monitoring.md](compliance-monitoring.md) | Full file |
| Sentence Task count · batching | [sentence-check-subagents.md](sentence-check-subagents.md) | §3 |
| Macro stages A–E | [stages.md](../physics-paper-editing-section/stages.md) | Full file |
| Chunk I/O | [chunk-contract.md](../physics-paper-editing-section/chunk-contract.md) | Full file |
| Routing micro ↔ macro | **This file** | § Routing |
| Verifier inheritance | **This file** | § Verifier model profile |
| Section resume | **This file** | § ON RESUME |

---

## Writer ≠ grader · Orchestrator ≠ self-auditor

| Invariant | Rule |
|-----------|------|
| **Writer ≠ grader** | Producer / chunk agent never sets `OVERALL`; synthesizer only. `OVERALL` is a **job-round** status, not a ship gate. |
| **Orchestrator ≠ self-auditor** | Section orchestrator does not launch micro verifier Tasks or certify task counts |
| **Pace** | Changes background-check scope only; never makes the user wait; never skips the synthesizer. Macro chunks always pass `caller: section-orchestrator`, so the standalone-micro fast-polish math skip never applies to a chunk. |

---

## ON RESUME (macro only)

When resuming a section edit (new chat, **next piece**, context compaction):

1. Read `.physics-edit/<slug>/`**session.md`** first.
2. Read `manifest.json` + `section-brief.md` + any `jobs/*/agents.json`.
3. If any job is `checking` → micro wake protocol (related hashes → interrupt → harvest → merge) **before** a new piece.
4. Honor `job_mode`, `pace`, and per-chunk `edit_gate`; do not re-ask.
5. Honor **User special requests**.
6. Profile must be resolved (`user_confirmed: true` or disclosed defaults) before verifier Tasks.
7. Execute **Next action**; rewrite `session.md` before ending the turn.

Detail: [disk-layout.md](../physics-paper-editing-section/disk-layout.md) § session.md · [automation.md](../physics-paper-editing-section/automation.md).
