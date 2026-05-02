import json
har_path = r'c:\Users\Gorri\Documents\Reports\Deriv\Deriv.har'
with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

results = []
keywords = ['registration', 'login', 'settings', 'phone', 'verify', 'otp', 'verification', 'sms', 'code']

for entry in data['log']['entries']:
    url = entry['request']['url']
    method = entry['request']['method']
    body = entry['request'].get('postData', {}).get('text', '')
    
    if any(k in url.lower() for k in keywords) or any(k in body.lower() for k in keywords):
        if 'google' in url or 'firebase' in url: continue
        results.append({
            'method': method,
            'url': url,
            'req_body': body[:500],
            'status': entry['response']['status'],
            'res_body': entry['response'].get('content', {}).get('text', '')[:500]
        })

with open(r'c:\Users\Gorri\Documents\Reports\Deriv\flow_debug.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
