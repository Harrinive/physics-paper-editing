---
name: physics-paper-editing
description: >-
  Physics-first, capability-adaptive editing for physics passages in LaTeX,
  Markdown, or plain text of at most 12 sentences. Routes low-risk work
  directly, gives economy models a structured scaffold, and adds independent
  physics or math review only when scientific risk warrants it. Canon is
  physics-paper-principles; longer passages use physics-paper-editing-section.
---

# Physics paper editing

Edit one physics passage in LaTeX, Markdown, or plain text of at most 12
typographic sentences. Use
**`physics-paper-principles`** as the prose canon. Route a whole section or a
longer passage to **`physics-paper-editing-section`**.

The harness is version 2. Legacy/version-1 jobs are closed historical records:
never resume them or reuse their PASS state. A repeated edit starts a fresh
version-2 job or inherits a fresh version-2 section round.

## Read order

1. Read [adaptive-routing.md](adaptive-routing.md) and select the path.
2. Read [quality-contract.md](quality-contract.md).
3. Read [language-coverage.md](language-coverage.md) when a section supplies a
   coverage mode or the user requests a language audit.
4. Read only the canon layers triggered by the passage:
   [sentence.md](../physics-paper-principles/sentence.md),
   [narrative.md](../physics-paper-principles/narrative.md),
   [math.md](../physics-paper-principles/math.md), and
   [physical-lead.md](../physics-paper-principles/physical-lead.md).
5. Read [scaffolded-mode.md](scaffolded-mode.md) only for an economy editor.
6. Read [review-prompts.md](review-prompts.md) only when launching an
   independent reviewer.
7. For a top-level edit, read [runtime-contract.md](runtime-contract.md) before
   the first reply so the conversation-level model choice is collected at
   intake. A chunk invoked by the section skill inherits that choice.
8. Before any user-facing reply, read
   [user-communication.md](user-communication.md).

Direct edits do not load scaffolded or independent-review material. They load
coverage or persistence instructions only when an inherited coverage contract
or resumable file edit requires them. Legacy material is historical only.

## Core procedure

1. Count sentences and determine `edit_intent`, language coverage, model tier,
   and scientific risk.
2. If essential scientific meaning is unresolved, ask the author the specific
   question; do not delegate the ambiguity.
3. Build a short private physics spine. Audit every new or changed
   story-bearing object before drafting.
4. Draft the edit. For substantive work, a correct formula does not excuse a
   poor object choice, unearned helper, or pointless normalization.
5. Run the path selected by [adaptive-routing.md](adaptive-routing.md). Every
   path includes canon closure on the completed draft: check all sentence
   principles on every changed or newly written sentence, all applicable
   passage-level principles, every required math check, and every triggered
   story-bearing-object check.
6. Apply the declared checks in [language-coverage.md](language-coverage.md).
   Coverage selects sentences, not principles.
7. Apply clear fixes. A required axis marked `FIX` must be repaired and
   rechecked; `USER_DECISION` goes to the author.
8. Return the edited text and only the decisions or limitations that matter.

## Path summary

| Path | Use | Process |
|---|---|---|
| `direct` | Low risk | One editor; full canon self-check; no workers or job state |
| `guided` | Ordinary substantive work | Editor plus one holistic reviewer; math reviewer only when triggered |
| `independent` | High risk | Holistic and applicable math review; adjudicator only on conflict |

No version-2 path launches one worker per sentence or requires a synthesizer for
every edit. Exhaustive language coverage uses one editor or language reviewer
for the whole chunk and records a verdict for each sentence.

The paths change scaffolding, reviewer independence, and persisted evidence;
they do not change which applicable canon principles are mandatory. “Direct”
means less orchestration, not reduced quality coverage.

## Model choice at conversation intake

In the first user-facing reply of every new conversation that invokes this
skill as a top-level editor, ask which models to use if subagents are needed.
Ask before substantive editing, even when the passage may later take a direct
path and use no subagents. Offer the recommended role-to-model choices (with
actual model names and reasoning effort when available), parent-model
inheritance, and a custom choice. A standing preference may supply the
recommended option, but it does not replace the intake question. Wait for an
explicit answer; a displayed default, silence, or an adapter-resolved tier is
not a choice. Reuse the answer throughout that conversation unless the user
changes it. A micro chunk invoked by an active section edit inherits the
section's conversation-level answer and does not ask again. See
[runtime-contract.md](runtime-contract.md) for the profile and fallback.

## Persistence

Ordinary synchronous short edits create no marks, snapshots, or `.physics-edit`
state. Use [job-state.md](job-state.md) only for asynchronous, concurrent,
resumable, file-based, or exhaustive-audit work where frozen-source comparison
is needed. Persist the version-2 routing, coverage, snapshot, and quality state
defined in [runtime-contract.md](runtime-contract.md).

## User constraints

If the user prohibits subagents, do not launch them. Use the strongest available
editor for the required checks, record `verification_independence: self_only`,
and do not imply that review was independent.

## Completion

Use the quality axes and deterministic completion rule in
[quality-contract.md](quality-contract.md). Shape the user-facing reply with
[user-communication.md](user-communication.md). Do not emit a legacy `OVERALL`
status for a version-2 job. No path may complete while an applicable canon
principle fails within the required edit scope. A scoped copyedit may finish
with an untouched, out-of-scope pre-existing violation only when it is reported
as a limitation; that result is not a claim that the whole passage passes the
canon.

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
- Resuming or reactivating a legacy/version-1 job
- Treating algebraic validity as proof that a definition belongs in the story
