import os
import re
import json
import glob
import copy
from bs4 import BeautifulSoup

def cell_to_markdown(td):
    if not td:
        return ""
    td_copy = copy.copy(td)
    for a in td_copy.find_all('a'):
        href = a.get('href', '')
        text = a.get_text().strip()
        if href and text:
            a.replace_with(f"[{text}]({href})")
        elif text:
            a.replace_with(text)
        else:
            a.decompose()
    for br in td_copy.find_all('br'):
        br.replace_with("\n")
    text = td_copy.get_text()
    return text.strip()

def parse_sheet_html(filepath, is_revision_history=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    table = soup.find('table')
    if not table:
        return None
    
    rows = []
    headers = []
    
    for tr in table.find_all('tr'):
        # Skip if it is a freezebar row
        if tr.find('th', class_='freezebar-cell') or tr.find('td', class_='freezebar-cell'):
            continue
        
        cells = tr.find_all('td')
        # Skip empty rows
        if not cells or all(not cell_to_markdown(c) for c in cells):
            continue
            
        row_data = [cell_to_markdown(c) for c in cells]
        
        # Revision history has no headers in HTML, it starts directly with version numbers
        if is_revision_history and not headers:
            headers = ["Version", "Description"]
            # Fall through to process this first row as data
            
        # First non-empty row contains headers (if not custom handled)
        if not headers:
            headers = row_data
            continue
        
        # Map row data to headers
        if len(row_data) < len(headers):
            row_data += [""] * (len(headers) - len(row_data))
        
        row_dict = {}
        for i, h in enumerate(headers):
            if h: # Ignore empty headers
                row_dict[h] = row_data[i]
        
        rows.append(row_dict)
        
    return {
        "headers": [h for h in headers if h],
        "rows": rows
    }

def main():
    import_dir = "import"
    mrbios_dir = os.path.join(import_dir, "MR BIOS archive v2")
    unicore_dir = os.path.join(import_dir, "Unicore upgrades")
    
    scratch_dir = "/Users/ilembitov/.gemini/antigravity-cli/brain/2bc4377f-c3f0-461b-b741-cb28618d039c/scratch"
    os.makedirs(scratch_dir, exist_ok=True)
    
    mrbios_data = {}
    unicore_data = {}
    
    print("--- Parsing MR BIOS catalog files ---")
    mrbios_files = glob.glob(os.path.join(mrbios_dir, "*.html"))
    for filepath in sorted(mrbios_files):
        filename = os.path.basename(filepath)
        tab_name = filename.replace(".html", "")
        
        # Info is general text, skip structured table parsing
        if tab_name == "Info":
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                cell = soup.find('td')
                mrbios_data["Info"] = cell_to_markdown(cell)
            print(f"Parsed Info.html (description file)")
            continue
            
        is_rev = (tab_name == "Revision history")
        result = parse_sheet_html(filepath, is_revision_history=is_rev)
        if result:
            mrbios_data[tab_name] = result["rows"]
            print(f"Parsed {filename}: {len(result['rows'])} rows, columns: {result['headers']}")
            
    print("\n--- Parsing Unicore upgrades catalog files ---")
    unicore_files = glob.glob(os.path.join(unicore_dir, "*.html"))
    for filepath in sorted(unicore_files):
        filename = os.path.basename(filepath)
        tab_name = filename.replace(".html", "")
        
        # Info is general text, skip structured table parsing
        if tab_name == "Info":
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                cell = soup.find('td')
                unicore_data["Info"] = cell_to_markdown(cell)
            print(f"Parsed Info.html (description file)")
            continue
            
        result = parse_sheet_html(filepath)
        if result:
            unicore_data[tab_name] = result["rows"]
            print(f"Parsed {filename}: {len(result['rows'])} rows, columns: {result['headers']}")
            
    # Save datasets to scratch directory
    mrbios_out = os.path.join(scratch_dir, "extracted_mrbios.json")
    unicore_out = os.path.join(scratch_dir, "extracted_unicore.json")
    
    with open(mrbios_out, 'w', encoding='utf-8') as f:
        json.dump(mrbios_data, f, indent=2, ensure_ascii=False)
        
    with open(unicore_out, 'w', encoding='utf-8') as f:
        json.dump(unicore_data, f, indent=2, ensure_ascii=False)
        
    print(f"\nSuccessfully wrote extraction results to:")
    print(f"- {mrbios_out}")
    print(f"- {unicore_out}")

if __name__ == "__main__":
    main()
