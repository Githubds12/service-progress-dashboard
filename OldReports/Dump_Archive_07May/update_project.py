import os
import sys
import argparse
import requests
from api_portal import login, get_app_details, parse_report, sync_research

API_BASE = "http://51.195.24.179:8092/api"

def main():
    parser = argparse.ArgumentParser(description="Update an existing project's Engineering Details / Files without attempting a new service claim.")
    parser.add_argument("folder_path", help="Folder containing records (e.g. OnePlus)")
    parser.add_argument("--project", "-p", required=True, help="The distinct Project ID (UUID) from the portal UI")
    parser.add_argument("--artifacts", action="store_true", help="Re-sync HAR and Report files (creates duplicate upload blocks in UI)")
    parser.add_argument("--confirm", action="store_true", help="Execute the update request")
    
    args = parser.parse_args()

    project_id = args.project
    folder_path = args.folder_path
    
    if not os.path.exists(folder_path):
        print(f"[-] Error: Folder '{folder_path}' does not exist.")
        sys.exit(1)

    source = get_app_details(folder_path)
    if not source:
        print("[-] Error: Source target invalid. Check googlesheet.txt format (e.g. com.app.site 1.0.0).")
        sys.exit(1)

    eng_payload = parse_report(folder_path, source)
    
    if not eng_payload:
        print("[-] Error: Could not successfully map report metadata. Validate standard report.md template structure.")
        sys.exit(1)

    if not args.confirm:
        print("\n[*] DATA MAP SUCCESSFUL - PENDING SYSTEM CONFIRMATION")
        print(f"Target Project ID   : {project_id}")
        print(f"Sync Artifacts?     : {args.artifacts}")
        print(f"Engineering JSON    : Active & Loaded (Payload length {len(str(eng_payload))})")
        print("\nIf output is expected, run again appending the '--confirm' flag.")
        return

    try:
        print("[*] Retrieving active API token...")
        token = login()
    except Exception as e:
        print(f"[-] Authentication handshake failed: {e}")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"\n[*] 1. Syncing precise Engineering Metrics -> Project: {project_id}")
    res_put = requests.put(f"{API_BASE}/projects/{project_id}", headers=headers, json=eng_payload)
    print(f"PUT Transaction Route: HTTP {res_put.status_code}")
    
    if res_put.status_code != 200:
        print("[-] Rejection Reason:", res_put.text)
        
    if args.artifacts:
        print(f"\n[*] 2. Triggering discrete Research Data Attachment (HARs/Markdown)...")
        print("[-] NOTICE: API routes do not natively drop old files; this will mount a new attachment header.")
        sync_research(folder_path, project_id, headers)
    else:
        print("\n[*] Skipping research artifacts mapping (--artifacts flag disabled).")

if __name__ == "__main__":
    main()
