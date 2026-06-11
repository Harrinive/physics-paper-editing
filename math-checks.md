# Math and logic checks

Use whenever the text has mathematical objects, equations, or logical arguments — any length. Consider the snippet plus surrounding and earlier paper text.

**Who runs this file:**

| Phase | Runner | Scope |
|-------|--------|-------|
| **Phase 1** | Main agent after sentence work ([verification-loop.md](verification-loop.md)) | Full passage under edit |
| **Phase 2** | Math **verifier** Task — producer **never** inline ([phase2-verify-subagents.md](phase2-verify-subagents.md)) | **Always** full passage |

**Run Step 0 first, then the checks for each statement's type. Name every check; state how it applies and whether it surfaces an issue. If N/A: not applicable, and why.**

---

## Step 0 — Classify each math statement

For every definition, condition, equation, lemma, theorem, or model in the passage, state its type explicitly before running checks. A statement can be dual-typed (run both check sets):

| Type | Description | Criterion to verify |
|------|-------------|---------------------|
| **Derived** | Follows from earlier statements by logical deduction. | Rigor — is the conclusion forced by the premises? |
| **Posited** | Given as a starting point: definitions, conditions, models, axioms. | Faithfulness — does the formula encode the stated intent? |
| **Imported** | Cited result, experimental fact, or conjecture from outside the paper's deductive chain. | Provenance — is the source identified, applicable, and correctly invoked? |
| **Convention choice** | A choice among equivalent alternatives: canonical representative, gauge/basis fixing, sign or normalization convention. | Legitimacy — does the choice exist, and are downstream results independent of it? |

---

## Type 1 checks (Derived)

Run every check below in order.

| Check | What to verify |
|-------|----------------|
| **Scope and well-definedness** | Objects defined before use; choices canonical or justified; existence/uniqueness clear; domains and ranges stated or obvious. |
| **Logical completeness** | No unjustified leaps; conclusions do not need unstated assumptions. |
| **Definitions and notation** | No symbol overload; definitions not silently changed; local notation matches global conventions. |
| **Quantifiers and generalizations** | "For all …" backed for all cases, not only examples. |
| **Implicit assumptions** | Commutativity, invertibility, finiteness, independence, etc. declared where needed. |
| **Direction of implications** | "If and only if" vs "if"; equivalences bidirectional when claimed; conclusion follows from premises. |
| **Circular reasoning** | No claim used in its own justification. |
| **Consistency with earlier results** | No contradiction with prior definitions, lemmas, or claims in the paper. |

---

## Type 2 checks (Posited)

Posited statements must be purpose-first: intent → natural-language statement → formalization. Run every check below in order.

| Check | What to verify |
|-------|----------------|
| **Negative-space question** | What pathology does this condition exclude? Name it in words. If it cannot be named, the intent is not yet understood — flag and ask the author. |
| **First-use test** | Where is this statement first used downstream? The motivation should foreshadow that use. If the gap is large, consider moving the statement adjacent to its first use. |
| **Back-translation flag** | Does the motivating prose read as a literal gloss of the formula's syntax ("for every … there exists …")? If so, flag it: the prose was likely back-translated from the formula rather than written from intent. Intent must be expressible symbol-free. |
| **Round-trip test** | Formalize the natural-language sentence alone, without looking at the actual formula. Compare. Any mismatch (different quantifier order, different inclusion direction, different domain) means the prose is unfaithful. Fix the prose, not the formula. |
| **Quantifier audit** | Verify quantifier order matches intent (∀∃ vs ∃∀ are different conditions). Check that ∝ excludes zero, that existential witnesses are nontrivial (no empty sets, no trivially satisfying objects). |
| **Ordering in the text** | Motivation must appear before formalization. A formula introduced before its purpose is explained is a Tier-3 confusion-on-first-read problem (see narrative-checks.md). |

**Worked example — QEC consistency condition**

*Setup.* A QEC code encodes a qubit into a physical Hilbert space \(\mathcal{H}\) with code space \(\mathcal{H}_\mathrm{L} = \mathrm{span}\{\ket{0_\mathrm{L}}, \ket{1_\mathrm{L}}\}\). A QEC protocol measures syndrome operators \(\{\hat{S}_i\}\), obtains syndrome \(\mathbf{s}\), projects to the simultaneous eigenspace \(\mathcal{H}_\mathbf{s} = \hat{P}_\mathbf{s}\mathcal{H}\), and applies a recovery unitary \(\hat{R}_\mathbf{s}\) for each syndrome \(\mathbf{s}\) in a designated set \(\mathbb{S}\). An error \(\hat{E}\) is \(\mathfrak{Q}\)-correctable if \(\hat{R}_\mathbf{s}\hat{P}_\mathbf{s}\hat{E}\ket{\psi} \propto \ket{\psi}\) for all \(\ket{\psi} \in \mathcal{H}_\mathrm{L}\) and all \(\mathbf{s}\) reached by \(\hat{E}\).

