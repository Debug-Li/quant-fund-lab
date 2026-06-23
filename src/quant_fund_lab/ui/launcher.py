from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def main() -> None:
    app_path = Path(__file__).resolve().parent / "streamlit_app.py"
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)], check=True)


if __name__ == "__main__":
    main()
