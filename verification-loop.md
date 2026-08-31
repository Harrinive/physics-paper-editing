# Verification loops

**For agents:** Start with [SKILL.md](SKILL.md) § Agent read order. **Read with the Read tool** when [SKILL.md](SKILL.md) steps **4 or 6** run.

**Canonical phase comparison** (this file). Execution: [gate.md](gate.md) (Phase 1) · [phase2-verify-subagents.md](phase2-verify-subagents.md) (Phase 2).

---

## Phase comparison

| | Phase 1 — source verify | Phase 2 — output verify |
|--|-------------------------|-------------------------|
| **Step** | 4 | 6 |
| **Target** | User's existing prose | Producer's generated draft |
| **When** | Polish only; **skipped** on major rewrite | **Every** edit turn |
| **Routing** | fast → INLINE; full → SUBAGENTS when feasible | **No gate; same at both paces** except the standalone-micro fast-polish scope below |
| **Sentence checks** | All sentences — main agent or sentence Tasks | **Changed sentences only** — sentence verifier Tasks |
| **Narrative + math** | Main agent on full passage | Verifier Tasks on **full passage**; math Task skipped when `edit_gate: polish` + `pace: fast` + `caller: micro` and no equations ([fast-polish.md](fast-polish.md)) |
| **Who decides done** | Main agent (informs step 5) | **Verifier synthesizer** — sole `OVERALL` authority |
| **CHECKS / hook** | No | Required; hook enforces |

---

## Phase 1 — source verify (step 4)

**When:** Edit gate Q2 = polish. **Skipped** on major rewrite.

**Purpose:** Audit source before editing — notation, scope, issues to fix in step 5.

```
1. Read the pace confirmed in the single editing intake
2. Emit Task plan (`INLINE` at fast pace; N labels at full pace, N≥2)
3. Sentence-level — fast: producer runs all 13 checks INLINE; full: SUBAGENTS
   (**N Tasks**, one per label)
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
1. Confirm the single intake resolved the verifier model profile
2. Identify changed sentences → see phase2-verify-subagents.md § Changed sentences
3. Emit Task plan (phase2_sentence_tasks = changed labels only)
4. Launch verifier Tasks (only after steps 1–3):
     • narrative — always, full passage (+ Step 0 compliance)
     • math — full passage when applicable (+ Step 0 compliance); skipped on
       `edit_gate: polish` + `pace: fast` + `caller: micro` with no equations
       ([fast-polish.md](fast-polish.md) § 1)
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
- Single editing intake before any editing Task; rewrite does not waive it.
- Never auto-select model slugs; skill recommendations require user confirmation via `AskQuestion`.
- Never skip Phase 2 because Phase 1 ran.
- Never end the turn without synthesizer `OVERALL: PASS`.
- Never ship when `compliance_orchestrator_plan: FAIL` or `compliance_worker_reports: FAIL` in CHECKS.
- After any Phase 2 draft fix, relaunch the verifier suite (new Tasks): narrative + math on full passage; sentence Tasks only for sentences changed in that fix pass.
- Pace changes Phase 1 routing, and — only on `edit_gate: polish` + `caller: micro` — narrows the Phase 2 narrative/math question and may skip the math Task when there is no equation ([fast-polish.md](fast-polish.md)). It never skips the synthesizer, never skips a changed sentence's Task, and never applies this exception to macro chunks or full pace.
