import json

with open(r'c:\Users\Gorri\Documents\Reports\Aegan\Aegan.har', 'r', encoding='utf-8') as f:
    data = json.load(f)

target_urls = [
    'connect/auth/password',
    'connect/send-otp',
    'connect/v2/validate-otp'
]

results = []
for entry in data['log']['entries']:
    url = entry['request']['url']
    if any(target in url for target in target_urls):
        results.append(entry)

print(json.dumps(results, indent=2))
