import json

har_path = r"c:\Users\Gorri\Documents\Reports\chagee\chagee.har"
try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    
    with open("full_login_request.txt", "w", encoding="utf-8") as out:
        for entry in entries:
            req = entry.get("request", {})
            url = req.get("url", "")
            
            if "/api/user-client/customer/loginOrRegister" in url:
                res = entry.get("response", {})
                
                out.write("### FULL REQUEST ###\n")
                out.write(f"URL: {url}\n")
                out.write(f"Method: {req.get('method')}\n")
                out.write("Headers:\n")
                out.write(json.dumps({h['name']: h['value'] for h in req.get('headers', [])}, indent=2) + "\n")
                out.write("Body:\n")
                out.write(req.get('postData', {}).get('text', '') + "\n\n")
                
                out.write("### FULL RESPONSE ###\n")
                out.write(f"Status: {res.get('status')}\n")
                out.write("Headers:\n")
                out.write(json.dumps({h['name']: h['value'] for h in res.get('headers', [])}, indent=2) + "\n")
                out.write("Body:\n")
                out.write(res.get('content', {}).get('text', '') + "\n")
                out.write("="*80 + "\n")

    print("Extraction done.")
except Exception as e:
    print(f"Error: {e}")
