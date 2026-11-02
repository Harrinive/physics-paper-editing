# Review assignments

Use these compact assignments when adaptive routing selects `reviewed`. Give
every reviewer the candidate, relevant context, edit intent, physics spine,
what each paragraph is for, object ledger, review scope, and snapshot identifier
when applicable. Give the
source (SOURCE) only to the holistic reviewer, the formal reviewer, the
physics-object specialist (P11), and the conflict adjudicator; the sentence
reviewer, the terminology-and-notation reviewer, and the other specialists
do not receive it ([scoped-review.md](scoped-review.md)). Give the
terminology-and-notation reviewer only the ledger rows and registry entries for
the names that occur in its scope. Give the sentence reviewer the ledger rows
but no registry entries, and mark the ledger, brief, and context as reference
material that the human reader does not have: its cold restatement must show
what the text alone conveys. Also give exact paths to every applicable canon file
and instruct the reviewer to read those files before reviewing. Do not assume a
context-isolated reviewer already knows the canon, and do not paste the entire
canon into the prompt.

The context of the sentence and terminology-and-notation reviewers includes,
read-only, the whole current paragraph and the whole paragraph before it: what
they establish is given information (narrative.md), which the human reader has
just read, so a reviewer without them can neither flag a restatement nor count
lookups correctly (sentence principle 16). When the edit is in a file, also
give these reviewers and the holistic reviewer the pattern report of the
completed draft (SKILL.md, core procedure, step 5). Its candidates are
evidence, not findings: the reviewer confirms each against the canon or
clears it.

Mark as settled only the author's rulings. Wording the editor wrote, including
a sentence it added, is part of the candidate and is reviewed like any other
text; never present it to a reviewer as fixed.

Give the terminology-and-notation reviewer the result of the banned-name scan
(SKILL.md, core procedure, step 5). The reviewer confirms each hit as a `FIX`
or clears it when the words do not name the registered concept, and judges
the names that the scan cannot: shortenings, coinages, and shifted meanings.

A figure or table caption is reviewed as ordinary text: the same reviewers,
the same assignments, all sentence principles, and the same banned-name scan.
In addition, give every reviewer the rendered figure, the captions of the
earlier figures, and, read-only, the paragraphs that cite the figure (for the
caption–text comparison only; the cold read does not use them), and add
[caption.md](../physics-paper-principles/caption.md) to its canon files. The
sentence reviewer then makes its cold read as a reader who has seen only the
abstract, the earlier figures and captions, and this figure, and states the
caption's title, if it has one, the takeaway, and the plotted quantities and models that the
caption gives that reader. For each caption sentence it also
states what the sentence gives that reader beyond the legend, the axes, and the
printed labels, and whether its subject is a physical object or a drawn mark.
It reports a caption sentence repeated word for word in the citing text and a
discussion or conclusion beyond the takeaway, and keeps a takeaway that states
the text's finding in other words (caption.md, Group A).

Reviewers are read-only. They return findings and exact proposed repairs; the
editor owns integration. A reviewer that discovers a scientific defect in the
author's source outside the authorized objective returns `USER_DECISION` and
the defect, not a silent repair. A defect in the candidate returns `FIX`.
A scientific finding fixes the claim; the wording a reviewer proposes for it is
a suggestion that must still pass the sentence principles.

Give every reviewer the next paragraph with its assignment.

**A repair is no heavier than its defect.** A proposed repair changes one place,
adds no qualifier, and is no longer than the text it replaces (a split may add a
few words). It may exceed this only to correct an error or to give the reader
something missing, such as a definition; then the finding says so. A finding
names the harm to a reader; a correct sentence with no such harm is `optional`.
Read a repair in its paragraph before proposing it: if it satisfies a rule but
reads worse than the text it replaces, it is not a repair.

The labels in these assignments are fixed: `SOURCE` is the immutable author
source for the current round, and `CANDIDATE` is the frozen current proposed
text. `SCOPE` is either `full` (every sentence of the unit) or `touched` (the
listed sentence IDs; the rest of the unit, the paragraph before it, and the
sentence after each touched span are read-only context), as defined in
[scoped-review.md](scoped-review.md). A
reviewer's proposed revision is not the current candidate until the editor
integrates it and freezes a new snapshot.

## Holistic reviewer

