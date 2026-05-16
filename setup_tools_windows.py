import os
import zipfile
import urllib.request
import shutil

# Configuration
TOOLS_DIR = r"c:\Users\Gorri\Documents\Reports\bin"
os.makedirs(TOOLS_DIR, exist_ok=True)

TOOLS = {
    "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_windows_amd64.zip",
    "dnsx": "https://github.com/projectdiscovery/dnsx/releases/download/v1.2.1/dnsx_1.2.1_windows_amd64.zip",
    "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_windows_amd64.zip",
    "naabu": "https://github.com/projectdiscovery/naabu/releases/download/v2.3.1/naabu_2.3.1_windows_amd64.zip",
    "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_windows_amd64.zip",
    "assetfinder": "https://github.com/tomnomnom/assetfinder/releases/download/v0.1.1/assetfinder-windows-amd64-0.1.1.zip",
    "amass": "https://github.com/owasp-amass/amass/releases/download/v4.2.0/amass_windows_amd64.zip"
}

def download_and_extract(name, url):
    print(f">> Downloading {name}...")
    zip_path = os.path.join(TOOLS_DIR, f"{name}.zip")
    try:
        # Use a custom User-Agent to avoid blocks
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(zip_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith(".exe"):
                    filename = os.path.basename(file)
                    # For Amass, it might be in a subfolder, we want just the exe
                    source = zip_ref.open(file)
                    target_name = f"{name}.exe"
                    target = open(os.path.join(TOOLS_DIR, target_name), "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)
                    print(f"   [+] Installed {target_name}")
        os.remove(zip_path)
    except Exception as e:
        print(f"   [!] Failed to install {name}: {e}")

if __name__ == "__main__":
    print("Full 7-Tool Security Chain Initialization...")
    for name, url in TOOLS.items():
        download_and_extract(name, url)
    print(f"\nAll tools ready in {TOOLS_DIR}")
