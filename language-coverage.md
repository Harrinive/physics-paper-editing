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

## Modes

| Mode | Required evidence |
|---|---|
| `selective` | Check every changed or specifically diagnosed sentence and assess the chunk's prose as a whole. Identify checked sentence IDs; untouched sentences may remain ungraded. |
| `exhaustive` | Give every typographic sentence in the current chunk a current-snapshot language verdict. No skipped or missing sentence may count as completion. |

Use exhaustive coverage when the user explicitly requests every sentence, line
by line, a full language audit, or equivalent coverage. For a section round,
inherit its declared mode. If the expected coverage is ambiguous and would
materially change the result, ask before editing.

Coverage does not authorize broader changes. An exhaustive copyedit still
preserves claims, equations, definitions, symbols, order, and scientific scope.

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

For exhaustive coverage, persist:

```yaml
language_review:
  coverage: exhaustive
  chunk_snapshot_id: <sha256>
  reviewer:
    role: language_reviewer | editor
    requested_model: <value or unknown>
    resolved_model: <value or unknown>
    reasoning_effort: <value or unknown>
    verification_independence: independent | self_only | unavailable
  sentence_results:
    - {sentence_id: S01, span_hash: <sha256>, status: PASS | FIX | USER_DECISION, note: <only when needed>}
```

One reviewer checks the whole chunk. Never launch one worker per sentence.

## Invalidation and completion

The snapshot and invalidation rules below apply only when the workflow requires
the sentence map defined above. For an ordinary synchronous direct edit,
completion instead requires a fresh canon check of the final text in hand.

- A verdict is valid only for its recorded sentence and chunk snapshot.
- After any source repair, recompute the sentence and chunk hashes and rerun the
  complete chunk language check. Chunks contain at most 12 sentences, so this
  avoids carrying verdicts across a changed chunk snapshot.
- A split, merge, reorder, or renumbering invalidates the affected sentence map.
- Historical, legacy, superseded, and stale results are context only.
- Exhaustive language coverage passes only when every sentence in every current
  chunk has a current `PASS`; `FIX`, `USER_DECISION`, skipped, or missing blocks
  completion.
