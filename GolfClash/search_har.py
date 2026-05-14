import json

har_path = r"c:\Users\Gorri\Documents\Reports\GolfClash\GolfClash.har"
keywords = ["phone", "mobile", "sms", "verify", "code", "login", "auth"]

def search_json(data, path=""):
    results = []
    if isinstance(data, dict):
        for k, v in data.items():
            current_path = f"{path}.{k}" if path else k
            if any(kw in k.lower() for kw in keywords):
                results.append((current_path, k))
            if isinstance(v, (dict, list)):
                results.extend(search_json(v, current_path))
            elif isinstance(v, str):
                if any(kw in v.lower() for kw in keywords):
                    results.append((current_path, v[:100]))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            current_path = f"{path}[{i}]"
            results.extend(search_json(item, current_path))
    return results

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    found = search_json(har_data)
    for p, v in found:
        # Filter out some noise
        if "google" in p or "facebook" in p or "singular" in p or "firebase" in p:
            continue
        print(f"{p}: {v}")
except Exception as e:
    print(f"Error: {e}")
