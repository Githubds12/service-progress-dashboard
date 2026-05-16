import urllib.request
import json
import os

URL = "https://otx.alienvault.com/api/v1/indicators/domain/replit.com/url_list?limit=50"
OUT_PATH = r"c:\Users\Gorri\Documents\Reports\recon_storage\katana_real_data_v2.json"

try:
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = response.read().decode()
        with open(OUT_PATH, "w") as f:
            f.write(data)
    print(f"Successfully saved {len(data)} bytes to {OUT_PATH}")
except Exception as e:
    print(f"Error: {e}")
