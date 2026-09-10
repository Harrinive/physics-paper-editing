# Background output verify

**For agents:** Start with [SKILL.md](SKILL.md) § Agent read order. **Read with the Read tool** before launching checkers or closing a round ([coworker-loop.md](coworker-loop.md)).

Required for **every** micro edit — standalone or macro chunk. Checkers grade a **frozen snapshot** against **`physics-paper-principles`**. The live `.tex` is already written.

Also read: [severity.md](severity.md) · [sentence-check-subagents.md](sentence-check-subagents.md) · [compliance-monitoring.md](compliance-monitoring.md) · [job-state.md](job-state.md). When `edit_gate: polish` + `pace: fast` + `caller: micro`: also [fast-polish.md](fast-polish.md).

---

## At a glance

| Always run (full snapshot) | Run only on changed sentences |
|---------------------------|-------------------------------|
| Narrative verifier | Sentence verifiers (all 14 sentence principles each) |
| Math verifier (when math or logical argument — see footnote) | |
| Synthesizer (**after the round** — wave complete or interrupt harvest) | |

Footnote — **fast polish, standalone micro only:** skip the math Task only when [fast-polish.md](fast-polish.md) § 1's mechanical test finds nothing to launch.

- Fresh Tasks every wave — never resume old Tasks except `interrupt: true` to flush.
- **Producer** must not inline-check the draft or set `OVERALL`.
- **Synthesizer** is the sole authority for CHECKS and job-round `OVERALL` (`PASS` | `CONFLICTS` | `PARTIAL`).

---

## Roles

| Role | Who | May edit `.tex`? | May emit CHECKS / OVERALL? |
|------|-----|------------------|----------------------------|
| Producer | Main agent | Yes (draft, mark, merge) | **No** |
| Sentence verifiers | Background Tasks | No — append `findings.jsonl`; may suggest `Edited:` | No |
| Narrative verifier | Background Task | No — append jsonl | No |
| Math verifier | Background Task | No — append jsonl | No |
| Verifier synthesizer | Task after the round | No | **Yes** |

Use **`readonly: true`** and **`run_in_background: true`** on every verifier Task. Synthesizer may run in the foreground at round end.

---

## Changed sentences

Label **S1, S2, …** on the snapshot ([sentence-check-subagents.md](sentence-check-subagents.md) §2).

| Wave | Baseline | Compare to |
|------|----------|------------|
| First wave | User's source prose (after stripping `[bracket comments]`) | Marked draft |
| Rewrite | — | **Every** sentence is changed |
| Later wave | Previous snapshot | New snapshot after merge |

**Changed:** label exists in both, but text differs. **Unchanged:** no sentence Task. Narrative and math still get the full snapshot.

**Zero changed sentences:** skip sentence Tasks; still run narrative (+ math if applicable) and synthesizer.

---

## Model profile

**Do not launch verifier Tasks until slugs are resolved** — by inheritance or defaults, not by blocking AskQuestion every job ([gate.md](gate.md), [user-communication.md](user-communication.md)).

| Valid source | Action |
|--------------|--------|
| User already chose a profile for **this draft scope in this chat** | Reuse |
| Section `session.md` has `user_confirmed: true` | Inherit `{ sentence, deep, synth }` |
| Neither | Use recommended slugs below; mention once that they can change checkers |

**Recommended slugs** (defaults when nothing is inherited):

1. **Sentence** (fast tier) — Cursor Composer (fast) when available.
2. **Narrative & logic** (deep) — at `pace: full` or `rewrite`, a flagship high-reasoning model; at `pace: fast` + `polish`, a medium-effort flagship ([fast-polish.md](fast-polish.md) § 5).
3. **Synthesizer** (never fast tier) — same recommendation as (2).

If a recommended slug is not in the session list, pick the closest available flagship in that tier and say so once.

### Per-Task model assignment

| Task | Tier | Slug |
|------|------|------|
| Sentence verifiers | Fast | sentence |
| Narrative / math | Deep | deep |
| Synthesizer | Deep | synth |

---

## Workflow

```
1. Models resolved (inherit or defaults)
2. Passage summary → every verifier prompt
3. Label S1…SN; mark changed labels
4. Emit Task plan (findings_path + phase2_sentence_tasks = changed labels)
5. Launch in parallel, run_in_background: true:
     • narrative — full snapshot
     • math — when applicable
     • sentence — one Task per changed label
   Write agents.json
6. End the turn (verify:running)
7. At round end (all done or interrupt harvest):
     • harvest findings.jsonl
     • launch synthesizer with reports + harvest tags
     • producer applies merge-policy.md
```

