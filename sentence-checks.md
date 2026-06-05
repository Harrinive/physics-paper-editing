# Sentence-level checks

Apply to standalone sentences and local passages. **Run every objective below in order.** Name each objective, state how it applies, and report issues. If one does not apply, say **not applicable** and why.

Do not skip, merge, or abbreviate objectives.

| # | Objective |
|---|-----------|
| 1 | **Clarify local references** — every pronoun (“it”, “which”, “this”, …) points to a specific noun; short back-references tie unambiguously to the concept they invoke. |
| 2 | **Clarify cross-boundary references** — for equation/result/conclusion references across an obvious boundary (section, proof, paragraph block, etc.), remind the reader what the referenced item says or does, not just its label. If that reminder is awkward or hard to state, flag that the reference may be too minor or too distant, suggesting reordering or moving the referenced material closer. |
| 3 | **Define or replace undefined terminology** — non-standard terms are defined on first use or replaced with standard equivalents. Do not coin labels when a plain description suffices (e.g. “operator that annihilates the code space” vs “null branch”). Name a term only if standard in the field or if it recurs enough to warrant a definition (then define on first use). |
| 4 | **Fix subject–verb–object mismatches** — grammatical agreement and semantic fit, including inside clauses (e.g. states do not “yield” results; a model does not “prove” a conclusion). |
| 5 | **Streamline narrative** — coherent flow between sentences; remove redundant phrases or nouns that signal convoluted logic. |
| 6 | **Polish non-native wording** — concise, idiomatic English; preserve meaning and technical accuracy. |
| 7 | **Balance rigor with narrative** — state physical/mathematical facts as givens, not conditional premises (“Because X is Y, …” not “If X is Y, then …” when X is established). |
| 8 | **Minimal changes** — edit only what clarity and flow require; substantial reordering only with explicit user instruction. |
| 9 | **Prefer active voice** unless passive improves clarity. |
| 10 | **Rewrite “For A, it does B”** — find this structure and rewrite as “A does B”. |
| 11 | **Let physics tell the story** — give math objects physical meaning where possible; avoid math that reads detached from the physics question. |
| 12 | **Use math for math** — reserve prose for motivation, connections, physics, and understanding; use equations and formal notation for definitions, relations, and claims. Flag sentences that paraphrase math in words when the content belongs in math. |
| 13 | **Confusion-on-first-read ordering** — flag sentences that confuse on first encounter due to reversed arrangement (symbol before definition, claim before motivation, effect before cause). Grade by when the confusion resolves: deferred & explicitly flagged (low — rearrange only if narrative-neutral); resolved in the next sentence (mild — tighten via a short `where`-clause or reorder so definition/motivation precedes use); resolved far later or never (severe — resolve immediately). |
