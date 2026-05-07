import json

har_path = r'c:\Users\Gorri\Documents\Reports\ViyaLite\ViyaLite.har'
with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

targets = [
    "https://api.salamyo.com/auth/account/checkAccount",
    "https://api.salamyo.com/auth/security/getWebToken",
    "https://web.kinkey.tech/h5-api/auth/account/getCaptchaSetting",
    "https://api.salamyo.com/auth/account/getAuthSms",
    "https://api.salamyo.com/auth/account/login"
]

results = []

for entry in data['log']['entries']:
    url = entry['request']['url']
    if any(t in url for t in targets):
        req = entry['request']
        res = entry['response']
        
        req_body = req.get('postData', {}).get('text', '')
        res_body = res.get('content', {}).get('text', '')
        
        # Try to decode if base64 (though likely JSON)
        # But HAR usually has text directly if it's JSON
        
        results.append({
            "url": url,
            "method": req['method'],
            "request_headers": req['headers'],
            "request_body": req_body,
            "response_headers": res['headers'],
            "response_body": res_body,
            "status": res['status']
        })

print(json.dumps(results, indent=2))
