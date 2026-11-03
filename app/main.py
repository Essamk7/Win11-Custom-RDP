import os
import platform
import secrets
import socket
import time

from fastapi import FastAPI, Header, HTTPException

app = FastAPI(
    title="Windows Environment Manager",
    docs_url=None,
    redoc_url=None
)

_started = time.monotonic()
_api_key = os.environ.get("API_KEY", "")


def require_key(value: str | None) -> None:
    if not _api_key or not value or not secrets.compare_digest(value, _api_key):
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/")
def root():
    return {
        "service": "Windows Environment Manager",
        "status": "online"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/system")
def system(x_api_key: str | None = Header(default=None)):
    require_key(x_api_key)

    return {
        "os": platform.platform(),
        "architecture": platform.machine(),
        "hostname": socket.gethostname(),
        "python": platform.python_version(),
        "uptime_seconds": int(time.monotonic() - _started),
    }
