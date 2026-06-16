from pydantic import BaseModel, Field, model_validator
from typing import Literal
from datetime import datetime, date, timezone

class Forecast(BaseModel):
    city: str
    forecast_date: date
    model_source: Literal['HRRR', 'NAM', 'ECMWF', 'GFS', 'NBM']
    predicted_high: float = Field(ge=-20, le=130)
    predicted_low: float = Field(ge=-20, le=100)
    forecast_horizon_hrs: int = Field(ge=0)
    fetched_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @model_validator(mode="after")
    def high_must_exceed_low(self):
        if self.predicted_high < self.predicted_low:
            raise ValueError("predicted_high cannot be below predicted_low")
        return self