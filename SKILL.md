---
name: physics-paper-editing
description: >-
  Physics-first, capability-adaptive editing for LaTeX physics passages of at
  most 12 sentences. Routes low-risk work directly, gives economy models a
  structured scaffold, and adds independent physics or math review only when
  the scientific risk warrants it. Canon is physics-paper-principles; longer
  passages use physics-paper-editing-section.
---

# Physics paper editing

Edit one passage of at most 12 typographic sentences. Use
**`physics-paper-principles`** as the prose canon. Route a whole section or a
longer passage to **`physics-paper-editing-section`**.

The default harness is version 2. Existing jobs without `harness_version: 2`
resume through [legacy-v1/LEGACY.md](legacy-v1/LEGACY.md); never migrate a live
version-1 job mid-round.

## Read order

1. Read [adaptive-routing.md](adaptive-routing.md) and select the path.
2. Read [quality-contract.md](quality-contract.md).
3. Read only the canon layers triggered by the passage:
   [sentence.md](../physics-paper-principles/sentence.md),
   [narrative.md](../physics-paper-principles/narrative.md),
   [math.md](../physics-paper-principles/math.md), and
   [physical-lead.md](../physics-paper-principles/physical-lead.md).
4. Read [scaffolded-mode.md](scaffolded-mode.md) only for an economy editor.
5. Read [review-prompts.md](review-prompts.md) only when launching an
   independent reviewer.
6. Read [runtime-contract.md](runtime-contract.md) only when model selection,
   delegation, persistence, or a runtime fallback is needed.
7. Before any user-facing reply, read
   [user-communication.md](user-communication.md).

Direct edits do not load scaffolded, review, persistence, or legacy material.

## Core procedure

1. Count sentences and determine `edit_intent`, model tier, and scientific risk.
2. If essential scientific meaning is unresolved, ask the author the specific
   question; do not delegate the ambiguity.
3. Build a short private physics spine. Audit every new or changed
   story-bearing object before drafting.
4. Draft the edit. For substantive work, a correct formula does not excuse a
   poor object choice, unearned helper, or pointless normalization.
5. Run the path selected by [adaptive-routing.md](adaptive-routing.md).
6. Apply clear fixes. A required axis marked `FIX` must be repaired and
   rechecked; `USER_DECISION` goes to the author.
7. Return the edited text and only the decisions or limitations that matter.

## Path summary

| Path | Use | Process |
|---|---|---|
| `direct` | Low risk | One editor; compact self-check; no workers or job state |
| `guided` | Ordinary substantive work | Editor plus one holistic reviewer; math reviewer only when triggered |
| `independent` | High risk | Holistic and applicable math review; adjudicator only on conflict |
| `legacy_full` | Explicit compatibility or live v1 job | [legacy-v1/LEGACY.md](legacy-v1/LEGACY.md) |

No version-2 path launches one worker per sentence or requires a synthesizer for
every edit. Sentence-level help is permitted only for a specific local repair
already diagnosed by the editor or holistic reviewer.

## Model choice before delegation

For each new top-level edit that needs subagents, ask the user which models to
use before the first launch. Offer the recommended role-to-model choices (with
actual model names and reasoning effort when available), parent-model
inheritance, and a custom choice. Wait for an explicit answer; a displayed
default, silence, or an adapter-resolved tier is not a choice. Reuse the answer
for this job's review rounds and for chunks inherited from a section session.
See [runtime-contract.md](runtime-contract.md) for the profile and fallback.

## Persistence

Ordinary synchronous short edits create no marks, snapshots, or `.physics-edit`
state. Use [job-state.md](job-state.md) only for asynchronous, concurrent,
resumable, or file-based work where frozen-source comparison is genuinely
needed. Persist the version-2 routing and quality state defined in
[runtime-contract.md](runtime-contract.md).

## User constraints

If the user prohibits subagents, do not launch them. Use the strongest available
editor for the required checks, record `verification_independence: self_only`,
and do not imply that review was independent.

## Completion

Use the quality axes and deterministic completion rule in
[quality-contract.md](quality-contract.md). Shape the user-facing reply with
[user-communication.md](user-communication.md). Do not emit a legacy `OVERALL`
status for a version-2 job.

## Related skills

- **physics-paper-principles** — drafting and review canon
- **physics-paper-editing-section** — whole sections or passages over 12 sentences

## Validation fixtures

Not part of ordinary edit routing. Use when checking portability or retiring
legacy behavior:

| File | Role |
|---|---|
| [portability-test-matrix.md](portability-test-matrix.md) | Host/behavior scenarios for version 2 |
| [semantic-fixtures.md](semantic-fixtures.md) | Physics-decision oracles (grade substance, not wording) |

## Out of scope

- Inventing physical meaning, hypotheses, or an operational equivalence
- Running the version-1 worker fan-out for a new version-2 edit
- Treating algebraic validity as proof that a definition belongs in the story
