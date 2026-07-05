# Ticket-005: GitHub Actions CI/CD Pipeline for GitHub Pages

- **Label**: `roadmap:task`
- **Status**: Open
- **Assignee**: Unassigned
- **Blocked by**: [Hugo Templates for MR BIOS and Unicore Catalogs](file:///Users/ilembitov/Projects/bios/roadmap/tickets/ticket-004-hugo-templates.md)

## Question
How do we configure a GitHub Actions workflow to automatically build and deploy the Hugo site to GitHub Pages whenever changes are pushed to `main`?

## Plan
1. Create a GitHub Actions workflow file in `.github/workflows/hugo.yml`.
2. Configure it to trigger on pushes to the `main` branch.
3. Steps should include:
   - Checkout repository.
   - Install Hugo (extended version).
   - Build Hugo site (with output in `public/` directory).
   - Upload site build artifact.
   - Deploy build artifact to GitHub Pages.
4. Verify the build and deployment settings on your GitHub repository.
