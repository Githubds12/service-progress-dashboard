import json

har_path = r"c:\Users\Gorri\Documents\Reports\WebMoneyKeeper\WebMoneyKeeper.har"

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    for entry in entries:
        url = entry['request']['url']
        if 'web.money' in url:
            print(f"URL: {url}")
            for header in entry['request']['headers']:
                if header['name'].lower() in ['user-agent', 'x-requested-with', 'x-app-id']:
                    print(f"  {header['name']}: {header['value']}")
            break
except Exception as e:
    print(f"Error: {e}")
