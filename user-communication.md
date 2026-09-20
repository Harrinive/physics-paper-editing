# User communication

Lead with the edited result. Keep the private physics spine, object ledger, and
review worksheets out of the response unless they explain a consequential
choice.

- For `completion: ready`, give the revised text and one concise note about any
  substantive physics-led restructuring.
- For `needs_fix`, continue fixing when the source determines the answer; do not
  hand routine quality work back to the user.
- For `needs_user`, preserve the supported text and ask one specific scientific
  question that distinguishes the unresolved meanings.
- Mention `verification_independence: self_only` only when independent review
  was expected, requested, or materially relevant.
- Do not expose internal model routing, progress bars, worker counts, or routine
  schema fields unless the user asks for an audit.

Legacy version-1 jobs retain their original communication contract under
[legacy-v1/user-communication.md](legacy-v1/user-communication.md).
