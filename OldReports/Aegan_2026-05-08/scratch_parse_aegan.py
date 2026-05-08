import json

with open(r'c:\Users\Gorri\Documents\Reports\Aegan\Aegan.har', 'r', encoding='utf-8') as f:
    data = json.load(f)

keywords = ['enroll', 'login', 'auth', 'otp', 'sms', 'verify', 'member', 'milesandbonus']

interesting_entries = []
for entry in data['log']['entries']:
    url = entry['request']['url']
    method = entry['request']['method']
    
    # Exclude static assets
    if any(ext in url.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.js', '.css', '.woff']):
        continue

    # Check URL or Body
    post_data = entry['request'].get('postData', {})
    text = post_data.get('text', '')
    
    if any(k in url.lower() for k in keywords) or any(k in text.lower() for k in keywords):
        interesting_entries.append(entry)

# Print summary
for i, entry in enumerate(interesting_entries):
    print(f"{i}: {entry['request']['method']} {entry['request']['url']}")
    if 'postData' in entry['request']:
        print(f"   Body: {entry['request']['postData'].get('text', '')[:200]}")
    print("-" * 50)
