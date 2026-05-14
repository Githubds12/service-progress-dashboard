import json
import base64

har_path = r"c:\Users\Gorri\Documents\Reports\WebMoneyKeeper\WebMoneyKeeper.har"
otp = "0815"

def safe_print(s):
    try:
        print(s)
    except:
        print(s.encode('ascii', 'ignore').decode('ascii'))

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    for i, entry in enumerate(entries):
        url = entry['request']['url']
        req_text = entry['request'].get('postData', {}).get('text', '')
        resp_text = entry['response'].get('content', {}).get('text', '')
        
        if otp in req_text or otp in resp_text:
            safe_print(f"--- Entry {i}: {url} ---")
            safe_print(f"OTP Found in {'Request' if otp in req_text else 'Response'}")
            safe_print(f"Request: {req_text[:500]}")
            safe_print(f"Response: {resp_text[:500]}")
            
except Exception as e:
    print(f"Error: {e}")
