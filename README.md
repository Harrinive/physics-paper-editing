# physics-paper-editing

Portable Agent Skill for a draft-first LaTeX physics and mathematics editing
loop. It writes a marked short passage, independently verifies a frozen
snapshot, and merges one round at a time. The prose canon is the sibling
[physics-paper-principles](https://github.com/Harrinive/physics-paper-principles).

**Scope:** one passage of at most 12 typographic sentences. For longer material,
install and use [physics-paper-editing-section](https://github.com/Harrinive/physics-paper-editing-section).

## Install

Clone the three public repositories as siblings. The canonical portable layout
is `~/.agents/skills/`; each host may also support its own discovery path.

```bash
git clone https://github.com/Harrinive/physics-paper-principles.git ~/.agents/skills/physics-paper-principles
git clone https://github.com/Harrinive/physics-paper-editing.git ~/.agents/skills/physics-paper-editing
git clone https://github.com/Harrinive/physics-paper-editing-section.git ~/.agents/skills/physics-paper-editing-section
```

The principles and this skill are sufficient for a short passage. The section
skill is required for whole sections or longer passages.

## Runtime support

The workflow core follows the [Agent Skills specification](https://agentskills.io/specification).
Select the adapter that matches the active host before delegating verification:

| Host | Adapter |
|------|---------|
| Cursor | [runtime-cursor.md](runtime-cursor.md) |
| OpenAI Codex | [runtime-codex.md](runtime-codex.md) |
| Claude Code | [runtime-claude.md](runtime-claude.md) |

The shared [runtime contract](runtime-contract.md) defines the model profile,
capability fallbacks, result shards, and resume semantics. It is the source of
truth; do not fork the workflow per host.

Use the [portability test matrix](portability-test-matrix.md) when validating a
host update or adapter change.

## Entry point

Read [SKILL.md](SKILL.md), then [user-communication.md](user-communication.md)
and [coworker-loop.md](coworker-loop.md). Before the first top-level editing
session, obtain one model-profile choice: accept the role-based profile, use
the parent model for all verifier roles, or supply custom mappings. The selected
adapter resolves and records actual model identifiers.

## License

MIT — see [LICENSE](LICENSE).
