import json

def extract_bp_details(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data['log']['entries']
    
    with open('bp_details.txt', 'w', encoding='utf-8') as out:
        for entry in entries:
            url = entry['request']['url']
            if 'bp.com' in url or 'bpglobal.com' in url:
                out.write(f"--- {entry['request']['method']} {url} ---\n")
                
                # Headers
                out.write("Headers:\n")
                for h in entry['request']['headers']:
                    out.write(f"{h['name']}: {h['value']}\n")
                
                # Request Body
                post_data = entry['request'].get('postData', {}).get('text', '')
                out.write(f"\nRequest Body:\n{post_data}\n")
                
                # Response
                out.write(f"\nResponse Code: {entry['response']['status']}\n")
                res_content = entry['response'].get('content', {}).get('text', '')
                out.write(f"Response Body:\n{res_content}\n")
                out.write("="*50 + "\n\n")

if __name__ == "__main__":
    extract_bp_details('BPme.har')
