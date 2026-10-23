from pydantic import BaseModel
from typing import List, Dict, Any

class DataPoint(BaseModel):
    startTime: str  # ISO timestamp
    generation: float

class SeriesResponse(BaseModel):
    date: str
    series: List[DataPoint]

class MetricsResponse(BaseModel):
    date: str
    mae: float
    rmse: float
    bias: float
