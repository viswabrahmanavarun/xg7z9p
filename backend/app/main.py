from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from .fetcher import get_forecast_series, get_actual_series
from .metrics import compute_metrics
from .models import SeriesResponse, MetricsResponse

app = FastAPI(title="Renewable Wind Forecast API")

@app.get("/forecasts", response_model=SeriesResponse)
async def forecasts(date: str):
    data = await get_forecast_series(date)
    if not data:
        raise HTTPException(status_code=404, detail="No forecast data for given date")
    return SeriesResponse(date=date, series=data)

@app.get("/actuals", response_model=SeriesResponse)
async def actuals(date: str):
    data = await get_actual_series(date)
    if not data:
        raise HTTPException(status_code=404, detail="No actual data for given date")
    return SeriesResponse(date=date, series=data)

@app.get("/metrics", response_model=MetricsResponse)
async def metrics(date: str):
    forecast = await get_forecast_series(date)
    actual = await get_actual_series(date)
    if not forecast or not actual:
        raise HTTPException(status_code=404, detail="Insufficient data for metrics")
    mae, rmse, bias = compute_metrics(forecast, actual)
    return MetricsResponse(date=date, mae=mae, rmse=rmse, bias=bias)
