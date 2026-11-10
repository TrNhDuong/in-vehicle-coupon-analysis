"""Project paths and a small, explicit schema contract."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
RAW_CSV_PATH = DATA_RAW_DIR / "in-vehicle-coupon-recommendation.csv"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
TABLES_DIR = PROJECT_ROOT / "reports" / "tables"
TARGET = "Y"

# Column spellings correspond to the downloaded CSV, not cleaned aliases.
REQUIRED_COLUMNS = {
    "destination", "passanger", "weather", "temperature", "time",
    "coupon", "expiration", "age", "income", "Bar", "CoffeeHouse",
    "CarryAway", "RestaurantLessThan20", "Restaurant20To50",
    "toCoupon_GEQ15min", "toCoupon_GEQ25min", "direction_same", "Y",
}
