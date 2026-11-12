# Team rules and settings

Loaded by every agent through `CLAUDE.md`. Defines how the Coordinator, `po`, `sa`, `dev` and `reviewer` work together.
Project facts live in `CONTEXT.md`; the Jira setup lives in `docs/jira-mapping.md`.
Each project repo keeps its own copy of this file: change the settings there.

## Settings

```yaml
brief_check_by_architect: true   # true | false             sa checks each new or changed brief for cost and feasibility before the owner confirms scope
code_review_by: architect        # architect | reviewer | none   who reviews each slice's PR before it goes to Owner review
max_negotiation_rounds: 2        # send-backs allowed per loop before the Coordinator decides or escalates
```

The values shown are the defaults. If a setting is missing or has a value not listed, use the default and mention it in your report.

Fixed by guardrails, not by settings:
- Every change lands as a PR from `feature/<TASK-ID>-<slug>`, and only the owner merges
  (enforced by `.claude/settings.json`, `.claude/hooks/guard_bash.py` and branch protection).
- Anything hard to undo (first deploy, data changes, release to users, security-relevant code) always also goes to `reviewer`, whatever `code_review_by` says.

## How the team communicates

- The Coordinator is the main session and the only agent that talks to the owner.
- Subagents are started only by the Coordinator. They cannot reach the owner or each other during a task.
- Anything meant for someone else (a question, an objection, a proposed change) goes into the report. The Coordinator routes it.
- One task per run. When finished or blocked, return the report and stop. For follow-up on the same work the Coordinator may continue the same agent; a `reviewer` run is always fresh.

## Report format

Every subagent ends every task with this report, plus any role-specific items its agent file lists.
Keep it short: detail goes into files, the report gives paths. Leave out empty sections.

```
Result:          done | partly done | blocked | needs decision (one line)
Files:           created or changed, with paths
Verified:        how (commands run and their outcome), or "not verified" and why
Assumptions:     what you treated as true without confirmation
Questions:       each tagged [owner] [po] [sa] [dev]; blocking yes/no; what you will assume if unanswered
Objections:      disagreement with the brief, design or review: reason and alternative
Context updates: proposed lines for CONTEXT.md
```

## Where questions go

The Coordinator first answers from `CONTEXT.md` and the docs if it can. Otherwise:

| The question is about | Routed to |
|---|---|
| What to build, scope, priority, acceptance criteria | `po` |
| How to build: design, technology, component cost | `sa` |
| How the existing code works | `dev` |
| Business facts, money, access, or anything under "When to involve the owner" in `prompts/coordinator.md` | owner, via the Coordinator |

## Feedback loops

A **round** is one send-back from the Coordinator to an agent within a loop. When a loop reaches
`max_negotiation_rounds` without agreement, the Coordinator decides using the project priorities
(cost, then speed of delivery, then simplicity) and records the decision in `CONTEXT.md`. If the decision
belongs to the owner, the Coordinator escalates it with both positions stated fairly and a recommendation.

1. **Brief check** (when `brief_check_by_architect: true`)
   `po` writes or changes the brief → `sa` checks cost and feasibility only, not product value →
   objections go back to `po`, who revises the scope or defends it with reasons → the owner confirms scope.
2. **Design and scope clarification** (always)
   A `dev` question or objection about design goes to `sa`, who answers and updates `docs/architecture.md`
   if the design changes. A question about scope goes to `po`.
3. **Slice review** (per PR, after `dev` reports the PR open with verification evidence; missing evidence is sent back first and is not a round)
   - `architect`: `sa` reviews the PR against `docs/architecture.md` and the task's done-when.
   - `reviewer`: a fresh `reviewer` run reviews the PR.
   - `none`: no review; the Coordinator checks the evidence and the PR checks only.

   The verdict is **approved** or **changes required**. Must-fix items go back to `dev` on the same branch and PR;
   `dev` fixes them or objects with reasons. Suggestions never block. Approved and checks passing → Owner review.
4. **Owner decisions**
   Once the owner decides, everyone works with the decision. An agent that still disagrees records it as a risk;
   it does not reopen the decision.
