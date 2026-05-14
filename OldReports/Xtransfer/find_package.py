import json
import sys
import re

def find_package_name(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Common patterns for package names in HAR
    # 1. User-Agent
    # 2. Query parameters (e.g. bundleId, appId, package)
    # 3. Request/Response body
    
    potential_packages = set()
    
    for entry in data['log']['entries']:
        # Check User-Agent
        for header in entry['request']['headers']:
            if header['name'].lower() == 'user-agent':
                val = header['value']
                # Look for strings like com.xxx.yyy
                matches = re.findall(r'[a-zA-Z][a-zA-Z0-9_]*\.[a-zA-Z][a-zA-Z0-9_]*\.[a-zA-Z][a-zA-Z0-9_.]*', val)
                potential_packages.update(matches)
        
        # Check URL
        url = entry['request']['url']
        matches = re.findall(r'com\.[a-zA-Z0-9_.]+', url)
        potential_packages.update(matches)
        
        # Check Post Data
        post_data = entry['request'].get('postData', {})
        text = post_data.get('text', '')
        if text:
            matches = re.findall(r'com\.[a-zA-Z0-9_.]+', text)
            potential_packages.update(matches)

    for pkg in sorted(potential_packages):
        if 'xtransfer' in pkg.lower():
            print(pkg)

if __name__ == "__main__":
    find_package_name(sys.argv[1])
