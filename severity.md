# Severity (harness)

**For agents:** Start with [SKILL.md](SKILL.md). Read with the Read tool before launching checkers, synthesizing a round, or merging.

Canon for *what is wrong* is **`physics-paper-principles`**. This file maps those violations to **BLOCKER** vs **SUGGEST** for the coworker loop. Do not restate the principles here.

Workers and the synthesizer use only these closed BLOCKER classes. Everything else is SUGGEST. Downgrade out-of-list BLOCKERs.

**Never auto-apply a guessed operational criterion** ([physical-lead.md](../physics-paper-principles/physical-lead.md), [merge-policy.md](merge-policy.md)).

---

## Contract

| Label | Meaning |
|-------|---------|
| **BLOCKER** | Must-fix on **untouched** text (auto-apply) **or** a serious clash with user text (report, leave yours). Construction-as-definition / missing physical lead: **always report; never auto-apply**. |
| **SUGGEST** | Never auto-applies; never a user decision; never sets `OVERALL: CONFLICTS` by itself. |
| **PACKET_GAP** | Fast-polish only — finding needs more manuscript context ([fast-polish.md](fast-polish.md)). Not a must-fix. |

When unsure, use SUGGEST and state what evidence would promote it.

---

## Narrative BLOCKER classes (6)

Only these closed classes, against [narrative.md](../physics-paper-principles/narrative.md):

1. **Contradiction or false relation** — the draft contradicts supplied context, or a transition/causal/contrast connective asserts a relation the source does not support.
2. **Unbound essential object** — an operator, symbol, referent, or declared set needed to interpret the claim is absent from the supplied manuscript context.
3. **Broken reasoning** — a non-sequitur, reversed implication, or omitted essential premise changes whether the stated conclusion follows.
4. **Claim-strength mismatch** — prose asserts necessity, sufficiency, equivalence, generality, novelty, or evidence stronger than the theorem, derivation, citation, or results supplied.
5. **Meaning loss or invention** — the edit drops a required limitation or introduces a scientific mechanism, assumption, or conclusion absent from the source.
6. **Construction-as-definition** — a named object in the physical or protocol story is introduced only by a labeling, spanning, or computation recipe, with no operational membership criterion before that recipe ([physical-lead.md](../physics-paper-principles/physical-lead.md)). Same class as math BLOCKER 6. Use this class when the math Task did not run; if math already reported it, do not invent a second criterion.

Everything else—including alternative framing, roadmap strategy, optional motivation, economy, recoverable ordering, and stylistic preference—is a SUGGEST.

---

## Math BLOCKER classes (6)

Only these closed classes, against [math.md](../physics-paper-principles/math.md) and [physical-lead.md](../physics-paper-principles/physical-lead.md):

1. **Invalid or inconsistent mathematics** — an equation, derivation, quantifier, domain, implication, or convention is false or internally inconsistent under the supplied assumptions.
2. **Undefined essential object** — a symbol, operator, domain, map, or assumption required to interpret or evaluate the statement is unavailable in the supplied manuscript context.
3. **Formula–prose mismatch** — natural language and formal statement encode materially different assertions.
4. **Unsupported logical strength** — necessity, sufficiency, equivalence, uniqueness, generality, or “without loss of generality” is stronger than the supplied proof, theorem, citation, or evidence.
5. **Incorrect import** — a cited result is misstated or its hypotheses do not hold in the present setting.
6. **Construction-as-definition** — a named object in the physical or protocol story is introduced only by a labeling, spanning, or computation recipe, with no operational membership criterion before that recipe. Accurate constructions still instantiate this class.

Unverified-but-plausible imports, optional derivation detail, motivation, presentation order, notation preference, and possible strengthening are SUGGEST unless they instantiate a class above.

---

## Sentence workers

Sentence Tasks grade wording against [sentence.md](../physics-paper-principles/sentence.md) (all 14). They are **not** the physics/math adjudicator.

| Finding | Severity |
|---------|----------|
| Grammar or reference failure that makes the target unreadable or reverses/materially changes the supplied meaning | `BLOCKER` |
| Tautological / type-gloss clauses (principle 14) that need a contrast or consequence | `SUGGEST` + proposed `Edited:` — do not invent a scientific point |
| Missing physical lead on a newly named object (principle 11) | Do not invent the criterion. `ESCALATE_TO: math` (or narrative if no math Task) and `Needs user / main-agent judgment` |
| Any physics, mathematics, scope, theorem, evidence, or scientific-correctness concern | `SUGGEST` + `ESCALATE_TO: narrative` or `math`; never a confident physics conclusion |

Silent fixes (unambiguous pronoun, SVO, “For A, it does B”, typos, punctuation) are allowed when they do not add a scientific claim — [sentence-check-subagents.md](sentence-check-subagents.md).

---

## Fast polish overlay

When `edit_gate: polish` + `pace: fast` + `caller: micro`, [fast-polish.md](fast-polish.md) **narrows which BLOCKERs fire** (delta vs the user’s source; word-delta class; `PACKET_GAP`). It does not change the principle files. Construction-as-definition on an object **this quote introduces** is not waived as pre-existing.
