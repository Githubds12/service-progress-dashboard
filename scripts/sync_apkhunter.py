import os
import json
import csv
import urllib.parse
from datetime import datetime

# --- CONFIGURATION ---
PORTAL_DIR = r"C:\HTB-Notes-Portal"
CSV_FILE = os.path.join(PORTAL_DIR, "fresh_detailed.csv")
DB_FILE = os.path.join(PORTAL_DIR, "apk_local_database.json")
OUTPUT_FILE = os.path.join(os.getcwd(), "dashboard", "apkhunter_data.js")

# --- SECURITY INTELLIGENCE (Mirrored from ApkHunter.py) ---
SECURITY_INTEL = {
    "signal": 98, "whatsapp": 95, "yoomoney": 95, "ing": 95, "payoneer": 95, 
    "openbank": 95, "wise": 95, "revolut": 95, "boursorama": 95, "plus500": 95,
    "binance": 95, "okx": 95, "ziraatbank": 95, "citibank": 95, "pnc": 95,
    "bolt": 90, "uber": 90, "dhl": 90, "fedex": 85, "airasia": 88, "yandex": 90, 
    "tsb": 95, "gaijin": 90, "steam": 85, "tfl": 85, "grab": 90, "lalamove": 85,
    "fpmarkets": 85, "doctolib": 85, "lidl": 85, "etoro": 88,
    "aliexpress": 85, "shopee": 80, "adidas": 75, "nike": 75, "temu": 75, "shein": 75,
    "airbnb": 75, "leboncoin": 75, "marktplaats": 75, "wallapop": 75,
    "fiverr": 75, "up": 75, "vinted": 75, "shopeepay": 80,
    "tinder": 65, "bumble": 65, "okcupid": 65, "bigo": 70, "garmin": 65, "fiverr": 45, 
    "vonage": 45, "quora": 40, "tunecore": 30, "indeed": 35, "mixpanel": 25,
    "gofundme": 50, "cigna": 60, "prudential": 60, "cgd": 60, "bankera": 60, "lego": 50
}

def load_db():
    if not os.path.exists(DB_FILE): 
        return {"claimed":{},"notes":{},"issues":{},"root_detected":{},"not_found":{},"last_updated":{}}
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except: 
            return {"claimed":{},"notes":{},"issues":{},"root_detected":{},"not_found":{},"last_updated":{}}

def sync():
    print(f"[*] Starting APKHunter Sync...")
    db = load_db()
    c_d = db.get("claimed", {})
    n_d = db.get("notes", {})
    i_d = db.get("issues", {})
    r_d = db.get("root_detected", {})
    nf_d = db.get("not_found", {})
    u_d = db.get("last_updated", {})
    
    targets = []
    
    if not os.path.exists(CSV_FILE):
        print(f"[!] Error: {CSV_FILE} not found.")
        return

    TIER_MAP = {
        "Tier 2: SMS OTP Only": "Standard Tier 2 service (SMS-only flow).",
        "Tier 1: No 2FA / Unknown": "Legacy Tier 1 service. Minimal security.",
        "Tier 2: OTP Only": "Standard Tier 2 service (OTP-only flow).",
        "Tier 1: High Security": "Tier 1 High-Security service."
    }

    with open(CSV_FILE, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("Name") or "Unknown").strip()
            tid = (row.get("API_ID") or row.get("Slug") or "").strip().lower()
            tier = (row.get("Category") or "Unknown").strip()
            
            if not tid: tid = "missing_id_" + str(hash(name))
            
            is_c = c_d.get(tid, False)
            is_r = r_d.get(tid, False)
            is_nf = nf_d.get(tid, False)
            note = n_d.get(tid, "").strip()
            
            base_score = SECURITY_INTEL.get(tid, 50)
            diff = base_score
            
            p_issues = i_d.get(tid, [])
            intel_pool = (" ".join([str(x.get('text','')).lower() for x in p_issues]) + " " + note.lower()).strip()

            if tid in SECURITY_INTEL:
                diff = SECURITY_INTEL[tid]
                cat = "Banking/Fintech" if diff >= 95 else "Logistics" if diff >= 85 else "E-Commerce" if diff >= 70 else "Social/Utility"
                reason = f"Score {diff}: {cat} (Researched security posture)."
            else:
                reason = TIER_MAP.get(tier, f"Base score {base_score}: Standard service.")
            
            triggers = []
            if is_nf: 
                diff, triggers = 100, ["Binary Not Found"]
            
            flow_keywords = ["no web flow", "no phone", "no endpoint", "only available on mobile"]
            found_flow = [k for k in flow_keywords if k in intel_pool]
            if found_flow:
                diff = max(diff, 95)
                triggers.append(f"No Endpoint ({found_flow[0]})")

            ssl_keywords = ["pinning", "ssl", "flutter"]
            found_ssl = [k for k in ssl_keywords if k in intel_pool]
            if found_ssl:
                diff = max(diff, 90)
                triggers.append(f"Hard Security ({found_ssl[0]})")

            if triggers:
                reason = f"Score {diff}: Triggers: {', '.join(triggers)}."
            
            final_diff = int(max(0, min(100, diff)))
            
            q = urllib.parse.quote_plus(name)
            targets.append({
                "id": tid, "name": name, "sms": row.get("Sample_Message", ""), 
                "claimed": is_c, "note": note, "root_detected": is_r, "not_found": is_nf,
                "difficulty": final_diff, "reason": reason,
                "last_updated": u_d.get(tid, "NEVER"),
                "urls": {
                    "play": f"https://play.google.com/store/search?q={q}&c=apps",
                    "pure": f"https://apkpure.net/search?q={q}",
                    "aptoide": f"https://en.aptoide.com/search?query={q}",
                    "mirror": f"https://www.apkmirror.com/?searchtype=apk&s={q}",
                    "uptodown": f"https://en.uptodown.com/android/search?q={q}"
                }
            })

    print(f"[*] Processed {len(targets)} targets.")
    
    # Sort by difficulty descending for high-value targets first
    targets.sort(key=lambda x: x['difficulty'], reverse=True)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"window.apkhunterData = {json.dumps(targets, indent=2)};\n")
        f.write(f"window.apkhunterLastSync = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}';\n")
    
    print(f"[+] Sync Complete: {OUTPUT_FILE}")

if __name__ == "__main__":
    sync()
