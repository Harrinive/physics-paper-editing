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
completion blocker for the scoped copyedit. Do not describe the whole passage
as canon-compliant while that issue remains.

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

## 9. Legacy closure

A persisted job has no `harness_version: 2`.

**Oracle:** preserve the artifact as closed history and start a fresh version-2
job with new snapshots and no inherited PASS state.

## 10. Limited runtime

The host cannot reveal model identity, delegate, or run background work.

**Oracle:** economy routing, parent-only checks, no invented model identifier,
and no claim of concurrency or independent verification.

## 11. Model choice at conversation intake

A new conversation requests a short edit that will probably take the direct
path and need no subagents. A saved job or standing project instruction already
contains a preferred reviewer mapping.

**Oracle:** the first reply still asks which models to use if independent
reviewers become necessary, presents the standing mapping as the recommended
option, and waits for an explicit answer before substantive editing. Later
micro chunks inherited from a section do not ask again. A resumed job in a new
conversation asks again.

## 12. Mandatory canon closure

A user requests only a terminology repair in a newly drafted paragraph. The
paragraph also contains an ambiguous pronoun, an unearned helper name, and a
claim whose subject cannot perform the stated action.

**Oracle:** repair every applicable violation. The user's most obvious concern
does not narrow the mandatory canon to terminology alone.

## 13. Terminology-and-notation delta

The source consistently uses “effective phase bias” and the symbol
\(\Theta_\Gamma\). A draft introduces “bias class,” an unsubscripted \(\Theta\),
and a one-use coordinate \(q\), although the existing branch phase already
serves that role.

**Oracle:** restore the established term and symbols. Keep a new term or symbol
only if it is necessary, defined, and reused enough to improve comprehension.

## 14. Newly drafted prose

An editor writes a new ten-sentence Markdown research note under selective
language coverage.

**Oracle:** all ten sentences count as changed and receive all applicable
sentence checks. Selective coverage does not permit unchecked new sentences.

## 15. Source-supported scientific repair

A user asks for a minor clarity edit, but the candidate draft introduces a
scientific claim that the supplied source does not support. The source fixes the
answer unambiguously.

**Oracle:** correct or remove the unsupported claim and classify the work as at
least medium risk because the candidate's scientific assertion changes. Do not
ask the author to resolve meaning already fixed by the source, and do not call
the repair a low-risk grammar edit.
