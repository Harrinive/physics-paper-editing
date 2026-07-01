# physics-paper-editing

Agent Skill for editing LaTeX physics and mathematics prose at graduate level.

**Scope:** one passage of **≤12 sentences**. Passages longer than 12 sentences should use the companion [physics-paper-editing-section](https://github.com/Harrinive/physics-paper-editing-section) skill instead.

## What it does

Runs a **two-phase verification pipeline** on LaTeX prose:

1. **Phase 1 (source verify)** — audit the user's existing prose before editing (polish path only).
2. **Phase 2 (output verify)** — independent verifier subagents grade the producer's draft before shipping.

The producer writes the draft and applies fixes; it does not grade its own output.

## Install (Cursor)

```bash
git clone https://github.com/Harrinive/physics-paper-editing.git ~/.cursor/skills/physics-paper-editing
```

For whole-section edits, also install the macro skill as a **sibling folder**:

```bash
git clone https://github.com/Harrinive/physics-paper-editing-section.git ~/.cursor/skills/physics-paper-editing-section
```

Both skills use relative cross-links (`../physics-paper-editing/`, `../physics-paper-editing-section/`). They resolve only when installed as siblings under the same parent directory.

## Entry point

Read **`SKILL.md`** first. Linked detail files (`gate.md`, `phase2-verify-subagents.md`, etc.) hold the full rules.

---

## Not Cursor? Adapt this skill

**This skill was authored for Cursor Agent.** It references Cursor-specific tools (`AskQuestion`, `Task` subagents, compliance monitoring). Do not run it verbatim on other platforms — **adapt it** to your agent's tool surface and install layout.

### How to adapt

Use your platform's skill-creation workflow first, then port the workflow logic (not copy-paste paths):

| Platform | Install path (typical) | Use this to adapt |
|----------|------------------------|-------------------|
| **Cursor** | `~/.cursor/skills/<name>/` | [Cursor Skills docs](https://cursor.com/docs/context/skills) — or run `/create-skill` in Agent chat |
| **Claude Code** | `~/.claude/skills/<name>/` or `.claude/skills/<name>/` | [Claude Code skills docs](https://code.claude.com/docs/en/skills) |
| **OpenAI Codex** | `~/.codex/skills/<name>/` or `~/.agents/skills/<name>/` | [Codex Agent Skills](https://developers.openai.com/codex/skills) — run **`$skill-creator`** in Codex to scaffold the port |
| **GitHub Copilot** | `~/.copilot/skills/<name>/` or `.github/skills/<name>/` | [Copilot: add skills](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) |
| **Any agent (format reference)** | varies | [Agent Skills open spec](https://agentskills.io/specification) — shared `SKILL.md` frontmatter + body structure |

### Adaptation checklist

1. Read `SKILL.md` and linked detail files to understand the workflow.
2. Invoke your platform's skill-creation guide (table above) — do not hand-roll folder layout.
3. Map Cursor-only constructs: `AskQuestion` → interactive prompts; `Task` subagents → your platform's subagent/delegation model; `.physics-edit/` disk state paths → equivalent session storage.
4. Keep sibling install layout if using both micro + macro skills (`../physics-paper-editing/` links).
5. Test on a short LaTeX passage before relying on the full verifier pipeline.

## License

MIT — see [LICENSE](LICENSE).
