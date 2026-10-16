# Scoped re-review

A repair changes a few sentences. Re-reviewing the whole unit after every
repair draws a new set of findings on text that did not change, and with
stochastic reviewers the loop does not settle. Review a repair where it was
made, and review the whole unit once, at its close.

## Rules

1. **First review: full scope.** The first review of a drafted unit covers
   every sentence of the declared coverage.
2. **After a repair: touched scope.** The touched set is every sentence whose
   text changed, the sentence directly after each changed sentence (an
   antecedent such as "this probability" lives in the sentence before it), and
   every sentence of a split, merged, or moved passage. A verdict on any other
   sentence stays current while that sentence and its predecessor are
   unchanged. A context or object-ledger revision still invalidates everything.
3. **What the reviewer is given.** The reviewer receives CANDIDATE, the touched
   sentence IDs as its scope, and the sentence before and after each touched
   span as read-only context. It applies all 15 principles to the scoped
   sentences. It reports a defect in a context sentence only when the edit
   caused it (a broken antecedent, a repeated phrase, a changed premise).
4. **Closing a finding.** A finding is closed by checking the repair against
   it and by the scoped review of the touched sentences, not by a fresh review
   of the whole unit.
5. **Batch.** Apply every accepted finding of one review in a single pass, then
   review the touched set once. Do not review after each single fix.
6. **Close of the unit: one full review.** When a unit has no pending verdict,
   run one whole-unit sentence review and one whole-unit terminology-and-
   notation review of the final text. Their findings are repaired and verified
   by rules 2 to 5. A second whole-unit review is warranted only when a repair
   changed a claim, a definition, a count, or a condition.
7. **Stopping.** A finding marked optional by its reviewer never starts a
   repair loop. A sentence that is flagged a third time, or findings that
   alternate between equivalent wordings, go to the author as a decision with
   one recommendation.
8. **Section stages.** Repairs that come from a section-wide review, from an
   author ruling, or from a change of another unit follow rules 2 to 5 as well.

## Source is not given to sentence and terminology reviewers

SOURCE (the round-start text) is given to the holistic reviewer, the formal
reviewer, the physics-object specialist (P11), and the conflict adjudicator,
whose task is fidelity to what the source meant. It is not given to the
sentence reviewer, the terminology-and-notation reviewer, or the other
principle specialists. They judge the candidate against the canon, the object
ledger, the project vocabulary, and the surrounding text; a comparison with the
source adds context length and no finding for them. The terminology delta is
taken against the ledger, the registry, and the earlier text of the candidate:
a name or symbol that none of them establishes is new.
