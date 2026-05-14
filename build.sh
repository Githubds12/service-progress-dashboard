#!/bin/bash
# Security Toolchain Auto-Installer for Render Deployment

echo ">> Initializing Security Toolchain Deployment..."

# Install Go if missing
if ! command -v go &> /dev/null; then
    echo ">> Installing Go..."
    # Render environments usually have Go or we can use a Go-based base image.
    # If using Python image, we might need to apt-get.
    apt-get update && apt-get install -y golang
fi

# Set Go paths
export GOBIN=$HOME/bin
export PATH=$PATH:$GOBIN
mkdir -p $GOBIN

echo ">> Installing ProjectDiscovery Tools..."
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install -v github.com/projectdiscovery/katana/cmd/katana@latest

echo ">> Installing Amass..."
go install -v github.com/owasp-amass/amass/v4/...@latest

echo ">> Installing Assetfinder..."
go install -v github.com/tomnomnom/assetfinder@latest

# Move binaries to path accessible by backend
cp $HOME/go/bin/* $GOBIN/

echo ">> Toolchain ready. BINARIES in $GOBIN"
