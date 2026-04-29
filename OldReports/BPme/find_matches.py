import json
import re

def find_matches(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    content = str(har_data)
    matches = re.findall(r'authIndexValue=(\w+)', content)
    print("Matches:", set(matches))

if __name__ == "__main__":
    find_matches('BPme.har')