*Original passage (two sentences):*
> "We require that the protocol \(\mathfrak{Q}\) is consistently defined: each recovery operator \(\hat{R}_\mathbf{s}\) indeed maps the post-measurement states back to the logical space. Formally, for every \(\mathbf{s}\in\mathbb{S}\) and every logical state \(\ket{\phi}\in\mathcal{H}_\mathrm{L}\), there exists a post-measurement state \(\ket{\chi}\in\mathcal{H}_\mathbf{s}\) such that \(\hat{R}_\mathbf{s}\ket{\chi}=\ket{\phi}\)."

*Type classification:* **Posited** (defining which protocols are of interest).

*Applying the checks:*

- **Negative-space question:** The condition should exclude protocols that carry a dead recovery — a specified \(\hat{R}_\mathbf{s}\) for a syndrome \(\mathbf{s}\) that no correctable error ever triggers. The prose says nothing about this. ❌
- **First-use test:** The condition is used to show the canonical error \(\hat{F}_\mathbf{s} = \hat{R}_\mathbf{s}^\dagger\hat{P}_\mathrm{L}\) is itself \(\mathfrak{Q}\)-correctable. The prose gives no hint of this payoff. ❌
- **Back-translation flag:** The prose "each recovery operator maps post-measurement states back to the logical space" is a back-translation of the ∀∃ quantifier pattern. The word "maps" suggests \(\hat{R}_\mathbf{s}\mathcal{H}_\mathbf{s} \subseteq \mathcal{H}_\mathrm{L}\) (forward inclusion), but the formula says \(\mathcal{H}_\mathrm{L} \subseteq \hat{R}_\mathbf{s}\mathcal{H}_\mathbf{s}\) (reverse inclusion — every logical state has a pre-image in \(\mathcal{H}_\mathbf{s}\)). These differ when \(\dim\mathcal{H}_\mathbf{s} > \dim\mathcal{H}_\mathrm{L}\), which is the generic case. The prose is unfaithful. ❌
- **Round-trip test:** A naive reader formalizes the prose as \(\hat{R}_\mathbf{s}\mathcal{H}_\mathbf{s} \subseteq \mathcal{H}_\mathrm{L}\), not the ∀∃ formula given. ❌
- **Quantifier audit:** The formula \(\forall\mathbf{s}\,\forall\ket{\phi}\,\exists\ket{\chi}\) is the reverse-inclusion condition, not the exclusion of dead recoveries. The actual intent ("every \(\hat{R}_\mathbf{s}\) is exercised by some correctable error") is \(\forall\mathbf{s}\in\mathbb{S},\,\exists\hat{E}\in\mathbb{E}_\mathfrak{Q}\) with \(\mathbf{s}\in\mathbb{S}_{\hat{E}}\) — a different quantifier structure. ❌
- **Ordering:** The definition appears before \(\mathfrak{Q}\)-correctability is defined, so the condition cannot be stated in terms of correctable errors. The statement falls from the sky. ❌

*Purpose-first fix:* Define \(\mathfrak{Q}\)-correctable errors first. Then motivate: "not every recovery is of interest — a protocol could specify \(\hat{R}_\mathbf{s}\) for a syndrome that no correctable error triggers. We restrict to *consistent* protocols, where every specified recovery is exercised." State the condition: for every \(\mathbf{s}\in\mathbb{S}\), there exists \(\hat{E}\in\mathbb{E}_\mathfrak{Q}\) with \(\mathbf{s}\in\mathbb{S}_{\hat{E}}\). The operator form \(\hat{P}_\mathbf{s}\hat{R}_\mathbf{s}^\dagger\hat{P}_\mathrm{L}=\hat{R}_\mathbf{s}^\dagger\hat{P}_\mathrm{L}\) is then a *derived* equivalent form (Lemma), not a posited one.

---

## Type 3 checks (Imported)

Run every check below in order; escalate when verification is not possible.

| Check | What to verify |
|-------|----------------|
| **Citation present** | A citation is attached to the statement. Flag any uncited import — treat it as unverified until sourced. |
| **Hypotheses satisfied** | The source theorem's hypotheses hold in the present setting. Flag mismatches (e.g., finite vs. infinite dimension, bounded vs. unbounded operators, real vs. complex field). |
| **Notation translation** | Differences between the source's notation and the paper's notation are stated or obvious; no silent relabeling that changes meaning. |
| **Status match** | The statement is presented at the same strength as in the source: a conjecture or numerical observation is not presented as an established result. |
| **Verification** | If the cited source is accessible (DOI, arXiv, standard textbook), fetch or search it and confirm the statement appears as claimed. If not accessible, record the result as **user-trusted** in the check report and ask the author to confirm. Never silently trust an unverifiable import. |

---

## Type 4 checks (Convention choice)

Run every check below in order.

| Check | What to verify |
|-------|----------------|
| **Framed as a choice** | The text uses language like "we choose", "fix", "without loss of generality", or "for definiteness" — not language that asserts a unique fact. |
| **Existence** | The object being chosen exists (the equivalence class is nonempty; the canonical form is achievable). |
| **Independence** | Downstream results do not depend on the choice, or the dependence is explicitly tracked. "Without loss of generality" claims are justified. |
| **Uniformity** | The convention is applied consistently throughout; any deviation from the field's standard convention is flagged to the reader. |
