from __future__ import annotations

import pandas as pd

from quant_fund_lab.ui.services.report_service import list_reports_service, preview_report_service


def test_report_service_handles_missing_dir(tmp_path) -> None:
    result = list_reports_service(tmp_path / "missing")
    assert result.success is True
    assert result.dataframe is not None
    assert result.dataframe.empty


def test_report_service_previews_csv(tmp_path) -> None:
    path = tmp_path / "sample.csv"
    pd.DataFrame({"a": [1], "b": [2]}).to_csv(path, index=False)
    result = preview_report_service(path)
    assert result.success is True
    assert result.dataframe is not None
    assert result.dataframe.iloc[0]["a"] == 1
