"""
Database Initialization Script
This script initializes the database and optionally loads sample data.
"""
import os
import sys
import asyncio
import argparse
import logging

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main(load_sample_data=False):
    """
    Initialize the database.
    
    Args:
        load_sample_data: Whether to load sample data
    """
    try:
        # Import after adding src to path
        from src.infrastructure.database import init_db
        
        # Initialize database schema
        logger.info("Initializing database schema...")
        init_db()
        logger.info("Database schema initialized successfully!")
        
        # Load sample data if requested
        if load_sample_data:
            logger.info("Loading sample data...")
            from src.infrastructure.database.init_sample_data import init_sample_data
            await init_sample_data()
            logger.info("Sample data loaded successfully!")
        
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Initialize the database")
    parser.add_argument("--sample-data", action="store_true", help="Load sample data")
    args = parser.parse_args()
    
    # Run the initialization
    asyncio.run(main(load_sample_data=args.sample_data))
