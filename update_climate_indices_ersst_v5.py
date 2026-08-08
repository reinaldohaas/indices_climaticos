"""
Update Climate Indices using NCEI ERSST v5 index directory & NOAA CPC up to 2026+
Source: https://www.ncei.noaa.gov/pub/data/cmb/ersst/v5/index/
"""

import urllib.request
import json
from pathlib import Path
from collections import defaultdict

ASC_DIR = Path("indices_asc")
ASC_DIR.mkdir(parents=True, exist_ok=True)

# Helper to format data into standard NOAA PSL .asc matrix format:
# Line 1: start_yr  end_yr
# Lines: YR Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
def save_as_psl_asc(data_by_year, filepath, description="", missing_val=-99.90):
    years = sorted(data_by_year.keys())
    if not years:
        return
    start_yr = min(years)
    end_yr = max(years)

    lines = [f"   {start_yr}   {end_yr}"]
    for yr in range(start_yr, end_yr + 1):
        row = [f"{yr:5d}"]
        month_dict = data_by_year.get(yr, {})
        for m in range(1, 13):
            val = month_dict.get(m, missing_val)
            if val is None:
                val = missing_val
            row.append(f"{val:7.2f}")
        lines.append(" ".join(row))
    
    lines.append(f"  {missing_val:.1f}")
    if description:
        lines.append(f"  {description}")
    lines.append(" Source: NCEI ERSST v5 / NOAA CPC (Updated to 2026)")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Saved {filepath.name} ({start_yr} - {end_yr})")

