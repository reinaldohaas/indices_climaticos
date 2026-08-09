"""
Refine Metadata Descriptions and Clean Short Sigla Labels for All Climate Indices
"""

import json
import pandas as pd
from pathlib import Path

# Clean short labels & descriptions dictionary
CLEAN_SPECS = {
    # ENSO
    'oni': ('ENSO', 'ONI', 'Oceanic Niño Index (NOAA CPC)'),
    'roni': ('ENSO', 'RONI', 'Relative Oceanic Niño Index (NOAA CPC)'),
    'mei': ('ENSO', 'MEI v1', 'Multivariate ENSO Index v1 (NOAA PSL)'),
    'meiv2': ('ENSO', 'MEI v2', 'Multivariate ENSO Index v2 (NOAA PSL)'),
    'nina1': ('ENSO', 'Niño 1+2', 'Niño 1+2 SST (ERSST v5)'),
    'nina1_anom': ('ENSO', 'Niño 1+2 Anom', 'Niño 1+2 Anomaly (ERSST v5)'),
    'nina3': ('ENSO', 'Niño 3', 'Niño 3 SST (ERSST v5)'),
    'nina3_anom': ('ENSO', 'Niño 3 Anom', 'Niño 3 Anomaly (ERSST v5)'),
    'nina34': ('ENSO', 'Niño 3.4', 'Niño 3.4 SST (ERSST v5)'),
    'nina34_anom': ('ENSO', 'Niño 3.4 Anom', 'Niño 3.4 Anomaly (ERSST v5)'),
    'nina4': ('ENSO', 'Niño 4', 'Niño 4 SST (ERSST v5)'),
    'nina4_anom': ('ENSO', 'Niño 4 Anom', 'Niño 4 Anomaly (ERSST v5)'),
    'soi': ('ENSO', 'SOI', 'Southern Oscillation Index (NOAA CPC)'),
    'tni': ('ENSO', 'TNI', 'Trans-Niño Index (NOAA PSL)'),
    'censo': ('ENSO', 'BEST ENSO', 'BEST Bivariate ENSO Index'),
    'censo.long': ('ENSO', 'BEST ENSO Long', 'BEST Bivariate ENSO Index Long'),
    'ersst5.nino.mth.91-20': ('ENSO', 'Niño 3.4 Climatology', 'Niño 3.4 ERSSTv5 Climatology'),

    # Hemisfério Sul
    'sam': ('Hemisfério Sul', 'SAM', 'Southern Annular Mode Station-based (BAS)'),
    'aao': ('Hemisfério Sul', 'AAO', 'Antarctic Oscillation / SAM (NOAA CPC)'),
    'psa1': ('Hemisfério Sul', 'PSA1', 'Pacific-South American Pattern 1 (NCEP 500hPa)'),
    'psa2': ('Hemisfério Sul', 'PSA2', 'Pacific-South American Pattern 2 (NCEP 500hPa)'),

    # Atlântico Sul
    'sad': ('Atlântico Sul', 'SAD', 'South Atlantic Dipole Index (ERSSTv5)'),
    'sasdi': ('Atlântico Sul', 'SASDI', 'South Atlantic Subtropical Dipole Index (ERSSTv5)'),
    'sacz': ('Atlântico Sul', 'SACZ', 'South Atlantic Convergence Zone OLR Index'),
    'amm': ('Atlântico Sul', 'AMM', 'Atlantic Meridional Mode (NOAA PSL)'),
    'ammsst': ('Atlântico Sul', 'AMM SST', 'Atlantic Meridional Mode SST Component'),
    'amon.us': ('Atlântico Sul', 'AMO Unsmoothed', 'Atlantic Multidecadal Oscillation Unsmoothed'),
    'amon.us.long': ('Atlântico Sul', 'AMO Unsmoothed Long', 'AMO Unsmoothed Long (ERSSTv5)'),
    'amon.sm': ('Atlântico Sul', 'AMO Smoothed', 'Atlantic Multidecadal Oscillation Smoothed'),
    'amon.sm.long': ('Atlântico Sul', 'AMO Smoothed Long', 'AMO Smoothed Long (ERSSTv5)'),
    'tna': ('Atlântico Sul', 'TNA', 'Tropical Northern Atlantic Index'),
    'tsa': ('Atlântico Sul', 'TSA', 'Tropical Southern Atlantic Index'),
    'nta': ('Atlântico Sul', 'NTA', 'North Tropical Atlantic Index'),
    'car': ('Atlântico Sul', 'CAR', 'Caribbean SST Index'),
    'CAR_ersst': ('Atlântico Sul', 'CAR ERSSTv5', 'Caribbean SST Index (ERSSTv5)'),
    'NTA_ersst': ('Atlântico Sul', 'NTA ERSSTv5', 'North Tropical Atlantic Index (ERSSTv5)'),
    'atltri': ('Atlântico Sul', 'Atlantic Tripole', 'Atlantic Tripole SST EOF Index'),

    # Pacífico
    'pdo': ('Pacífico', 'PDO', 'Pacific Decadal Oscillation Index (ERSSTv5)'),
    'pmm': ('Pacífico', 'PMM', 'Pacific Meridional Mode SST Index'),
    'npmm': ('Pacífico', 'NPMM', 'North Pacific Meridional Mode SST Index'),
    'np': ('Pacífico', 'NP', 'North Pacific Index (NCAR / NOAA PSL)'),
    'ipotpi.hadisst2': ('Pacífico', 'IPO / TPI', 'Interdecadal Pacific Oscillation (HadISST2)'),
    'pna': ('Pacífico', 'PNA', 'Pacific North American Index (NOAA CPC)'),
    'epo': ('Pacífico', 'EPO', 'East Pacific / North Pacific Index (NOAA CPC)'),
    'wp': ('Pacífico', 'WP', 'Western Pacific Index (NOAA CPC)'),
    'pacwarm': ('Pacífico', 'Pacific Warmpool', 'Pacific Warm Pool SST Region Index'),
    'pacwarmpool.ersst': ('Pacífico', 'Pacific Warmpool ERSSTv5', 'Pacific Warm Pool SST Region Long'),
    'eofpac': ('Pacífico', 'Pacific SST EOF', 'Tropical Pacific SST EOF Index'),
    'noi': ('Pacífico', 'NOI', 'North Pacific Oscillation Index'),

    # Teleconexões
    'nao': ('Teleconexões', 'NAO', 'North Atlantic Oscillation (NOAA CPC)'),
    'ao': ('Teleconexões', 'AO', 'Arctic Oscillation (NOAA CPC)'),
    'ea': ('Teleconexões', 'EA', 'East Atlantic Pattern (NOAA CPC)'),
    'eawr': ('Teleconexões', 'EA/WR', 'East Atlantic / Western Russia Pattern (NOAA CPC)'),
    'scand': ('Teleconexões', 'SCAND', 'Scandinavia Pattern (NOAA CPC)'),
    'jonesnao': ('Teleconexões', 'NAO (Jones)', 'North Atlantic Oscillation Station-based'),

    # Convecção / Monção / MJO
    'sami': ('Convecção', 'SAMI', 'South American Monsoon Index 850hPa Wind'),
    'mjo_omi': ('Convecção', 'MJO (OMI)', 'Madden-Julian Oscillation OMI Amplitude'),
    'mjo_vpm': ('Convecção', 'MJO (VPM)', 'Madden-Julian Oscillation VPM Amplitude'),
    'mjo_romi': ('Convecção', 'MJO (ROMI)', 'Madden-Julian Oscillation ROMI Amplitude'),
    'mjo_20e': ('Convecção', 'MJO 20E', 'MJO Longitude Band 20E (NOAA CPC)'),
    'mjo_70e': ('Convecção', 'MJO 70E', 'MJO Longitude Band 70E (NOAA CPC)'),
    'mjo_80e': ('Convecção', 'MJO 80E', 'MJO Longitude Band 80E (NOAA CPC)'),
    'mjo_100e': ('Convecção', 'MJO 100E', 'MJO Longitude Band 100E (NOAA CPC)'),
    'mjo_120e': ('Convecção', 'MJO 120E', 'MJO Longitude Band 120E (NOAA CPC)'),
    'mjo_140e': ('Convecção', 'MJO 140E', 'MJO Longitude Band 140E (NOAA CPC)'),
    'mjo_160e': ('Convecção', 'MJO 160E', 'MJO Longitude Band 160E (NOAA CPC)'),
    'mjo_120w': ('Convecção', 'MJO 120W', 'MJO Longitude Band 120W (NOAA CPC)'),
    'mjo_40w': ('Convecção', 'MJO 40W', 'MJO Longitude Band 40W (NOAA CPC)'),
    'mjo_10w': ('Convecção', 'MJO 10W', 'MJO Longitude Band 10W (NOAA CPC)'),
    'mjo_pentad': ('Convecção', 'MJO Pentad', 'MJO Pentad Series (NOAA CPC)'),
    'mjo_fase': ('Convecção', 'MJO Fase', 'MJO Phase Index (1-8)'),
    'mjo_modulo': ('Convecção', 'MJO Módulo', 'MJO Amplitude / Modulo Index'),
    'brazilrain': ('Convecção', 'NE Brazil Rain', 'Northeast Brazil Rainfall Anomaly Index'),
    'sahelrain': ('Convecção', 'Sahel Rain', 'Sahel Rainfall Anomaly Index'),
    'indiamon': ('Convecção', 'India Monsoon', 'Central Indian Monsoon Precipitation Index'),
    'swmonsoon': ('Convecção', 'SW Monsoon', 'Southwest Monsoon Region Rainfall Index'),
    'espi': ('Convecção', 'ESPI', 'ENSO Precipitation Index'),
    'qbo': ('Convecção', 'QBO', 'Quasi-Biennial Oscillation Index (NOAA PSL)'),
    'glaam': ('Convecção', 'GLAAM', 'Globally Integrated Angular Momentum Index'),

    # Solar & Clima Global
    'ssn': ('Solar', 'SSN', 'Sunspot Number Monthly Total (SILSO)'),
    'solar': ('Solar', 'Solar Flux 10.7cm', 'Solar Flux 10.7cm (NOAA / DRAO)'),
    'gmsst': ('Solar', 'Global SST Mean', 'Global Mean Land/Ocean Temperature Index'),
    'GLB.Ts+dSST': ('Solar', 'GISTEMP Global', 'NASA GISTEMP Global Land-Ocean Temperature'),
    'trend': ('Solar', 'Global Trend', 'Global Temperature Trend Line'),
    'hurr': ('Solar', 'Hurricane Activity', 'Atlantic Tropical Hurricane Activity Index')
}

