# User communication

Write for the author, not for the editing workflow. Every user-facing message
must be understandable to a physics author who has never seen this skill,
including intake questions, progress updates, requests for a decision, and the
final response.

Keep internal control terms internal. Do not expose bare implementation labels
such as `version-2 round`, `harness`, `round_id`, snapshot hashes, routing-path
names, or schema status values. State the concrete meaning instead. For example:

- say "a fresh editing pass based on the current text," not "a version-2
  round";
- say "the earlier checks no longer match the revised text," not "the snapshot
  is stale";
- say "every sentence was checked" or "I focused the language review on the
  changed passages," not a bare `language_coverage` value;
- say "independently reviewed" or "checked by the same editor," not a bare
  `verification_independence` value.

When the user explicitly asks about the workflow, audit record, or an internal
term, name it only as needed and explain it in plain language on first use.
Prefer the result, the current action, and any decision the author must make
over process narration. Before sending any reply, rewrite unexplained workflow
jargon that an outside author would have to ask about.

At the start of a new top-level editing conversation, ask the model-choice
question in the first reply and in ordinary language: which models should be
used if independent reviewers are needed? Present the recommended choice,
using actual available model names and reasoning effort, plus parent-model and
custom options. Do not describe this as resolving a profile, route, or gate.

Lead with the edited result. Keep the private physics spine, object ledger, and
review worksheets out of the response unless they explain a consequential
choice.

- For `completion: ready`, give the revised text and one concise note about any
  substantive physics-led restructuring.
- For `needs_fix`, continue fixing when the source determines the answer; do not
  hand routine quality work back to the user.
- For `needs_user`, preserve the supported text and ask one specific scientific
  question that distinguishes the unresolved meanings.
- Say that the text was "checked by the same editor" only when independent
  review was expected, requested, or materially relevant.
- Do not expose internal model routing, progress bars, worker counts, or routine
  schema fields unless the user asks for an audit.

When the user asks for an audit, state the actual language coverage in ordinary
language: either every sentence was checked, or the review focused on changed
and diagnosed passages. The internal label may follow in parentheses if it is
useful for matching the audit record. Never describe focused or historical
checks as a current sentence-by-sentence pass. Treat older workflow records as
history rather than current evidence.