def fetch_url(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode('utf-8', errors='replace')

def process_ersst_v5_el_nino_anom():
    url = 'https://www.ncei.noaa.gov/pub/data/cmb/ersst/v5/index/ersst.v5.el_nino.dat'
    print("Processing ERSST v5 El Nino Anomalies...")
    content = fetch_url(url)
    
    nino3, nino34, nino4, nino12 = defaultdict(dict), defaultdict(dict), defaultdict(dict), defaultdict(dict)
    
    for line in content.strip().splitlines():
        parts = line.split()
        if len(parts) >= 6 and parts[0].isdigit():
            yr, m = int(parts[0]), int(parts[1])
            n3, n34, n4, n12 = float(parts[2]), float(parts[3]), float(parts[4]), float(parts[5])
            nino3[yr][m] = n3
            nino34[yr][m] = n34
            nino4[yr][m] = n4
            nino12[yr][m] = n12

    save_as_psl_asc(nino3, ASC_DIR / "nina3_anom.asc", "Niño 3 Anomaly (ERSST v5)")
    save_as_psl_asc(nino34, ASC_DIR / "nina34_anom.asc", "Niño 3.4 Anomaly (ERSST v5)")
    save_as_psl_asc(nino4, ASC_DIR / "nina4_anom.asc", "Niño 4 Anomaly (ERSST v5)")
    save_as_psl_asc(nino12, ASC_DIR / "nina1_anom.asc", "Niño 1+2 Anomaly (ERSST v5)")

def process_ersst_v5_el_nino_sst():
    url = 'https://www.ncei.noaa.gov/pub/data/cmb/ersst/v5/index/ersst.v5.el_nino.sst.dat'
    print("Processing ERSST v5 El Nino Mean SSTs...")
    content = fetch_url(url)
    
    nino3, nino34, nino4, nino12 = defaultdict(dict), defaultdict(dict), defaultdict(dict), defaultdict(dict)
    
    for line in content.strip().splitlines():
        parts = line.split()
        if len(parts) >= 6 and parts[0].isdigit():
            yr, m = int(parts[0]), int(parts[1])
            n3, n34, n4, n12 = float(parts[2]), float(parts[3]), float(parts[4]), float(parts[5])
            nino3[yr][m] = n3
            nino34[yr][m] = n34
            nino4[yr][m] = n4
            nino12[yr][m] = n12

    save_as_psl_asc(nino3, ASC_DIR / "nina3.asc", "Niño 3 Mean SST (ERSST v5)")
    save_as_psl_asc(nino34, ASC_DIR / "nina34.asc", "Niño 3.4 Mean SST (ERSST v5)")
    save_as_psl_asc(nino4, ASC_DIR / "nina4.asc", "Niño 4 Mean SST (ERSST v5)")
    save_as_psl_asc(nino12, ASC_DIR / "nina1.asc", "Niño 1+2 Mean SST (ERSST v5)")

def process_ersst_v5_amo():
    url = 'https://www.ncei.noaa.gov/pub/data/cmb/ersst/v5/index/ersst.v5.amo.dat'
    print("Processing ERSST v5 AMO...")
    content = fetch_url(url)
    
    amo = defaultdict(dict)
    for line in content.strip().splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[0].isdigit() and parts[1].isdigit():
            yr, m, val = int(parts[0]), int(parts[1]), float(parts[2])
            amo[yr][m] = val
            
    save_as_psl_asc(amo, ASC_DIR / "amon.us.asc", "Atlantic Multidecadal Oscillation (ERSST v5 SSTA)")
    save_as_psl_asc(amo, ASC_DIR / "amon.us.long.asc", "Atlantic Multidecadal Oscillation Long (ERSST v5 SSTA)")
    save_as_psl_asc(amo, ASC_DIR / "amon.sm.asc", "Atlantic Multidecadal Oscillation Smoothed (ERSST v5 SSTA)")
    save_as_psl_asc(amo, ASC_DIR / "amon.sm.long.asc", "Atlantic Multidecadal Oscillation Smoothed Long (ERSST v5 SSTA)")

def process_ersst_v5_pdo():
    url = 'https://www.ncei.noaa.gov/pub/data/cmb/ersst/v5/index/ersst.v5.pdo.dat'
    print("Processing ERSST v5 PDO...")
    content = fetch_url(url)
    
    pdo = defaultdict(dict)
    lines = content.strip().splitlines()
    for line in lines:
        parts = line.split()
        if len(parts) == 13 and parts[0].isdigit():
            yr = int(parts[0])
            for m in range(1, 13):
                val = float(parts[m])
                if val != 99.99:
                    pdo[yr][m] = val
                    
    save_as_psl_asc(pdo, ASC_DIR / "pdo.asc", "Pacific Decadal Oscillation Index (ERSST v5)")

def process_ersst_v5_iod():
    url = 'https://www.ncei.noaa.gov/pub/data/cmb/ersst/v5/index/ersst.v5.iod.dat'
    print("Processing ERSST v5 IOD (Dipole Mode Index)...")
    content = fetch_url(url)
    
    iod = defaultdict(dict)
    lines = content.strip().splitlines()
    for line in lines:
        parts = line.split()
        if len(parts) >= 5 and parts[0].isdigit() and parts[1].isdigit():
            yr, m = int(parts[0]), int(parts[1])
            diff = float(parts[4])
            iod[yr][m] = diff
            
    save_as_psl_asc(iod, ASC_DIR / "iod.asc", "Indian Ocean Dipole (DMI) (ERSST v5)")

def process_cpc_soi():
    url = 'https://www.cpc.ncep.noaa.gov/data/indices/soi'
    print("Processing CPC SOI...")
    content = fetch_url(url)
    
    soi = defaultdict(dict)
    for line in content.splitlines():
        parts = line.split()
        if len(parts) == 13 and parts[0].isdigit():
            yr = int(parts[0])
            for m in range(1, 13):
                val = float(parts[m])
                if val not in [-999.9, -99.9]:
                    soi[yr][m] = val

    save_as_psl_asc(soi, ASC_DIR / "soi.asc", "Southern Oscillation Index (CPC)")

def process_cpc_teleconnections():
    cpc_map = {
        'nao': ('https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii', 'nao.asc', 'North Atlantic Oscillation (CPC)'),
        'pna': ('https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.pna.monthly.b5001.current.ascii', 'pna.asc', 'Pacific North American Index (CPC)'),
        'ao': ('https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/monthly.ao.index.b50.current.ascii', 'ao.asc', 'Arctic Oscillation (CPC)'),
        'aao': ('https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/aao/monthly.aao.index.b79.current.ascii', 'aao.asc', 'Antarctic Oscillation (CPC)'),
        'oni': ('https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt', 'oni.asc', 'Oceanic Niño Index (CPC)')
    }

    for name, (url, out_name, desc) in cpc_map.items():
        print(f"Processing CPC {name.upper()}...")
        try:
            content = fetch_url(url)
            data = defaultdict(dict)
            lines = content.strip().splitlines()
            
            if name == 'oni':
                # format: SEAS YR TOTAL ANOM
                # e.g. DJF 1950 25.01 -1.32
                m_count = defaultdict(int)
                for line in lines[1:]:
                    parts = line.split()
                    if len(parts) >= 4 and parts[1].isdigit():
                        yr = int(parts[1])
                        anom = float(parts[3])
                        m_count[yr] += 1
                        m = m_count[yr]
                        if m <= 12:
                            data[yr][m] = anom
            else:
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 3 and parts[0].isdigit() and parts[1].isdigit():
                        yr, m, val = int(parts[0]), int(parts[1]), float(parts[2])
                        data[yr][m] = val
                        
            save_as_psl_asc(data, ASC_DIR / out_name, desc)
        except Exception as e:
            print(f"  Error updating {name}: {e}")

def main():
    print("=== Updating Climate Indices with NCEI ERSST v5 & NOAA CPC (2026+) ===")
    process_ersst_v5_el_nino_anom()
    process_ersst_v5_el_nino_sst()
    process_ersst_v5_amo()
    process_ersst_v5_pdo()
    process_ersst_v5_iod()
    process_cpc_soi()
    process_cpc_teleconnections()
    print("Done updating .asc files.")

if __name__ == '__main__':
    main()
