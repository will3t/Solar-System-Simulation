 # app_paths.py
import os, platform, sys
from pathlib import Path

APP_NAME = "Solar System Simulation"  # <-- pick your app name

def user_data_dir(app_name: str = APP_NAME) -> Path:
    if platform.system() == "Windows":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    elif platform.system() == "Darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    d = base / app_name
    d.mkdir(parents=True, exist_ok=True)
    return d

def data_path(name: str) -> Path:
    """Prefer the per-user dir; fall back to CWD for older runs/files."""
    p = user_data_dir() / name
    return p if p.exists() else Path.cwd() / name
