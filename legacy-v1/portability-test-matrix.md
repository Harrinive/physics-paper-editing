# Portability test matrix

Run this matrix before claiming support for a new host version or changing an
adapter. The assertions are behavior-level: the host implementation may differ,
but the persisted artifacts and user-visible guarantees must match.

| Scenario | Fixture | Required assertion |
|---|---|---|
| Short polish | ≤12 sentences; no equations | Marked draft precedes verification; sentence and narrative shards exist; math is skipped only by the mechanical rule. |
| Long section | >12 sentences with chunk boundary | Parent records one confirmed profile, passes it to chunks, and never repeats the profile question. |
| Custom profile | User supplies one role mapping | Manifest records requested tiers, resolved identifiers or `unknown`, reasoning when exposed, and `custom` source. |
| Unavailable model | Requested tier unavailable | Fallback is recorded; no invented identifier; verification still follows the frozen snapshot. |
| Limited concurrency | More verifier assignments than available slots | Scheduler uses waves; every required scope is covered exactly once. |
| No read-only enforcement | Host cannot restrict source writes | Assignment prohibits source edits; manifest and source audit show only result-shard output. |
| No background work | Host runs verifiers in foreground | Draft remains written; status does not claim that the user can edit concurrently. |
| No interruption | User edits a checked sentence during verification | Old shard survives but is tagged stale; only the fresh snapshot enters synthesis. |
| Worker failure and resume | One result shard missing or failed | Resume preserves valid shards and relaunches only incomplete scopes. |

Run the short-polish and long-section fixtures on Cursor, Codex, and Claude
Code. For each run, retain the marked draft, snapshot, `agents.json`, result
shards, harvest record, CHECKS output, and final merge as evidence. A pass on
only one host or one fixture is not portability evidence.
