# Ticket-003: Hugo Static Site Bootstrap

- **Label**: `roadmap:task`
- **Status**: Closed
- **Assignee**: Antigravity
- **Blocks**: [Hugo Templates for MR BIOS and Unicore Catalogs](file:///Users/ilembitov/Projects/bios/roadmap/tickets/ticket-004-hugo-templates.md)

## Question
How do we initialize and bootstrap the Hugo site repository structure and configuration?

## Plan
1. Initialize the Hugo project inside `/site` folder.
2. Select or create a simple, ultra-lightweight responsive theme to minimize dependencies (prefer a basic custom layout in `layouts/` folder to avoid importing external git submodules, which can break in the future).
3. Create `site/hugo.toml` with base parameters:
   - Site title: "MR BIOS & Unicore Award BIOS Archive"
   - Host URL configured for GitHub Pages (e.g., `https://<username>.github.io/<repo>/`).
4. Set up the basic homepage structure (`site/content/_index.md`) introducing the catalogs and linking them.

## Resolution
- Bootstrapped Hugo project inside `/site` folder.
- Configured [hugo.toml](file:///Users/ilembitov/Projects/bios/site/hugo.toml) with relative URLs enabled (making the build compatible with any GitHub Pages subdirectory deployment) and safe HTML rendering config.
- Created custom theme layouts to avoid submodule dependency risk:
  - Base Layout: [baseof.html](file:///Users/ilembitov/Projects/bios/site/layouts/_default/baseof.html)
  - Home Layout: [index.html](file:///Users/ilembitov/Projects/bios/site/layouts/index.html)
  - Section List Layout: [list.html](file:///Users/ilembitov/Projects/bios/site/layouts/_default/list.html)
  - Single Page Layout: [single.html](file:///Users/ilembitov/Projects/bios/site/layouts/_default/single.html)
- Implemented premium responsive design and dark aesthetics in [styles.css](file:///Users/ilembitov/Projects/bios/site/static/css/styles.css) (Outfit font, custom glassmorphism panels, responsive table containers, hover animations).
- Verified build compiles warning-free inside 17ms.

