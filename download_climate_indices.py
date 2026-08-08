"""
NOAA PSL Climate Indices Downloader & Aggregator
Source: https://psl.noaa.gov/data/climateindices/list/

This script:
1. Scrapes https://psl.noaa.gov/data/climateindices/list/ for all climate index data files.
2. Downloads all time series data files (.data, .ascii, .txt, .scaled).
3. Saves each climate index in `.asc` format inside the output directory (`indices_asc/`).
4. Creates a detailed catalog (`index_catalog.json` and `index_catalog.csv`) with metadata.
"""

import os
import re
import json
import ssl
import urllib.request
from urllib.parse import urljoin
from pathlib import Path
from bs4 import BeautifulSoup

BASE_URL = "https://psl.noaa.gov/data/climateindices/list/"
DOMAIN = "https://psl.noaa.gov"
OUTPUT_DIR = Path("indices_asc")
DEFAULT_TIMEOUT = 15  # seconds timeout to prevent hanging

def create_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def fetch_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = urllib.request.Request(url, headers=headers)
    ctx = create_ssl_context()
    with urllib.request.urlopen(req, context=ctx, timeout=DEFAULT_TIMEOUT) as resp:
        return resp.read().decode('utf-8', errors='replace')

def sanitize_filename(name):
    clean = re.sub(r'[^\w\-\.\(\)]', '_', name)
    clean = re.sub(r'_+', '_', clean).strip('_')
    return clean

def parse_indices_from_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    
    indices_list = []
    
    if not table:
        print("Warning: Table not found in HTML.")
        return indices_list

    rows = table.find_all('tr')
    for row in rows[1:]:  # skip header
        cols = row.find_all(['td', 'th'])
        if len(cols) >= 2:
            name_text = cols[0].get_text(strip=True)
            desc_text = cols[1].get_text(' ', strip=True)
            
            for a in row.find_all('a', href=True):
                href = a['href']
                # Skip FTP or invalid schemes that hang
                if href.startswith('ftp://'):
                    continue
                full_url = urljoin(DOMAIN, href)
                link_text = a.get_text(strip=True)
                
                if any(full_url.endswith(ext) for ext in ['.data', '.ascii', '.txt', '.scaled']) or '/data/correlation/' in full_url or '/data/timeseries/' in full_url:
                    if not full_url.endswith('/') and not full_url.endswith('.html') and not full_url.endswith('.shtml') and not full_url.endswith('.gif'):
                        indices_list.append({
                            'name': name_text,
                            'label': link_text,
                            'description': desc_text,
                            'url': full_url
                        })

    seen_urls = set()
    unique_indices = []
    for item in indices_list:
        if item['url'] not in seen_urls:
            seen_urls.add(item['url'])
            unique_indices.append(item)

    return unique_indices

def parse_asc_metadata(content):
    lines = content.strip().splitlines()
    if not lines:
        return {}

    first_line = lines[0].strip().split()
    start_year, end_year = None, None
    if len(first_line) == 2 and first_line[0].isdigit() and first_line[1].isdigit():
        start_year = int(first_line[0])
        end_year = int(first_line[1])
    
    missing_value = None
    for line in reversed(lines):
        line_s = line.strip()
        if line_s.startswith("-99") or line_s.startswith("-999"):
            missing_value = line_s
            break

    return {
        'start_year': start_year,
        'end_year': end_year,
        'line_count': len(lines),
        'missing_value_code': missing_value
    }

def main():
    print(f"Fetching index list from {BASE_URL}...")
    try:
        html = fetch_html(BASE_URL)
    except Exception as e:
        print(f"Error fetching page: {e}")
        return

    indices = parse_indices_from_page(html)
    print(f"Found {len(indices)} downloadable climate index datasets.\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    catalog = []
    ctx = create_ssl_context()

    for idx in indices:
        url = idx['url']
        url_filename = url.split('/')[-1]
        
        base_name = Path(url_filename).stem
        if base_name.endswith('.anom'):
            asc_filename = f"{base_name.replace('.anom', '_anom')}.asc"
        elif base_name.endswith('.data'):
            asc_filename = f"{base_name[:-5]}.asc"
        else:
            asc_filename = f"{base_name}.asc"

        out_path = OUTPUT_DIR / asc_filename
        if out_path.exists():
            prefix = sanitize_filename(idx['name'])
            asc_filename = f"{prefix}_{asc_filename}"
            out_path = OUTPUT_DIR / asc_filename

        print(f"Downloading [{idx['name']} - {idx['label']}] -> {out_path.name}...")
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx, timeout=DEFAULT_TIMEOUT) as resp:
                raw_bytes = resp.read()
                content = raw_bytes.decode('utf-8', errors='replace')
            
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(content)

            meta = parse_asc_metadata(content)
            
            catalog.append({
                'index_name': idx['name'],
                'label': idx['label'],
                'asc_filename': asc_filename,
                'file_path': str(out_path),
                'file_size_bytes': len(raw_bytes),
                'url': url,
                'start_year': meta.get('start_year'),
                'end_year': meta.get('end_year'),
                'line_count': meta.get('line_count'),
                'description': idx['description']
            })
            
        except Exception as e:
            print(f"  [TIMEOUT/FAILED] {url}: {e}")

    catalog_json_path = OUTPUT_DIR / "catalog.json"
    with open(catalog_json_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    catalog_csv_path = OUTPUT_DIR / "catalog.csv"
    with open(catalog_csv_path, 'w', encoding='utf-8') as f:
        f.write("index_name,label,asc_filename,url,start_year,end_year,file_size_bytes,description\n")
        for c in catalog:
            desc_clean = c['description'].replace('"', '""')
            f.write(f'"{c["index_name"]}","{c["label"]}","{c["asc_filename"]}","{c["url"]}",{c["start_year"]},{c["end_year"]},{c["file_size_bytes"]},"{desc_clean}"\n')

    print(f"\nCompleted! Downloaded {len(catalog)} climate index ASC files to '{OUTPUT_DIR.resolve()}'.")

if __name__ == '__main__':
    main()
