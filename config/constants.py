# config/constants.py

# Kalshi fee formula
KALSHI_FEE_COEFFICIENT = 0.07       # Fee = ceil(0.07 * C * P * (1 - P))

# Signal generation
MIN_EDGE_THRESHOLD = 0.05           # minimum net edge in dollars to fire signal
MIN_MODELS_AGREED = 2               # minimum models that must agree on direction
MIN_SAMPLE_SIZE = 50                # minimum observations before trusting bias correction

MODEL_WEIGHTS = {
    "HRRR": 0.35,
    "NAM": 0.25,
    "ECMWF": 0.20,
    "GFS": 0.10,
    "NBM": 0.10,
}

MODEL_HORIZON_HRS = {
    "HRRR": 48,
    "NAM": 84,
    "ECMWF": 240,
    "GFS": 384,
    "NBM": 168,
}

# Position sizing
MAX_POSITION_DOLLARS = 50           # max dollars per trade at $300 bankroll
MAX_PORTFOLIO_EXPOSURE = 0.30       # max 30% of bankroll in open positions
BANKROLL = 300                      # starting capital

# Data ingestion
REQUEST_TIMEOUT_SECS = 30
MAX_RETRIES = 3
RETRY_BACKOFF_SECS = 2
FETCH_INTERVAL_HRS = 6              # how often GitHub Actions runs pipeline

# Bias correction
MIN_CORRECTION_SAMPLE = 50         # minimum observations to apply correction
MAX_CORRECTION_DEGREES = 10        # reject corrections larger than this, likely bad data

# Brier score
BASELINE_BRIER = 0.25              # naive 50/50 baseline score to beat

# Seasons
SEASON_MAP = {
    12: "winter", 1: "winter", 2: "winter",
    3: "spring", 4: "spring", 5: "spring",
    6: "summer", 7: "summer", 8: "summer",
    9: "fall", 10: "fall", 11: "fall",
}