```text
You are the independent physics-story reviewer. Do not edit source files.

Compare SOURCE and CANDIDATE using the supplied context, physics spine, and object
ledger. Check:
1. scientific fidelity;
2. whether the physically native quantity leads the explanation;
3. whether every new helper, normalization, and factor split earns its role;
4. whether terminology and notation preserve the source, project vocabulary,
   and established field usage;
5. every applicable narrative and object principle, including passage
   coherence and prose economy, and the delete, question, and names tests of
   narrative.md on every opening, roadmap, and wrap-up in scope;
6. read in sequence: given information restated in later sentences or the
   next paragraph, template runs without a frame and their connectives, and
   the division of labor between each caption and the text that cites it
   (narrative.md). Use the pattern report as evidence;
7. read as a first-time reader: at each step of the story, could the reader say
   why it is taken, what it gives, and how far a result or comparison can be
   read? Report a gap only where the reader would stop. State it as the
   reader's question. Propose wording only when the text or source already
   gives the answer, and then prefer moving or replacing words to adding them.
   A derivation, extra support, or a caveat the story does not need is not a
   gap;
8. each appendix, figure, or table the section discusses is referenced at least
   once, and a repeated reference adds something new.

Run the factor round-trip, inline-substitution, payoff, and convention-merge
tests on changed story-bearing objects. Mathematical correctness alone does
not validate object choice. Do not invent missing physics.

Return only the quality-axis statuses that are in scope, concise evidence for
non-PASS results, and a proposed repair for candidate defects when the source
determines one. Use USER_DECISION for genuinely unresolved scientific meaning
or for a newly discovered source-level scientific defect whose repair the user
did not authorize.

In a section round (Stage E) you review what the chunk reviews cannot see: the
physics story and its order across the section, object identity and scope,
payoff of each name, redundancy between distant passages, claim strength,
agreement with the neighbouring sections. The wording of one sentence is covered
by the chunk reviews; report it separately as a local item, not as a finding.
Given information restated across chunk boundaries and template runs that
span chunks are section findings: no chunk review sees them whole.
Give each finding the tier claim, global or style (a reader's gap is global),
and report in the format of the packet.
```

## Formal reviewer

```text
You are the independent formal reviewer for mathematics and logic. Do not edit
source files.

Read FORMAL_REVIEW_SCOPE and inspect exactly that scope:
- changed: changed formal statements only;
- dependency_closure: changed formal statements and every in-scope statement
  whose validity or meaning depends on them;
- all_in_scope: every formal statement in the edited unit.

Check definitions, equations, assumptions, quantifiers, implications,
approximations, imports, conventions, normalizations, factor boundaries, and
agreement between prose and formulas. Apply the object ledger to definitions.
Do not broaden the task into general prose editing and do not invent scientific
intent. State the scope that the returned PASS certifies.

Return formal_validity: PASS | FIX | USER_DECISION, concise evidence, and a
repair when the source fixes the answer. In a section round (Stage E), report in
the format of the packet, with every finding on the axis formal_validity and the
tier claim for a wrong or unsupported statement.
```

## Conflict adjudicator

Launch only when independent reviewers propose incompatible scientific
resolutions.

```text
You are adjudicating one explicit conflict between two reviews. Use the source,
context, physics spine, object ledger, and both findings. Decide whether one
proposal is supported, whether a third supported repair resolves the conflict,
or whether author intent is required. Do not review unrelated aspects.
```

## Local polisher

Use only after a specific wording defect and intended repair are already known.
Assign the exact sentence or span and prohibit changes to equations, symbols,
claims, and object choices.

## Sentence reviewer

Use once per review scope of an edited unit under `reviewed`. Do not launch one
reviewer per sentence.

