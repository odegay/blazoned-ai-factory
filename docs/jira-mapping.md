# Jira mapping — FILL THIS IN (owner)

Leave the project key as `NONE` to track tasks in TASKS.md instead.

- Jira site: https://<your-site>.atlassian.net
- Project key: NONE
- Issue type for tasks: Task (Bug for bugs)

## Statuses (use your workflow's exact names)
| Meaning      | Jira status |
|--------------|-------------|
| Todo         | To Do       |
| Doing        | In Progress |
| Blocked      | Blocked (or label `blocked` if no such status) |
| Owner review | In Review   |
| Done         | Done        |

## Role labels
`role-po`, `role-sa`, `role-dev`, `role-owner` (a decision is waiting on the owner)

## Phases
Grouping: Epic   (Epic | Label; use Label if the project has no epics)

| Phase   | Epic name | Label         |
|---------|-----------|---------------|
| PoC     | PoC       | phase-poc     |
| MVP     | MVP       | phase-mvp     |
| Not now | Not now   | phase-not-now |

## Ordering
- Backlog rank follows the build-plan order; the Coordinator keeps it current.
- Dependencies: issue link type `Blocks` (use your site's exact link name).
