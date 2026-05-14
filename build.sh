#!/bin/bash
# Security Toolchain Direct Binary Installer for Render (No Root Needed)

echo ">> Initializing Security Toolchain Deployment (Binary Mode)..."

# Setup local bin directory
mkdir -p $HOME/bin
export PATH=$PATH:$HOME/bin

# Helper to download and extract
download_tool() {
    local name=$1
    local url=$2
    local zip_file="${name}.zip"
    
    echo ">> Downloading ${name}..."
    wget -q $url -O $zip_file
    
    if [[ $url == *.zip ]]; then
        unzip -o -q $zip_file -d $HOME/bin/
    elif [[ $url == *.tar.gz ]] || [[ $url == *.tgz ]]; then
        tar -xzf $zip_file -C $HOME/bin/
    fi
    
    rm $zip_file
    chmod +x $HOME/bin/${name}* 2>/dev/null || true
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

# Amass is special (nested folder)
echo ">> Downloading Amass..."
wget -q "https://github.com/owasp-amass/amass/releases/download/v4.2.0/amass_linux_amd64.zip" -O amass.zip
unzip -o -q amass.zip
cp amass_linux_amd64/amass $HOME/bin/
rm -rf amass_linux_amd64 amass.zip

echo ">> Toolchain ready. Binaries in $HOME/bin"
ls -F $HOME/bin/
