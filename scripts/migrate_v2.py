import os
import re
import json
import shutil
import yaml

def sanitize_filename(name):
    name = name.lower()
    name = name.replace("c&t", "c_and_t")
    name = name.replace("ttl discrete logic", "ttl_discrete_logic")
    name = name.replace("motherboards that came with stock mrbios", "motherboards_with_stock_mrbios")
    name = name.replace(" ", "_")
    name = re.sub(r'[^a-z0-9_]', '', name)
    return name

def main():
    # 1. Move directories to their final repo locations
    if os.path.exists("import/MRBIOS") and not os.path.exists("bios/mrbios"):
        os.makedirs("bios", exist_ok=True)
        shutil.move("import/MRBIOS", "bios/mrbios")
        print("Moved import/MRBIOS -> bios/mrbios")
        
    if os.path.exists("import/UNICORE") and not os.path.exists("bios/unicore"):
        os.makedirs("bios", exist_ok=True)
        shutil.move("import/UNICORE", "bios/unicore")
        print("Moved import/UNICORE -> bios/unicore")

    # 2. Build index of files in bios/mrbios and bios/unicore
    print("Indexing bios files...")
    mrbios_files = []
    unicore_files = []
    
    if os.path.exists("bios/mrbios"):
        for root, dirs, files in os.walk("bios/mrbios"):
            for file in files:
                if file.upper().endswith(('.BIN', '.BIO', '.ROM')):
                    mrbios_files.append(os.path.relpath(os.path.join(root, file)))
                    
    if os.path.exists("bios/unicore"):
        for root, dirs, files in os.walk("bios/unicore"):
            for file in files:
                if file.upper().endswith(('.BIN', '.BIO', '.ROM')):
                    unicore_files.append(os.path.relpath(os.path.join(root, file)))

    print(f"Found {len(mrbios_files)} MR BIOS files and {len(unicore_files)} Unicore files.")

    # Load extracted JSON datasets from scratch
    scratch_dir = "/Users/ilembitov/.gemini/antigravity-cli/brain/2bc4377f-c3f0-461b-b741-cb28618d039c/scratch"
    
    with open(os.path.join(scratch_dir, "extracted_mrbios.json"), "r", encoding="utf-8") as f:
        mrbios_catalog = json.load(f)
        
    with open(os.path.join(scratch_dir, "extracted_unicore.json"), "r", encoding="utf-8") as f:
        unicore_catalog = json.load(f)

    # 3. Process Unicore catalog and link files
    # Unicore files are matched by Folder ID (Award bios string/folder)
    print("\nProcessing Unicore catalog...")
    os.makedirs("data/unicore", exist_ok=True)
    
    # Pre-index unicore files by folder id
    unicore_file_map = {}
    for filepath in unicore_files:
        # Extract folder id (e.g. 2A5KKA29) from the path
        parts = filepath.split(os.sep)
        for part in parts:
            if re.match(r'^[A-Z0-9]{8}$', part.upper()):
                unicore_file_map.setdefault(part.upper(), []).append(filepath)
                
    for tab_name, rows in unicore_catalog.items():
        if tab_name == "Info":
            # Save Info page
            os.makedirs("site/content/unicore", exist_ok=True)
            with open("site/content/unicore/_index.md", "w", encoding="utf-8") as f:
                f.write(f"---\ntitle: \"Unicore Awards BIOS catalog\"\n---\n\n{rows}\n")
            print("Wrote site/content/unicore/_index.md")
            continue
            
        updated_rows = []
        linked_count = 0
        for row in rows:
            folder_id = row.get("Folder", "").strip().upper()
            linked_files = []
            if folder_id in unicore_file_map:
                linked_files = sorted(unicore_file_map[folder_id])
                linked_count += 1
            row["files"] = linked_files
            updated_rows.append(row)
            
        out_yaml_path = f"data/unicore/{sanitize_filename(tab_name)}.yml"
        with open(out_yaml_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(updated_rows, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"Wrote {out_yaml_path} with {len(updated_rows)} entries ({linked_count} linked to binaries)")
        
        # Write matching Markdown content file
        md_filename = sanitize_filename(tab_name)
        with open(f"site/content/unicore/{md_filename}.md", "w", encoding="utf-8") as f_md:
            f_md.write(f"---\ntitle: \"{tab_name} Chipsets\"\nlayout: \"catalog\"\ncatalog_type: \"unicore\"\ncatalog_name: \"{md_filename}\"\n---\n")

    # 4. Process MR BIOS catalog and link files
    # MR BIOS files are matched by Part Number or Code
    print("\nProcessing MR BIOS catalog...")
    os.makedirs("data/mrbios", exist_ok=True)
    
    # Pre-index MR BIOS files
    # We index by part number regex matches in path/filename, and by code/shareware filename
    mrbios_part_map = {}
    mrbios_code_map = {}
    
    part_no_regex = re.compile(r'V\d{3}[A-Z0-9]{4}', re.IGNORECASE)
    
    for filepath in mrbios_files:
        filename = os.path.basename(filepath)
        name_no_ext = os.path.splitext(filename)[0].upper()
        
        # Match by filename
        mrbios_code_map.setdefault(name_no_ext, []).append(filepath)
        
        # Match part number regex anywhere in path
        path_parts = filepath.upper().split(os.sep)
        for part in path_parts:
            # Check for standard part number format VxxxXxxx
            m = part_no_regex.search(part)
            if m:
                mrbios_part_map.setdefault(m.group(0).upper(), []).append(filepath)
            # Also check for shareware names like MR_ACER
            if part.startswith("MR_"):
                mrbios_code_map.setdefault(part, []).append(filepath)
                
    for tab_name, rows in mrbios_catalog.items():
        if tab_name == "Info":
            # Save Info page
            os.makedirs("site/content/mrbios", exist_ok=True)
            with open("site/content/mrbios/_index.md", "w", encoding="utf-8") as f:
                f.write(f"---\ntitle: \"MR BIOS catalog\"\n---\n\n{rows}\n")
            print("Wrote site/content/mrbios/_index.md")
            continue
            
        if tab_name == "Revision history":
            # Save Revision history as content page
            os.makedirs("site/content/mrbios", exist_ok=True)
            with open("site/content/mrbios/revision_history.md", "w", encoding="utf-8") as f:
                f.write("---\ntitle: \"MR BIOS Revision History\"\n---\n\n| Version | Description |\n|---|---|\n")
                for row in rows:
                    f.write(f"| {row.get('Version','')} | {row.get('Description','').replace(chr(10), '<br>')} |\n")
            print("Wrote site/content/mrbios/revision_history.md")
            continue
            
        updated_rows = []
        linked_count = 0
        for row in rows:
            part_no = (row.get("Part Number") or row.get("Part number") or row.get("INTL50C") or "").strip().upper()
            code = row.get("Code", "").strip().upper()
            shareware = row.get("Shareware filename", "").strip().upper()
            
            linked_files = set()
            
            # Match by Part Number
            if part_no in mrbios_part_map:
                linked_files.update(mrbios_part_map[part_no])
                
            # Match by Code
            if code in mrbios_code_map:
                linked_files.update(mrbios_code_map[code])
                
            # Match by Shareware filename (which might be multiline)
            if shareware:
                for line in shareware.split('\n'):
                    line_clean = line.strip().upper()
                    if line_clean in mrbios_code_map:
                        linked_files.update(mrbios_code_map[line_clean])
                        
            linked_files_list = sorted(list(linked_files))
            if linked_files_list:
                linked_count += 1
                
            row["files"] = linked_files_list
            updated_rows.append(row)
            
        out_yaml_path = f"data/mrbios/{sanitize_filename(tab_name)}.yml"
        with open(out_yaml_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(updated_rows, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"Wrote {out_yaml_path} with {len(updated_rows)} entries ({linked_count} linked to binaries)")
        
        # Write matching Markdown content file
        md_filename = sanitize_filename(tab_name)
        with open(f"site/content/mrbios/{md_filename}.md", "w", encoding="utf-8") as f_md:
            f_md.write(f"---\ntitle: \"{tab_name} Chipsets\"\nlayout: \"catalog\"\ncatalog_type: \"mrbios\"\ncatalog_name: \"{md_filename}\"\n---\n")

    print("\nMigration completed successfully!")

if __name__ == "__main__":
    main()
