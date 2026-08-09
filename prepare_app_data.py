"""
Prepare App Data and Metadata JSON for Ultra-Fast Web App Loading
With Complete Category Mapping for All Climate Indices
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path

APP_DIR = Path("app")
APP_DIR.mkdir(parents=True, exist_ok=True)

# Comprehensive Category Mapping
CATEGORY_MAP = {
    # ENSO
    'oni': ('ENSO', 'Oceanic Niño Index (NOAA CPC)'),
    'roni': ('ENSO', 'Relative Oceanic Niño Index (NOAA CPC)'),
    'mei': ('ENSO', 'Multivariate ENSO Index v1 (NOAA PSL)'),
    'meiv2': ('ENSO', 'Multivariate ENSO Index v2 (NOAA PSL)'),
    'nina1': ('ENSO', 'Niño 1+2 SST (ERSST v5)'),
    'nina1_anom': ('ENSO', 'Niño 1+2 Anomaly (ERSST v5)'),
    'nina3': ('ENSO', 'Niño 3 SST (ERSST v5)'),
    'nina3_anom': ('ENSO', 'Niño 3 Anomaly (ERSST v5)'),
    'nina34': ('ENSO', 'Niño 3.4 SST (ERSST v5)'),
    'nina34_anom': ('ENSO', 'Niño 3.4 Anomaly (ERSST v5)'),
    'nina4': ('ENSO', 'Niño 4 SST (ERSST v5)'),
    'nina4_anom': ('ENSO', 'Niño 4 Anomaly (ERSST v5)'),
    'soi': ('ENSO', 'Southern Oscillation Index (NOAA CPC)'),
    'tni': ('ENSO', 'Trans-Niño Index (NOAA PSL)'),
    'censo': ('ENSO', 'BEST Bivariate ENSO Index'),
    'censo.long': ('ENSO', 'BEST Bivariate ENSO Index Long'),
    'ersst5.nino.mth.91-20': ('ENSO', 'Niño 3.4 ERSSTv5 Climatology'),

    # Hemisfério Sul
    'sam': ('Hemisfério Sul', 'Marshall Station-based Southern Annular Mode Index (BAS)'),
    'aao': ('Hemisfério Sul', 'Antarctic Oscillation / SAM (NOAA CPC)'),
    'psa1': ('Hemisfério Sul', 'Pacific-South American Pattern 1 Index (NCEP 500hPa)'),
    'psa2': ('Hemisfério Sul', 'Pacific-South American Pattern 2 Index (NCEP 500hPa)'),

    # Atlântico Sul
    'sad': ('Atlântico Sul', 'South Atlantic Dipole Index (Morioka 2011 / ERSSTv5)'),
    'sasdi': ('Atlântico Sul', 'South Atlantic Subtropical Dipole Index (Rodrigues 2015 / ERSSTv5)'),
    'sacz': ('Atlântico Sul', 'South Atlantic Convergence Zone (SACZ) OLR Index (Carvalho 2004)'),
    'amm': ('Atlântico Sul', 'Atlantic Meridional Mode (NOAA PSL)'),
    'ammsst': ('Atlântico Sul', 'Atlantic Meridional Mode SST Component'),
    'amon.us': ('Atlântico Sul', 'Atlantic Multidecadal Oscillation Unsmoothed (ERSSTv5)'),
    'amon.us.long': ('Atlântico Sul', 'Atlantic Multidecadal Oscillation Unsmoothed Long'),
    'amon.sm': ('Atlântico Sul', 'Atlantic Multidecadal Oscillation Smoothed (ERSSTv5)'),
    'amon.sm.long': ('Atlântico Sul', 'Atlantic Multidecadal Oscillation Smoothed Long'),
    'tna': ('Atlântico Sul', 'Tropical Northern Atlantic Index (NOAA PSL)'),
    'tsa': ('Atlântico Sul', 'Tropical Southern Atlantic Index (NOAA PSL)'),
    'nta': ('Atlântico Sul', 'North Tropical Atlantic Index'),
    'car': ('Atlântico Sul', 'Caribbean SST Index'),
    'CAR_ersst': ('Atlântico Sul', 'Caribbean SST Index (ERSSTv5)'),
    'NTA_ersst': ('Atlântico Sul', 'North Tropical Atlantic Index (ERSSTv5)'),
    'atltri': ('Atlântico Sul', 'Atlantic Tripole SST EOF Index'),

    # Pacífico
    'pdo': ('Pacífico', 'Pacific Decadal Oscillation Index (ERSSTv5)'),
    'pmm': ('Pacífico', 'Pacific Meridional Mode SST Index (Chiang & Vimont 2004)'),
    'npmm': ('Pacífico', 'North Pacific Meridional Mode SST Index (Chiang & Vimont 2004)'),
    'np': ('Pacífico', 'North Pacific Index Trenberth & Hurrell (NCAR / NOAA PSL)'),
    'ipotpi.hadisst2': ('Pacífico', 'Interdecadal Pacific Oscillation / TPI (HadISST2)'),
    'pna': ('Pacífico', 'Pacific North American Index (NOAA CPC)'),
    'epo': ('Pacífico', 'East Pacific / North Pacific Index (NOAA CPC)'),
    'wp': ('Pacífico', 'Western Pacific Index (NOAA CPC)'),
    'pacwarm': ('Pacífico', 'Pacific Warm Pool SST Region Index'),
    'pacwarmpool.ersst': ('Pacífico', 'Pacific Warm Pool SST Region Long (ERSSTv5)'),
    'eofpac': ('Pacífico', 'Tropical Pacific SST EOF Index'),
    'noi': ('Pacífico', 'North Pacific Oscillation Index'),

    # Teleconexões
    'nao': ('Teleconexões', 'North Atlantic Oscillation (NOAA CPC)'),
    'ao': ('Teleconexões', 'Arctic Oscillation (NOAA CPC)'),
    'ea': ('Teleconexões', 'East Atlantic Pattern (NOAA CPC)'),
    'eawr': ('Teleconexões', 'East Atlantic / Western Russia Pattern (NOAA CPC)'),
    'scand': ('Teleconexões', 'Scandinavia Pattern (NOAA CPC)'),
    'jonesnao': ('Teleconexões', 'North Atlantic Oscillation (Jones Station-based)'),

    # Convecção / Monção / MJO
    'sami': ('Convecção', 'South American Monsoon Index 850hPa Zonal Wind (Vera 2006)'),
    'mjo_omi': ('Convecção', 'Madden-Julian Oscillation OMI Amplitude (NOAA PSL)'),
    'mjo_vpm': ('Convecção', 'Madden-Julian Oscillation VPM Amplitude (NOAA PSL)'),
    'mjo_romi': ('Convecção', 'Madden-Julian Oscillation ROMI Amplitude (NOAA PSL)'),
    'mjo_20e': ('Convecção', 'MJO Longitude Band 20E (NOAA CPC)'),
    'mjo_70e': ('Convecção', 'MJO Longitude Band 70E (NOAA CPC)'),
    'mjo_80e': ('Convecção', 'MJO Longitude Band 80E (NOAA CPC)'),
    'mjo_100e': ('Convecção', 'MJO Longitude Band 100E (NOAA CPC)'),
    'mjo_120e': ('Convecção', 'MJO Longitude Band 120E (NOAA CPC)'),
    'mjo_140e': ('Convecção', 'MJO Longitude Band 140E (NOAA CPC)'),
    'mjo_160e': ('Convecção', 'MJO Longitude Band 160E (NOAA CPC)'),
    'mjo_120w': ('Convecção', 'MJO Longitude Band 120W (NOAA CPC)'),
    'mjo_40w': ('Convecção', 'MJO Longitude Band 40W (NOAA CPC)'),
    'mjo_10w': ('Convecção', 'MJO Longitude Band 10W (NOAA CPC)'),
    'mjo_pentad': ('Convecção', 'MJO Pentad Series (NOAA CPC)'),
    'mjo_fase': ('Convecção', 'MJO Amplitude / Phase Index'),
    'mjo_modulo': ('Convecção', 'MJO Modulo / Amplitude Index'),
    'brazilrain': ('Convecção', 'Northeast Brazil Rainfall Anomaly Index'),
    'sahelrain': ('Convecção', 'Sahel Rainfall Anomaly Index'),
    'indiamon': ('Convecção', 'Central Indian Monsoon Precipitation Index'),
    'swmonsoon': ('Convecção', 'Southwest Monsoon Region Rainfall Index'),
    'espi': ('Convecção', 'ENSO Precipitation Index'),
    'qbo': ('Convecção', 'Quasi-Biennial Oscillation Index (NOAA PSL)'),
    'glaam': ('Convecção', 'Globally Integrated Angular Momentum Index'),

    # Solar & Clima Global
    'ssn': ('Solar', 'Sunspot Number Monthly Total (SILSO)'),
    'solar': ('Solar', 'Solar Flux 10.7cm (NOAA / DRAO)'),
    'gmsst': ('Solar', 'Global Mean Land/Ocean Temperature Index'),
    'GLB.Ts+dSST': ('Solar', 'NASA GISTEMP Global Land-Ocean Temperature Index'),
    'trend': ('Solar', 'Global Temperature Trend Line'),
    'hurr': ('Solar', 'Atlantic Tropical Hurricane Activity Index')
}

print("Reading all_climate_indices_monthly.csv...")
df = pd.read_csv("indices_asc/all_climate_indices_monthly.csv")

# Filter out NaNs / None and format dict
print("Formatting time series data...")
data_dict = {}
for idx_name, group in df.groupby("index"):
    group = group.sort_values("date")
    clean_group = group.dropna(subset=["value"])
    data_dict[idx_name] = {
        "dates": clean_group["date"].tolist(),
        "values": [round(float(v), 3) for v in clean_group["value"].values],
        "years": [int(y) for y in clean_group["year"].values],
        "months": [int(m) for m in clean_group["month"].values]
    }

# Save data.json
data_json_path = APP_DIR / "data.json"
with open(data_json_path, "w", encoding="utf-8") as f:
    json.dump(data_dict, f, ensure_ascii=False)
print(f"Saved app/data.json ({data_json_path.stat().st_size / 1024 / 1024:.2f} MB).")

# Build comprehensive metadata.json
meta_list = []
for idx_name in sorted(data_dict.keys()):
    group = df[(df["index"] == idx_name) & (df["value"].notna())].sort_values("date")
    if group.empty:
        continue
    start_date = f"{group['year'].min()}-{group['month'].min():02d}-01"
    end_date = f"{group['year'].max()}-{group['month'].max():02d}-01"

    cat, desc = CATEGORY_MAP.get(idx_name, ("Outros", f"Índice Climático {idx_name.upper()}"))
    
    meta_list.append({
        "index": idx_name,
        "filename": f"{idx_name}.asc",
        "category": cat,
        "description": desc,
        "source": "NOAA PSL / CPC / SILSO / BAS / NCAR",
        "source_url": "https://psl.noaa.gov/data/climateindices/list/",
        "start_date": start_date,
        "end_date": end_date,
        "units": "standardized / absolute",
        "reference": "NOAA PSL Climate Indices Database"
    })

meta_json_path = APP_DIR / "metadata.json"
with open(meta_json_path, "w", encoding="utf-8") as f:
    json.dump(meta_list, f, indent=2, ensure_ascii=False)
print(f"Saved app/metadata.json ({len(meta_list)} items).")

# Also save climate_indices_metadata.csv
pd.DataFrame(meta_list).to_csv("climate_indices_metadata.csv", index=False, encoding="utf-8")
print("Saved climate_indices_metadata.csv.")
