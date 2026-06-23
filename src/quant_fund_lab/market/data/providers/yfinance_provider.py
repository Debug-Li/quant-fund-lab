from __future__ import annotations

from datetime import date
from datetime import datetime, timedelta, timezone

import pandas as pd
import requests
import yfinance as yf

from quant_fund_lab.market.data.providers.base import BaseDataProvider
from quant_fund_lab.utils.exceptions import DataProviderError


class YFinanceProvider(BaseDataProvider):
    source = "yfinance"

    def fetch_history(
        self,
        symbol: str,
        start: str | date,
        end: str | date | None = None,
        timeframe: str = "1d",
    ) -> pd.DataFrame:
        yf_error: Exception | None = None
        try:
            raw = yf.download(
                symbol,
                start=start,
                end=end,
                interval=timeframe,
                auto_adjust=False,
                progress=False,
            )
        except Exception as exc:  # pragma: no cover - network dependent
            yf_error = exc
            raw = pd.DataFrame()

        if raw.empty:
            try:
                return self._fetch_yahoo_chart(symbol, start, end, timeframe)
            except Exception as exc:  # pragma: no cover - network dependent
                detail = f"; yfinance error: {yf_error}" if yf_error else ""
                raise DataProviderError(
                    f"yfinance returned no data for {symbol}; Yahoo chart fallback also failed: {exc}{detail}"
                ) from exc

        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = raw.columns.get_level_values(0)

        df = raw.reset_index().rename(
            columns={
                "Date": "datetime",
                "Datetime": "datetime",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
                "Adj Close": "adjusted_close",
            }
        )
        df["symbol"] = symbol
        df["source"] = self.source
        df["timeframe"] = timeframe
        if "amount" not in df:
            df["amount"] = None
        columns = [
            "symbol",
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "amount",
            "adjusted_close",
            "source",
            "timeframe",
        ]
        return df[columns].dropna(subset=["datetime", "open", "high", "low", "close"])

    def _fetch_yahoo_chart(
        self,
        symbol: str,
        start: str | date,
        end: str | date | None = None,
        timeframe: str = "1d",
    ) -> pd.DataFrame:
        start_ts = _to_unix_timestamp(start)
        end_dt = pd.Timestamp(end).to_pydatetime() if end else datetime.now()
        end_ts = int((end_dt + timedelta(days=1)).replace(tzinfo=timezone.utc).timestamp())
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        response = requests.get(
            url,
            params={
                "period1": start_ts,
                "period2": end_ts,
                "interval": timeframe,
                "events": "history",
                "includeAdjustedClose": "true",
            },
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()
        payload = response.json()
        df = _normalize_yahoo_chart_payload(payload, symbol=symbol, timeframe=timeframe)
        if df.empty:
            raise DataProviderError("Yahoo chart returned no bars")
        return df


def _to_unix_timestamp(value: str | date) -> int:
    timestamp = pd.Timestamp(value).to_pydatetime()
    return int(timestamp.replace(tzinfo=timezone.utc).timestamp())


def _normalize_yahoo_chart_payload(payload: dict, symbol: str, timeframe: str) -> pd.DataFrame:
    chart = payload.get("chart", {})
    error = chart.get("error")
    if error:
        raise DataProviderError(str(error))
    result = chart.get("result") or []
    if not result:
        return pd.DataFrame()

    item = result[0]
    timestamps = item.get("timestamp") or []
    quote = ((item.get("indicators") or {}).get("quote") or [{}])[0]
    adjclose_values = ((item.get("indicators") or {}).get("adjclose") or [{}])[0].get("adjclose")
    df = pd.DataFrame(
        {
            "datetime": pd.to_datetime(timestamps, unit="s").tz_localize("UTC").tz_convert(None),
            "open": quote.get("open", []),
            "high": quote.get("high", []),
            "low": quote.get("low", []),
            "close": quote.get("close", []),
            "volume": quote.get("volume", []),
        }
    )
    if adjclose_values:
        df["adjusted_close"] = adjclose_values
    else:
        df["adjusted_close"] = df["close"]
    df["symbol"] = symbol
    df["source"] = "yahoo_chart"
    df["timeframe"] = timeframe
    df["amount"] = None
    columns = [
        "symbol",
        "datetime",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "amount",
        "adjusted_close",
        "source",
        "timeframe",
    ]
    return df[columns].dropna(subset=["datetime", "open", "high", "low", "close"])
