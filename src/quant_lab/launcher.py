from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    web_dir = root / "apps" / "web"
    api = subprocess.Popen([sys.executable, "-m", "uvicorn", "quant_lab.api.main:app", "--host", "127.0.0.1", "--port", "8000"], cwd=root)
    try:
        subprocess.run(["npm", "run", "dev"], cwd=web_dir, check=True)
    finally:
        api.terminate()
        api.wait(timeout=10)


if __name__ == "__main__":
    main()
