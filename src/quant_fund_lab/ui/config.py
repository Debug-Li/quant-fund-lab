from __future__ import annotations

from pathlib import Path

from quant_fund_lab.config.settings import settings


UI_TITLE = "Quant Fund Lab"
PROJECT_ROOT = settings.project_root
RAW_PRICE_PATH = PROJECT_ROOT / "data" / "raw" / "etf_daily.parquet"
PROCESSED_PRICE_PATH = PROJECT_ROOT / "data" / "processed" / "etf_close.parquet"
ROTATION_STATS_PATH = PROJECT_ROOT / "reports" / "rotation_stats.csv"
LATEST_SIGNAL_PATH = PROJECT_ROOT / "reports" / "latest_signal.csv"


def path_status(path: Path) -> dict[str, str | bool]:
    return {
        "path": str(path),
        "exists": path.exists(),
        "size": f"{path.stat().st_size / 1024:.1f} KB" if path.exists() else "-",
    }
