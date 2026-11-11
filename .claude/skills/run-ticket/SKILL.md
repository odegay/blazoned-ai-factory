---
name: run-ticket
description: Coordinator workflow for one task or request — "run BAF-12", "run T-007", "take the next task", "start a new project from CONTEXT.md". Main session only.
---
# Run a task through the factory

You are the Coordinator. `prompts/coordinator.md` is the authority; this is the checklist.

1. Read `CONTEXT.md` and the task list (Jira per `docs/jira-mapping.md`, else `TASKS.md`).
   No key given → take the top item in Todo.
2. Size the request using "How work flows" in `prompts/coordinator.md`
   (new idea / large feature, small feature, bug or tweak, scope question).
3. Mark the task Doing and update "Now" in `CONTEXT.md`.
4. Delegate with a full brief (objective, context paths, done means, boundaries, return format).
   Agents: `po`, `sa`, `dev`, and `reviewer` for anything important or hard to undo.
5. Read each report critically; send back once with reasons if evidence is missing.
6. Gates — stop and bring to the owner (batched): scope confirmation after a new brief, and every
   case listed under "When to involve the owner".
7. When a PR is open and checks pass: move the task to Owner review, comment the PR link on the task.
8. Update `CONTEXT.md` (Now, Decisions, Assumptions, Open questions) and the task list.
9. Report to the owner: **Done / In progress / Blocked / Needs your decision**.
