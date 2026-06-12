# Micro ↔ macro — shared rules

**Audience:** macro orchestrator · micro agents **invoked from macro Stage D** · skill maintainers (canonical index).

**Do not read this file** for a standalone short-passage edit (≤12 sentences, only micro skill attached). That path is fully specified in [SKILL.md](SKILL.md) and the pipeline detail files — no macro context required.

| Read cross-skill when… | Section |
|------------------------|---------|
| Micro scope is **>12** or user wants a whole section | § Routing |
| Macro Stages A–E or resume | § ON RESUME · § Verifier model profile |
| Micro chunk agent with `session.md` / chunk-contract inputs | § Verifier model profile |
| Maintaining skills — avoid duplicating canonical tables | § Canonical rules |

| Skill | Path | Scope |
|-------|------|-------|
| **Micro** | [physics-paper-editing/SKILL.md](SKILL.md) | One passage **≤12 sentences** — self-contained |
| **Macro** | [physics-paper-editing-section/SKILL.md](../physics-paper-editing-section/SKILL.md) | Whole `\section{...}` or **>12 sentences** |

Standalone micro needs only one fact about macro: **if the quote exceeds 12 sentences, stop** and suggest [physics-paper-editing-section](../physics-paper-editing-section/SKILL.md) or ask the user to narrow — see [SKILL.md](SKILL.md) § Scope overflow. No other macro knowledge is required on that path.

---

## Routing

```
How many sentences in the target passage?
│
├─ ≤12 ──► micro skill (this repo: physics-paper-editing)
│           • Run full steps 1–7 in micro SKILL.md
│           • AskQuestion for verifier models (unless valid skip — § Verifier model profile)
│           • No macro required
│
└─ >12 or whole section ──► macro skill (physics-paper-editing-section)
                            • Stages A–E; prose only via micro per chunk
                            • Do not run micro on the full section in one turn
```

| Situation | Route |
|-----------|--------|
| User quotes ≤12 sentences | **Micro only** |
| User quotes >12 sentences | **Macro** (or ask user to narrow) |
| User asks to edit a whole `\section{...}` | **Macro** |
| Macro Stage D chunk | **Micro** on that chunk's `chunk_text` only |
| Macro Stage E boundary fix | **Micro** on ≤12-sentence span |
| Q3 not feasible in micro gate | [gate.md](gate.md) AskQuestion → macro, inline, or narrow |

**Micro gate canonical:** sentence-count table in [SKILL.md](SKILL.md) § Roles and terms.

---

## Terminology map

| Concept | Micro | Macro |
|---------|-------|-------|
| Pipeline unit | Passage (≤12 sentences) | Section → chunks |
| Main agent role | **Producer** — authors chunk prose | **Section orchestrator** — structure only |
| Verification phases | **Phase 1** (polish) · **Phase 2** (always) | Phase 1/2 run **inside Stage D** per chunk |
| Phase 1 skip | Edit gate Q2 → major rewrite | `edit_gate: rewrite` or `job_mode: rewrite` (frozen Stage A) |
| Grades `OVERALL` | Verifier **synthesizer** only | Same — per chunk; orchestrator never grades |
| Section-scale review | N/A | Stages **B** and **E** (`Scope: section`) |
| Disk state | None (optional) | `.physics-edit/<slug>/` — [disk-layout.md](../physics-paper-editing-section/disk-layout.md) |
| Resume boot | N/A | Read **`session.md` first** — § ON RESUME below |

**Chunk agent** = micro Producer invoked by macro Stage D. Same steps 1–7; extra inputs in [chunk-contract.md](../physics-paper-editing-section/chunk-contract.md).

---

## Verifier model profile

### Standalone micro (no macro)

1. **Phase 1 SUBAGENTS** — `AskQuestion` *Sentence checker model* before sentence Tasks ([sentence-check-subagents.md](sentence-check-subagents.md) §4).
2. **Phase 2** — `AskQuestion` *Verifier model profile* (three questions) before any verifier Task ([phase2-verify-subagents.md](phase2-verify-subagents.md) § Model selection gate).
3. **Valid skip (same chat):** user already chose models for **this draft scope** — reuse slugs on FAIL→fix loops; do not re-ask.

Macro paths below **do not apply** unless a section edit is in progress.

### Macro (section edit)

1. **Stage A** — one `AskQuestion` (*Verifier model profile*); persist slugs in `session.md`, `section-brief.md`, `manifest.json`.
2. Set **`user_confirmed: true`** only after AskQuestion returns — never from brief/manifest alone.
3. **Stages B, D, E** — inherit slugs when `user_confirmed: true`; document `Verifier profile: inherited from session.md (Stage A confirmed)`.
4. **Per chunk (Stage D)** — no re-ask when confirmed; chunk agent uses session table:

| Session row | Used for |
|-------------|----------|
| Phase 1 sentence | Phase 1 SUBAGENTS (polish); may equal Phase 2 sentence |
| Phase 2 sentence | Phase 2 changed-sentence Tasks; **default for Phase 1** when Phase 1 row omitted |
| Phase 2 deep | Narrative + math (macro Stages B/E and micro Phase 2) |
| Phase 2 synth | Synthesizer only — never fast tier |

**Invalid skips:** `manifest.json` / `section-brief.md` slugs without `session.md` `user_confirmed: true`; skill "(Recommended)" labels; Phase 1 skipped does **not** waive Phase 2 AskQuestion on first iteration (standalone micro).

**Hard stop:** no verifier `Task` until slugs are resolved ([phase2-verify-subagents.md](phase2-verify-subagents.md) § Model selection gate).

---

## Canonical rules (single source per topic)

Do not duplicate these tables in SKILL.md — link here or to the canonical file.

| Topic | Canonical file | Section |
|-------|----------------|---------|
| Phase 1 vs Phase 2 | [verification-loop.md](verification-loop.md) | Phase comparison |
| Edit gate · source verify gate | [gate.md](gate.md) | Decision tree |
| Phase 2 workflow · changed sentences | [phase2-verify-subagents.md](phase2-verify-subagents.md) | Full file |
| Task plan · COMPLIANCE · anti-patterns | [compliance-monitoring.md](compliance-monitoring.md) | Full file |
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
| **Writer ≠ grader** | Producer / chunk agent never sets `OVERALL`; synthesizer only ([phase2-verify-subagents.md](phase2-verify-subagents.md)) |
| **Orchestrator ≠ self-auditor** | Section orchestrator does not launch micro verifier Tasks or certify task counts; workers Step 0 + synthesizer procedural merge ([compliance-monitoring.md](compliance-monitoring.md)) |
| **User speed constraints** | Never reduce one-sentence-per-Task count or skip synthesizer |

---

## ON RESUME (macro only)

When resuming a section edit (new chat, "continue", context compaction):

1. Read `.physics-edit/<slug>/`**session.md`** first.
2. Read `manifest.json` + `section-brief.md`.
3. Honor **`job_mode`** / per-chunk **`edit_gate`** — do **not** re-run micro edit gate Q2.
4. Honor **User special requests** (standing + `deferred_edits`).
5. **`user_confirmed: true`** required before verifier Tasks — else AskQuestion and END TURN if awaiting answer.
6. Execute **Next action** only; rewrite `session.md` before END TURN.

Detail: [disk-layout.md](../physics-paper-editing-section/disk-layout.md) § session.md · [automation.md](../physics-paper-editing-section/automation.md) § Context compaction recovery.
