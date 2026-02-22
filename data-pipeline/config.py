import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost:5432/ev_charging_db')

# API configurations
OPENCHARGE_API_KEY = os.getenv('OPENCHARGE_API_KEY', '')
OPENCHARGE_BASE_URL = 'https://api.openchargemap.io/v3/poi'

# Data collection settings
MAX_RESULTS = 1000
COUNTRY_CODES = ['US', 'CA', 'GB', 'DE', 'FR']  # Add more as needed
UPDATE_INTERVAL_HOURS = 24