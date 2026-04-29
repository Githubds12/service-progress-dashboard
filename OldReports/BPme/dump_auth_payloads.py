import json
import sys

def dump_auth_payloads(har_file, indices):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    with open('auth_payloads_dump.txt', 'w', encoding='utf-8') as out:
        for i in indices:
            entry = har_data['log']['entries'][i]
            out.write(f"--- ENTRY {i} ---\n")
            out.write(f"Request: {entry['request'].get('postData', {}).get('text', '')}\n")
            out.write(f"Response: {entry['response'].get('content', {}).get('text', '')}\n")
            out.write("-" * 50 + "\n\n")

if __name__ == "__main__":
    dump_auth_payloads('BPme.har', [170, 221, 228, 231, 232])
