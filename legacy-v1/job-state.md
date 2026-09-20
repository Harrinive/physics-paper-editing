# Job state — marks, snapshot, result shards, stop request

**For agents:** Start with [LEGACY.md](LEGACY.md) § Agent read order. Read with the coworker loop ([coworker-loop.md](coworker-loop.md)).

`PPE` means **physics-paper-editing**. It is a machine tag, not a physics acronym.

---

## Construction-area sentinels

Whole-line `%` comments. Invisible in the PDF. Compile is unchanged.

```latex
% PPE-BEGIN job=j12 rev=0 status=checking created=2026-09-03T12:21:00-05:00
% PPE-NOTE you may edit inside; agent merges once per check round
The flux jump is defined by ...
A second sentence stays in the zone ...
% PPE-END job=j12
```

| Field | Rule |
|-------|------|
| `job=` | Unique per pair. Micro: `j` + short id. Section chunk: `j-<chunk_id>` or `j-<chunk_id>-<n>` |
| `rev=` | `0` at wrap; `+=1` after each merge write |
| `status=` | `checking` while workers run · `merging` only during the write · `conflict` if a serious conflict is waiting · omit after unmark |
| `created=` | Set **once** at wrap, local ISO-8601 with offset (`YYYY-MM-DDTHH:MM:SS±HH:MM`) |
| `updated=` | Added/replaced after each merge; same timestamp format |

Rules:

- **Interior** = every line strictly between `PPE-BEGIN` and `PPE-END` for that `job`. Sentinels are never hashed.
- Each sentinel is its own line; first non-space characters `% PPE-BEGIN` / `% PPE-END`. Not mid-sentence, not inside `\(`, `$`, or an environment.
- One job per pair. Two areas in one file = two pairs. **No nesting.**
- **What gets wrapped.** Micro: the quoted passage. Section Stage D: that chunk’s `tex_anchor` span. Never wrap a whole section in one pair.
- User and the merge step may edit the **interior**. The parent updates `rev` / `status` / `updated=` on BEGIN after each round. Interior is rewritten **once per round**, not per sentence.
- **Unmark:** delete BEGIN, NOTE, and END; leave the interior. Do this when no verifier jobs are running and no open serious conflicts remain.
- **Missing sentinel:** do not re-wrap silently. Fall back to last snapshot + `tex_anchor`; tell the user the marks are missing; re-wrap only after they confirm or paste the marks back.

---

## Disk layout

**Standalone micro**

```
.physics-edit/micro/<job_id>/
├── snapshot.tex        # frozen interior for this round
├── sentences.json      # S1…SN + hashes + bodies
├── findings/           # one append-only JSONL shard per worker
├── round.md            # last harvest / OVERALL
└── agents.json         # runtime and worker manifest
```

**Section job** (under the section slug)

```
.physics-edit/<section-slug>/jobs/<job_id>/
├── snapshot.tex
├── sentences.json
├── findings/
├── round.md
└── agents.json
```

Add `.physics-edit/` to the project `.gitignore` when this state is ephemeral.

### sentences.json

```json
{
  "job": "j12",
  "round": 0,
  "tex_file": "Notes/example.tex",
  "created": "2026-09-03T12:21:00-05:00",
  "sentences": [
    {"label": "S1", "hash": "<16 hex>", "text": "<exact interior sentence>"}
  ]
}
```

**Hash:** first 16 hex chars of SHA-256 over the sentence body with trailing whitespace stripped. Same split as [sentence-check-subagents.md](sentence-check-subagents.md) §2.

### Result shards

Every verifier receives its own path, such as `findings/sentence-S1.jsonl`,
`findings/narrative.jsonl`, or `findings/math.jsonl`. It appends finding records
as they exist and finishes with one terminal `event:"completion"` record.
Every record repeats the worker envelope below; the shard is immutable after
that terminal record. Verifiers never edit the `.tex`.

The parent reads shards in lexical path order, then file order within each
shard. This is the deterministic merged ledger for the synthesizer; never let
multiple workers append to the same file.

```json
{"schema_version":1,"worker_id":"sentence-S1","agent_id":"<host id or unknown>","role":"sentence","scope":["S1"],"snapshot_id":"sha256:<hash>","runtime":"cursor|codex|claude|other","model":{"requested_tier":"fast","resolved_model":"<id or unknown>","reasoning":"<level or unknown>","resolution_source":"accepted_default|custom|inherit|fallback"},"status":"running","event":"finding","finding":{"check":"notation","severity":"blocker","summary":"…"}}
{"schema_version":1,"worker_id":"sentence-S1","agent_id":"<host id or unknown>","role":"sentence","scope":["S1"],"snapshot_id":"sha256:<hash>","runtime":"cursor|codex|claude|other","model":{"requested_tier":"fast","resolved_model":"<id or unknown>","reasoning":"<level or unknown>","resolution_source":"accepted_default|custom|inherit|fallback"},"status":"complete","event":"completion"}
```

Narrative / math use `label":"narrative"` or `"math"` and hash the full snapshot body.

### agents.json

```json
{
  "job": "j12",
  "round": 0,
  "runtime": "cursor|codex|claude|other",
  "model_profile": {
    "profile_choice": "recommended|parent|custom",
    "profile_source": "accepted_default|custom|inherit|fallback",
    "user_confirmed": true,
    "sentence": {"requested_tier": "fast", "resolved_model": "<id or unknown>", "reasoning": "<level or unknown>", "resolution_source": "accepted_default|custom|inherit|fallback"},
    "deep": {"requested_tier": "capable", "resolved_model": "<id or unknown>", "reasoning": "<level or unknown>", "resolution_source": "accepted_default|custom|inherit|fallback"},
    "synth": {"requested_tier": "capable", "resolved_model": "<id or unknown>", "reasoning": "<level or unknown>", "resolution_source": "accepted_default|custom|inherit|fallback"}
  },
  "running": [
    {
      "worker_id": "sentence-S2",
      "agent_id": "<host id or unknown>",
      "role": "sentence",
      "label": "S2",
      "requested_tier": "fast",
      "resolved_model": "<id or unknown>",
      "reasoning": "<level or unknown>",
      "status": "queued|running|complete|interrupted|failed|stale",
      "result_path": "findings/sentence-S2.jsonl",
      "started_at": "<ISO-8601 or unknown>",
      "completed_at": "<ISO-8601 or unknown>"
    }
  ]
}
```

Retain completed entries with their final status. A missing host identifier is
`unknown`, never an invented value. Send a stop request only to workers still
listed as `running` when the selected runtime supports it.

---

## Stop-request prompt

On a related change, send this request to each still-running verifier when the
runtime supports interruption:

```text
Stop specialist work. Append any findings you already have to
<absolute path to this worker's result shard> (one JSON object per line; include a
terminal completion record for your label if you finished). Then stop. Do not edit the .tex.
```

Do not expect hidden deliberation from any host. Salvage consists of lines
already on disk plus a final flush when the worker can receive the request. If
the runtime cannot stop workers, let them finish and mark results stale when
their snapshot no longer matches.

---

## Harvest tags

After a stop request or wave completion, merge all result shards deterministically and tag each finding record (not terminal completion records):

| Tag | When |
|-----|------|
| `valid` | `sentence_hash` still matches live text for that label |
| `stale` | hash no longer matches (user rewrote that sentence) |
| `open` | label has no terminal completion record |

Keep stale lines. They are merge input, not trash.

`round.md` records: completion or wake reason, related labels, shard paths,
harvest counts, synthesizer `OVERALL`, and whether the interior was rewritten.
