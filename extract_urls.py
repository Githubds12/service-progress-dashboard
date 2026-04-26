import json
import sys
import os

def extract_urls(har_path):
    with open(har_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Derive output filename from HAR name
    base_name = os.path.basename(har_path).replace('.har', '')
    output_file = f"{base_name}_targets.txt"
    
    with open(output_file, 'w', encoding='utf-8') as out:
        for entry in data['log']['entries']:
            url = entry['request']['url']
            method = entry['request']['method']
            # Broaden filter to catch more auth-related traffic
            keywords = ['weltrade', 'cubamessenger', 'register', 'phone', 'verify', 'otp', 'sms', 'auth', 'login', 'token', 'confirm']
            if any(k in url.lower() for k in keywords):
                out.write(f"--- {method} {url} ---\n")
                for h in entry['request']['headers']:
                    out.write(f"{h['name']}: {h['value']}\n")
                if 'postData' in entry['request']:
                    out.write(f"Body: {entry['request']['postData'].get('text', '')}\n")
                
                # Also include response body if it's JSON or short text
                if 'response' in entry and 'content' in entry['response']:
                    content = entry['response']['content']
                    if 'text' in content:
                        out.write(f"Response: {content['text'][:2000]}\n")
                
                out.write("\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        extract_urls(sys.argv[1])
