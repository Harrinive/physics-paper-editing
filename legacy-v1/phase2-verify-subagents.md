# Frozen-snapshot verification

**For agents:** Start with [LEGACY.md](LEGACY.md) § Agent read order. **Read with the Read tool** before launching checkers or closing a round ([coworker-loop.md](coworker-loop.md)).

Required for **every** micro edit — standalone or macro chunk. Verifiers grade a **frozen snapshot** against **`physics-paper-principles`**. The live `.tex` is already written. Read [runtime-contract.md](runtime-contract.md) before delegation.

Also read: [severity.md](severity.md) · [sentence-check-subagents.md](sentence-check-subagents.md) · [compliance-monitoring.md](compliance-monitoring.md) · [job-state.md](job-state.md). When `edit_gate: polish` + `pace: fast` + `caller: micro`: also [fast-polish.md](fast-polish.md).

---

## At a glance

| Always run (full snapshot) | Run only on changed sentences |
|---------------------------|-------------------------------|
| Narrative verifier (artifact-first, then groups 1–4) | Sentence verifiers (artifact-first, then unresolved 1–15) |
| Math verifier (when math or logical argument — see footnote) | |
| Synthesizer (**after the round** — wave complete or interrupt harvest) | |

Footnote — **fast polish, standalone micro only:** skip math verification only when [fast-polish.md](fast-polish.md) § 1's mechanical test finds nothing to launch.

- Fresh verifier jobs every wave — never reuse an old review job; only request a flush from a still-running worker when the runtime supports it.
- **Producer** must not inline-check the draft or set `OVERALL`.
- **Synthesizer** is the sole authority for CHECKS and job-round `OVERALL` (`PASS` | `CONFLICTS` | `PARTIAL`).

---

## Roles

| Role | Who | May edit `.tex`? | May emit CHECKS / OVERALL? |
|------|-----|------------------|----------------------------|
| Producer | Main agent | Yes (draft, mark, merge) | **No** |
| Sentence verifiers | Independent subagents | No — write assigned result shards; may suggest `Edited:` | No |
| Narrative verifier | Independent subagent | No — write assigned result shard | No |
| Math verifier | Independent subagent | No — write assigned result shard | No |
| Verifier synthesizer | Subagent after the round | No | **Yes** |

Request enforced read-only access for every verifier. If the runtime cannot enforce it, state the restriction in the assignment and accept only the assigned result shard. Schedule verification asynchronously when supported; the synthesizer may run after a foreground wave.

---

## Changed sentences

Label **S1, S2, …** on the snapshot ([sentence-check-subagents.md](sentence-check-subagents.md) §2).

| Wave | Baseline | Compare to |
|------|----------|------------|
| First wave | User's source prose (after stripping `[bracket comments]`) | Marked draft |
| Rewrite | — | **Every** sentence is changed |
| Later wave | Previous snapshot | New snapshot after merge |

**Changed:** label exists in both, but text differs. **Unchanged:** no sentence verifier. Narrative and math still get the full snapshot.

**Zero changed sentences:** skip sentence verifiers; still run narrative (+ math if applicable) and synthesizer.

---

## Model profile

Resolve the profile once per top-level session through [runtime-contract.md](runtime-contract.md). Do not delegate until the profile is confirmed, inherited from a confirmed section session, or recorded through the no-interaction fallback.

| Role | Requested tier | Purpose |
|------|----------------|---------|
| Sentence verifier | `fast` | High-volume wording checks |
| Narrative / math | `capable` | Physics, logic, and structure |
| Synthesizer | `capable` | Independent adjudication |

The adapter records the resolved identifier, reasoning level when exposed, and a fallback or unknown value when it cannot resolve the requested tier. Never invent a model identifier.

---

## Workflow

