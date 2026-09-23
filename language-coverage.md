# Language coverage

Language coverage is independent of scientific risk and edit intent.

Coverage selects which sentences require current evidence; it never selects
which sentence principles are enforced. Every sentence within the declared
coverage is checked against all 15 sentence principles. Every sentence in
newly drafted prose counts as changed.

For each checked sentence, compare terminology and notation with the source,
the surrounding document, and any project vocabulary registry. A newly coined
technical phrase or mathematical alias is a current finding even when the
sentence is otherwise grammatical.

Language coverage is inspection coverage, not permission to broaden the edit.
If inspection reveals a scientific defect in the author's source that the
requested task did not authorize repairing, pause the entire task and ask the
author. Ordinary candidate-language defects remain `FIX` findings for the
editor. Preserve an unauthorized, non-scientific observation outside the
repair scope as an advisory rather than silently editing it; this does not
weaken any principle within the declared inspection coverage.

## Modes

| Mode | Required evidence |
|---|---|
| `selective` | Check every changed, newly written, or specifically diagnosed sentence and assess the chunk's prose as a whole. Record checked sentence IDs; untouched sentences may remain ungraded. |
| `exhaustive` | Give every typographic sentence in the current chunk a current-snapshot language verdict. No skipped or missing sentence may count as completion. |

Use exhaustive coverage when the user explicitly requests every sentence, line
by line, a full language audit, or equivalent coverage. For a section round,
inherit its declared mode. If the expected coverage is ambiguous and would
materially change the result, ask before editing.

Coverage does not authorize broader changes. An exhaustive copyedit still
preserves claims, equations, definitions, symbols, order, and scientific scope;
a newly discovered scientific defect pauses rather than silently expanding the
repair scope.

## Reviewer escalation

Under `direct`, the editor performs the sentence check. Under `reviewed`, one
independent sentence reviewer checks all sentences selected by the coverage
mode, and one independent terminology-and-notation reviewer checks the entire
edited unit regardless of coverage mode.

The sentence reviewer records a hit map for principles `P01` through `P15`.
Any `FIX`, or a `USER_DECISION` that is not a source-level scientific halt,
triggers a specialist sweep of the whole edited unit for that principle or its
tightly coupled group. The first finding is evidence of a possible pattern;
the specialist does not inspect only the originally flagged sentence. A
source-level scientific `USER_DECISION` pauses before further review. Reviewers
return findings and exact proposed repairs but never write the live manuscript
or file.

## Sentence map

Create and persist the sentence map only when current-snapshot evidence is
required: a section-inherited coverage contract, an exhaustive audit, or a
resumable or concurrent file edit. An ordinary synchronous direct edit performs
the same applicable sentence checks without manufacturing hashes or job state.

When a sentence map is required, at the start of a chunk review:

1. freeze the chunk snapshot and its SHA-256 identifier;
2. assign stable IDs `S01`, `S02`, ... to typographic sentences without
   splitting equations, citations, references, or definitions from their
   immediate sentence;
3. record each exact sentence span's hash;
4. apply all 15 sentence principles and return `PASS | FIX | USER_DECISION` for
   every required sentence.

When snapshot evidence is required, persist the checked-sentence evidence for
both modes:

```yaml
language_review:
  coverage: selective | exhaustive
  chunk_snapshot_id: <sha256>
  reviewer:
    role: sentence_reviewer | editor
    requested_model: <value or unknown>
    resolved_model: <value or unknown>
    reasoning_effort: <value or unknown>
    verification_independence: independent | self_only | unavailable
  checked_sentence_ids: [S01, S03]
  sentence_results:
    - {sentence_id: S01, span_hash: <sha256>, status: PASS | FIX | USER_DECISION, note: <only when needed>}
  principle_hits:
    P03: {status: PASS | FIX | USER_DECISION, sentence_ids: [S03]}
```

For exhaustive coverage, `checked_sentence_ids` and `sentence_results` contain
every sentence. For selective coverage, they contain every changed, newly
written, or diagnosed sentence. One reviewer checks the whole chunk; never
launch one reviewer per sentence.

## Invalidation and completion

The snapshot and invalidation rules below apply only when the workflow requires
the sentence map defined above. For an ordinary synchronous direct edit,
completion instead requires a fresh canon check of the final text in hand.

- A verdict is valid only for its recorded sentence and chunk snapshot.
- After any candidate repair, recompute the sentence and chunk hashes and rerun the
  complete chunk language check. Ordinary micro chunks contain at most 12
  sentences; a section-owned indivisible oversized unit follows the same rule.
- A split, merge, reorder, or renumbering invalidates the affected sentence map.
- Historical, legacy, superseded, and stale results are context only.
- Exhaustive language coverage passes only when every sentence in every current
  chunk has a current `PASS`; `FIX`, `USER_DECISION`, skipped, or missing blocks
  completion.
- Reviewed work also requires a current terminology-and-notation `PASS` for the
  entire edited unit and current results from every triggered principle
  specialist.
