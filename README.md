# physics-paper-editing

Cursor skill for the **coworker-loop process**: draft a short LaTeX physics/mathematics passage into the file, background-check a frozen snapshot, merge. Conventions developed through work with Prof. Jens Koch.

**Canon** (what the prose should be) is the sibling skill [physics-paper-principles](https://github.com/Harrinive/physics-paper-principles). This skill does not restate those principles.

## What it does

This skill **decouples editing from verification**: the main agent writes a marked draft into your `.tex` immediately; separate subagents check a frozen snapshot in the background and flush findings to disk. You can keep editing. Each check round three-way-merges with your live text. The synthesizer sets a job-round status (`PASS` / `CONFLICTS` / `PARTIAL`) — it does not block the first write.

**Scope:** one short passage of **≤12 sentences**. For longer material, use the parent **section skill** [physics-paper-editing-section](https://github.com/Harrinive/physics-paper-editing-section).

## Install on [Cursor](https://cursor.com)

Requires [physics-paper-principles](https://github.com/Harrinive/physics-paper-principles) as a **sibling folder**. Install all three skills together (see the [Cursor Skills docs](https://cursor.com/docs/context/skills)):

```bash
git clone https://github.com/Harrinive/physics-paper-principles.git ~/.cursor/skills/physics-paper-principles
git clone https://github.com/Harrinive/physics-paper-editing.git ~/.cursor/skills/physics-paper-editing
git clone https://github.com/Harrinive/physics-paper-editing-section.git ~/.cursor/skills/physics-paper-editing-section
```

For a short-passage job only, the first two folders are enough. Whole-section edits also need the parent skill.

## Entry point

Read **`SKILL.md`** first, then [user-communication.md](user-communication.md) and [coworker-loop.md](coworker-loop.md). Linked detail files hold marks, merge, severity, and checker prompts. Drafting canon: sibling `../physics-paper-principles/`.

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

**Porter read order:** [SKILL.md](SKILL.md) → platform scaffold (item 2) → sibling [../physics-paper-principles/SKILL.md](../physics-paper-principles/SKILL.md) → parent [../physics-paper-editing-section/cross-skill.md](../physics-paper-editing-section/cross-skill.md) → [compliance-monitoring.md](compliance-monitoring.md). If using the parent too: sibling [physics-paper-editing-section/SKILL.md](../physics-paper-editing-section/SKILL.md) plus `disk-layout.md` / `session.md`.

1. Read `SKILL.md` and linked detail files to understand the workflow. Keep principles in the sibling skill — do not copy them into this one.
2. Invoke your platform's skill-creation guide (table above) — do not hand-roll folder layout.
3. **Map Cursor-only constructs** to your platform:
   - `AskQuestion` → job (polish/rewrite) only when unclear; inherit or default pace and models.
   - `Task` → delegation API; pass per-worker `model` when supported.
   - Linked principles → read/preload before drafting ([SKILL.md](SKILL.md) step 2).
4. **Verifier model profile** — preserve the gate and three verifier roles ([cross-skill.md](../physics-paper-editing-section/cross-skill.md) · [phase2-verify-subagents.md](phase2-verify-subagents.md)):
   - **Fast-tier model** — background changed-sentence Tasks.
   - **Deep** — narrative + math workers (one model, two roles).
   - **Deep synthesizer** — merges worker reports; **sole** grader of job-round `OVERALL`.
   - **Intake:** inherit models or use defaults; do not block every job on AskQuestion.
   - **Per-platform model assignment** (even within one vendor):
     - Cursor: `Task(model=…)` · SDK/automation: separate agent runs, one model each — no `Task` tool.
     - Claude Code: `Agent` frontmatter or invocation `model`.
     - Codex: `~/.codex/agents/*.toml` presets.
     - Copilot: `.agent.md` / `task(model=…)` (may be plan-guarded).
   - If runtime per-invocation pick isn't supported, use **named agent presets** instead of AskQuestion forms.
5. **Compliance chain** — orchestrator publishes Task plan → each worker Step 0 COMPLIANCE → synthesizer-only `OVERALL` ([compliance-monitoring.md](compliance-monitoring.md); **writer ≠ grader**).
6. Keep sibling install layout for principles + this skill (+ parent if used).
7. Test on a short LaTeX passage before relying on the full verifier pipeline.

## License

MIT — see [LICENSE](LICENSE).