**Task count:** narrative + math (0 if skipped) + **C** sentence Tasks. Synthesizer is extra, at round end. Mode line **M** = C.

---

## Producer rules

**Allowed:** track changed sentences; apply merge-policy; interrupt + harvest; relaunch open/dirty labels.

**Forbidden:**

- Waiting to write `.tex` until `OVERALL: PASS`
- Writing a construction-only definition of a named physical object (definition halt — ask first)
- Launching with `run_in_background: false` and blocking the user
- Auto-selecting a **new** profile when one can be inherited (defaults are OK if mentioned)
- Running principles inline on the draft or setting `OVERALL`
- Sentence Tasks for unchanged labels
- Batching ≤10 sentences in one Task
- Dropping `findings.jsonl` on interrupt

---

## Incremental flush (every worker)

As soon as a finding exists, **append one JSON line** to `findings_path` from the Task plan ([job-state.md](job-state.md)). Then a `done` line when that label (or narrative/math) is finished. Do not wait for the final chat report. Do not edit the `.tex`.

On `interrupt: true`: flush remaining lines, then stop.

---

## Verifier prompts

Keep `readonly: true` and `run_in_background: true`. Description must include the label (`background sentence: S2`).

### Sentence verifier

Same template as [sentence-check-subagents.md](sentence-check-subagents.md) §6. Target is the **snapshot sentence**, not the live file.

```text
Task(
  subagent_type: "generalPurpose",
  readonly: true,
  run_in_background: true,
  model: <sentence slug>,
  description: "background sentence: S<k>",
  prompt: <sentence-check-subagents.md §6>
)
```

### Narrative verifier

```text
Task(
  subagent_type: "generalPurpose",
  readonly: true,
  run_in_background: true,
  model: <deep slug>,
  description: "background narrative",
  prompt: <template below>
)
```

```text
You are a narrative verifier for a physics paper. You did NOT write this draft.

## Orchestrator task plan (verify in Step 0 — read-only)
<paste identical block — includes findings_path>

## Passage summary (shared)
<identical block>

## Snapshot under review (frozen — do not edit the live .tex)
<full snapshot>

## Adjacent context (if helpful)
<1–3 sentences before/after, or omit>

## User's original source (only when edit_gate: polish, pace: fast, caller: micro)
<the user's quoted source>

## Step 0 — Assignment compliance (run FIRST)
Confirm full snapshot + valid Task plan. See compliance-monitoring.md.

## Incremental ledger
Append each finding (and a final done line, label "narrative") to findings_path
as JSON lines the moment you have them. Do not edit the .tex.

## Instructions

**If `edit_gate: polish`, `pace: fast`, `caller: micro`:**
Read ../physics-paper-principles/narrative.md and physics-paper-editing/severity.md;
narrow classes 1–5 to what **this edit changed**
relative to "User's original source". Pre-existing defects are
`SUGGEST — pre-existing in source`. Apply the word-delta class in fast-polish.md § 2.
Do not Grep/Read beyond this prompt; use PACKET_GAP instead.

**Otherwise:** run narrative.md against the full manuscript context.
Closed BLOCKER list in severity.md; everything else is SUGGEST.

Do not edit the draft. Report each group in file order.

## Output format
### Assignment compliance
COMPLIANCE: PASS | FAIL
Role: narrative
Reason: <one line>

### Narrative verification
**Group 1 — Core message and framing:** <findings or PASS>
**Group 2 — Logical arc and motivation:** <findings or PASS>
**Group 3 — Consistency and economy:** <findings or PASS>
**Group 4 — Claims and audience:** <findings or PASS>

**BLOCKER items:** <class + check + one-line reason; or "none">
**SUGGEST items:** <or "none">
**PACKET_GAP:** <fast polish only; or "none">
```

### Math verifier

**Skip** when `edit_gate: polish`, `pace: fast`, `caller: micro`, and [fast-polish.md](fast-polish.md) § 1 finds nothing to launch. Record `phase2_math_task: skipped (no equations)`.

Otherwise:

```text
Task(
  subagent_type: "generalPurpose",
  readonly: true,
  run_in_background: true,
  model: <deep slug>,
  description: "background math",
  prompt: <template below>
)
```

