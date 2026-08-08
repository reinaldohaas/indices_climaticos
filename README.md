# 🌍 Índices Climáticos (NOAA PSL, NCEI ERSST v5 & CPC)

Repositório automatizado para raspagem, atualização e padronização de **índices climáticos globais** em formato ASCII (`.asc`) e dataset consolidado CSV.

---

## 📌 Fontes de Dados
Os dados são coletados e continuamente atualizados a partir das seguintes fontes oficiais da NOAA:
1. **NOAA Physical Sciences Laboratory (PSL):** [https://psl.noaa.gov/data/climateindices/list/](https://psl.noaa.gov/data/climateindices/list/)
2. **NOAA NCEI ERSST v5 Index:** [https://www.ncei.noaa.gov/pub/data/cmb/ersst/v5/index/](https://www.ncei.noaa.gov/pub/data/cmb/ersst/v5/index/)
3. **NOAA Climate Prediction Center (CPC):** [https://www.cpc.ncep.noaa.gov/data/indices/](https://www.cpc.ncep.noaa.gov/data/indices/)

---

## 📊 Principais Índices Climáticos Incluídos

| Categoria | Índices (`.asc`) | Período de Dados |
| :--- | :--- | :--- |
| **ENSO (El Niño / La Niña)** | `nina1_anom.asc`, `nina3_anom.asc`, `nina34_anom.asc`, `nina4_anom.asc`, `nina1.asc`, `nina3.asc`, `nina34.asc`, `nina4.asc`, `oni.asc`, `soi.asc`, `tni.asc`, `censo.asc` | **1854 – 2026+** |
| **Bacia do Pacífico** | `pdo.asc` (Pacific Decadal Oscillation), `ipotpi.hadisst2.asc` (TPI/IPO), `pna.asc` (Pacific North American), `epo.asc` (EP/NP), `wp.asc` (Western Pacific), `pacwarm.asc` | **1854 – 2026+** |
| **Bacia do Atlântico** | `amon.us.asc` (AMO Unsmoothed), `amon.sm.asc` (AMO Smoothed), `ammsst.asc` (Atlantic Meridional Mode), `tna.asc`, `tsa.asc`, `whwp.asc`, `NTA_ersst.asc`, `CAR_ersst.asc` | **1854 – 2026+** |
| **Oscilações Polares & Globais** | `nao.asc` (North Atlantic Oscillation), `ao.asc` (Arctic Oscillation), `aao.asc` (Antarctic Oscillation), `qbo.asc` (Quasi-Biennial Oscillation), `glaam.asc` | **1950/1979 – 2026+** |
| **Precipitação & Monções** | `iod.asc` (Indian Ocean Dipole / DMI), `brazilrain.asc` (Nordeste do Brasil), `sahelrain.asc`, `indiamon.asc`, `swmonsoon.asc`, `espi.asc` | **1854 – 2026+** |

---

## 📁 Estrutura do Repositório

```
indices_climaticos/
├── download_climate_indices.py        # Script para baixar todos os índices da NOAA PSL
├── update_climate_indices_ersst_v5.py # Script para atualizar os índices com NCEI ERSST v5 e CPC
├── parse_asc_to_df.py                 # Consolida todos os .asc em um único CSV
├── update_catalog.py                  # Gera metadados dos índices em catalog.csv e catalog.json
└── indices_asc/                        # Pasta contendo os arquivos .asc e o dataset unificado
    ├── catalog.csv                     # Tabela de inventário de todos os arquivos .asc
    ├── catalog.json                    # Inventário em formato JSON
    ├── all_climate_indices_monthly.csv # Dataset unificado em CSV (108.000+ observações)
    ├── pna.asc                         # Arquivos individuais de índices no formato matriz ASCII
    ├── nao.asc
    ├── nina34_anom.asc
    └── ...
```

---

## ⚙️ Como Atualizar os Dados

Para atualizar os arquivos `.asc` e o dataset CSV com as informações mais recentes publicadas pela NOAA, basta executar os scripts Python na ordem abaixo:

```bash
# 1. Baixar lista completa da NOAA PSL
python download_climate_indices.py

# 2. Atualizar índices com NOAA NCEI ERSST v5 & NOAA CPC (2026+)
python update_climate_indices_ersst_v5.py

# 3. Atualizar inventário e compilar dataset CSV unificado
python update_catalog.py
python parse_asc_to_df.py
```

---

## 📄 Formato dos Arquivos `.asc`

Os arquivos seguem a convenção matricial padrão da NOAA:
- **Linha 1:** `Ano_Inicial  Ano_Final`
- **Linhas 2 em diante:** `Ano  Jan  Fev  Mar  Abr  Mai  Jun  Jul  Ago  Set  Out  Nov  Dez`
- **Valor ausente:** `-99.90` ou `-999.0`

---

## 📜 Licença e Fonte

Dados de domínio público disponibilizados pela **NOAA (National Oceanic and Atmospheric Administration)**.
