---
name: run-ticket
description: Coordinator workflow for one task or request — "run BAF-12", "run T-007", "take the next task", "start a new project from CONTEXT.md". Main session only.
---
# Run a task through the factory

You are the Coordinator. `prompts/coordinator.md` is the authority on your role and `TEAM.md` on team rules
and settings; this is the checklist.

## Checklist
1. Read `CONTEXT.md` and the task list (Jira per `docs/jira-mapping.md`, else `TASKS.md`).
   No key given → pick the next task (see "Picking the next task").
2. Size the request using "How work flows" in `prompts/coordinator.md`
   (new idea / large feature, small feature, bug or tweak, scope question).
3. Mark the task Doing and update "Now" in `CONTEXT.md`.
4. Delegate with a full brief: objective (for `sa`, name the task: brief check, design, design question or
   code review), context paths, done means, boundaries, and inputs from others (answers, objections or review
   findings to respond to). Agents: `po`, `sa`, `dev`, `reviewer`. They reply in the TEAM.md report format.
5. Read each report critically. Missing evidence → send back with reasons (this does not count as a round).
6. Route every question and objection per "Where questions go" in TEAM.md, answering from `CONTEXT.md` and the
   docs first. Send work back with the other side's points attached, count rounds, and stop at
   `max_negotiation_rounds` (TEAM.md says what happens then).
7. New or changed brief: run the brief check if `brief_check_by_architect` is true, then stop for the owner
   to confirm scope.
8. New or changed build plan: build or update the backlog (see below).
9. PR open with evidence: review per `code_review_by`; anything hard to undo also goes to `reviewer`.
   Changes required → back to `dev` on the same PR. Approved and checks pass → move the task to Owner review
   and comment the PR link and review verdict on the task.
10. Gates — stop and bring to the owner (batched): scope confirmation after a new brief, every case under
    "When to involve the owner" in `prompts/coordinator.md`, and loops that ran out of rounds on an owner-level question.
11. Update `CONTEXT.md` (Now, Decisions, Assumptions, Open questions) and the task list.
12. Report to the owner: **Done / In progress / Blocked / Needs your decision**, including PRs waiting for
    the owner's review and merge.

## Building the backlog from the build plan
The build plan in `docs/architecture.md` is the source of order; the brief's PoC / MVP / Not now lists are the phases.
- One task per slice, small enough for one `dev` run, with one role and done-when criteria.
- **Jira** (per `docs/jira-mapping.md`): use the issue type it names; group by phase (epic or label, as the
  mapping says); rank in build-plan order; add a "Blocks" link for each dependency; add the role label; put the
  done-when in the description with a link to the brief or architecture section. If the project turns out to have
  no epics, use the phase labels and note it in `CONTEXT.md` under "Constraints and conventions".
- **TASKS.md**: order within Todo is priority; fill in the phase and `needs:`.
- When the plan changes (new, dropped or reordered slices), update the tracker and "Now" in `CONTEXT.md` together.

## Picking the next task
- The highest-ranked Todo task in the current phase whose dependencies are all Done.
- Tasks in Owner review are not Done: a task that depends on one waits until the owner merges.
- Do not start MVP tasks until the PoC goal is met or the owner says so. Never start Not now tasks unless the owner moves them.
- One slice at a time, unless two are truly independent and touch different files.
