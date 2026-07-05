# Ticket-001: Unicore and MR BIOS HTML Data Extraction Script

- **Label**: `roadmap:task`
- **Status**: Closed
- **Assignee**: Antigravity
- **Blocks**: [YAML Catalog and Image Organization Schema](file:///Users/ilembitov/Projects/bios/roadmap/tickets/ticket-002-data-schema.md)

## Question
How do we programmatically parse the HTML documents exported from Google Sheets in `import/Unicore upgrades/` and `import/MR BIOS archive v2/` to extract all metadata tables cleanly without losing any data?

## Plan
1. Create a Python script in `scripts/migrate.py` using BeautifulSoup.
2. Read all the `.html` files in:
   - `import/MR BIOS archive v2/*.html` (excluding `Info.html`, `Revision history.html`, `resources`)
   - `import/Unicore upgrades/*.html` (excluding `Info.html`, `resources`)
3. Parse the standard table structure (`<table>`, `<tr>`, `<td>`) that Google Sheets HTML uses.
4. Extract headers and rows for each file. Ensure empty cells, notes, part numbers, and manufacturer names are completely preserved.
5. Save the output of the extraction temporarily as clean JSON datasets in the scratch directory for verification.

## Resolution
- Created [migrate.py](file:///Users/ilembitov/Projects/bios/scripts/migrate.py) which handles HTML BeautifulSoup parsing.
- Programmatically processed 30 files for MR BIOS (extracting all tabs including Stock Motherboards and Revision history) and 8 files for Unicore.
- Exported clean, verified JSON datasets containing parsed rows to the scratch directory:
  - [extracted_mrbios.json](file:///Users/ilembitov/.gemini/antigravity-cli/brain/2bc4377f-c3f0-461b-b741-cb28618d039c/scratch/extracted_mrbios.json)
  - [extracted_unicore.json](file:///Users/ilembitov/.gemini/antigravity-cli/brain/2bc4377f-c3f0-461b-b741-cb28618d039c/scratch/extracted_unicore.json)
