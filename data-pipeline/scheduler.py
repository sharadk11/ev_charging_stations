import schedule
import time
import logging
from data_collector import EVChargingDataCollector
from config import UPDATE_INTERVAL_HOURS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_data_collection():
    """Wrapper function for scheduled data collection"""
    logger.info("Starting scheduled data collection")
    collector = EVChargingDataCollector()
    try:
        collector.run_data_collection()
    except Exception as e:
        logger.error(f"Data collection failed: {e}")
    finally:
        collector.close_connection()

def main():
    """Main scheduler function"""
    logger.info(f"Starting scheduler - will run every {UPDATE_INTERVAL_HOURS} hours")
    
    # Schedule the job
    schedule.every(UPDATE_INTERVAL_HOURS).hours.do(run_data_collection)
    
    # Run once immediately
    run_data_collection()
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()