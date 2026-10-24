from typing import Optional
from pydantic import BaseModel

class Metrics(BaseModel):
    mae: Optional[float] = None
    rmse: Optional[float] = None
    bias: Optional[float] = None
    mape: Optional[float] = None
    observations: int = 0

class Observation(BaseModel):
    startTime: str
    forecast: Optional[float] = None
    actual: Optional[float] = None
    error: Optional[float] = None
    publishTime: Optional[str] = None