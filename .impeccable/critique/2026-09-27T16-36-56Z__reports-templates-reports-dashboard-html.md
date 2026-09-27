---
target: reports/templates/reports/dashboard.html
total_score: 20
max_score: 40
na_heuristics: 
p0_count: 1
p1_count: 3
target_identity: "file:D:\\citywatch\\reports\\templates\\reports\\dashboard.html"
target_fingerprint: "sha256:47e2774bc04748d8e968cbedaeb2db92cfeff531152c191f4a76f944147014b3"
target_path: "D:\\citywatch\\reports\\templates\\reports\\dashboard.html"
timestamp: 2026-09-27T16-36-56Z
slug: reports-templates-reports-dashboard-html
---
## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 2 | Stat cards show counts but no loading states or timestamps |
| 2 | Match System / Real World | 3 | Language is citizen-friendly; add_a_photo icon on Submit Report is wrong metaphor |
| 3 | User Control and Freedom | 2 | No undo, no breadcrumbs, sidebar has escape but no in-page safety nets |
| 4 | Consistency and Standards | 2 | Color palette diverges from login/register; sidebar active state has ~3.5:1 contrast |
| 5 | Error Prevention | 2 | Empty states exist inconsistently; Community Board empty state has no CTA |
| 6 | Recognition Rather Than Recall | 3 | Nav is labeled, stat cards are labeled, action cards are clear |
| 7 | Flexibility and Efficiency | 1 | No filters, no search in My Reports, no keyboard shortcuts |
| 8 | Aesthetic and Minimalist Design | 2 | Stat cards are identical white boxes; layout is flat and generic |
| 9 | Error Recovery | 2 | Empty states exist but inconsistently applied |
| 10 | Help and Documentation | 1 | No tooltips, no contextual guidance, no help link |
| **Total** | | **20/40** | **Acceptable — significant improvement needed** |

## Design Specificity Verdict
Dashboard could belong to any generic SaaS product. No authored CityWatch/civic character. Color palette diverges completely from auth pages (#002045 navy vs #156b3e green). Detector found 2 issues: flat-type-hierarchy (all headings/body render at 16px same weight) and skipped-heading (h1 -> h3 with no h2).

## Priority Issues
- [P0] Broken Color System: primary is #002045 here vs #156b3e on auth pages. Sidebar active state is white on #1a365d (~3.5:1 contrast, fails WCAG AA).
- [P1] Flat Type Hierarchy: detector confirmed all text roles resolve to 16px. No visual hierarchy.
- [P1] Stat Cards Are Visually Inert: identical white boxes, no status color coding, no urgency signal.
- [P1] Wrong Icon on Primary CTA: add_a_photo implies photo upload, not civic report filing.
- [P2] No Mobile Navigation: sidebar is hidden lg:flex with no fallback. Entire nav disappears on mobile.

## Persona Red Flags
- Jordan (First-Timer): confused by identical stat cards, wrong icon on CTA, passive empty states.
- Casey (Mobile): sidebar disappears on phone, no mobile nav, cannot navigate after filing report.
- Sam (Accessibility): h1->h3 heading skip breaks screen reader outline; sidebar active contrast fails WCAG AA.

## Minor Observations
- text-blue-100 hardcoded color not in design system
- My Active Reports only shows non-resolved but title doesn't clarify this
- Inconsistent section header treatment between Community Board and My Active Reports
- resident_sidebar.html has style tag in body, not head
