import asyncio
import pytest
from backend.app.fetcher import get_forecast_series, get_actual_series

@pytest.mark.asyncio
async def test_fetch_forecast_series_january_2026():
    # Use a known date; the API is public, but we just ensure function returns a list
    series = await get_forecast_series("2026-01-01")
    assert isinstance(series, list)
    # At least one record expected (cannot guarantee exact count)
    if series:
        first = series[0]
        assert "startTime" in first and "generation" in first

@pytest.mark.asyncio
async def test_fetch_actual_series_january_2026():
    series = await get_actual_series("2026-01-01")
    assert isinstance(series, list)
    if series:
        first = series[0]
        assert "startTime" in first and "generation" in first
