from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass
class ServiceResult:
    success: bool
    message: str
    data: Any | None = None
    dataframe: pd.DataFrame | None = None
    files: list[Path] = field(default_factory=list)
    logs: list[str] = field(default_factory=list)
    error_detail: str | None = None
