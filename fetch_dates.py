import requests
from api_portal import login, API_BASE

def main():
    print("[*] Logging into portal...")
    try:
        token = login()
    except Exception as e:
        print(f"[-] Login failed: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}
    
    print("[*] Fetching projects...")
    res = requests.get(f"{API_BASE}/projects", headers=headers)
    
    if res.status_code == 200:
        projects = res.json()
        print(f"[+] Successfully fetched {len(projects)} projects.\n")
        
        for p in projects:
            # Safely get the name and created_at fields, adjusting based on actual JSON keys
            name = p.get('source') or p.get('name') or p.get('id')
            created_at = p.get('created_at') or p.get('createdAt') or "Unknown Date"
            print(f"Project: {name} | Created At: {created_at}")
    else:
        print(f"[-] Failed to fetch projects. Status Code: {res.status_code}")
        print(f"Response: {res.text}")

if __name__ == "__main__":
    main()
