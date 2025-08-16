# PowerShell script to install optional dependencies for Requiem on Windows
# Requires running in an elevated PowerShell session

$ErrorActionPreference = 'Stop'

# Install Chocolatey if missing
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host 'Installing Chocolatey...'
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

choco install -y mongodb
choco install -y cuda
choco install -y python

python -m pip install --upgrade pip
pip install requests pymongo torch
pip install flask transformers psutil openllm
