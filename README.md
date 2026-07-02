# physics-paper-editing

Cursor skill for graduate-level LaTeX editing in physics and mathematics papers. Its checks and workflows reflect editing conventions developed through work with Prof. Jens Koch.

## What it does

This skill **decouples editing from verification**: the main agent rewrites your LaTeX passage and applies fixes; separate subagents check the draft against the style guide and return a pass/fail verdict. That split keeps quality review independent of the draft. On a failing verdict, the producer revises and verification runs again—iteration continues until the draft passes.

**Scope:** one short passage of **≤12 sentences**. For longer material, use the companion **macro skill** [physics-paper-editing-section](https://github.com/Harrinive/physics-paper-editing-section).

## Install on [Cursor](https://cursor.com)

Clone into your skills directory (see the [Cursor Skills docs](https://cursor.com/docs/context/skills) for more details) with the following command:
```bash
git clone https://github.com/Harrinive/physics-paper-editing.git ~/.cursor/skills/physics-paper-editing
```

For whole-section edits, also install the macro skill as a **sibling folder**:
```bash
git clone https://github.com/Harrinive/physics-paper-editing-section.git ~/.cursor/skills/physics-paper-editing-section
```

## Entry point

Read **`SKILL.md`** first. Linked detail files (`gate.md`, `phase2-verify-subagents.md`, etc.) hold the full rules.

---

## Not Cursor? Adapt this skill

**This skill was made for Cursor Agent.** It references Cursor-specific tools (`AskQuestion`, `Task` subagents, compliance monitoring). Do not run it verbatim on other platforms — **adapt it** to your agent's tool surface and install layout.

### How to adapt

Use your platform's skill-creation workflow first, then port the workflow logic (not copy-paste paths):

| Platform | Install path (typical) | Use this to adapt |
|----------|------------------------|-------------------|
| **Cursor** | `~/.cursor/skills/<name>/` | [Cursor Skills docs](https://cursor.com/docs/context/skills) — or run `/create-skill` in Agent chat |
| **Claude Code** | `~/.claude/skills/<name>/` or `.claude/skills/<name>/` | [Claude Code skills docs](https://code.claude.com/docs/en/skills) |
| **OpenAI Codex** | `~/.agents/skills/<name>/` or `.agents/skills/<name>/` (`~/.codex/skills/` legacy) | [Codex Agent Skills](https://developers.openai.com/codex/skills) — run **`$skill-creator`** in Codex to scaffold the port |
| **GitHub Copilot** | `~/.copilot/skills/<name>/` or `~/.agents/skills/<name>/`; project: `.github/skills/<name>/` or `.agents/skills/<name>/` | [Copilot: add skills](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) |
| **Any agent (format reference)** | varies | [Agent Skills open spec](https://agentskills.io/specification) — shared `SKILL.md` frontmatter + body structure |

### Adaptation checklist

1. Read `SKILL.md` and linked detail files to understand the workflow.
2. Invoke your platform's skill-creation guide (table above) — do not hand-roll folder layout.
3. Map Cursor-only constructs: `AskQuestion` → user-choice hard stops; `Task` → delegation API + per-worker `model` when supported; linked checklists → read/preload before gates (`SKILL.md` “Read with the Read tool”).
4. **Verifier model profile** — preserve the gate and three roles in `cross-skill.md` / `phase2-verify-subagents.md` (fast sentence · deep narrative+math · deep synthesizer; no verifier until user confirms slugs). Per-subagent models are platform-specific even within one vendor — e.g. Cursor `Task(model=…)`; Claude Code `Agent` frontmatter or invocation `model`; Codex `~/.codex/agents/*.toml` presets; Copilot `.agent.md` / `task(model=…)` (may be plan-guarded). If runtime per-invocation pick isn't supported, use named agent presets instead of AskQuestion forms. Cursor SDK/automation: separate agent runs, one model each — no `Task` tool.
5. **Compliance chain** — Task plan → worker Step 0 COMPLIANCE → synthesizer-only `OVERALL` (`compliance-monitoring.md`; writer ≠ grader).
6. Keep sibling install layout if using both micro + macro skills (`../physics-paper-editing/` links).
7. Test on a short LaTeX passage before relying on the full verifier pipeline.

## License

MIT — see [LICENSE](LICENSE).
