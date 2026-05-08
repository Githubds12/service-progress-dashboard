import json
import sys

def parse_har(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    entries = data['log']['entries']
    interesting_endpoints = [
        'account/validate/register',
        'account/smsCode/deliver',
        'account/smsCode/validate'
    ]
    
    for entry in entries:
        url = entry['request']['url']
        method = entry['request']['method']
        
        # Check if it's the deliver endpoint AND successful
        if 'account/smsCode/deliver' in url:
            resp_text = entry['response']['content'].get('text', '')
            if '"code":10001' in resp_text:
                print("--- SUCCESSFUL OTP REQUEST ---")
                print(f"URL: {url}")
                print(f"Method: {method}")
                print("Request Headers:")
                print(json.dumps(entry['request']['headers'], indent=2))
                
                if 'postData' in entry['request']:
                    print("Request Body:")
                    print(entry['request']['postData'].get('text', 'No body text'))
                
                print("Response Status:", entry['response']['status'])
                print("Response Body:")
                print(resp_text)
                print("-" * 50)

if __name__ == "__main__":
    parse_har("Soul.har")
