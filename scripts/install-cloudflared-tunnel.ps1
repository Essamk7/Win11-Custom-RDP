# Run PowerShell as Administrator.

$ErrorActionPreference = "Stop"

if (-not $env:CF_TUNNEL_TOKEN) {
    throw "Set CF_TUNNEL_TOKEN in this PowerShell session first."
}

$cloudflared = Get-Command cloudflared -ErrorAction SilentlyContinue

if (-not $cloudflared) {
    winget install --id Cloudflare.cloudflared --exact --accept-source-agreements --accept-package-agreements

    $cloudflared = Get-Command cloudflared -ErrorAction SilentlyContinue
}

if (-not $cloudflared) {
    throw "cloudflared was not found. Reopen PowerShell and retry."
}

cloudflared.exe service install $env:CF_TUNNEL_TOKEN

Start-Service cloudflared

Get-Service cloudflared | Format-Table Name, Status
