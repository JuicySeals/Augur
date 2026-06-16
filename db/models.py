from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, ForeignKey
from db.session import get_session, Base
from datetime import datetime

class Forecasts(Base):
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String, nullable=False)
    forecast_date = Column(Date, nullable=False)
    model_source = Column(String, nullable=False)
    predicted_high = Column(Integer)
    predicted_low = Column(Integer)
    forecast_horizon_hrs = Column(Integer)
    fetched_at = Column(DateTime, default=datetime.utcnow)

class Actuals(Base):
    __tablename__ = "actuals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String, nullable=False)
    observation_date = Column(Date, nullable=False)
    actual_high = Column(Integer)
    actual_low = Column(Integer)
    observed_at = Column(DateTime)

class BiasCorrections(Base):
    __tablename__ = "bias_corrections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String)
    model_source = Column(String)
    season = Column(String)
    temp_type = Column(String)
    correction_degrees = Column(Float)
    sample_size = Column(Integer)
    trained_at = Column(DateTime)

class BrierScores(Base):
    __tablename__ = "brier_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String)
    model_source = Column(String)
    season = Column(String)
    temp_type = Column(String)
    brier_score = Column(Float)
    sample_size = Column(Integer)
    baseline_score = Column(Float)
    improvement_pct = Column(Float)
    calculated_at = Column(DateTime)


class KalshiMarket(Base):
    __tablename__ = "kalshi_markets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    kalshi_market_id = Column(String, unique=True, nullable = False)
    city = Column(String)
    event_date = Column(Date)
    ticker = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolves_at = Column(DateTime)
    temp_type = Column(String, nullable=False)

class KalshiPrices(Base):
    __tablename__ = "kalshi_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    market_id = Column(Integer, ForeignKey("kalshi_markets.id"), nullable=False)
    yes_price = Column(Float)
    no_price = Column(Float)
    spread = Column(Float)
    captured_at = Column(DateTime)

class Signals(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    market_id = Column(Integer, ForeignKey("kalshi_markets.id"), nullable=False)
    predicted_temp = Column(Float)
    kalshi_price = Column(Float)
    net_edge = Column(Float)
    signal_type = Column(String, nullable=False)
    confidence = Column(Float)
    models_agreed = Column(Integer)
    generated_at = Column(DateTime, default=datetime.utcnow)

class Trades(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, autoincrement=True)
    signal_id = Column(Integer, ForeignKey("signals.id"), nullable=False)
    market_id = Column(Integer, ForeignKey("kalshi_markets.id"), nullable=False)
    is_paper = Column(Boolean, nullable=False)
    position = Column(String, nullable=False)
    size_dollars = Column(Float)
    entry_price = Column(Float)
    exit_price = Column(Float)
    outcome = Column(String)
    pnl = Column(Float)
    placed_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)

if __name__ == "__main__":
    from db.session import engine
    Base.metadata.create_all(bind=engine)
    print("All tables created.")