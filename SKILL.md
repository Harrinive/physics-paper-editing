---
name: physics-paper-editing
description: >-
  Physics-first editing for physics passages in LaTeX, Markdown, or plain text
  of at most 12 sentences. Uses a direct path for exactly bounded low-risk work
  and a reviewed path with mandatory sentence and terminology-and-notation
  review plus
  content-triggered specialists. Canon is physics-paper-principles; longer
  passages and whole sections use physics-paper-editing-section.
---

# Physics paper editing

Edit one non-section physics passage in LaTeX, Markdown, or plain text of at
most 12 typographic sentences. Use
**`physics-paper-principles`** as the prose canon. Route a whole section or a
longer passage to **`physics-paper-editing-section`**.

The harness is version 2. Legacy/version-1 jobs are closed historical records:
never resume them or reuse their PASS state. A repeated edit starts a fresh
version-2 job or inherits a fresh version-2 section round.

## Read order

1. Read [adaptive-routing.md](adaptive-routing.md) and select the path.
2. Read [quality-contract.md](quality-contract.md).
3. Read [language-coverage.md](language-coverage.md) for every edit.
4. Always read [sentence.md](../physics-paper-principles/sentence.md). Read the
   other canon layers when their content is present:
   [narrative.md](../physics-paper-principles/narrative.md),
   [math.md](../physics-paper-principles/math.md), and
   [physical-lead.md](../physics-paper-principles/physical-lead.md).
5. Read [scaffolded-mode.md](scaffolded-mode.md) only for an economy editor.
6. Read [review-prompts.md](review-prompts.md) only for `reviewed` work.
7. For a top-level edit, read [runtime-contract.md](runtime-contract.md) before
   the first reply, then read the selected host adapter before resolving models
   or launching reviewers. A chunk invoked by the section skill inherits the
   active role-to-model policy.
8. Before any user-facing reply, read
   [user-communication.md](user-communication.md).

Direct edits do not load review prompts. Economy or unknown editors still load
the scaffold, including on direct work. Persistence instructions apply when
the work lifecycle requires them, independently of path. Legacy material is
historical only.

## Core procedure

1. Count sentences and determine `edit_intent`, language coverage, model tier,
   scientific risk, and `direct | reviewed` path.
2. If a scientific defect in the author's source is newly discovered and its
   repair is not already authorized, pause the entire task and ask the author
   one focused question. Do not continue unrelated edits. Repair defects
   introduced by the candidate without treating them as author decisions.
3. Build a short private physics spine, terminology-and-notation baseline, and
   any required object ledger before drafting.
4. Draft the edit. For substantive work, a correct formula does not excuse a
   poor object choice, unearned helper, or pointless normalization.
5. Run the path selected by [adaptive-routing.md](adaptive-routing.md). Every
   path includes canon closure on the completed draft: check all sentence
   principles on every sentence in the declared coverage, resolve every
   terminology-and-notation delta item, and run all applicable narrative,
   formal, and story-bearing-object checks.
6. Apply the declared checks in [language-coverage.md](language-coverage.md).
   Coverage selects sentences, not principles.
7. Under `reviewed`, run the mandatory sentence and terminology-and-notation
   reviewers, every triggered principle specialist, the holistic reviewer, and
   the applicable formal review. Integrate findings without allowing reviewers
   to write the live manuscript or file.
8. Apply clear candidate fixes and recheck affected axes. `USER_DECISION`
   pauses the task and goes to the author.
9. Return the edited text and only the decisions that matter.

## Path summary

| Path | Use | Process |
|---|---|---|
| `direct` | Exactly bounded low risk | One editor; full canon and terminology self-check; no reviewer |
| `reviewed` | Substantive work, terminology/language audit, specialist trigger, or high scientific risk | Sentence and terminology-and-notation review, principle specialists on hits, holistic review, scoped formal review, and adjudication only for scientific conflict |

No version-2 path launches one reviewer per sentence. One sentence reviewer
checks the whole declared coverage; one terminology-and-notation reviewer
checks the whole edited unit. A principle hit launches a whole-unit specialist
rather than a reviewer for the seed sentence.

The paths change reviewer independence, not which applicable canon principles
are mandatory. Persistence depends on lifecycle and evidence needs rather than
path.

## Model choice at conversation intake

At the start of a top-level editing conversation, look first for a standing
project or conversation role-to-model policy. If one exists, tell the user
which model mapping will be used and continue without asking for confirmation.
If none exists, ask which models to use if reviewers are needed and wait for an
answer before substantive editing. Reuse the active mapping unless the user
changes it. A micro chunk invoked by an active section edit inherits the
section's mapping and does not ask again. See
[runtime-contract.md](runtime-contract.md).

## Persistence

Ordinary synchronous short edits create no marks, snapshots, or `.physics-edit`
state, regardless of path. Use [job-state.md](job-state.md) for asynchronous,
concurrent, resumable, file-based, or exhaustive-audit work where frozen-source
comparison is needed. Persist the immutable original source, current candidate,
routing, coverage, dependency revisions, and quality state defined in
[runtime-contract.md](runtime-contract.md).

## User constraints

If the user prohibits subagents, do not launch them. Use the strongest available
editor for the required checks, record `verification_independence: self_only`,
and do not imply that review was independent.

## Completion

Use the quality axes and deterministic completion rule in
[quality-contract.md](quality-contract.md). Shape the user-facing reply with
[user-communication.md](user-communication.md). Do not emit a legacy `OVERALL`
status for a version-2 job. No path may complete while an applicable canon
principle or required quality axis fails. A newly discovered scientific defect
in the author's source pauses the entire task unless its repair was already
authorized; it cannot be converted into a completion-time limitation.

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
