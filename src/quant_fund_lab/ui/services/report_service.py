from __future__ import annotations

from pathlib import Path

import pandas as pd

from quant_fund_lab.config.settings import settings
from quant_fund_lab.ui.services.result import ServiceResult


def list_reports_service(reports_dir: Path = settings.project_root / "reports") -> ServiceResult:
    try:
        if not reports_dir.exists():
            return ServiceResult(True, "暂无报告目录", dataframe=pd.DataFrame(columns=["name", "path", "size_kb"]), files=[])
        files = sorted(
            [path for path in reports_dir.iterdir() if path.suffix.lower() in {".csv", ".html", ".png", ".jpg", ".jpeg", ".parquet", ".md"}]
        )
        df = pd.DataFrame(
            {
                "name": [path.name for path in files],
                "path": [str(path) for path in files],
                "size_kb": [round(path.stat().st_size / 1024, 1) for path in files],
                "suffix": [path.suffix for path in files],
            }
        )
        return ServiceResult(True, f"发现 {len(files)} 个报告文件", dataframe=df, data=files, files=files)
    except Exception as exc:
        return ServiceResult(False, f"扫描报告失败: {exc}", error_detail=repr(exc))


def preview_report_service(path: str | Path) -> ServiceResult:
    report_path = Path(path)
    if not report_path.exists():
        return ServiceResult(False, f"报告不存在: {report_path}")
    try:
        if report_path.suffix.lower() == ".csv":
            df = pd.read_csv(report_path)
            return ServiceResult(True, f"已预览 CSV: {report_path.name}", dataframe=df, files=[report_path])
        if report_path.suffix.lower() == ".parquet":
            df = pd.read_parquet(report_path)
            return ServiceResult(True, f"已预览 Parquet: {report_path.name}", dataframe=df, files=[report_path])
        return ServiceResult(True, f"文件可下载: {report_path.name}", files=[report_path])
    except Exception as exc:
        return ServiceResult(False, f"预览报告失败: {exc}", error_detail=repr(exc), files=[report_path])
