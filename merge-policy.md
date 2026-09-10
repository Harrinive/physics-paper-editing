# Merge policy

**For agents:** Start with [SKILL.md](SKILL.md) § Agent read order. Run once per check **round** after harvest ([coworker-loop.md](coworker-loop.md), [job-state.md](job-state.md)).

The producer applies this rubric to the file. The synthesizer classifies severity ([severity.md](severity.md)) and sets job-round `OVERALL`. The producer does **not** set `OVERALL`.

---

## Three-way merge

A round ends when the full wave completes **or** an interrupt harvest runs. Then exactly one write of the marked interior (`rev += 1`).

| Side | Source |
|------|--------|
| **Base** | `snapshot.tex` for this round |
| **Yours** | current marked interior (all user edits since that snapshot) |
| **Agent** | base + still-`valid` must-fix findings from `findings.jsonl` |

Split all three the same way ([sentence-check-subagents.md](sentence-check-subagents.md) §2). Align by label. If the user split or joined sentences, treat the overlapping span as one unit.

Do **not** patch the file each time a single checker finishes.

---

## Per-sentence action

| Situation | Action |
|-----------|--------|
| User did not touch the sentence; finding is a must-fix (`valid` BLOCKER) | **Auto-apply** the agent fix |
| Finding is construction-as-definition / missing physical lead ([severity.md](severity.md) math/narrative class 6), whether or not the user touched the sentence | **Do not apply.** Never invent an operational criterion at merge. Leave yours. Report **Need your call** |
| User made a reasonable edit (already fixed it, or an intentional rephrase that does not reintroduce the defect) | **Accept yours** |
| Minor conflict (style, equivalent wording, punctuation) | **Auto-resolve**; prefer yours when both are valid |
| Serious conflict (contradictory physics, sign/equation, changed claim or quantifier) | **Do not apply.** Leave yours. Report that sentence |

Stale findings never auto-apply on the new wording. They only inform the classifier (“the old wording had this defect”).

SUGGEST items never auto-apply and never create a decision.

---

## Serious vs minor vs reasonable

**Serious** (report, leave yours) — any of:

- Contradictory physics claim
- Sign, operator, or equation disagreement that changes the result
- Changed claim, quantifier, or scope word (*only / all / iff / necessary / sufficient / always* vs *may / can*)
- Notation that changes meaning (not a typo)
- Construction-as-definition / missing physical lead ([severity.md](severity.md) class 6) — always report; never auto-apply a guessed criterion

**Minor** (auto-resolve, prefer yours):

- Style, synonym, punctuation, discourse connective that does not change the claim
- Equivalent rephrase of the same physics

**Reasonable user edit** (accept yours):

- User already fixed the defect a different way
- User added a constraint or hedge they clearly intended
- User changed the claim **intentionally** (treat as serious only if a `valid` finding still contradicts the new claim — then report, do not revert)

When unsure whether a clash is serious, **leave yours** and report. Do not guess.

---

## After the write

1. Set BEGIN `status=checking` (or `conflict` if a serious item is waiting), `rev+=1`, `updated=<now>`. `created=` never changes.
2. Write a new snapshot + `sentences.json` from the **merged** interior.
3. Relaunch background checkers only for:
   - labels tagged `open` (never finished)
   - labels whose live hash is new (user or merge changed them)
4. Do **not** relaunch a label that is `valid`, finished, and unchanged by the merge.
5. If no Tasks remain and no open serious conflicts: **unmark**.
6. User-facing receipt: [user-communication.md](user-communication.md). Quote at most **one** serious conflict. Put CHECKS in the audit drawer.

---

## Synthesizer job-round `OVERALL`

| Result | When |
|--------|------|
| `PASS` | No unresolved must-fix on live text; no serious conflict waiting |
| `CONFLICTS` | At least one serious item reported to the user (including any physical-lead / construction-as-definition finding) |
| `PARTIAL` | Harvest after interrupt, or labels still `open`, and no `CONFLICTS` |

`FAIL` in old CHECKS maps to: procedural plan defect → relaunch that wave (fresh Tasks, do not block the user); content must-fix on **untouched** sentences → auto-apply then continue; content vs user → `CONFLICTS`.
