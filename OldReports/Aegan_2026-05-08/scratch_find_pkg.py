import json

with open(r'c:\Users\Gorri\Documents\Reports\Aegan\Aegan.har', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Search for package names or app versions in headers
keywords = ['X-Android-Package', 'X-App-Version', 'gr.aegean', 'aegean', 'version']

results = []
for entry in data['log']['entries']:
    url = entry['request']['url']
    headers = entry['request']['headers']
    
    for h in headers:
        if any(k.lower() in h['name'].lower() or k.lower() in h['value'].lower() for k in keywords):
            results.append((url, h['name'], h['value']))

# Print unique findings
unique_results = set(results)
for r in list(unique_results)[:20]:
    print(r)
