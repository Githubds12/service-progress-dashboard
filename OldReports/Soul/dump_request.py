import json

with open("Soul.har", "r", encoding="utf-8") as f:
    data = json.load(f)

for entry in data['log']['entries']:
    if 'account/validate/register' in entry['request']['url']:
        resp_text = entry['response']['content'].get('text', '')
        if '"code":10001' in resp_text:
            print(json.dumps(entry['request'], indent=2))
