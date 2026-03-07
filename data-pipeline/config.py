import os
from dotenv import load_dotenv

# Load environment variables from .env
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


# ==============================
# DATABASE CONFIGURATION
# ==============================

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL not set. Please configure it in your .env file."
    )


# ==============================
# OPENCHARGEMAP API CONFIG
# ==============================

OPENCHARGE_API_KEY = os.getenv("OPENCHARGE_API_KEY")
if not OPENCHARGE_API_KEY:
    raise ValueError(
        "OPENCHARGE_API_KEY not set. Please configure it in your .env file."
    )

OPENCHARGE_BASE_URL = "https://api.openchargemap.io/v3/poi"


# ==============================
# DATA COLLECTION SETTINGS
# ==============================

# Recommended to keep reasonable to avoid API throttling
MAX_RESULTS = int(os.getenv("MAX_RESULTS", 500))

# Focused dataset (India)
COUNTRY_CODES = os.getenv("COUNTRY_CODES", "IN").split(",")

# How often scheduler runs (hours)
UPDATE_INTERVAL_HOURS = int(os.getenv("UPDATE_INTERVAL_HOURS", 24))