```
1. Confirmed or inherited model profile resolved
2. Passage summary → every verifier prompt
3. Label S1…SN; mark changed labels
4. Emit worker plan (result paths + changed-label assignments)
5. Schedule in runtime-aware waves:
     • narrative — full snapshot
     • math — when applicable
     • sentence — one assignment per changed label when scope is ten or fewer
   Write agents.json
6. Return control when the runtime supports asynchronous workers; otherwise continue through foreground waves
7. At round end (all done or stale-result harvest):
     • harvest result shards
     • delegate synthesizer with reports + harvest tags
     • producer applies merge-policy.md
```

**Worker count:** narrative + math (0 if skipped) + **C** sentence assignments. Synthesizer is extra, at round end. Mode line **M** = C.

---

## Producer rules

**Allowed:** track changed sentences; apply merge-policy; interrupt + harvest; relaunch open/dirty labels.

**Forbidden:**

- Waiting to write `.tex` until `OVERALL: PASS`
- Inventing physical meaning or choosing between unresolved scientific alternatives (definition halt only when essential to faithful drafting)
- Withholding the written draft while a runtime runs foreground verification
- Replacing a confirmed or inherited profile without the user's choice
- Running principles inline on the draft or setting `OVERALL`
- Sentence verifiers for unchanged labels
- Batching ≤10 sentences in one assignment
- Dropping result shards after a stop request

---

## Incremental result write (every worker)

As soon as a finding exists, **append one enveloped JSON record** to the worker's `result_path` from the worker plan ([job-state.md](job-state.md)). Finish with the terminal completion record. Do not wait for the final report. Do not edit the `.tex`.

On a supported stop request: flush remaining lines, then stop.

---

## Verifier prompts

Use the selected adapter to launch these assignments. Every assignment must name its role and labels, request read-only behavior, include the worker plan, and write only to its own `result_path`.

### Sentence verifier

Same template as [sentence-check-subagents.md](sentence-check-subagents.md) §6. Target is the **snapshot sentence**, not the live file.

```text
role: sentence
labels: [S<k>]
model_role: sentence
write_policy: result-shard-only
completion: asynchronous-when-supported
prompt: sentence-check-subagents.md §6
```

### Narrative verifier

```text
role: narrative
labels: [full-passage]
model_role: deep
write_policy: result-shard-only
completion: asynchronous-when-supported
prompt: template below
```

```text
You are a narrative verifier for a physics paper. You did NOT write this draft.

## Worker plan (verify in Step 0 — read-only)
<paste identical block — includes this worker's result_path>

## Passage summary (shared)
<identical block>

## Snapshot under review (frozen — do not edit the live .tex)
<full snapshot>

## Adjacent context (if helpful)
<1–3 sentences before/after, or omit>

## User's original source (only when edit_gate: polish, pace: fast, caller: micro)
<the user's quoted source>

## Step 0 — Assignment compliance (run FIRST)
Confirm full snapshot + valid worker plan. See compliance-monitoring.md.

## Incremental ledger
Append each finding and a terminal completion record (label "narrative") to result_path
as JSON lines the moment you have them. Do not edit the .tex.

## Instructions

Read ../../physics-paper-principles/legacy-v1/narrative.md (Detect lines) and
physics-paper-editing/severity.md. Do **not** walk groups 1–4 as the
primary loop. Run the workflow below. Fast polish does not skip Diagnostics.

**If `edit_gate: polish`, `pace: fast`, `caller: micro`:**
narrow classes 1–5 to what **this edit changed**
relative to "User's original source". Pre-existing defects are
`SUGGEST — pre-existing in source`. Apply the word-delta class in fast-polish.md § 2.
Do not Grep/Read beyond this prompt; use PACKET_GAP instead.

**Otherwise:** full manuscript context. Closed BLOCKER list in severity.md;
everything else is SUGGEST.

Do not edit the draft.

## Workflow
1. Produce artifacts (do not write a weakness until the artifact exists).
2. Under each artifact, check only the listed bullets.
3. Then fill **Group 1–4**.

### Artifacts → groups
**Reverse outline** (one phrase per sentence)
  Then: G1 central / novelty roles; G2 motivation, prose-vs-math, ordering; G3 economy
**Because-chain** (S_n because S_{n-1}, or named gap)
  Then: G2 logical arc; G2 signposting (connectives licensed by the chain)
**Takeaway** (one sentence, no hedge stacks)
  Then: G1 central message, G1 framing
**CARS tags** (territory | niche:<type> | occupy | N/A)
  Then: G2 motivation
**Connective inventory**
  Then: G2 signposting
**CRE + strength words**
  Then: G4 scope
**Entry-point list**
  Then: G4 audience
**Promise / payoff**
  Then: G3 consistency
**Physical meaning and definition choice** (role, category, operational option, chosen name/form)
  Then: G2 physical lead
**Speech-act**
  Then: G2 model setup

Empty Diagnostics field → incomplete homework (synthesizer: this role open /
OVERALL PARTIAL).

## Output format
### Assignment compliance
COMPLIANCE: PASS | FAIL
Role: narrative
Reason: <one line>

### Narrative verification
**Diagnostics** (required):
- Reverse outline: <one phrase per sentence>
- Because-chain: <or named gap>
- Takeaway: <one sentence>
- CARS tags: territory | niche:<type> | occupy | N/A
- Connective inventory: <word → licensed by chain? yes/no; or none>
- CRE + strength words: <claim / reason / evidence; strength list or none>
- Entry-point list: <or none>
- Promise / payoff: <or none>
- Physical meaning and definition choice: <role; category; operational option; chosen name/form and reason, or N/A>
- Speech-act: setup | hypothesis | proof-strategy | N/A

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
role: math
labels: [full-passage]
model_role: deep
write_policy: result-shard-only
completion: asynchronous-when-supported
prompt: template below
```

