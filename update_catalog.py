"""
Update Catalog for indices_asc directory
"""

import json
from pathlib import Path

ASC_DIR = Path("indices_asc")

def parse_asc_metadata(content):
    lines = [l.strip() for l in content.strip().splitlines() if l.strip()]
    if not lines:
        return {}

    first_line = lines[0].split()
    start_year, end_year = None, None
    if len(first_line) >= 2 and first_line[0].isdigit() and first_line[1].isdigit():
        start_year = int(first_line[0])
        end_year = int(first_line[1])
    
    missing_value = None
    desc = ""
    for line in lines[1:]:
        if line.startswith("-99") or line.startswith("-999"):
            missing_value = line
        elif len(line.split()) > 0 and not line.split()[0].isdigit():
            desc += " " + line

    return {
        'start_year': start_year,
        'end_year': end_year,
        'line_count': len(lines),
        'missing_value_code': missing_value,
        'description': desc.strip()
    }

def main():
    asc_files = sorted(list(ASC_DIR.glob("*.asc")))
    catalog = []
    
    for asc in asc_files:
        try:
            with open(asc, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            meta = parse_asc_metadata(content)
            
            catalog.append({
                'asc_filename': asc.name,
                'file_path': str(asc.resolve()),
                'file_size_bytes': asc.stat().st_size,
                'start_year': meta.get('start_year'),
                'end_year': meta.get('end_year'),
                'line_count': meta.get('line_count'),
                'description': meta.get('description', '')
            })
        except Exception as e:
            print(f"Error reading {asc.name}: {e}")

    with open(ASC_DIR / "catalog.json", "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    with open(ASC_DIR / "catalog.csv", "w", encoding="utf-8") as f:
        f.write("asc_filename,start_year,end_year,file_size_bytes,description\n")
        for c in catalog:
            desc_clean = c['description'].replace('"', '""')
            f.write(f'"{c["asc_filename"]}",{c["start_year"]},{c["end_year"]},{c["file_size_bytes"]},"{desc_clean}"\n')

    print(f"Catalog updated successfully for {len(catalog)} .asc files.")

if __name__ == '__main__':
    main()
