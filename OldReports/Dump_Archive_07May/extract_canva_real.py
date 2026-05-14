import json
import os

har_path = 'OldReports/Canva/Canva.har'
target_phone = '+918791267460'

with open(har_path, 'r', encoding='utf-8') as f:
    har = json.load(f)

print("--- Searching for exact Canva OTP Traces ---")
for entry in har['log']['entries']:
    req_text = ""
    if 'postData' in entry['request']:
        req_text = entry['request']['postData'].get('text', '')
    
    if target_phone in req_text:
        print(f"MATCH FOUND: {entry['request']['url']}")
        print(f"METHOD: {entry['request']['method']}")
        print(f"REQUEST BODY:\n{req_text}")
        
        res_text = ""
        if 'content' in entry['response']:
            res_text = entry['response']['content'].get('text', '')
        print(f"RESPONSE BODY:\n{res_text}")
        print("-" * 50)

# Also search for the verification code from inf.txt (531839) to see the verify request
verify_code = '531839'
for entry in har['log']['entries']:
    req_text = ""
    if 'postData' in entry['request']:
        req_text = entry['request']['postData'].get('text', '')
    
    if verify_code in req_text:
        print(f"VERIFY MATCH FOUND: {entry['request']['url']}")
        print(f"METHOD: {entry['request']['method']}")
        print(f"REQUEST BODY:\n{req_text}")
        
        res_text = ""
        if 'content' in entry['response']:
            res_text = entry['response']['content'].get('text', '')
        print(f"RESPONSE BODY:\n{res_text}")
        print("-" * 50)
