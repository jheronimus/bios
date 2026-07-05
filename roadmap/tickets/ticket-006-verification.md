# Ticket-006: Regression Test & Verification

- **Label**: `roadmap:task`
- **Status**: Closed
- **Assignee**: Antigravity
- **Blocked by**: [Hugo Templates for MR BIOS and Unicore Catalogs](file:///Users/ilembitov/Projects/bios/roadmap/tickets/ticket-004-hugo-templates.md)

## Question
How do we verify that the data migration is 100% complete and correct (no rows/tabs lost) and that all download links point to valid binary files?

## Plan
1. Write a verification script in `scripts/verify.py` that:
   - Compares the total row count of each HTML file in the `import` directory against the total item count of each generated YAML catalog.
   - Verifies that every record's linked file (specified in YAML) actually exists in the repository (e.g. at `/bios/mrbios/...` or `/bios/unicore/...`).
   - Checks that all binary BIOS files are non-empty and have correct read permissions.
2. Run the verification script and generate a report showing:
   - Total rows extracted from MR BIOS sheets.
   - Total rows extracted from Unicore sheets.
   - Any mismatched or missing binary files.

## Resolution
- Created [verify.py](file:///Users/ilembitov/Projects/bios/scripts/verify.py) implementing standalone assert-based data verification tests.
- Verified 100% catalog integrity:
  - Validated all 36 chipset categories.
  - Compared and matched exactly 4,244 database entries.
  - Checked and verified that all 3,980 referenced BIOS files exist locally.

