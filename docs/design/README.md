# Design process (Google Stitch)

How UI designs are made, approved and handed to the build. Rules for who does what are in `TEAM.md` (loop 6).

## Folder per design ticket: `docs/design/<TICKET>/`
| File | What | Writer |
|---|---|---|
| `brief.md` | Design brief + the Stitch prompts | `ux` |
| `*.png` | Screenshots, named `<screen>-<390\|1280>[-<direction>].png` | Coordinator (from Stitch) |
| `*.html` | Stitch HTML export. Reference only: never shipped, never copied into `src/` | Coordinator (from Stitch) |
| `approval.md` | The owner's approval (template below) | Coordinator |
| `DESIGN.md` | Tokens + rules for the approved variant | `ux` |

## Steps
1. `po` writes the design ticket: scope, screens or sections, audience, constraints, deliverables.
   `po` marks every ticket that changes UI as `needs design: <TICKET>`.
2. `ux` writes `brief.md` with the prompts: usually 2-3 style directions for a new visual style,
   one inside an approved style. Mobile 390px and desktop 1280px. EN copy; note longer RU/UK strings. WCAG AA contrast.
3. The Coordinator runs the prompts in Stitch, saves the screenshots here, and has `ux` review them.
4. The Coordinator shows the owner the screenshots and the Stitch link. **Approval gate:** nothing is built before
   the owner approves. The Coordinator writes `approval.md`.
5. The Coordinator exports the approved screens (PNG + HTML) here; `ux` writes `DESIGN.md`.
6. First approved design in a project: `sa` adds a **design bootstrap** slice before any feature UI:
   tokens as CSS variables, base styles, a few base components, all from `DESIGN.md`.
7. `dev` builds UI slices to match the approved screenshots and `DESIGN.md`, inside the project's stack and CSP.
   Stitch HTML loads Tailwind, fonts and images from CDNs: do not ship it or its CDN links.
8. Slice review of a UI slice adds a visual parity check (see `TEAM.md` loop 4).

## Running Stitch (Coordinator only)
- Official Google tools only: the `@google/stitch` CLI, `@google/stitch-sdk`, or the hosted MCP
  `https://stitch.googleapis.com/mcp`. Web UI: stitch.withgoogle.com.
- The key comes only from the environment variable `STITCH_API_KEY`. Never print, log, echo or commit it,
  and never pass it to a subagent.
- On a connection error or timeout, do not retry the generation: list or get the project's screens first,
  because the generation may have finished. Retry only if it is not there.
- Credits are daily and free, with no paid plan. Generate only what the brief asks for; variants only when asked.
  If the daily limit is hit, stop and continue the next day; note it under "Now" in `CONTEXT.md`.
- Prompts contain no personal data, client data, addresses, secrets or the owner's location
  (free Labs service; inputs may be used for training).
- Cost: Stitch uses no Claude tokens, only Stitch credits. The `ux` runs (briefs, reviews) are cheap.

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
