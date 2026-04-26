import json
with open('WellTrade/WellTrade.har', 'r', encoding='utf-8') as f:
    data = json.load(f)
for entry in data['log']['entries']:
    for h in entry['request']['headers']:
        if h['name'].lower() == 'x-requested-with':
            print(h['value'])
            exit()
