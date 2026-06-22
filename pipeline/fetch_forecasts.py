import logging
from config.cities import CITIES
from ingestion.open_mateo import get_forecasts
from ingestion.forecast import Forecast
from db.models import Forecasts
from db.session import get_session
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_and_store_forecasts():
    for code, city in CITIES.items():
        try:
            forecasts = []
            for info in get_forecasts(code):
                try:
                    validated = Forecast(
                        city=info['city'],
                        forecast_date=info['forecast_date'],
                        model_source=info['model_source'],
                        predicted_high=info['predicted_high'],
                        predicted_low=info['predicted_low'],
                        forecast_horizon_hrs=info['forecast_horizon_hrs'],
                        fetched_at=info['fetched_at']
                    )
                    forecasts.append(validated)
                except Exception as e:
                    logger.warning(f"Validation failed for {code} row: {e}")
                    continue

            written = 0
            with get_session() as session:
                for forecast in forecasts:
                    existing = session.query(Forecasts).filter_by(
                        city=forecast.city,
                        forecast_date=forecast.forecast_date,
                        model_source=forecast.model_source
                    ).first()

                    if existing:
                        continue

                    session.add(Forecasts(**forecast.model_dump()))
                    written += 1

                session.commit()

            logger.info(f"{code}: wrote {written}/{len(forecasts)} forecasts")

        except SQLAlchemyError as e:
            logger.error(f"{code}: database error — {e}")
            continue
        except Exception as e:
            logger.error(f"{code}: failed — {e}")
            continue

if __name__ == "__main__":
    fetch_and_store_forecasts()