# Verification loops

**Read with the Read tool** when [SKILL.md](SKILL.md) steps **4 or 6** run.

**Canonical phase comparison** (this file). Execution: [gate.md](gate.md) (Phase 1) · [phase2-verify-subagents.md](phase2-verify-subagents.md) (Phase 2).

---

## Phase comparison

| | Phase 1 — source verify | Phase 2 — output verify |
|--|-------------------------|-------------------------|
| **Step** | 4 | 6 |
| **Target** | User's existing prose | Producer's generated draft |
| **When** | Polish only; **skipped** on major rewrite | **Every** edit turn |
| **Routing** | [gate.md](gate.md) → INLINE or SUBAGENTS | **No gate** |
| **Sentence checks** | All sentences — main agent or sentence Tasks | **Changed sentences only** — sentence verifier Tasks |
| **Narrative + math** | Main agent on full passage | Verifier Tasks on **full passage** |
| **Who decides done** | Main agent (informs step 5) | **Verifier synthesizer** — sole `OVERALL` authority |
| **CHECKS / hook** | No | Required; hook enforces |

---

## Phase 1 — source verify (step 4)

**When:** Edit gate Q2 = polish. **Skipped** on major rewrite.

**Purpose:** Audit source before editing — notation, scope, issues to fix in step 5.

```
1. Source verify gate (Q2 skipped — always polish)
2. Emit Task plan (phase1_sentence_tasks = N labels when polish, N≥2)
3. Sentence-level — INLINE or SUBAGENTS per gate (SUBAGENTS: **N Tasks**, one per label)
4. Passage-level — narrative + math checklists (main agent)
5. → step 5 (produce draft)
```

If understanding changes materially, revise the edit plan and re-run from step 1.

**Do not** skip Phase 1 because Phase 2 will run later.

---

## Phase 2 — output verify (step 6)

**When:** Every edit turn, including major rewrites.

**Purpose:** Independent agents grade the producer's draft before shipping.

```
1. AskQuestion — verifier model profile (hard stop — see phase2-verify-subagents.md § Model selection gate)
2. Identify changed sentences → see phase2-verify-subagents.md § Changed sentences
3. Emit Task plan (phase2_sentence_tasks = changed labels only)
4. Launch verifier Tasks (only after steps 1–3):
     • narrative — always, full passage (+ Step 0 compliance)
     • math — full passage when applicable (+ Step 0 compliance)
     • sentence — **one Task per changed label** (+ Step 0 compliance)
   → synthesizer (merges procedural + content)
5. Synthesizer emits Mode line + CHECKS + OVERALL (procedural FAIL blocks ship)
6. FAIL → fix draft and/or Task plan → restart from step 2 (fresh Tasks)
7. PASS → step 7 (ship)
```

**Producer must not** run checklists inline or set OVERALL.

**CHECKS block:** Copy **verbatim** from synthesizer into the final user response.

**Hook:** `~/.cursor/hooks/check-editing-session.sh` on `stop` — missing CHECKS or `OVERALL: FAIL` → follow-up (up to `loop_limit: 3` in `~/.cursor/hooks.json`).

Full execution detail: [phase2-verify-subagents.md](phase2-verify-subagents.md).

---

## Non-negotiable rules

- Phase 2: always fresh verifier subagents; no gates; no producer self-grade.
- **AskQuestion before any Phase 2 verifier `Task`** — major rewrite does not waive this ([phase2-verify-subagents.md](phase2-verify-subagents.md) § Model selection gate).
- Never auto-select model slugs; skill recommendations require user confirmation via `AskQuestion`.
- Never skip Phase 2 because Phase 1 ran.
- Never end the turn without synthesizer `OVERALL: PASS`.
- Never ship when `compliance_orchestrator_plan: FAIL` or `compliance_worker_reports: FAIL` in CHECKS.
- After any Phase 2 draft fix, relaunch the verifier suite (new Tasks): narrative + math on full passage; sentence Tasks only for sentences changed in that fix pass.
- User speed/loop/minor-only constraints **do not** reduce sentence Task count — [compliance-monitoring.md](compliance-monitoring.md).
