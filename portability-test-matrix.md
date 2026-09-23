# Portability and behavior matrix

Validate behavior, not host command spelling.

| Scenario | Required result |
|---|---|
| Ordinary synchronous low-risk strong edit | Direct path; no reviewer, state directory, snapshot, or legacy `OVERALL` |
| Low-risk economy edit | Scaffolded direct path; no exhaustive `N/A` list |
| Medium substantive edit | Reviewed path; mandatory whole-unit sentence and terminology-and-notation reviewers, triggered principle specialists, holistic review, and scoped formal review |
| High-risk edit | Reviewed high-risk profile; blind applicable physics/formal reviews; adjudicator only on an actual conflict |
| No delegation | Parent checks; `verification_independence: self_only`; no false independence claim |
| Unknown model | Economy routing; no invented model identifier |
| No background capability | Foreground review; no concurrency claim |
| Stale snapshot | Obsolete review preserved but not applied to changed text |
| Selective language coverage | Changed/diagnosed sentence IDs are recorded; untouched sentences are not described as checked |
| Exhaustive language coverage | One sentence reviewer per chunk; required terminology and specialist reviews may also run; every current sentence has a verdict; no skipped sentence completes |
| Version-1 artifact | Treated as closed history; fresh version-2 job starts with pending checks |
| Section edit | Global physics spine/object ledger inherited by every chunk |
| Direct canon coverage | Same editor checks every applicable canon principle; any additional candidate or authorized in-scope principle hit upgrades to reviewed; persistence depends on lifecycle rather than path |
| Terminology and notation | Output-only technical terms and symbols are replaced, defined and justified, or removed |
| Standing role-to-model policy | First reply states the active mapping and continues without requesting confirmation |
| No standing role-to-model policy | First reply asks for a role-to-model mapping and waits before substantive editing |
| Principle hit | One hit launches a whole-unit specialist for that principle or coupled group |
| Newly discovered source defect | Entire task pauses for the author's decision; no unrelated edits continue |
| Formal dependency | Formal reviewer certifies the declared changed, dependency-closure, or all-in-scope set |
| Resumable source recovery | Immutable original and current candidate are both present; hashes alone are insufficient |
| Context-only change | A context revision or applicable object-ledger revision invalidates dependent reviews even when text hashes match |
| Newly drafted passage | Every sentence counts as changed under selective coverage |
| Markdown physics note | Routes by sentence count and risk exactly like equivalent LaTeX prose |

Run the matrix on Cursor, Codex, and Claude Code where available. Retain compact
evidence: routing state, reviewer roles actually launched, axis result, and
final completion. Do not require host-specific artifacts for a direct edit.
