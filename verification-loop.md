# Verification (background, per round)

**For agents:** Start with [SKILL.md](SKILL.md) § Agent read order. Canonical loop: [coworker-loop.md](coworker-loop.md). Execution: [phase2-verify-subagents.md](phase2-verify-subagents.md). Marks/harvest: [job-state.md](job-state.md). Merge: [merge-policy.md](merge-policy.md).

There is **no Phase 1 source-audit gate**. Checklists are drafting principles plus background-checker objectives.

---

## What runs

| | Background output verify |
|--|--------------------------|
| **When** | After the marked draft is in the `.tex` — every job, including rewrite |
| **Target** | Frozen **snapshot** of the marked interior, not the live file |
| **Sentence checks** | Changed labels only (all labels on rewrite or first draft vs source) |
| **Narrative + math** | Full snapshot; math skipped only on standalone-micro fast polish with no equations ([fast-polish.md](fast-polish.md)) |
| **Who decides the round** | **Verifier synthesizer** — `OVERALL`: `PASS` \| `CONFLICTS` \| `PARTIAL` |
| **CHECKS / hook** | Audit drawer after a round. Hook does **not** reloop on FAIL. `verify:running` / `verify:partial` may end without CHECKS |

Workers launch with `run_in_background: true` and append `findings.jsonl` as they go.

---

## Launch (after mark + snapshot)

```
1. Confirm models (inherited or defaults — gate.md)
2. Label S1…SN; identify changed labels vs source (first wave) or prior snapshot
3. Emit Task plan (phase2_sentence_tasks = changed labels only)
4. Launch in parallel, run_in_background: true:
     • narrative — full snapshot
     • math — when applicable (or skip per fast-polish.md)
     • sentence — one Task per changed label
   Record Task ids in agents.json
5. End the turn — Mode: … · verify:running
6. Synthesizer runs at **round end** (wave complete or interrupt harvest), not as a ship gate
```

**Producer must not** run checklists inline on the draft or set `OVERALL`.

---

## Wake (every later turn while a job is live)

```
1. Re-read marked interior; rehash ([job-state.md](job-state.md))
2. Related change → interrupt still-running Tasks (flush then stop)
3. Harvest findings.jsonl; tag valid / stale / open
4. One merge ([merge-policy.md](merge-policy.md)); rewrite interior once
5. Synthesizer: job-round OVERALL from harvest + merge
6. New snapshot; relaunch open + newly dirty labels — or unmark
```

---

## Non-negotiable rules

- Always independent verifier subagents on the snapshot; no producer self-grade.
- Never wait to write `.tex` until `OVERALL: PASS`.
- Never end the draft-ready turn by blocking on checkers.
- Never auto-select a new model profile when one can be inherited; defaults are allowed and must be mentioned once ([user-communication.md](user-communication.md)).
- Never skip background checks because the producer “already followed the principles.”
- After a merge that changed labels, relaunch only those labels (plus still-`open` ones).
- Pace never makes the user wait. Fast-polish narrowing is standalone-micro polish only ([fast-polish.md](fast-polish.md)).

**Hook:** `~/.cursor/hooks/check-editing-session.sh` — `verify:running` / `verify:partial` / `draft-ready` may end without CHECKS. No auto-reloop on `OVERALL: FAIL|CONFLICTS|PARTIAL`.
