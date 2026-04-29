import requests
import json
import os
import glob
import re

API_BASE = "http://51.195.24.179:8092/api"
EMAIL = "deepanshu@test.com"
PASS = "deep@nshu"
PROJECT_ID = "dfbdd43f-5e35-495d-8394-b1f9138bac7f"
FOLDER = "iHerb"

def login():
    res = requests.post(f"{API_BASE}/auth/login", json={"email": EMAIL, "password": PASS})
    return res.json().get("access_token")

def update():
    token = login()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    report_file = os.path.join(FOLDER, "iHerb-report.md")
    with open(report_file, "r", encoding="utf-8") as f:
        raw_text = f.read()

    def extract_section(regex, text):
        match = re.search(regex, text, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    exec_summary = extract_section(r'## 1\. Executive Summary\n+(.*?)\n+## 2\.', raw_text)
    target_app = extract_section(r'-\s*\*\*Target URL/App\*\*:\s*`(.*?)`', raw_text)
    researcher = extract_section(r'-\s*\*\*Researcher\*\*:\s*`(.*?)`', raw_text)
    date_val = extract_section(r'-\s*\*\*Date\*\*:\s*`(.*?)`', raw_text)
    conc_text = extract_section(r'## 5\. Conclusion\n+(.*)', raw_text)
    
    feasibility_match = re.search(r'Automation Feasibility:\s*(\d+)%', raw_text, re.IGNORECASE)
    feasibility = "Low"
    if feasibility_match:
        val = int(feasibility_match.group(1))
        if val < 30: feasibility = "Low"
        elif val < 70: feasibility = "Medium"
        else: feasibility = "High"

    qa = {
        "captcha": {"status": "Unknown"},
        "encryption": {"status": "Unknown"},
        "verification_type": {"status": "Unknown"},
        "bot_protection": {"status": "Unknown"},
        "endpoints_involved": {"status": "Unknown", "details": ""},
        "rate_limits": {"status": "Unknown"}
    }
    for line in raw_text.split('\n'):
        if '|' in line and "---" not in line and "Feature" not in line:
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 2:
                feature = parts[0].replace('*', '').lower()
                status = parts[1]
                details = parts[2] if len(parts) > 2 else ""
                if 'verification' in feature: qa["verification_type"]["status"] = status
                elif 'captcha' in feature: qa["captcha"]["status"] = status
                elif 'encryption' in feature: qa["encryption"]["status"] = status
                elif 'limit' in feature: qa["rate_limits"]["status"] = status
                elif 'bot' in feature: qa["bot_protection"]["status"] = status
                elif 'endpoint' in feature:
                     qa["endpoints_involved"]["status"] = status
                     qa["endpoints_involved"]["details"] = details

    payload = {
        "engineering_details": {
            "executive_summary": exec_summary,
            "metadata": {
                "target_url_app": target_app,
                "researcher": researcher or "Deepanshu Singh",
                "date": date_val or "2026-04-27"
            },
            "quick_analysis": qa,
            "conclusion": {"feasibility": feasibility, "text": conc_text},
            "flow_details_raw": raw_text,
            "identified_steps": ["Check Account", "OTP Send", "OTP Validate", "Register"]
        }
    }
    
    res = requests.put(f"{API_BASE}/projects/{PROJECT_ID}", headers=headers, json=payload)
    print(f"Update Status: {res.status_code}")
    
    # Upload files
    har_file = os.path.join(FOLDER, "iHerb.har")
    files = []
    f1 = open(report_file, "rb")
    files.append(('report_file', (os.path.basename(report_file), f1, 'application/octet-stream')))
    if os.path.exists(har_file):
        f2 = open(har_file, "rb")
        files.append(('data_file', (os.path.basename(har_file), f2, 'application/octet-stream')))
    
    res_file = requests.post(f"{API_BASE}/projects/{PROJECT_ID}/research", headers={"Authorization": f"Bearer {token}"}, files=files)
    print(f"File Upload Status: {res_file.status_code}")

if __name__ == "__main__":
    update()
