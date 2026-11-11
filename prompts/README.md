# Role prompts (owner-maintained)

| File | Used by |
|---|---|
| `coordinator.md` | main session (CLAUDE.md tells it to read this) |
| `po.md` | `.claude/agents/po.md` |
| `sa.md` | `.claude/agents/sa.md` |
| `dev.md` | `.claude/agents/dev.md` |

These are used unchanged. Factory mechanics (file paths, git/PR rules, how to return questions)
live in `.claude/agents/*.md` and `CLAUDE.md`, so these files can stay generic across projects.
Leave the "Project context" sections empty; project context lives in `CONTEXT.md`.
If a prompt here conflicts with the guardrails in CLAUDE.md, the guardrails win.
