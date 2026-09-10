# Job state — marks, snapshot, ledger, interrupt

**For agents:** Start with [SKILL.md](SKILL.md) § Agent read order. Read with the coworker loop ([coworker-loop.md](coworker-loop.md)).

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
- **Unmark:** delete BEGIN, NOTE, and END; leave the interior. Do this when no Tasks are running and no open serious conflicts remain.
- **Missing sentinel:** do not re-wrap silently. Fall back to last snapshot + `tex_anchor`; tell the user the marks are missing; re-wrap only after they confirm or paste the marks back.

---

## Disk layout

**Standalone micro**

```
.physics-edit/micro/<job_id>/
├── snapshot.tex        # frozen interior for this round
├── sentences.json      # S1…SN + hashes + bodies
├── findings.jsonl      # append-only worker ledger
├── round.md            # last harvest / OVERALL
└── agents.json         # running Task ids for interrupt
```

**Section job** (under the section slug)

```
.physics-edit/<section-slug>/jobs/<job_id>/
├── snapshot.tex
├── sentences.json
├── findings.jsonl
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

### findings.jsonl

Workers **append** as soon as they have a result (and a `done` line). They do not edit the `.tex`.

```json
{"job":"j12","round":0,"label":"S1","sentence_hash":"a1b2c3d4e5f60718","check":"notation","severity":"blocker","summary":"…","status":"open"}
{"job":"j12","round":0,"label":"S1","sentence_hash":"a1b2c3d4e5f60718","event":"done"}
```

Narrative / math use `label":"narrative"` or `"math"` and hash the full snapshot body.

### agents.json

```json
{
  "job": "j12",
  "round": 0,
  "running": [
    {"role": "sentence", "label": "S2", "agent_id": "<Task id>"}
  ]
}
```

Remove an entry when that Task finishes. Interrupt only ids still listed.

---

## Interrupt prompt

On a related change, resume each still-running Task with `interrupt: true`:

```text
Stop specialist work. Append any findings you already have to
<absolute path to findings.jsonl> (one JSON object per line; include a
done line for your label if you finished). Then stop. Do not edit the .tex.
```

Cursor does not dump hidden reasoning. Salvage = lines already on disk plus a last flush if the worker is still alive.

---

## Harvest tags

After interrupt or wave completion, read `findings.jsonl` and tag each finding line (not `done` events):

| Tag | When |
|-----|------|
| `valid` | `sentence_hash` still matches live text for that label |
| `stale` | hash no longer matches (user rewrote that sentence) |
| `open` | label never got a `done` line |

Keep stale lines. They are merge input, not trash.

`round.md` records: wake reason, related labels, harvest counts, synthesizer `OVERALL`, whether the interior was rewritten.
