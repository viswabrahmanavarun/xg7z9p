import httpx
import csv
import os
import asyncio
from datetime import datetime, timezone
from typing import List, Dict, Any
from cachetools import TTLCache, cached
import pandas as pd

# URLs (public BMRS endpoints). They stream CSV data.
FORECAST_URL = "https://bmrs.elexon.co.uk/api/v1/datasets/WINDFOR/stream"
ACTUAL_URL = "https://bmrs.elexon.co.uk/api/v1/datasets/FUELHH/stream"

# Simple in‑memory cache (TTL 30 minutes) to avoid repeated network calls.
_cache = TTLCache(maxsize=128, ttl=30 * 60)

def _parse_csv(content: str) -> List[Dict[str, Any]]:
    """Parse CSV string into list of dict rows.
    The BMRS CSV files include a header row with column names.
    """
    reader = csv.DictReader(content.splitlines())
    return [row for row in reader]

async def _fetch_csv(url: str, params: Dict[str, str] = None) -> str:
    """Fetch the CSV stream from Elexon.
    If ``ELEXON_API_KEY`` is set in the environment, include it as an HTTP header.
    """
    headers = {}
    api_key = os.getenv("ELEXON_API_KEY")
    if api_key:
        headers["x-api-key"] = api_key
    async with httpx.AsyncClient(timeout=60.0, headers=headers) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.text

@cached(_cache)
async def get_forecast_series(date: str) -> List[Dict[str, Any]]:
    """Return forecast series for *date* (YYYY‑MM‑DD).
    The BMRS ``WINDFOR`` dataset contains rows for many publish times – we pick
    the most recent publishTime for each startTime on the requested day.
    """
    raw_csv = await _fetch_csv(FORECAST_URL)
    rows = _parse_csv(raw_csv)
    # Filter to WIND fuel type and the requested date (UTC).
    filtered = [r for r in rows if r.get("fuelType") == "WIND" and r.get("startTime").startswith(date)]
    # Convert to pandas for easy latest publishTime selection.
    df = pd.DataFrame(filtered)
    if df.empty:
        return []
    # Ensure proper datetime parsing
    df["publishTime"] = pd.to_datetime(df["publishTime"], utc=True)
    df["startTime"] = pd.to_datetime(df["startTime"], utc=True)
    # Keep the row with max publishTime for each startTime
    df = df.sort_values("publishTime").drop_duplicates(subset=["startTime"], keep="last")
    df = df.sort_values("startTime")
    # Return a list of dicts with iso timestamps and generation (MW)
    result = []
    for _, row in df.iterrows():
        result.append({
            "startTime": row["startTime"].isoformat(),
            "generation": float(row["generation"]),
        })
    return result

@cached(_cache)
async def get_actual_series(date: str) -> List[Dict[str, Any]]:
    """Return actual wind generation series for *date* (UTC).
    The ``FUELHH`` dataset already contains a single record per 30‑min interval.
    """
    raw_csv = await _fetch_csv(ACTUAL_URL)
    rows = _parse_csv(raw_csv)
    filtered = [r for r in rows if r.get("fuelType") == "WIND" and r.get("startTime").startswith(date)]
    df = pd.DataFrame(filtered)
    if df.empty:
        return []
    df["startTime"] = pd.to_datetime(df["startTime"], utc=True)
    df = df.sort_values("startTime")
    result = []
    for _, row in df.iterrows():
        result.append({
            "startTime": row["startTime"].isoformat(),
            "generation": float(row["generation"]),
        })
    return result
