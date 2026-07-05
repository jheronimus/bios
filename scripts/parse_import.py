import os
import re
import hashlib
import sys

def calculate_sha256(filepath):
    """Calculate SHA256 of a file to check for duplicates."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return None

def parse_bios_image(data: bytes):
    """
    Parses a raw BIOS ROM image to extract ID and version info.
    Supports MR BIOS (Microid Research) and Award/Unicore formats.
    """
    if len(data) < 512:
        return None
        
    tail = data[-512:]
    
    # 1. MR BIOS Identification
    if b"MR BIOS" in data:
        version, bio_id, date = None, None, None
        
        # Look for pattern: Ver: V1.41-ACER310
        ver_match = re.search(b"Ver:\\s*(V\\d+\\.\\d+)-?([A-Z0-9]+)", tail, re.IGNORECASE)
        if ver_match:
            version = ver_match.group(1).decode("ascii")
            bio_id = ver_match.group(2).decode("ascii")
        else:
            # Look for pattern: MR BIOS (r)  V2.02 \t OPTI4D4
            alt_match = re.search(b"MR BIOS \\(r\\)\\s+(V\\d+\\.\\d+)\\s+.*?([A-Z0-9]{3,})", tail)
            if alt_match:
                version = alt_match.group(1).decode("ascii")
                bio_id = alt_match.group(2).decode("ascii")
                
        dates = re.findall(b"\\b\\d{2}/\\d{2}/\\d{2,4}\\b", tail)
        if dates:
            date = dates[-1].decode("ascii")
            
        return {
            "type": "MR BIOS",
            "id": bio_id if bio_id else "",
            "version": version if version else "",
            "date": date if date else ""
        }
        
    # 2. Award / Unicore Identification
    # Standard Award ID string is 8 or 9 chars located in the tail
    tail_short = data[-128:]
    award_match = re.search(b"([2356][A-Z0-9]{4}[A-Z0-9]{2}[A-Z0-9])", tail_short)
    if award_match:
        award_id = award_match.group(1).decode("ascii")
        dates = re.findall(b"\\b\\d{2}/\\d{2}/\\d{2,4}\\b", data)
        date = dates[-1].decode("ascii") if dates else None
        
        return {
            "type": "Award/Unicore",
            "id": award_id if award_id else "",
            "version": "",
            "date": date if date else ""
        }
        
    return None

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    bios_dir = os.path.join(repo_root, 'bios')
    import_dir = os.path.join(repo_root, 'import')
    new_yml_path = os.path.join(import_dir, 'new.yml')
    
    # 1. Gather all existing BIOS file hashes
    existing_hashes = {}
    print("Scanning existing collection for binary comparison...")
    for root, _, files in os.walk(bios_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ('.bin', '.rom'):
                path = os.path.join(root, file)
                file_hash = calculate_sha256(path)
                if file_hash:
                    # Save relative path for reporting duplicates
                    rel_path = os.path.relpath(path, repo_root)
                    existing_hashes[file_hash] = rel_path
                    
    print(f"Loaded {len(existing_hashes)} existing unique BIOS hashes.")

    # 2. Find and process all imported BIOS files
    imported_entries = []
    duplicates_found = []
    
    # Supported import file extensions
    import_extensions = ('.bin', '.rom')
    
    # Walk the import directory
    for root, _, files in os.walk(import_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in import_extensions:
                filepath = os.path.join(root, file)
                rel_import_path = os.path.relpath(filepath, repo_root)
                
                # Check for duplicate
                file_hash = calculate_sha256(filepath)
                if not file_hash:
                    continue
                    
                if file_hash in existing_hashes:
                    duplicates_found.append((rel_import_path, existing_hashes[file_hash]))
                    print(f"WARNING: {rel_import_path} is a duplicate of existing file {existing_hashes[file_hash]}", file=sys.stderr)
                    continue
                
                # Read file content for parsing
                try:
                    with open(filepath, 'rb') as f:
                        data = f.read()
                except Exception as e:
                    print(f"Error reading file {rel_import_path}: {e}", file=sys.stderr)
                    continue
                    
                # Parse metadata
                info = parse_bios_image(data)
                if info:
                    imported_entries.append((rel_import_path, info))
                else:
                    # Fallback to unknown entry with file path
                    imported_entries.append((rel_import_path, {
                        "type": "Unknown",
                        "id": "",
                        "version": "",
                        "date": ""
                    }))

    # 3. Write new.yml
    # We overwrite the file on each run
    print(f"Writing {len(imported_entries)} entries to {new_yml_path}...")
    try:
        with open(new_yml_path, 'w', encoding='utf-8') as f:
            for rel_path, info in imported_entries:
                if info['type'] == 'MR BIOS':
                    f.write("- Part Number: ''\n")
                    f.write(f"  Code: '{info['id']}'\n")
                    f.write("  Chipset: ''\n")
                    f.write("  Turbo: ''\n")
                    f.write("  Note: ''\n")
                    f.write("  Should work with: ''\n")
                    f.write(f"  Versions found: '{info['version']}'\n")
                    f.write("  files:\n")
                    f.write(f"  - {rel_path}\n")
                elif info['type'] == 'Award/Unicore':
                    f.write(f"- Folder: '{info['id']}'\n")
                    f.write("  Manufacturer: ''\n")
                    f.write("  Chipset: ''\n")
                    f.write("  I/O: ''\n")
                    f.write("  Release: ''\n")
                    f.write("  Motherboard: ''\n")
                    f.write("  Aliases: ''\n")
                    f.write("  files:\n")
                    f.write(f"  - {rel_path}\n")
                else:
                    # Unknown type placeholder (defaults to Unicore-like structure or basic path mapping)
                    f.write(f"- Folder: '{os.path.basename(rel_path)}'\n")
                    f.write("  Manufacturer: ''\n")
                    f.write("  Chipset: ''\n")
                    f.write("  I/O: ''\n")
                    f.write("  Release: ''\n")
                    f.write("  Motherboard: ''\n")
                    f.write("  Aliases: ''\n")
                    f.write("  files:\n")
                    f.write(f"  - {rel_path}\n")
        print("Done!")
    except Exception as e:
        print(f"Failed to write new.yml: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Exit with non-zero code if duplicates are found to flag warnings in CI, but still generate the file
    if duplicates_found:
        print(f"\nCompleted with {len(duplicates_found)} duplicate(s) detected.", file=sys.stderr)

if __name__ == '__main__':
    main()
