# Ticket-002: YAML Catalog and Image Organization Schema

- **Label**: `roadmap:task`
- **Status**: Closed
- **Assignee**: Antigravity
- **Blocked by**: [Unicore and MR BIOS HTML Data Extraction Script](file:///Users/ilembitov/Projects/bios/roadmap/tickets/ticket-001-data-extraction.md)
- **Blocks**: [Hugo Templates for MR BIOS and Unicore Catalogs](file:///Users/ilembitov/Projects/bios/roadmap/tickets/ticket-004-hugo-templates.md)

## Question
How should the extracted metadata be structured into YAML files, and how should the raw BIOS image files be mapped, moved, and linked?

## Plan
1. Define the final folder structure for the repository:
   - `/data/mrbios/` (YAML files for MR BIOS chipsets/categories)
   - `/data/unicore/` (YAML files for Unicore chipsets/categories)
   - `/bios/mrbios/` (binary BIOS files)
   - `/bios/unicore/` (binary BIOS files)
2. Extend the Python migration script to write data to these directories:
   - For MR BIOS: Save each tab's rows as a list of YAML mappings in `data/mrbios/<tab_name>.yml`.
   - For Unicore: Save each tab's rows as a list of YAML mappings in `data/unicore/<tab_name>.yml`.
3. In the YAML entries, include a local path or filename mapping to the physical `.BIN` image in the repo.
4. Move files from `import/MRBIOS/` and `import/UNICORE/` into their clean repo locations (`bios/mrbios/` and `bios/unicore/`).
5. Ensure case sensitivity and directory name changes are fully handled so files match the spreadsheet descriptions.

## Resolution
- Wrote and executed [migrate_v2.py](file:///Users/ilembitov/Projects/bios/scripts/migrate_v2.py) to complete data mapping and schema storage.
- Moved BIOS binaries:
  - `import/MRBIOS/` -> `bios/mrbios/`
  - `import/UNICORE/` -> `bios/unicore/`
- Linked binaries:
  - Created YAML database files under `data/mrbios/` and `data/unicore/` containing exact row data and a `files` array listing matched files.
  - Linked 100% of Unicore folders (3,337 files indexed).
  - Linked active part numbers in MR BIOS sheets (815 files indexed).
- Structured site intro & revision content under `site/content/mrbios/` and `site/content/unicore/`.

