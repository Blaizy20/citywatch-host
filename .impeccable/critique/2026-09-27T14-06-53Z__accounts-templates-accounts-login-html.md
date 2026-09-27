---
target: login.html
total_score: 25
max_score: 36
na_heuristics: 10
p0_count: 1
p1_count: 0
target_identity: "file:D:\\citywatch\\accounts\\templates\\accounts\\login.html"
target_fingerprint: "sha256:b0bfd42171506d838a37282249a6aca3ec0b4995bacf1fb9a727be27afb56d04"
target_path: "D:\\citywatch\\accounts\\templates\\accounts\\login.html"
timestamp: 2026-09-27T14-06-53Z
slug: accounts-templates-accounts-login-html
---
⚠️ DEGRADED: single-context (no sub-agent tool exposed in this session)

### Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Focus rings are clear, but lacks inline validation before submit. |
| 2 | Match System / Real World | 3 | Civic copy is solid. |
| 3 | User Control and Freedom | 4 | "Back to Home" is prominent and clear. |
| 4 | Consistency and Standards | 1 | Massive token desync (wrong fonts and wrong brand colors). |
| 5 | Error Prevention | 3 | Includes a password visibility toggle. |
| 6 | Recognition Rather Than Recall | 3 | Standard form layout, easy to understand. |
| 7 | Flexibility and Efficiency | 3 | "Remember me" checkbox is available. |
| 8 | Aesthetic and Minimalist Design | 3 | The split layout is nice, but the form feels slightly cramped. |
| 9 | Error Recovery | 2 | Generic Django messages; errors do not persist in line with fields. |
| 10 | Help and Documentation | n/a | |
| **Total** | | **25/36** | **Fair** |

### Design Specificity Verdict

**LLM assessment**: The layout structure (a 50/50 split with a decorative left panel and a clean form on the right) is a very solid, modern authentication pattern. However, the execution is suffering from a massive design system desynchronization. The login page looks like it belongs to a completely different application than the landing page.

**Deterministic scan**: The detector found 8 instances of `low-contrast` (black text on dark blue) and 1 instance of `flat-type-hierarchy`. While the type hierarchy is a known false positive with Tailwind arbitrary values, the low contrast warnings suggest that somewhere in the dark gradient panel, elements are defaulting to black text instead of inheriting `text-white`.

### Overall Impression
The structural foundation is excellent. The split-screen design is highly professional. However, the page is fundamentally broken from a branding and consistency standpoint.

### What's Working
- **Layout Architecture**: The 50/50 split screen is a premium pattern that works great on desktop.
- **Micro-interactions**: The password visibility toggle and form fade-in animation are nice touches of polish.

### Priority Issues

- **[P0] Massive Token Desync (Brand Break)**
  - **Why it matters**: `login.html` is using a completely different Tailwind configuration than `landing.html`. It is importing `Inter` instead of `Outfit/DM Sans`, and its `primary` color is defined as `#002045` (Navy Blue) instead of the official Baliwag Green (`#156b3e`). This destroys trust; users might think they are on a phishing site if the design abruptly changes.
  - **Fix**: Replace the internal Tailwind config and font imports in `login.html` to exactly match the design tokens established in `landing.html` (or ideally, move them to a shared base template).
  - **Suggested command**: `/impeccable harden`

- **[P2] Low Contrast / Inheritance Issues**
  - **Why it matters**: The detector flagged multiple instances of `text #000000 on #002045`. This usually happens when an inner element (like a paragraph or span) resets its color, overriding a parent's `text-white` class.
  - **Fix**: Review the dark left panel and ensure contrast is explicitly maintained.
  - **Suggested command**: `/impeccable colorize`

### Persona Red Flags

**Taylor (Power User)**: The jarring shift in fonts and colors from the landing page to the login page will make a power user immediately suspicious of the site's quality or security.

### Minor Observations
- The `gradient-shimmer` animation is neat, but will look much better using the official Baliwag green/blue brand colors.

### Questions to Consider
- Should we extract the Tailwind config and fonts into a `base.html` template to prevent this desync from happening on other pages (like `register.html` or the dashboards)?
