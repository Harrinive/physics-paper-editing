# Mathematical and Logical Rigor Checks

Use these whenever the text under review contains mathematical objects, equations, or logical arguments — at any length, from a single equation-bearing sentence to a full proof or a whole paper. Consider not just the snippet in isolation, but also the surrounding and preceding text (and, where relevant, earlier parts of the paper).

**You must run every check below, in order.** Name each one explicitly, state how it applies, and report whether it surfaces an issue. Do not skip, merge, or abbreviate any point; if one does not apply, write "not applicable" and why.

- **Scope and well-definedness of variables and objects** — every mathematical object (set, operator, function, index, register, etc.) must be defined before first use. Check whether objects are well-defined: do they depend on choices that haven't been shown to be canonical or independent of those choices? Are existence and uniqueness established (explicitly or by clear appeal to a known result)? Are domains, codomains, and ranges stated or clear from context?

- **Logical completeness of arguments** — identify any implicit logical leaps: steps asserted without justification that go beyond what has been established. Flag claims that are presented as conclusions but require additional assumptions not stated in the paper.

- **Consistency of definitions and notation** — check that the same symbol isn't used for two different objects (even in different sections), that definitions are not silently extended or modified, and that notation introduced locally is consistent with the paper's global conventions.

- **Validity of quantifiers and generalizations** — check whether universal claims ("for all …") are actually proved for all cases, or only demonstrated for special cases. Flag overgeneralizations.

- **Implicit assumptions** — identify any assumption that is being made but not declared (e.g., commutativity, invertibility, finiteness, independence). Flag cases where the argument would fail if the assumption were dropped.

- **Direction of implications** — verify that "if and only if" is used correctly versus "if"; that equivalences are truly bidirectional when claimed; that the conclusion actually follows from the stated premises (and not the reverse).

- **Self-referential or circular reasoning** — check whether a claim is used in its own justification.

- **Consistency with earlier results** — flag any statement that appears to contradict or be inconsistent with a definition, lemma, or claim established earlier in the paper, even if individually the sentence reads fine.
