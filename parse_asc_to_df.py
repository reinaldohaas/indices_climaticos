"""
Convert downloaded NOAA PSL .asc climate indices into a single clean CSV dataset.
Columns: Index_Name, Year, Month, Value, Date
"""

import os
import glob
import pandas as pd
from pathlib import Path

ASC_DIR = Path("indices_asc")
OUTPUT_CSV = Path("indices_asc/all_climate_indices_monthly.csv")

def parse_asc_file(filepath):
    lines = []
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            lines.append(line.strip())
            
    if not lines:
        return []

    # NOAA PSL format starts with start_year end_year on line 1
    # followed by rows: Year Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
    # followed by missing value line (e.g. -99.9 or -99.90)
    
    first_split = lines[0].split()
    if len(first_split) != 2 or not (first_split[0].isdigit() and first_split[1].isdigit()):
        # Not standard matrix format, try to parse line by line
        return []

    start_yr = int(first_split[0])
    end_yr = int(first_split[1])
    
    index_code = filepath.stem
    
    records = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 13 and parts[0].isdigit():
            yr = int(parts[0])
            if start_yr <= yr <= end_yr + 5: # allow current year
                for m in range(1, 13):
                    val_str = parts[m]
                    try:
                        val = float(val_str)
                        if val in [-99.9, -99.90, -999.0, -999.00, -99.99]:
                            val = None
                        records.append({
                            'index': index_code,
                            'year': yr,
                            'month': m,
                            'value': val,
                            'date': f"{yr:04d}-{m:02d}-01"
                        })
                    except ValueError:
                        continue
    return records

def main():
    all_records = []
    asc_files = list(ASC_DIR.glob("*.asc"))
    print(f"Parsing {len(asc_files)} .asc files...")

    parsed_count = 0
    for asc in asc_files:
        recs = parse_asc_file(asc)
        if recs:
            all_records.extend(recs)
            parsed_count += 1
            
    df = pd.DataFrame(all_records)
    print(f"Successfully extracted {len(df)} monthly observations across {parsed_count} indices.")
    
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Unified dataset saved to {OUTPUT_CSV}")

if __name__ == '__main__':
    main()