```text
You are a math/logic verifier for a physics paper. You did NOT write this draft.

## Orchestrator task plan (verify in Step 0 — read-only)
<paste identical block>

## Passage summary (shared)
<identical block>

## Snapshot under review
<full snapshot>

## User's original source (only when edit_gate: polish, pace: fast, caller: micro)
<quoted source>

## Step 0 — Assignment compliance (run FIRST)
See compliance-monitoring.md § Math worker.

## Incremental ledger
Append findings and a done line (label "math") to findings_path immediately.
Do not edit the .tex.

## Instructions

**If fast polish scope:** narrow to what this edit changed; pre-existing → SUGGEST
except construction-as-definition / missing physical lead on an object this
quote introduces (fast-polish.md § 2); word-delta class from fast-polish.md § 2;
PACKET_GAP instead of searching. Still run physical-lead.md on any named
object the quote or draft introduces.

**Otherwise:** full math.md + physical-lead.md audit. Closed BLOCKER list in severity.md.
Named objects in the physical or protocol story: run physical lead.
Missing criterion is BLOCKER class 6 — report; do not invent the criterion.

If no math or logical argument: mark N/A — still complete the report and a done line.

## Output format
### Assignment compliance
COMPLIANCE: PASS | FAIL
Role: math
Reason: <one line>

### Math verification
**Step 0 — Classifications:** <or "no math statements">
**Per-statement / per-type findings:** <file order>
**BLOCKER items:** <or "none">
**SUGGEST items:** <or "none">
**PACKET_GAP:** <or "none">
```

### Verifier synthesizer (round end only)

```text
Task(
  subagent_type: "generalPurpose",
  readonly: true,
  model: <synth slug>,
  description: "round synthesizer",
  prompt: <template below>
)
```

```text
You are the verifier synthesizer. You did NOT write the draft. You set job-round OVERALL only.

## Passage summary (shared)
<identical block>

## Snapshot this round
<snapshot.tex>

## Live interior at harvest (may differ)
<current marked interior>

## Harvest tags
valid / stale / open per job-state.md — paste findings.jsonl summary

## Orchestrator task plan
<paste>

## Sentence scope
Total N. Changed: <list>. Skipped: <list>. C = sentence Tasks launched.

## Closed BLOCKER lists (do not open the principle files for this)

Use physics-paper-editing/severity.md. Paste:

Narrative (6): (1) contradiction or false relation, incl. unsupported connective;
(2) unbound essential object; (3) broken reasoning; (4) claim-strength mismatch;
(5) meaning loss or invention;
(6) construction-as-definition (when math did not already report it — never
auto-apply a guessed criterion). Else SUGGEST.

Math (6): (1) invalid or inconsistent mathematics; (2) undefined essential object;
(3) formula–prose mismatch; (4) unsupported logical strength; (5) incorrect import;
(6) construction-as-definition (named physical object introduced only by a
labeling/computation recipe — never auto-apply a guessed criterion).
Else SUGGEST.

Fast polish only: word-delta class in fast-polish.md § 2. Pre-existing in source → SUGGEST, except construction-as-definition on an object this quote introduces.

## Verifier reports
<paste worker reports and/or jsonl harvest; math may be "skipped — no equations">

## Instructions
1. Procedural compliance first (compliance-monitoring.md). Plan defects →
   compliance_* FAIL; do not treat that as a user-blocking ship gate.
2. Adjudicate BLOCKERs against the closed lists. Downgrade out-of-list items.
3. Apply merge-policy.md mentally: untouched + must-fix → not CONFLICTS;
   construction-as-definition / missing physical lead (math class 6) → always
   CONFLICTS (never auto-apply a guessed criterion);
   serious clash with live user text → CONFLICTS; open/stale-only wave → PARTIAL;
   else PASS.
4. SUGGEST and PACKET_GAP never set CONFLICTS by themselves.
5. Emit Mode + CHECKS. You are the only agent that may set OVERALL.

## Output format (final output — no extra commentary)
Mode: verify-subagents · verify:<partial|complete> · <N> sentences · <C> changed · <M> Tasks · sentence:<slug> · deep:<slug> · synth:<slug>

<!-- CHECKS
compliance_orchestrator_plan: PASS|FAIL
compliance_worker_reports: PASS|FAIL
sentence_S1: PASS|FAIL|skipped|open
...
narrative_group1: PASS|FAIL
math_step0: PASS|FAIL|N/A|N/A (skipped)
severity_downgrades: <count>
packet_gap: <count>
OVERALL: PASS|CONFLICTS|PARTIAL
-->

**Merge hints for producer:** <untouched must-fixes to apply / conflicts to report / none>
```

---

## After synthesizer returns

1. Copy `Mode:` and `<!-- CHECKS -->` into the **audit drawer** verbatim ([user-communication.md](user-communication.md)).
2. Apply [merge-policy.md](merge-policy.md) — one interior write, or unmark.
3. Do **not** silently loop until `PASS`. `CONFLICTS` → one user decision. `PARTIAL` → relaunch open/dirty labels in the background.
