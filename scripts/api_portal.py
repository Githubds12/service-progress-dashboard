import os
import sys
import json
import requests
import re
import argparse
import glob

API_BASE = "http://51.195.24.179:3000/api"
EMAIL = "deepanshu@test.com"
PASS = "deep@nshu"

def login():
    res = requests.post(f"{API_BASE}/auth/login", json={"email": EMAIL, "password": PASS})
    if res.status_code == 200:
        return res.json().get("access_token")
    else:
        raise Exception("Login failed: " + res.text)

def get_service_uuid(folder_path):
    inf_file = os.path.join(folder_path, "inf.txt")
    if os.path.exists(inf_file):
        with open(inf_file, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'\[([a-f0-9\-]{36})\]', content)
            if match:
                return match.group(1)
    return None

def get_app_details(folder_path):
    sheet_file = os.path.join(folder_path, "googlesheet.txt")
    source_val = ""
    if os.path.exists(sheet_file):
        with open(sheet_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith(("Date:", "Service", "Host", "Verification", "Captcha", "Encryption", "Rate", "Endpoint", "Bot", "Flow", "Proof", "Researcher", "com.google")):
                    parts = line.split()
                    if len(parts) >= 2:
                        source_val = f"{parts[0]} {parts[1]}"
                        break
    return source_val

def parse_report(folder_path, source_val):
    report_file = os.path.join(folder_path, "report.md")
    if not os.path.exists(report_file):
        report_files = glob.glob(os.path.join(folder_path, "*report.md"))
        report_file = None
        for r in report_files:
            if "automation" not in r.lower() and "vulnerability" not in r.lower():
                report_file = r
                break
        if not report_file and report_files:
            report_file = report_files[0]

    if not report_file: 
        return None
        
    with open(report_file, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Extract Target App from source_val (package name)
    target_app = source_val.split()[0] if source_val else "Unknown"
    # (Report matching skipped to ensure clean portal value)

    # Extract Date (Default to today)
    from datetime import datetime
    date_val = datetime.now().strftime("%Y-%m-%d")
    
    sheet_file = os.path.join(folder_path, "googlesheet.txt")
    if os.path.exists(sheet_file):
        with open(sheet_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("Date:"):
                    extracted_date = line.strip().split("Date:")[1].strip()
                    if extracted_date and extracted_date != "4/25/2026": # Check if it's a real date or placeholder
                        date_val = extracted_date
                    break

    # Exec Summary Parsing
    exec_match = re.search(r'## 1\. Executive Summary\n+(.*?)\n+## 2\.', raw_text, re.DOTALL | re.IGNORECASE)
    exec_summary = exec_match.group(1).strip() if exec_match else ""

    # Conclusion Parsing - Extract everything after the Conclusion header
    conc_match = re.search(r'## \d+\. Conclusion\n+(.*)', raw_text, re.DOTALL | re.IGNORECASE)
    conc_text = conc_match.group(1).strip() if conc_match else ""

    feasibility_match = re.search(r'Automation Feasibility:\s*(.*?)(?:\n|$)', raw_text, re.IGNORECASE)
    feasibility = "Low"
    if feasibility_match:
        f_text = feasibility_match.group(1)
        if "Low" in f_text: feasibility = "Low"
        elif "Medium" in f_text: feasibility = "Medium"
        elif "High" in f_text: feasibility = "High"

    # Quick Analysis Mapping
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

    return {
        "engineering_details": {
            "File Name": os.path.basename(report_file),
            "Report Metadata": {
                "Target URL/App": target_app,
                "Researcher": "Deepanshu Singh",
                "Date": date_val,
                "Status": "New",
                "HAR Files": None
            },
            "Executive Summary": exec_summary,
            "Quick Analysis": qa,
            "Flow Details": [],
            "Security Notes": None,
            "Conclusion & Feasibility": { "feasibility": feasibility, "text": conc_text },
            "Flow Details Raw": raw_text,
            "Identified Steps": [],
            "executive_summary": exec_summary,
            "metadata": {
                "target_url_app": target_app,
                "researcher": "Deepanshu Singh",
                "date": date_val
            },
            "flow_details_raw": raw_text,
            "conclusion": {
                "feasibility": feasibility,
                "text": conc_text
            },
            "identified_steps": ["Enter Number", "Solve Captcha", "Submit OTP"],
            "quick_analysis": qa
        }
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder_path", help="Folder containing records (e.g. DoLynkCare)")
    parser.add_argument("--confirm", action="store_true", help="Execute the API triggers")
    args = parser.parse_args()

    uuid = get_service_uuid(args.folder_path)
    source = get_app_details(args.folder_path)

    if not source:
        print("[-] Error: Source cannot be empty. It must have the service android package name followed by the date.")
        sys.exit(1)

    if not uuid:
        print("[-] Could not find UUID in inf.txt")
        return

    payload_claim = {"platform": "android", "source": source, "phone_flow": "yes"}
    payload_project = {"platform": "android", "source": source}
    engineering_payload = parse_report(args.folder_path, source)

    if not args.confirm:
        print("[*] DATA EXTRACTED - PENDING CONFIRMATION")
        print(f"Target UUID         : {uuid}")
        print(f"Claim Payload       : {json.dumps(payload_claim)}")
        print(f"Create Proj Payload : {json.dumps(payload_project)}")
        print(f"Data Object Ready   : {engineering_payload is not None} (Length: {len(str(engineering_payload))})")
        print("\nPass --confirm flag to execute.")
        return

    try:
        print("[*] Logging in to API...")
        token = login()
    except Exception as e:
        print(f"[-] {e}")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 1. CLAIM
    print("[*] 1. Submitting claim via API...")
    res_claim = requests.post(f"{API_BASE}/services/{uuid}/claim", headers=headers, json=payload_claim)
    print(f"Claim Status Code: {res_claim.status_code}")
    if res_claim.status_code == 200:
        print("[+] Claim Success!")
    else:
        print("[-] Claim Output:", res_claim.text)

    # 1.5 UPDATE PHONE FLOW
    print("[*] 1.5. Updating phone flow status...")
    res_phone = requests.put(f"{API_BASE}/services/{uuid}/claims/phone-flow", headers=headers, json=payload_claim)
    print(f"Phone Flow Status Code: {res_phone.status_code}")
    if res_phone.status_code == 200:
        print("[+] Phone Flow Updated Successfully!")
    else:
        print("[-] Phone Flow Update Failed:", res_phone.text)

    # 2. CREATE PROJECT
    print("\n[*] 2. Creating project via API...")
    res_proj = requests.post(f"{API_BASE}/services/{uuid}/create-project", headers=headers, json=payload_project)
    print(f"Project Status Code: {res_proj.status_code}")

    if res_proj.status_code == 200:
        proj_data = res_proj.json()
        project_id = proj_data.get('id')
    elif res_proj.status_code == 400 and "already created" in res_proj.text:
        # Fetch projects to find the existing one
        print("[*] Project already exists. Fetching project ID...")
        res_list = requests.get(f"{API_BASE}/projects", headers=headers)
        if res_list.status_code == 200:
            projs = res_list.json()
            # Match by linked_service_id (uuid)
            match = next((p for p in projs if p.get('linked_service_id') == uuid), None)
            project_id = match.get('id') if match else None
        else:
            project_id = None
    else:
        print("[-] Project Creation Failed:", res_proj.text)
        project_id = None

    if project_id:
        print(f"[+] Using Project ID: {project_id}")
        
        # 3. PUT UPLOAD DATA (Markdown content to Project fields)
        if engineering_payload:
            print(f"\n[*] 3. Uploading Markdown variables to Project {project_id}...")
            res_put = requests.put(f"{API_BASE}/projects/{project_id}", headers=headers, json=engineering_payload)
            print(f"PUT Status Code: {res_put.status_code}")
            
            # 4. POST RESEARCH ARTIFACTS (Files and Full Report)
            print(f"\n[*] 4. Syncing Research Artifacts (HARs & Report) to Project {project_id}...")
            sync_research(args.folder_path, project_id, headers)
            
            # 5. MARK MESSAGE RECEIVED (New step)
            mark_message_received(args.folder_path, project_id, headers)
            
        else:
            print("[-] Cannot PUT data. Failed parser.")

def mark_message_received(folder_path, project_id, headers):
    inf_file = os.path.join(folder_path, "inf.txt")
    if os.path.exists(inf_file):
        with open(inf_file, "r", encoding="utf-8") as f:
            content = f.read()
            if "Messages received successfully" in content or "OTP received" in content:
                print(f"\n[*] 5. Marking Message Received for Project {project_id}...")
                payload = {"message_received": "yes", "message_note": ""}
                res = requests.put(f"{API_BASE}/projects/{project_id}/message-received", headers=headers, json=payload)
                print(f"   -> Mark Message Status: {res.status_code}")
                if res.status_code != 200:
                    print("   [-] Details:", res.text)

def sync_research(folder_path, project_id, headers):
    report_file = os.path.join(folder_path, "report.md")
    if not os.path.exists(report_file):
        report_files = glob.glob(os.path.join(folder_path, "*report.md"))
        report_file = next((r for r in report_files if "automation" not in r.lower() and "vulnerability" not in r.lower()), None)
    
    har_files = glob.glob(os.path.join(folder_path, "*.har"))
    # Exclude SubmitNumber.har or SubmitOTP.har to only upload the main company.har
    main_hars = [h for h in har_files if "submit" not in os.path.basename(h).lower()]
    main_har = main_hars[0] if main_hars else None
    
    files = []
    open_handles = []
    
    try:
        if report_file:
            f = open(report_file, "rb")
            open_handles.append(f)
            files.append(('report_file', (os.path.basename(report_file), f, 'application/octet-stream')))
            
        if main_har:
            f2 = open(main_har, "rb")
            open_handles.append(f2)
            files.append(('data_file', (os.path.basename(main_har), f2, 'application/octet-stream')))
            
        file_headers = {"Authorization": headers["Authorization"]}
        print(f"[*] Uploading composite research payload to {project_id}... (Report: {os.path.basename(report_file) if report_file else 'None'}, Data: {os.path.basename(main_har) if main_har else 'None'})")
        res = requests.post(f"{API_BASE}/projects/{project_id}/research", headers=file_headers, files=files)
        print(f"   -> Composite Attachment Upload: {res.status_code}")
        if res.status_code != 200:
            print("   [-] Details:", res.text)
    finally:
        for f in open_handles:
            f.close()

if __name__ == "__main__":
    main()
