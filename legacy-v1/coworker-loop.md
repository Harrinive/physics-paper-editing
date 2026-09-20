# Coworker loop

**For agents:** Start with [LEGACY.md](LEGACY.md) § Agent read order. This file is canonical for draft-first verification. Runtime selection and fallbacks: [runtime-contract.md](runtime-contract.md). Marks and disk: [job-state.md](job-state.md). Merge: [merge-policy.md](merge-policy.md). User-facing copy: [user-communication.md](user-communication.md). Canon: **`physics-paper-principles`**.

The producer writes working text immediately, marks a construction area, and delegates independent checkers on a **frozen snapshot**. The user keeps editing whenever the runtime supports asynchronous delegation. A check **round** ends when the wave finishes or a stale-result harvest runs. Then one merge updates the marked interior. **Exception:** do not resolve an essential scientific ambiguity by inventing a definition — see § Definition halt.

**Phase 1 as a blocking pre-edit audit does not run.** Principles are drafting rules for the producer and objectives for background checkers. **Definition halt** (below) is intake, not Phase 1: it only fires when drafting the definition requires an unresolved scientific choice that supplied context cannot settle.

Runtime-specific monitoring is optional and belongs only in the selected adapter. `verify:running`, `verify:partial`, and `draft-ready` may end without CHECKS. No automatic reloop follows `OVERALL: FAIL|CONFLICTS|PARTIAL`.

---

## Loop

```
1. Scope ≤12 sentences (else route to the parent section skill)
2. Intake — polish versus rewrite if unclear; confirm the session model profile once (runtime-contract.md)
2a. Consider physical meaning and definition choice; halt only for unresolved essential scientific ambiguity (below)
3. Draft — physics-paper-principles (sentence / narrative / math / physical-lead as applicable)
4. Mark construction area + write .tex (job-state.md)
5. Snapshot interior → sentences.json + snapshot.tex
6. Schedule verifier jobs under the resolved runtime — phase2-verify-subagents.md
7. Continue asynchronously when supported; otherwise execute foreground waves while preserving the draft
8. On completion or wake — related-hash check → request stop if supported → harvest result shards
9. One merge round (merge-policy.md) → rewrite marked interior once (rev+=1)
10. New snapshot; relaunch only open + newly dirty labels — or unmark if done
```

Never wait for `OVERALL` before the first `.tex` write. Never withhold a draft-ready response merely because verification is running. **Definition halt is not an `OVERALL` wait** — it is intake, like scope overflow: pause only the definition whose faithful drafting requires an unresolved scientific choice; continue independent edits.

Never skip verification because the producer “already followed the principles.”

---

## Definition halt (before first write)

When the passage **introduces or rewrites** a named object in the physical or protocol story (`definition` environment, "we define", first-use coinage):

1. Run **Physical lead** and record **Physical meaning and definition choice** ([physical-lead.md](../../physics-paper-principles/legacy-v1/physical-lead.md)): role, category, operational option, and chosen name/form. Consider an operational definition; prefer it when precise and useful. Other definition forms remain valid.
2. If the object is well-defined, draft with its supported physical role and continue. Thin motivation is a presentation issue, not a halt; retain a valid construction when no better operational characterization is established.
3. Halt only if completing or changing the definition requires an essential choice between materially different physical meanings that the supplied context cannot resolve. Do not guess. State **Need your call** ([user-communication.md](user-communication.md)), quote the ambiguity, and ask the specific scientific question. Continue independent edits.

No halt merely because the passage uses an already-defined term, a construction, or no independent operational criterion. Classify polish versus rewrite by the extent and substance of the edit ([gate.md](gate.md)), not the definition form.

---

## Who does what

| Role | Writes `.tex`? | Grades `OVERALL`? |
|------|----------------|-------------------|
| Producer (main agent) | Yes — draft, mark, merge apply | **No** |
| Sentence / narrative / math workers | **No** — write their assigned result shard only | No |
| Synthesizer (per **round**) | No | **Yes** — `PASS` \| `CONFLICTS` \| `PARTIAL` |

**Writer ≠ grader** stays. `OVERALL` is a **job-round** status in the audit drawer, not a ship gate.

| `OVERALL` | Meaning |
|-----------|---------|
| `PASS` | No open must-fix on current live text; unmark if no verifier jobs remain |
| `CONFLICTS` | Serious conflict(s) left for the user; their text stays |
| `PARTIAL` | Interrupted or unfinished labels; a later wave will continue |

---

## Completion or wake → stale-result handling → harvest

Triggers: user chat message · verifier completion · optional host-native watcher.

On every wake while a job is `checking`:

1. Read the live marked interior ([job-state.md](job-state.md)).
2. Split and hash sentences the same way as the snapshot.
3. **Related** = at least one label this job is checking has a different hash. Edits outside the marks are ignored.
4. If related: request that every still-running verifier for that job flush its own result shard and stop, when the runtime supports interruption. Otherwise allow completion and reject stale output.
5. Harvest the deterministic merged ledger. Tag lines `valid` / `stale` / `open` ([job-state.md](job-state.md) § Harvest).
6. One merge ([merge-policy.md](merge-policy.md)). Rewrite the interior once. New snapshot. Relaunch only `open` + labels whose live text is new.

Stale findings are **kept**. They feed the merge (“this was wrong on the previous wording”).

Workers never write the live `.tex`. No wake → no interrupt; they keep grading the old snapshot.

---

## Pace

Pace does **not** change whether the user waits. It only scopes background checks:

| Pace | Background profile |
|------|-------------------|
| `fast` | Standalone micro + polish: narrower delta question; math verification may skip when there is no equation ([fast-polish.md](fast-polish.md)) |
| `full` | Full passage-vs-manuscript narrative + math; every changed sentence still gets a verifier assignment |

Rewrite and section chunks (`caller: section-orchestrator`) never get the fast-polish math skip.

---

## End of a job

Unmark ([job-state.md](job-state.md)) when no verifier jobs are running **and** there are no open serious conflicts. Leave the prose. Follow [user-communication.md](user-communication.md) — named state **Done**.
