# Roadmap: MR BIOS & Unicore Award BIOS Archive

This roadmap tracks the migration of the MR BIOS and Unicore Award BIOS Google Doc catalogs and Dropbox archive into a version-controlled GitHub repository, hosted on GitHub Pages using Hugo.

## Notes

- **SSG**: Hugo will be used to generate the static site.
- **Data Source**: Source data is stored in YAML list files in `data/mrbios/` and `data/unicore/`.
- **Images**: Served directly from GitHub's raw CDN (`raw.githubusercontent.com`).
- **Comments**: Deferred for V1.

## Decisions so far

- **[Catalog Data Format (YAML Mappings)](#decision-data-format)** — Store catalog entries as YAML lists of key-value pairs to allow flexible schemas per BIOS.
- **[Hugo SSG choice](#decision-hugo)** — Use Hugo as the static site generator for its speed and zero dependency maintenance.
- **[Direct Raw CDN downloads](#decision-downloads)** — Serve binary files via GitHub's raw file CDN to avoid slow builds and git bloat in the Pages deployment.
- **[Defer comments](#decision-comments-deferred)** — Comments are deferred for V1 to keep deployment simple and zero-dependency.
- **[Unicore and MR BIOS HTML Data Extraction Script](file:///Users/ilembitov/Projects/bios/roadmap/tickets/ticket-001-data-extraction.md)** — Parsed all 30 MR BIOS HTML sheets and 8 Unicore upgrades HTML sheets cleanly into structured scratch JSON files.
- **[YAML Catalog and Image Organization Schema](file:///Users/ilembitov/Projects/bios/roadmap/tickets/ticket-002-data-schema.md)** — Structured BIOS metadata into data/ as YAML lists and moved binaries to bios/, linking them dynamically.
- **[Hugo Static Site Bootstrap](file:///Users/ilembitov/Projects/bios/roadmap/tickets/ticket-003-hugo-bootstrap.md)** — Bootstrapped Hugo project inside site/, defined custom layouts, and created responsive CSS design.
- **[Git Repository Initialization](file:///Users/ilembitov/Projects/bios/roadmap/tickets/ticket-007-git-init.md)** — Git repository initialized and first commit created containing over 19,000 migrated files.
- **[Hugo Templates for MR BIOS and Unicore Catalogs](file:///Users/ilembitov/Projects/bios/roadmap/tickets/ticket-004-hugo-templates.md)** — Implemented a unified catalog layout template (`catalog.html`) with dynamic column ordering, raw CDN download links, and header navigation.
- **[GitHub Actions CI/CD Pipeline for GitHub Pages](file:///Users/ilembitov/Projects/bios/roadmap/tickets/ticket-005-ci-cd.md)** — Configured automated compile and deployment workflow (`deploy.yml`) under `.github/workflows/` targeting GitHub Pages.

## Frontier

- [Regression Test & Verification](file:///Users/ilembitov/Projects/bios/roadmap/tickets/ticket-006-verification.md) (unblocked)

## Open Tickets

- [Regression Test & Verification](file:///Users/ilembitov/Projects/bios/roadmap/tickets/ticket-006-verification.md)

## Fog

- **Search & Filter (V2)**: Implement Client-side searching (e.g., Pagefind or custom JS) once V1 is stable.
- **Inline Comments (V2)**: Investigate account-free, zero-login commenting widgets or Google Sheet submissions to allow reader annotations.
- **BIOS File Integrity Checks**: Implement automated CI checks to compute file size, hashes (MD5, SHA-256), and detect corrupted BIOS binaries automatically.