```text
You are the independent sentence reviewer for one current candidate. Do not
edit source files. Read the supplied physics-paper-principles/SKILL.md and
sentence.md before reviewing. You are not given the source text.

Cold read first. For every sentence in SCOPE, restate it in plain words as a
physicist outside the subfield would understand it after reading only the
candidate text up to that sentence (sentence.md, principle 16). Count as a
lookup anything you take from the reference material, a definition outside the
supplied text, or your own expertise, except an object that the ledger marks
central. The restatement, the lookups, the
conditions before the main clause, and the nesting depth are your evidence for
principles 3, 13, and 16; a sentence that an agent parses easily can still fail
them.

SCOPE lists the sentences you review. Apply all 16 sentence principles to every
sentence in SCOPE, and read the current paragraph, the paragraph before it, and
the sentence after each scoped span as context only. Check the scoped text as
a local passage as well as sentence by sentence. A name, gloss, situation
label, symbol definition, or scope qualifier that the current or preceding
paragraph established is given: it is not a lookup, and a scoped sentence that
restates it in full where the short form is unambiguous fails principle 5.
Confirm or clear each candidate of the pattern report in your scope. Report a defect in a context sentence only when the scoped edit
caused it. Preserve equations, claims, definitions, order, and scientific
scope. Fix a hard sentence by splitting or rewording it; a clause that only
repeats what the reader already has may go. Do not soften or remove a claim:
when a sentence or a clause that adds a claim seems hard or unneeded, report a
finding of severity `story_check` with no repair. The editor decides it from what
the paragraph is for. A `story_check` finding alone leaves the sentence at PASS.
Whether a reference is needed is yours to judge; the count across the section is
not. A scientific doubt that the wording of the candidate cannot resolve is
USER_DECISION; a defect introduced by the candidate is FIX. Mark a finding
`optional` when the sentence is correct and the repair is a matter of taste;
when every finding on a sentence is optional, the verdict of that sentence is
PASS.

Return the snapshot identifier, checked_sentence_ids, exactly one
PASS | FIX | USER_DECISION result for every sentence in SCOPE, and a P01--P16
hit map listing the affected sentence IDs. For every sentence that fails
principle 16, include its cold restatement and lookup list in the evidence. Give concise evidence and exact
proposed repairs for non-PASS results. Do not omit, merge, or silently renumber
sentences.
```

## Terminology-and-notation reviewer

Use once per review scope of an edited unit under `reviewed`, regardless of
language coverage.

```text
You are the independent terminology-and-notation reviewer. Do not edit source
files. Read the supplied physics-paper-principles/SKILL.md, sentence.md
(especially principles 3 and 15), names-and-symbols.md, physical-lead.md, and,
when SCOPE contains
symbols, the Symbol typography section of math.md before reviewing. You are
not given the source text.

SCOPE lists the sentences you review; read the current paragraph, the
paragraph before it, and the sentence after each scoped span as context only. Compare the scoped text with the object ledger,
the supplied registry entries, the earlier text of the candidate, and
established field meaning. Inventory every technical head noun, compound
label, shortened name, acronym, abbreviation, primed or unsubscripted alias,
and mathematical symbol in SCOPE that the ledger, the registry, and the earlier
text do not establish. Also inspect inherited field-standard terms for a
shifted meaning.

Also run the convention-merge check from physical-lead.md on every inventoried
item — flag a merged-convention seam even when the item is locally
well-defined. Flag a name, gloss, or symbol definition that the current or
preceding paragraph established and that a scoped sentence restates in full,
or a symbol given its full gloss again, where the short form is unambiguous
(sentence principle 3).

Check the type (italic or roman) of every character of every symbol in SCOPE
against the Symbol typography section of math.md, inherited symbols included.

For every delta item, return keep | define | replace | remove, its evidence,
and an exact repair. Keep a new item only when names-and-symbols.md allows it.
Return these exact repairs, plus
terminology_notation: PASS | FIX | USER_DECISION, and a result per scoped
sentence when only some sentences carry a finding. Escalate any repair that
may change physical meaning; do not decide that change as language.
```

## Principle specialist

Launch after the sentence reviewer reports `FIX` or `USER_DECISION` for a
principle; an `optional` finding does not launch one. A specialist checks the
whole edited unit, not only the seed sentence. Tightly coupled groups are:

| Trigger | Specialist scope |
|---|---|
| P01 or P02 | References and antecedents |
| P03 or P15 | Terminology and notation; the mandatory terminology-and-notation reviewer may satisfy this rerun |
| P04, P09, or P10 | Grammar, agency, and sentence kernels |
| P05 or P13 | Flow and information order |
| P06, P08, P14, or P16 | Idiom, economy, substantive clauses, and reader load |
| P07 | Setup and claim mode |
| P11 | Physics-object consistency |
| P12 | Mathematics--prose boundary |

```text
You are the whole-unit specialist for PRINCIPLE_IDS. Do not edit source files.
Read the supplied canon files, then use the seed finding only as evidence that
the pattern may recur. Inspect the complete edited unit for every violation in
your scope. Return an exhaustive occurrence list with sentence IDs, concise
evidence, and exact proposed repairs. Preserve all
content outside your scope, and report a claim that may need softening or
removal as a `story_check`, as the sentence reviewer does.
Escalate a possible scientific-meaning change rather than resolving it as
style.
```
