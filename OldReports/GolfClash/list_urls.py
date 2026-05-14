import json
from urllib.parse import urlparse

har_path = r"c:\Users\Gorri\Documents\Reports\GolfClash\GolfClash.har"
try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    urls = set()
    for entry in har_data.get("log", {}).get("entries", []):
        urls.add(entry.get("request", {}).get("url", ""))
    
    for url in sorted(urls):
        print(url)
except Exception as e:
    print(f"Error: {e}")
