---
target: spa public board
total_score: 22
max_score: 32
na_heuristics: 9,10
p0_count: 0
p1_count: 1
target_identity: "file:d:\\citywatch\\reports\\templates\\reports\\dashboard.html#spa-public-board"
timestamp: 2026-09-28T01-32-34Z
slug: s-reports-dashboard-html-spa-public-board-c519dc93
closed: true
---
Method: ⚠️ DEGRADED: single-context (no sub-agent tool exposed)

#### Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Filter updates lack immediate visual feedback before reload |
| 2 | Match System / Real World | 3 | Solid civic terminology used |
| 3 | User Control and Freedom | 2 | Auto-submitting forms can feel jarring; no explicit "Clear Filters" button |
| 4 | Consistency and Standards | 3 | Consistently applies standard web patterns |
| 5 | Error Prevention | 3 | Read-only view minimizes user error |
| 6 | Recognition Rather Than Recall | 3 | Current filter states are clearly visible in dropdowns |
| 7 | Flexibility and Efficiency | 3 | Search and filters work efficiently together |
| 8 | Aesthetic and Minimalist Design | 2 | Overly reliant on generic SaaS "startup" aesthetics |
| 9 | Error Recovery | n/a | Read-only public board |
| 10 | Help and Documentation | n/a | Self-explanatory interface |
| **Total** | | **22/32** | **Acceptable** |

#### Design Specificity Verdict

**LLM assessment**: The Community Transparency Board struggles to establish an official, authoritative civic identity. While it successfully incorporates the brand's primary color, the structural execution—specifically the statistic cards and report cards—leans heavily into generic B2B SaaS tropes (rounded borders, thin outlines, uppercase micro-headers). It looks like a startup dashboard, not a government transparency portal. 

**Deterministic scan**: The CLI detector found 2 warnings in `dashboard.html`:
- Flat type hierarchy (Dominant heading and body roles are separated by < 1.25x).
- Skipped heading level (e.g., `h1` straight to `h3`). Note: This specifically affects the "My Reports" tab, but the public board also suffers from structural heading mismatches (e.g., `h2` used for tiny `text-xs` labels on stats).

#### Overall Impression
The board is highly functional and clearly organized, but it lacks the visual gravity expected from an official city initiative. The biggest opportunity is grounding the interface by stripping away the "AI slop" (excessive rounding/borders) and replacing it with a bolder, more authoritative layout.

#### What's Working
- **Information Architecture**: The layout is logical—hero title, high-level stats, filters, and then the detailed list.
- **Clear Statusing**: The color-coded status badges on the report images are highly legible and immediately convey the state of each issue.

#### Priority Issues

- **[P1] Generic SaaS Stat Cards**
  - **Why it matters**: It dilutes the official civic authority of Baliwag City. The rounded-xl borders and flex-col layouts feel like a generic template rather than an official LGU transparency board.
  - **Fix**: Redesign the stat cards to be bolder and structurally grounded. Use sharp corners, solid background blocks, or stronger typography to evoke civic stability.
  - **Suggested command**: `$impeccable bolder`

- **[P2] Auto-submit Dropdowns Lacking Feedback**
  - **Why it matters**: The `onchange="this.form.submit()"` triggers a full page reload without any intermediate loading state, which breaks the SPA illusion and feels jarring.
  - **Fix**: Convert the filter form to use AJAX updates like the rest of the SPA, or at least show a loading indicator when a filter is selected.
  - **Suggested command**: `$impeccable harden`

- **[P2] Uninspired Report Cards**
  - **Why it matters**: The report cards look like standard blog post components. They don't feel like official municipal dockets or reports.
  - **Fix**: Improve the typography and structure of the report cards. Treat them more like formal documents or tickets with stronger structural lines.
  - **Suggested command**: `$impeccable typeset`

#### Persona Red Flags

**Alex (Power User)**: 
- Has to wait for a full page reload every time they change a single filter dropdown, rather than instantly sorting client-side or via AJAX.

**Jordan (First-Timer)**: 
- Might be confused by the auto-submitting dropdowns. If they try to select a Category, the page suddenly reloads before they can even read what happened.

#### Minor Observations
- The "Avg. Resolution Time" stat includes the word "Days" in a smaller font, but it's visually fighting with the large number.

#### Questions to Consider
- What if the stat cards weren't distinct "cards" at all, but a single, solid, authoritative banner of data?
- Does this need to feel like a modern web app, or should it feel more like a digital version of a formal municipal notice board?
