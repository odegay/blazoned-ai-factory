# Design process (Google Stitch)

How UI designs are made, approved and handed to the build. Rules for who does what are in `TEAM.md` (loop 6).

## Folder per design ticket: `docs/design/<TICKET>/`
| File | What | Writer |
|---|---|---|
| `brief.md` | Design brief + the Stitch prompts | `ux` |
| `*.png` | Screenshots, named `<screen>-<390\|1280>[-<direction>].png` | Coordinator (from Stitch) |
| `*.html` | Stitch HTML export. Reference only: never shipped, never copied into `src/` | Coordinator (from Stitch) |
| `approval.md` | The owner's approval (template below) | Coordinator |
| `stitch-design-system.md` | Stitch's generated design system for the approved variant (`styleGuidelines` + `theme` from the generation response), saved verbatim | Coordinator (from Stitch) |
| `DESIGN.md` | Tokens + rules for the approved variant, curated from `stitch-design-system.md` | `ux` |

`brief.md` outline: Goal · Audience · Screens (content blocks in order) · Constraints · Style directions ·
Stitch prompts (one `### <screen> / <direction> / <390|1280>` section each) · Generations requested (count).
For an output review, the Coordinator's brief to `ux` lists the saved screenshot paths and their prompt sections.

## Steps
1. `po` writes the design ticket: scope, screens or sections, audience, constraints, deliverables.
   `po` marks every ticket that changes UI as `needs design: <TICKET>`.
2. `ux` writes `brief.md` with the prompts: usually 2-3 style directions for a new visual style,
   one inside an approved style. Mobile 390px and desktop 1280px. EN copy; note longer RU/UK strings. WCAG AA contrast.
3. The Coordinator runs the prompts in Stitch, saves the screenshots here, and has `ux` review them.
4. The Coordinator shows the owner the screenshots and the Stitch link. **Approval gate:** nothing is built before
   the owner approves. The Coordinator writes `approval.md`.
5. The Coordinator exports the approved screens (PNG + HTML) and saves `stitch-design-system.md` here;
   `ux` curates `DESIGN.md` from it (no Stitch key needed).
6. **Design bootstrap slice** (the single definition; other files link here). First approved design in a
   project: `sa` plans it before any feature UI: tokens from `DESIGN.md` as CSS variables, base styles, and a
   few base components, mapped onto the project's component library. Later UI slices reuse them.
7. `dev` builds UI slices to match the approved screenshots and `DESIGN.md`, inside the project's stack and CSP.
   Stitch HTML loads Tailwind, fonts and images from CDNs: do not ship it or its CDN links.
8. Slice review of a UI slice adds a visual parity check (see `TEAM.md` loop 4).

## Running Stitch (Coordinator only)
- Official Google tools only: the `@google/stitch` CLI, `@google/stitch-sdk`, or the hosted MCP
  `https://stitch.googleapis.com/mcp`. Web UI: stitch.withgoogle.com.
- The key comes only from the environment variable `STITCH_API_KEY`. Never print, log, echo or commit it,
  and never pass it to a subagent.
- The Coordinator runs Stitch outside Claude Code's tool permissions (its own shell, key from env). Never put
  the key in a committed `.mcp.json` or settings file; this repo adds no Stitch allow rules or hooks.
- API/CLI/SDK generations use Flash models (`GEMINI_3_8_FLASH`, `GEMINI_3_5_FLASH_LITE`); Pro models are only
  in the web UI.
- On a connection error or timeout, do not retry the generation: list or get the project's screens first,
  because the generation may have finished. Retry only if it is not there.
- Credits are daily and free, with no paid plan. Generate only what the brief asks for; variants only when asked.
  If the daily limit is hit, stop and continue the next day; note it under "Now" in `CONTEXT.md`.
- Prompts contain no personal data, client data, addresses, secrets or the owner's location
  (free Labs service; inputs may be used for training).
- Cost: Stitch generation itself uses Stitch daily credits, not Claude/Codex usage. The `ux` runs (briefs,
  reviews) and the Coordinator's handling still cost agent tokens; keep them short.

## Known gaps (accepted for now)
- `ux`'s limits (write only under `docs/design/`, never `approval.md`) are prompt-only; no hook enforces them.
  The Coordinator checks `ux`'s changed files after each run.
- The `role-ux` Jira label must be created in the project the first time it is used.

## `approval.md` template
```markdown
# <TICKET> design approval
- Date: YYYY-MM-DD
- Approved by: owner
- Chosen variant: <direction / screen names>
- Stitch project id: <id>
- Stitch screen ids: <id>, <id>
- Stitch link: <url>
- Owner notes / requested changes: <none | list>
```
