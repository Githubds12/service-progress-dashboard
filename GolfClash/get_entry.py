import json

har_path = r"c:\Users\Gorri\Documents\Reports\GolfClash\GolfClash.har"
entry_indices = [387, 287]

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    for idx in entry_indices:
        if idx < len(entries):
            entry = entries[idx]
            print(f"=== Entry {idx} ===")
            print(f"URL: {entry['request']['url']}")
            print(f"Request Body: {entry['request'].get('postData', {}).get('text', 'N/A')}")
            print(f"Response Body: {entry['response'].get('content', {}).get('text', 'N/A')[:500]}...")
            print("\n")
except Exception as e:
    print(f"Error: {e}")
