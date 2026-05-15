#!/bin/bash
# Security Toolchain Direct Binary Installer for Render (No Root Needed)
# Optimized for absolute path reliability and binary discovery

echo ">> Initializing Security Toolchain Deployment (Binary Mode)..."

# Use absolute path for Render stability
BIN_DIR="/opt/render/project/src/bin"
mkdir -p $BIN_DIR
export PATH=$PATH:$BIN_DIR

echo ">> Installing system dependencies (if permitted)..."
# Attempt to install libpcap for naabu
apt-get update && apt-get install -y libpcap-dev || echo "   [!] Apt-get failed (expected on non-root). Proceeding with binary deployment."

# Helper to download, extract, and flatten binaries
download_tool() {
    local name=$1
    local url=$2
    local temp_dir="temp_${name}"
    mkdir -p $temp_dir
    
    echo ">> Downloading ${name}..."
    wget -q $url -O "${temp_dir}.dist"
    
    if [[ $url == *.zip ]]; then
        unzip -o -q "${temp_dir}.dist" -d $temp_dir
    elif [[ $url == *.tar.gz ]] || [[ $url == *.tgz ]]; then
        tar -xzf "${temp_dir}.dist" -C $temp_dir
    fi
    
    # Move the actual binary to BIN_DIR (flattening any subfolders)
    # Search for the binary file specifically
    find $temp_dir -type f -executable -name "${name}*" -exec cp {} $BIN_DIR/$name \;
    
    rm -rf $temp_dir "${temp_dir}.dist"
    chmod +x $BIN_DIR/$name
    echo "   [+] Installed $name to $BIN_DIR/$name"
}

# 1. Subfinder
download_tool "subfinder" "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip"

# 2. DNSX
download_tool "dnsx" "https://github.com/projectdiscovery/dnsx/releases/download/v1.2.1/dnsx_1.2.1_linux_amd64.zip"

# 3. HTTPX
download_tool "httpx" "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip"

# 4. Naabu
download_tool "naabu" "https://github.com/projectdiscovery/naabu/releases/download/v2.3.1/naabu_2.3.1_linux_amd64.zip"

# 5. Katana
download_tool "katana" "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip"

# 6. Assetfinder
download_tool "assetfinder" "https://github.com/tomnomnom/assetfinder/releases/download/v0.1.1/assetfinder-linux-amd64-0.1.1.tgz"

# 7. Amass (Using simpler flattening)
download_tool "amass" "https://github.com/owasp-amass/amass/releases/download/v4.2.0/amass_linux_amd64.zip"

echo ">> Toolchain ready. Binaries in $BIN_DIR"
ls -F $BIN_DIR
