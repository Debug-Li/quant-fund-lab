from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Settings:
    project_root: Path = PROJECT_ROOT
    data_dir: Path = PROJECT_ROOT / "data"
    raw_dir: Path = PROJECT_ROOT / "data" / "raw"
    processed_dir: Path = PROJECT_ROOT / "data" / "processed"
    database_path: Path = PROJECT_ROOT / "data" / "market_data.duckdb"
    strategy_dir: Path = PROJECT_ROOT / "strategies"


settings = Settings()
