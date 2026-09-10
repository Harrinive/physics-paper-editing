# Coworker loop

**For agents:** Start with [SKILL.md](SKILL.md) § Agent read order. This file is canonical for draft-first background checking. Marks and disk: [job-state.md](job-state.md). Merge: [merge-policy.md](merge-policy.md). User-facing copy: [user-communication.md](user-communication.md). Canon: **`physics-paper-principles`**.

The producer writes working text immediately, marks a construction area, and launches independent checkers on a **frozen snapshot**. The user keeps editing. A check **round** ends when the wave finishes or an interrupt harvest runs. Then one merge updates the marked interior. **Exception:** do not write a construction-only definition of a named physical object — see § Definition halt.

**Phase 1 as a blocking pre-edit audit does not run.** Principles are drafting rules for the producer and objectives for background checkers. **Definition halt** (below) is intake, not Phase 1: it only fires when a named physical object has no honest operational criterion.

**Hook:** `~/.cursor/hooks/check-editing-session.sh` — `verify:running` / `verify:partial` / `draft-ready` may end without CHECKS. No auto-reloop on `OVERALL: FAIL|CONFLICTS|PARTIAL`.

---

## Loop

```
1. Scope ≤12 sentences (else route to the parent section skill)
2. Intake — polish vs rewrite if unclear; inherit pace + models (gate.md)
2a. Definition halt if the passage introduces or rewrites a named physical object and no honest operational criterion is available (below)
3. Draft — physics-paper-principles (sentence / narrative / math / physical-lead as applicable)
4. Mark construction area + write .tex (job-state.md)
5. Snapshot interior → sentences.json + snapshot.tex
6. Launch background checkers (run_in_background: true) — phase2-verify-subagents.md
7. End the turn — user keeps writing
8. On wake — related-hash check → interrupt if needed → harvest findings.jsonl
9. One merge round (merge-policy.md) → rewrite marked interior once (rev+=1)
10. New snapshot; relaunch only open + newly dirty labels — or unmark if done
```

Never wait for `OVERALL` before the first `.tex` write. Never end a draft-ready turn by blocking on checkers. **Definition halt is not an `OVERALL` wait** — it is intake, like scope overflow: do not start the loop on a construction-only definition you cannot repair.

Never skip background checks because the producer “already followed the principles.”

---

## Definition halt (before first write)

When the passage **introduces or rewrites** a named object in the physical or protocol story (`definition` environment, "we define", first-use coinage):

1. Run the **Physical lead** diagnostic ([physical-lead.md](../physics-paper-principles/physical-lead.md)). Diagnosis is always possible.
2. If an operational criterion can be stated honestly → draft with definition layering (criterion → labeling/computation → coincidence pointer) and continue the loop.
3. If it cannot → **do not write** the construction as the definition and **do not invent** a criterion. Named state **Need your call** ([user-communication.md](user-communication.md)). Quote the construction; ask what membership test the lead should state (or confirm the object is purely formal). Finalize that definition before further edits of the object.

No halt when the passage only *uses* an already-defined term. Changing a construction-led definition into a physically led one is **rewrite**, not in-place polish ([gate.md](gate.md)).

---

## Who does what

| Role | Writes `.tex`? | Grades `OVERALL`? |
|------|----------------|-------------------|
| Producer (main agent) | Yes — draft, mark, merge apply | **No** |
| Sentence / narrative / math workers | **No** — append `findings.jsonl` only | No |
| Synthesizer (per **round**) | No | **Yes** — `PASS` \| `CONFLICTS` \| `PARTIAL` |

**Writer ≠ grader** stays. `OVERALL` is a **job-round** status in the audit drawer, not a ship gate.

| `OVERALL` | Meaning |
|-----------|---------|
| `PASS` | No open must-fix on current live text; unmark if no tasks remain |
| `CONFLICTS` | Serious conflict(s) left for the user; their text stays |
| `PARTIAL` | Interrupted or unfinished labels; a later wave will continue |

---

## Wake → interrupt → harvest

Wakes: user chat message · background wave completion · optional file watcher (~5–10s debounce).

On every wake while a job is `checking`:

1. Read the live marked interior ([job-state.md](job-state.md)).
2. Split and hash sentences the same way as the snapshot.
3. **Related** = at least one label this job is checking has a different hash. Edits outside the marks are ignored.
4. If related: `interrupt: true` on every still-running Task for that job, prompt: flush `findings.jsonl` then stop.
5. Harvest the ledger. Tag lines `valid` / `stale` / `open` ([job-state.md](job-state.md) § Harvest).
6. One merge ([merge-policy.md](merge-policy.md)). Rewrite the interior once. New snapshot. Relaunch only `open` + labels whose live text is new.

Stale findings are **kept**. They feed the merge (“this was wrong on the previous wording”).

Workers never write the live `.tex`. No wake → no interrupt; they keep grading the old snapshot.

---

## Pace

Pace does **not** change whether the user waits. It only scopes background checks:

| Pace | Background profile |
|------|-------------------|
| `fast` | Standalone micro + polish: narrower delta question; math Task may skip when there is no equation ([fast-polish.md](fast-polish.md)) |
| `full` | Full passage-vs-manuscript narrative + math; every changed sentence still gets a Task |

Rewrite and section chunks (`caller: section-orchestrator`) never get the fast-polish math skip.

---

## End of a job

Unmark ([job-state.md](job-state.md)) when no Tasks are running **and** there are no open serious conflicts. Leave the prose. Follow [user-communication.md](user-communication.md) — named state **Done**.
