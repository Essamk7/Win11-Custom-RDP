# Win11 Custom RDP — Self-hosted Windows 11

This project runs GitHub Actions on your own Windows 11 PC.

It does not turn GitHub-hosted runners into a permanent RDP server.

## 1. Requirements

- Windows 11 Pro, Enterprise, or Education for incoming Microsoft RDP.
- Windows 11 PC with internet access.
- Python 3.12.
- GitHub account.
- Cloudflare account.

Windows Home can run the GitHub self-hosted runner but cannot host Microsoft's built-in RDP server.

## 2. Enable Remote Desktop

Open:

Settings → System → Remote Desktop

Enable Remote Desktop.

Use a strong Windows password.

## 3. Register GitHub Runner

Open your repository:

Settings → Actions → Runners → New self-hosted runner.

Select Windows and the architecture matching your computer.

Follow the commands displayed by GitHub.

Add labels:

- Windows
- X64

Keep the runner service running.

## 4. Cloudflare Tunnel

1. Open Cloudflare Zero Trust.
2. Create a Cloudflare Tunnel.
3. Configure an RDP route to tcp://localhost:3389.
4. Apply a Cloudflare Access policy.
5. Restrict access to your own identity.
6. Enable MFA.

Open PowerShell as Administrator.

Set your tunnel token:

$env:CF_TUNNEL_TOKEN = 'YOUR_TOKEN'

Run:

.\scripts\install-cloudflared-tunnel.ps1

Never commit the tunnel token to GitHub.

## 5. Run FastAPI Locally

Open PowerShell from the repository directory.

Create environment:

python -m venv .venv

Activate:

.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Set API key:

$env:API_KEY = 'replace-with-a-long-random-secret'

Start API:

uvicorn app.main:app --host 127.0.0.1 --port 8000

Health check:

http://127.0.0.1:8000/health

The API binds to localhost only.

## 6. GitHub Actions

Commit the project to your repository.

Open:

Actions → Windows Custom Environment → Run workflow.

The workflow runs on your own Windows PC.

## Security

- Never expose TCP port 3389 directly to the internet.
- Use Cloudflare Access restrictions and MFA.
- Never publish API keys or tunnel tokens.
- GitHub-hosted runners are temporary and are not permanent VPS machines.
