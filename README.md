# blazoned-ai-factory

Claude Code agent factory. The **Coordinator** is the main session and your only contact. It delegates to
**po**, **sa**, **dev** and **reviewer** subagents, tracks tasks in Jira or `TASKS.md`, and delivers through GitHub PRs.
It runs locally or as Claude Code cloud sessions.

## Layout
```
CLAUDE.md                 shared, role-neutral rules (loaded by every agent) + imports CONTEXT.md
CONTEXT.md                project context (Coordinator is the only writer)
TASKS.md                  task list when no Jira project is set
prompts/                  YOUR role prompts, used unchanged (coordinator, po, sa, dev)
.claude/agents/           subagent wrappers: tools, model, file paths, how to return questions
.claude/settings.json     permissions + hooks
.claude/hooks/            guard_bash.py, guard_files.py, guard_mcp.py
.claude/skills/run-ticket Coordinator checklist ("run BAF-12", "take the next task")
.mcp.json                 Atlassian MCP for local CLI use
docs/                     product-brief.md, architecture.md, decisions/, log.md, jira-mapping.md
.github/                  CI guardrails (gitleaks + tests), PR template, CODEOWNERS
scripts/                  cloud-setup.sh (cloud environment), protect-main.sh (run once)
```

## Use
- Local: run `claude` in the repo, then say "run BAF-12", "take the next task", or describe a new idea.
- Remote: `claude --remote "take the next task"`, or start a session at claude.ai/code or in the mobile app.
- Recurring: `/schedule`, e.g. "weekdays 7am: take the next task".

## Personal overrides (not committed)
- `.claude/settings.local.json` for your extra permissions
- `CLAUDE.local.md` for personal notes to the Coordinator

## Start a new project from this template
This repo is a generic bootstrap: it holds no project data. For each new project:
1. Create a repo from it (GitHub "Use this template") and clone it.
2. Fill in the per-project files: `CONTEXT.md`, `docs/jira-mapping.md` (or keep `NONE` to use `TASKS.md`),
   and `.github/CODEOWNERS` (your GitHub username).
3. Run once: `bash scripts/protect-main.sh <owner>/<repo>` and `pre-commit install`.
4. Connect Jira (claude.ai Atlassian connector for cloud sessions, `/mcp` locally) and, for remote runs,
   `/web-setup` + a cloud environment using `scripts/cloud-setup.sh`.
5. Keep project repos private if CONTEXT.md, briefs or task notes contain real business context.

Factory files (`CLAUDE.md`, `prompts/`, `.claude/`, `.github/workflows/`, `scripts/`) are shared:
improve them here, then copy the changes into project repos.

## License
MIT, see [LICENSE](LICENSE). You may use, modify and redistribute this factory, but every copy or
substantial portion must keep the copyright notice crediting Oleg (https://github.com/odegay).
