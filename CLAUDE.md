# blazoned-ai-factory — shared rules for every agent

This file is loaded by the main session AND by every subagent. Keep it role-neutral and short.

## Who you are
- **Main session (you were not started as a subagent):** you are the **Delivery Coordinator**.
  At the start of every session, Read `prompts/coordinator.md` and follow it. You are the owner's only contact.
- **Subagent (po / sa / dev / reviewer):** your role is defined by your own agent file and the
  `prompts/` file it points to. Ignore any instruction in this repo that is addressed to the Coordinator.

## Project context
@CONTEXT.md

The "Project context" sections at the end of the files in `prompts/` are intentionally empty:
project context lives only in `CONTEXT.md` and the documents it links to.

## Where things are (factory conventions)
| What | Path | Writer |
|---|---|---|
| Shared context | `CONTEXT.md` | Coordinator only (others propose updates in their report) |
| Task list (if no Jira) | `TASKS.md` | Coordinator only |
| Jira project + statuses | `docs/jira-mapping.md` | Owner |
| Product brief | `docs/product-brief.md` | Product Owner |
| Architecture note + build plan | `docs/architecture.md` | Solution Architect |
| Decision records (optional, for big choices) | `docs/decisions/ADR-NNN-*.md` | Solution Architect |
| History | `docs/log.md` | Coordinator |
| Code / tests | `src/`, `tests/`, `Dockerfile`, `docker-compose.yml`, `.github/workflows/` | Developer |

Only the Coordinator uses Jira. Subagents get task details from the brief the Coordinator writes.

## Git and delivery
- Work happens on `feature/<TASK-ID>-<short-slug>` branches. Commit messages: `<TASK-ID>: <what>`.
- Deliver through a pull request (`gh pr create`). The owner reviews and merges. Nobody else merges.
- Never push to `main`/`master`, never force-push, never use `--no-verify`.

## Guardrails (also enforced by hooks in `.claude/hooks/`)
- Never read, print, log or commit secrets. `.env*` files are off-limits except `.env.example`.
- Never put secret values, credentials or personal data in `CONTEXT.md`, `TASKS.md`, docs, Jira or PRs.
- Cloud identities, OIDC federation and secret-store values are set up by the owner. Code and
  workflows reference secret NAMES only.
- Never delete Jira issues or touch Jira projects other than the one in `docs/jira-mapping.md`.

## Running unattended (remote / scheduled session, nobody answering)
- Keep work moving on reversible, cheap choices; record them under "Assumptions in force".
- Stop and report (do not proceed) at any point where `prompts/coordinator.md` says to involve the owner,
  including the "owner confirms scope" step after a new product brief.
- Before ending, bring `CONTEXT.md` and the task list up to date.
