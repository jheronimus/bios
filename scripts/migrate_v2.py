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
                f.write(f"---\ntitle: \"Unicore Upgrades\"\n---\n")
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
            f_md.write(f"---\ntitle: \"{tab_name}\"\nlayout: \"catalog\"\ncatalog_type: \"unicore\"\ncatalog_name: \"{md_filename}\"\n---\n")

    # 4. Process MR BIOS catalog and link files
    # MR BIOS files are matched by Part Number or Code
    print("\nProcessing MR BIOS catalog...")
    os.makedirs("data/mrbios", exist_ok=True)
    
    for tab_name, rows in mrbios_catalog.items():
        if tab_name == "Info":
            # Save Info page
            os.makedirs("site/content/mrbios", exist_ok=True)
            with open("site/content/mrbios/_index.md", "w", encoding="utf-8") as f:
                f.write(f"---\ntitle: \"MR BIOS\"\n---\n")
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
            
            # Substring match on Part Number
            if len(part_no) >= 4:
                for filepath in mrbios_files:
                    if part_no in filepath.replace("\\", "/").upper():
                        linked_files.add(filepath)
            
            # Special fallback for Mosel V047B404 typo in sheet (actual folder is V047B405)
            if part_no == "V047B404":
                for filepath in mrbios_files:
                    if "V047B405" in filepath.replace("\\", "/").upper():
                        linked_files.add(filepath)
                        
            # Substring match on Code
            if len(code) >= 4:
                for filepath in mrbios_files:
                    filename_no_ext = os.path.splitext(os.path.basename(filepath))[0].upper()
                    if code in filepath.replace("\\", "/").upper() or filename_no_ext == code:
                        linked_files.add(filepath)
                        
            # Substring match on Shareware filename (which might be multiline)
            if shareware:
                for line in shareware.split('\n'):
                    line_clean = line.strip().upper()
                    if len(line_clean) >= 4:
                        for filepath in mrbios_files:
                            if line_clean in filepath.replace("\\", "/").upper():
                                linked_files.add(filepath)
                        
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
            f_md.write(f"---\ntitle: \"{tab_name}\"\nlayout: \"catalog\"\ncatalog_type: \"mrbios\"\ncatalog_name: \"{md_filename}\"\n---\n")

    print("\nMigration completed successfully!")

if __name__ == "__main__":
    main()
