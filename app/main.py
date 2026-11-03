
import os
import platform
import socket
import time

from fastapi import FastAPI, Header, HTTPException

app = FastAPI(
    title="Windows Environment Manager",
    version="1.0.0",
    docs_url=None
)

START_TIME = time.time()
API_KEY = os.environ.get("API_KEY", "")


def authorize(key):
    import secrets

    if not API_KEY or not key:
        raise HTTPException(401, "Unauthorized")

    if not secrets.compare_digest(key, API_KEY):
        raise HTTPException(401, "Unauthorized")


@app.get("/")
def home():
    return {
        "name": "Windows Environment Manager",
        "version": "1.0.0",
        "status": "online"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/system")
def system(x_api_key: str = Header(None)):
    authorize(x_api_key)

    return {
        "os": platform.system(),
        "version": platform.version(),
        "architecture": platform.machine(),
        "hostname": socket.gethostname(),
        "uptime_seconds": int(time.time() - START_TIME),
        "python": platform.python_version()
    }
