# Ticket-004: Hugo Templates for MR BIOS and Unicore Catalogs

- **Label**: `roadmap:task`
- **Status**: In-Progress
- **Assignee**: Antigravity
- **Blocked by**: [YAML Catalog and Image Organization Schema](file:///Users/ilembitov/Projects/bios/roadmap/tickets/ticket-002-data-schema.md), [Hugo Static Site Bootstrap](file:///Users/ilembitov/Projects/bios/roadmap/tickets/ticket-003-hugo-bootstrap.md)
- **Blocks**: [GitHub Actions CI/CD Pipeline for GitHub Pages](file:///Users/ilembitov/Projects/bios/roadmap/tickets/ticket-005-ci-cd.md), [Regression Test & Verification](file:///Users/ilembitov/Projects/bios/roadmap/tickets/ticket-006-verification.md)

## Question
How do we create layout templates in Hugo to dynamically read our YAML files from `data/` and render them as beautiful, responsive tables?

## Plan
1. Create content pages for each catalog tab (e.g. `content/mrbios/intel.md`, `content/unicore/ali.md`).
2. Implement custom Hugo layouts in `layouts/catalog/single.html` that read from `.Site.Data.mrbios` or `.Site.Data.unicore`.
3. In the layouts, render the catalog entries as HTML tables. Since different tabs/files have different fields:
   - Dynamically discover headers from the YAML list mappings.
   - Or define custom header mappings for known sheets.
4. Add direct download buttons for each row, pointing to:
   `https://raw.githubusercontent.com/<username>/<repo>/main/bios/<catalog_type>/<relative_path>`
5. Add basic responsive CSS styles for table sizing, highlighting, and mobile scroll-bars.
