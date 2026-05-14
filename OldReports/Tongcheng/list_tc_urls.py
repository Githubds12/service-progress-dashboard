import json
import sys

# Set output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

har_path = r'c:\Users\Gorri\Documents\Reports\Tongcheng\Tongcheng.har'

with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

entries = har_data['log']['entries']
urls = set()

for entry in entries:
    url = entry['request']['url']
    if 'tc.com' in url:
        urls.add(url)

for url in sorted(urls):
    print(url)
