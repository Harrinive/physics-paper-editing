# Narrative checks

Use for anything longer than one standalone sentence: paragraph, subsection, section, or full paper.

**Scope the unit under review:** one paragraph → “the whole” means that paragraph; a section → that section; full paper → the paper. When a check needs broader context (e.g. vs abstract), read surrounding material first.

**Run all four groups and every bullet in order.** Name each group and bullet; state how it applies and whether it surfaces an issue. If N/A: **not applicable** and why.

---

## Group 1 — Core message and framing

- **Central message** — one clear takeaway per unit; flag missing or competing messages.
- **Framing alignment** — consistent with title, abstract, introduction, conclusion (for full paper: promise vs delivery).
- **Result framing and novelty** — main results highlighted vs supporting material; novelty vs prior work clear.

## Group 2 — Logical arc and motivation

- **Logical arc** — each part follows from what precedes; flag gaps, non-sequiturs, unmotivated steps.
- **Motivation and stakes** — problem and gap before heavy technical content; thread sustained.
- **Prose vs math** — language carries motivation, connections, physical interpretation, and understanding; math carries definitions, relations, and formal claims. Flag passages that describe in words what should be stated as math.
- **Signposting and transitions** — roadmaps, summaries, forward/back references; flag abrupt jumps. For references to equations, results, or conclusions across section/proof/paragraph boundaries, the text should remind readers what is being invoked; if that reminder is hard to phrase, flag the referenced item as too minor or too distant and consider reordering or moving the material closer.
- **Confusion-on-first-read ordering** — flag any sentence that confuses on first encounter because content is arranged in a reversed order (effect before cause, symbol before its definition, claim before its motivation). Severity depends on *when and how* the confusion is resolved; grade and act by tier:
  - **Tier 1 — deferred & flagged:** the confusion is acknowledged in place and explicitly promised a later resolution (e.g. “⟨confusing part⟩. We show this in the following paragraph.”). Low harm; acceptable as is, but prefer a rearrangement that removes the confusion *if it does not disturb the narrative*.
  - **Tier 2 — resolved next sentence:** the confusion is cleared immediately afterward (e.g. an undefined symbol followed by a long explanation instead of a short `where` clause; or a high-level/unmotivated claim followed by its justification or relevance). Mild but must be tightened — prefer a short `where`-clause, reorder so the definition/motivation precedes use, or compress.
  - **Tier 3 — never resolved / resolved much later:** the reader is left hanging or the resolution appears far away (e.g. notation explained only sections later, or not at all). Very harmful — resolve immediately by defining/motivating before use or moving the resolution adjacent.

## Group 3 — Consistency and economy

- **Cross-part consistency** — notation, terminology, claims; promises paid off.
- **Redundancy and balance** — no purposeless repetition; length matches importance; right section vs appendix.

## Group 4 — Claims and audience

- **Scope of claims** — conclusions match evidence; limitations acknowledged; no over- or under-claiming.
- **Audience and entry points** — background introduced before use; flag prerequisites assumed too early.
