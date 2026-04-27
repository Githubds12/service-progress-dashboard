import json
import re

def find_journeys(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    journeys = set()
    for entry in har_data['log']['entries']:
        url = entry['request']['url']
        match = re.search(r'startJourney=([^&\"\' ]+)', url)
        if match:
            journeys.add(match.group(1))
    
    print("Found Journeys:", journeys)

if __name__ == "__main__":
    find_journeys('BPme.har')