```text
You are a math/logic verifier for a physics paper. You did NOT write this draft.

## Worker plan (verify in Step 0 — read-only)
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
Append findings and a terminal completion record (label "math") to result_path immediately.
Do not edit the .tex.

## Instructions

Read ../../physics-paper-principles/legacy-v1/math.md (Required products) and
physical-lead.md. Do **not** walk type-check lists as the primary loop.
Run the workflow below. Fast polish does not skip Diagnostics.

**If fast polish scope:** narrow to what this edit changed; pre-existing → SUGGEST
except unresolved physical meaning (class 6) on an object this
quote introduces (fast-polish.md § 2); word-delta class from fast-polish.md § 2;
PACKET_GAP instead of searching. Still run physical-lead.md on any named
object the quote or draft introduces.

**Otherwise:** full math.md + physical-lead.md audit. Closed BLOCKER list in severity.md.
Named objects in the physical or protocol story: run physical lead.
Use severity.md class 6 only for unresolved essential scientific ambiguity.
A valid construction or missing operational criterion alone is not a BLOCKER;
thin motivation is SUGGEST. Do not invent physical meaning.

If no math or logical argument: mark N/A — still complete Diagnostics as N/A,
the report, and a terminal completion record.

## Workflow (per statement)
1. Classify type (Step 0).
2. Produce only the artifacts that type needs.
3. Under each artifact, run the listed checks.
4. Then fill **Per-statement / per-type findings**.

### Artifacts → checks
**Type tag** — all statements
**Implication arrow + leap words + where hypotheses are used**
  Then: Type 1 completeness, direction, implicit assumptions
**Independent formalization** (exact prose characterization, then compare; motivation-only → N/A)
  Then: Type 2 round-trip, back-translation, formula–prose mismatch
**Excluded pathology** (or intended use / N/A when no exclusion is claimed)
  Then: Type 2 negative-space, first-use
**Physical meaning and definition choice** (role, category, operational option, chosen name/form)
  Then: physical lead, Type 2 physical-lead / layering
**Approximation ledger** (retained and discarded content; mechanism and regime; probability/bound scope; claim strength)
  Then: approximation claims
**Import: quoted hypotheses vs used; status; theorem/page**
  Then: Type 3
**WLOG-reason** (symmetry named | unjustified)
  Then: Type 4

Empty Diagnostics field → incomplete homework (synthesizer: this role open /
OVERALL PARTIAL).

## Output format
### Assignment compliance
COMPLIANCE: PASS | FAIL
Role: math
Reason: <one line>

### Math verification
**Step 0 — Classifications:** <or "no math statements">
**Diagnostics** (per statement; required):
- Type tag:
- Implication arrow + leap words + where hypotheses are used: P⇒Q | Q⇒P | iff | N/A; <leap/hyp-use or N/A>
- Independent formalization: <exact prose characterization, or N/A with reason>
- Excluded pathology: <or intended use / N/A with reason>
- Physical meaning and definition choice: <role; category; operational option; chosen name/form and reason; any unresolved scientific choice | N/A>
- Approximation ledger: <or N/A with reason>
- Import: quoted hypotheses vs used; status; theorem/page | N/A
- WLOG-reason: <symmetry named | unjustified | N/A>
**Per-statement / per-type findings:** <file order>
**BLOCKER items:** <or "none">
**SUGGEST items:** <or "none">
**PACKET_GAP:** <or "none">
```

