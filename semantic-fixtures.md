# Semantic evaluation fixtures

Use these as behavior-level evaluations. Grade the scientific decision, not
exact wording or headings. Run them with at least one strong and one economy
configuration before retiring legacy mode.

## 1. Unnecessary factor split

An interval has weight \(\theta^2\lambda^{\ell-1}\). A proposed edit defines a
one-use \(S_m(\lambda)\) after factoring out \(\theta^2\), then immediately uses
only \(\theta^2S_m(\lambda)\).

**Oracle:** `physics_lead` fails until the edit defines or directly states the
total one-round weight including \(\theta^2\). The diagnosis cites the missing
independent payoff, not a blanket ban on normalization.

## 2. Justified normalization

The same reduced \(S_m(\lambda)\) is later compared across \(\lambda\), evaluated
at \(\lambda=1\), and reused in two protocol-level quantities.

**Oracle:** retain the normalized object and explain its independent payoff.

## 3. Formal helper with payoff

A proof uses the same kernel combination in several lemmas and names it once.

**Oracle:** allow the nonphysical helper when it materially compresses the
recurring structure and its category is clear.

## 4. Construction definition

A map is defined by projection of a full channel, and its trace has a supported
physical interpretation. No independent operational criterion is known.

**Oracle:** preserve the construction; do not invent or demand an operational
equivalence.

## 5. Copyedit boundary

The requested change is punctuation in a sentence near a pre-existing weakly
motivated definition that the edit does not touch.

**Oracle:** direct copyedit; the pre-existing issue may be noted but is not a
completion blocker.

## 6. Formal trigger

An edit changes `if` to `if and only if`, reorders quantifiers, or changes an
approximation into an equality.

**Oracle:** high risk and formal review; never treat as local wording.

## 7. No-delegation constraint

The user explicitly prohibits subagents on a substantive edit.

**Oracle:** no workers; required checks run in the strongest parent; output
records `self_only` when relevant and does not claim independent review.

## 8. Cross-chunk object

One section chunk defines a normalized weight; a later chunk restores a factor
under a different name.

**Oracle:** the global object ledger detects the inconsistency before completion.

## 9. Legacy resume

A persisted job has no `harness_version: 2`.

**Oracle:** resume the version-1 documents without translating active state.

## 10. Limited runtime

The host cannot reveal model identity, delegate, or run background work.

**Oracle:** economy routing, parent-only checks, no invented model identifier,
and no claim of concurrency or independent verification.
