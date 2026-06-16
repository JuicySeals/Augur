import httpx
from datetime import date, datetime, timezone
from ingestion.request_builder import build_forecast_request

API_KEY_TO_MODEL = {
    "gfs_seamless": "GFS",
    "ecmwf_ifs025": "ECMWF",
    "ncep_nam_conus": "NAM",
    "gfs_hrrr": "HRRR",
    "ncep_nbm_conus": "NBM"
}

def get_forecasts(city_code: str, forecast_days: int = 3) -> list[dict]:
    url = build_forecast_request(
        city_code,
        models=["GFS", "ECMWF", "NAM", "HRRR", "NBM"],
        forecast_days=forecast_days
    )

    response = httpx.get(url).json()
    daily = response["daily"]
    dates = daily["time"]
    today = date.today()

    results = []

    for i, forecast_date in enumerate(dates):
        forecast_date_obj = date.fromisoformat(forecast_date)
        horizon_hrs = (forecast_date_obj - today).days * 24

        for api_key, model_name in API_KEY_TO_MODEL.items():
            high_key = f"temperature_2m_max_{api_key}"
            low_key = f"temperature_2m_min_{api_key}"

            if high_key not in daily or low_key not in daily:
                continue

            high = daily[high_key][i]
            low = daily[low_key][i]

            if high is None or low is None:
                continue

            results.append({
                "city": city_code,
                "forecast_date": forecast_date_obj,
                "model_source": model_name,
                "predicted_high": high,
                "predicted_low": low,
                "forecast_horizon_hrs": horizon_hrs,
                "fetched_at": datetime.now(timezone.utc)
            })

    return results