### Verifier synthesizer (round end only)

```text
role: synthesizer
labels: [round]
model_role: synth
write_policy: no-source-edits
completion: after-verifier-harvest
prompt: template below
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
valid / stale / open per job-state.md — paste the deterministic result-shard summary

## Worker plan
<paste>

## Sentence scope
Total N. Changed: <list>. Skipped: <list>. C = sentence verifier assignments launched.

## Closed BLOCKER lists (do not open the principle files for this)

Use physics-paper-editing/severity.md. Paste:

Narrative (6): (1) contradiction or false relation, incl. unsupported connective;
(2) unbound essential object; (3) broken reasoning; (4) claim-strength mismatch;
(5) meaning loss or invention;
(6) unresolved physical meaning (essential scientific choice needed to define
the object; when math did not already report it — never guess). Else SUGGEST.

Math (6): (1) invalid or inconsistent mathematics; (2) undefined essential object;
(3) formula–prose mismatch; (4) unsupported logical strength; (5) incorrect import;
(6) unresolved physical meaning (essential scientific choice needed to define
the object cannot be settled from supplied context — never guess).
A construction, thin motivation, or missing operational criterion alone is not
class 6. Else SUGGEST.

Fast polish only: word-delta class in fast-polish.md § 2. Pre-existing in source → SUGGEST, except unresolved physical meaning (class 6) on an object this quote introduces.

## Verifier reports
<paste worker reports and/or result-shard harvest; math may be "skipped — no equations">

## Instructions
1. Procedural compliance first (compliance-monitoring.md). Plan defects →
   compliance_* FAIL; do not treat that as a user-blocking ship gate.
2. Missing or empty **Diagnostics** on a worker report → that role is `open`;
   OVERALL: PARTIAL. This is incomplete homework, not a user-text CONFLICTS.
   Do not add it to the closed BLOCKER lists.
3. Adjudicate BLOCKERs against the closed lists. Downgrade out-of-list items.
4. Apply merge-policy.md mentally: untouched + must-fix → not CONFLICTS;
   unresolved physical meaning (math/narrative class 6) →
   CONFLICTS (never invent the scientific choice);
   serious clash with live user text → CONFLICTS; open/stale-only wave → PARTIAL;
   else PASS.
5. SUGGEST and PACKET_GAP never set CONFLICTS by themselves.
6. Emit Mode + CHECKS. You are the only agent that may set OVERALL.

## Output format (final output — no extra commentary)
Mode: verify-subagents · verify:<partial|complete> · <N> sentences · <C> changed · <M> verifier assignments · profile:<accepted_default|custom|inherit|fallback>

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
3. Do **not** silently loop until `PASS`. `CONFLICTS` → one user decision. `PARTIAL` → reschedule open or dirty labels through the selected runtime.
