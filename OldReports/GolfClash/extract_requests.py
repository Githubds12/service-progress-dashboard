import json

har_path = r"c:\Users\Gorri\Documents\Reports\GolfClash\GolfClash.har"
try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    
    with open("relevant_requests.txt", "w", encoding="utf-8") as out:
        for entry in entries:
            req = entry.get("request", {})
            url = req.get("url", "")
            
            # Searching for auth, login, otp, send, verify, or playdemic related URLs
            if any(k in url.lower() for k in ["auth", "otp", "send", "verify", "login", "playdemic", "sms"]):
                res = entry.get("response", {})
                
                out.write(f"URL: {url}\n")
                out.write(f"Method: {req.get('method')}\n")
                out.write("--- Request Headers ---\n")
                for h in req.get("headers", []):
                    out.write(f"{h['name']}: {h['value']}\n")
                
                post_data = req.get("postData", {}).get("text", "")
                if post_data:
                    out.write("--- Request Body ---\n")
                    out.write(post_data + "\n")
                
                out.write(f"--- Response Status: {res.get('status')} ---\n")
                res_content = res.get("content", {}).get("text", "")
                if res_content:
                    out.write("--- Response Body ---\n")
                    out.write(res_content + "\n")
                out.write("="*80 + "\n")

    print("Extraction done.")
except Exception as e:
    print(f"Error: {e}")
