from __future__ import annotations

from pathlib import Path

import pandas as pd

from quant_fund_lab.data.akshare_loader import fetch_universe_prices, load_universe, to_price_matrix
from quant_fund_lab.data.download_sample import build_demo_prices, save_price_data
from quant_fund_lab.ui.config import PROCESSED_PRICE_PATH, RAW_PRICE_PATH
from quant_fund_lab.ui.services.result import ServiceResult


def load_universe_service() -> ServiceResult:
    try:
        config = load_universe()
        df = pd.DataFrame(config.get("assets", []))
        return ServiceResult(True, f"已加载研究池，共 {len(df)} 个标的", data=config, dataframe=df)
    except Exception as exc:
        return ServiceResult(False, f"加载研究池失败: {exc}", error_detail=repr(exc))


def generate_demo_data_service() -> ServiceResult:
    try:
        raw_prices, price_matrix = build_demo_prices()
        save_price_data(raw_prices, price_matrix)
        return ServiceResult(
            True,
            f"演示数据已生成: raw={raw_prices.shape}, processed={price_matrix.shape}",
            dataframe=price_matrix.reset_index().rename(columns={"index": "date"}),
            files=[RAW_PRICE_PATH, PROCESSED_PRICE_PATH],
        )
    except Exception as exc:
        return ServiceResult(False, f"生成演示数据失败: {exc}", error_detail=repr(exc))


def download_live_data_service() -> ServiceResult:
    try:
        raw_prices = fetch_universe_prices()
        price_matrix = to_price_matrix(raw_prices)
        save_price_data(raw_prices, price_matrix)
        return ServiceResult(
            True,
            f"真实数据已下载: raw={raw_prices.shape}, processed={price_matrix.shape}",
            dataframe=price_matrix.reset_index().rename(columns={"index": "date"}),
            files=[RAW_PRICE_PATH, PROCESSED_PRICE_PATH],
        )
    except Exception as exc:
        return ServiceResult(
            False,
            f"下载真实数据失败: {exc}。可先使用演示数据继续研究。",
            error_detail=repr(exc),
        )


def load_processed_price_matrix_service(path: Path = PROCESSED_PRICE_PATH) -> ServiceResult:
    if not path.exists():
        return ServiceResult(False, "未找到 processed 数据，请先生成演示数据或下载真实数据。", files=[path])
    try:
        prices = pd.read_parquet(path)
        return ServiceResult(
            True,
            f"已读取 processed 数据: {prices.shape}",
            dataframe=prices.reset_index().rename(columns={"index": "date"}),
            data=prices,
            files=[path],
        )
    except Exception as exc:
        return ServiceResult(False, f"读取 processed 数据失败: {exc}", error_detail=repr(exc), files=[path])


def load_raw_price_data_service(path: Path = RAW_PRICE_PATH) -> ServiceResult:
    if not path.exists():
        return ServiceResult(False, "未找到 raw 数据，请先生成演示数据或下载真实数据。", files=[path])
    try:
        raw = pd.read_parquet(path)
        return ServiceResult(True, f"已读取 raw 数据: {raw.shape}", dataframe=raw, data=raw, files=[path])
    except Exception as exc:
        return ServiceResult(False, f"读取 raw 数据失败: {exc}", error_detail=repr(exc), files=[path])