def clean_key_name(k):
    # Formats raw key to a nice short display sigla if not in dictionary
    clean = k.replace('_', ' ').replace('.asc', '')
    # Remove duplicate tokens (e.g. PDO PDO -> PDO)
    tokens = clean.split()
    seen = []
    for t in tokens:
        if t.lower() not in [x.lower() for x in seen]:
            seen.append(t)
    return " ".join(seen).upper()

def main():
    df = pd.read_csv("indices_asc/all_climate_indices_monthly.csv")
    unique_indices = sorted(df["index"].unique())

    meta_list = []
    for idx_name in unique_indices:
        group = df[(df["index"] == idx_name) & (df["value"].notna())].sort_values("date")
        if group.empty:
            continue
        start_date = f"{group['year'].min()}-{group['month'].min():02d}-01"
        end_date = f"{group['year'].max()}-{group['month'].max():02d}-01"

        if idx_name in CLEAN_SPECS:
            cat, sigla, desc = CLEAN_SPECS[idx_name]
        else:
            sigla = clean_key_name(idx_name)
            cat = "Outros"
            desc = f"Índice Climático {sigla}"

        meta_list.append({
            "index": idx_name,
            "sigla": sigla,
            "category": cat,
            "description": desc,
            "filename": f"{idx_name}.asc",
            "source": "NOAA PSL / CPC / SILSO / BAS / NCAR",
            "source_url": "https://psl.noaa.gov/data/climateindices/list/",
            "start_date": start_date,
            "end_date": end_date,
            "units": "standardized / absolute",
            "reference": "NOAA PSL Climate Indices Database"
        })

    # Save app/metadata.json
    APP_DIR = Path("app")
    APP_DIR.mkdir(parents=True, exist_ok=True)

    with open(APP_DIR / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta_list, f, indent=2, ensure_ascii=False)
    print(f"Saved app/metadata.json with {len(meta_list)} clean index specifications.")

    # Save climate_indices_metadata.csv
    pd.DataFrame(meta_list).to_csv("climate_indices_metadata.csv", index=False, encoding="utf-8")
    print("Saved climate_indices_metadata.csv.")

if __name__ == '__main__':
    main()
