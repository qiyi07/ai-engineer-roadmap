from pydantic import BaseModel, Field
from typing import Optional, List

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    condition: str
    humidity: Optional[int] = None
    wind_speed: Optional[float] = None

class CalculationResponse(BaseModel):
    expression: str
    result: float
    explanation: Optional[str] = None

class SearchResponse(BaseModel):
    query: str
    results: List[str]
    summary: str