"""
Initialize Sample Data
This script initializes the database with sample data for development and testing.
"""
import asyncio
import logging
from datetime import datetime, timezone

from ...core.entities.user_profile import UserProfile, UserPreferences, SavedLocation, SavedPerson
from ...core.entities.birth_chart import BirthChart
from ...infrastructure.repositories import birth_chart_repository, user_profile_repository
from ...infrastructure.astro.calculator_service import calculator_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_sample_user_profiles():
    """Create sample user profiles."""
    logger.info("Creating sample user profiles...")
    
    # Create sample user 1
    user1 = UserProfile(
        username="johndoe",
        email="john.doe@example.com",
        preferences=UserPreferences(
            ayanamsa="Lahiri",
            house_system="Placidus",
            chart_style="North Indian",
            language="en",
            theme="light"
        ),
        saved_locations=[
            SavedLocation(
                name="New York",
                latitude=40.7128,
                longitude=-74.0060,
                timezone="America/New_York",
                notes="The Big Apple"
            ),
            SavedLocation(
                name="London",
                latitude=51.5074,
                longitude=-0.1278,
                timezone="Europe/London",
                notes="Capital of UK"
            )
        ],
        saved_people=[
            SavedPerson(
                name="Jane Doe",
                date_of_birth="1990-05-15",
                time_of_birth="08:30:00",
                latitude=40.7128,
                longitude=-74.0060,
                timezone="America/New_York",
                gender="Female",
                notes="Wife"
            )
        ],
        is_active=True,
        is_verified=True,
        roles=["user"]
    )
    
    # Create sample user 2
    user2 = UserProfile(
        username="janedoe",
        email="jane.doe@example.com",
        preferences=UserPreferences(
            ayanamsa="KP",
            house_system="Equal",
            chart_style="South Indian",
            language="en",
            theme="dark"
        ),
        saved_locations=[
            SavedLocation(
                name="Mumbai",
                latitude=19.0760,
                longitude=72.8777,
                timezone="Asia/Kolkata",
                notes="Financial capital of India"
            )
        ],
        saved_people=[
            SavedPerson(
                name="John Doe",
                date_of_birth="1988-10-20",
                time_of_birth="14:15:00",
                latitude=51.5074,
                longitude=-0.1278,
                timezone="Europe/London",
                gender="Male",
                notes="Husband"
            )
        ],
        is_active=True,
        is_verified=True,
        roles=["user"]
    )
    
    # Save users to repository
    user1_id = await user_profile_repository.save(user1)
    user2_id = await user_profile_repository.save(user2)
    
    logger.info(f"Created user profile with ID: {user1_id}")
    logger.info(f"Created user profile with ID: {user2_id}")
    
    return user1_id, user2_id


async def create_sample_birth_charts(user_ids):
    """
    Create sample birth charts.
    
    Args:
        user_ids: List of user IDs
    """
    logger.info("Creating sample birth charts...")
    
    # Sample birth data
    birth_data = [
        {
            "date_time": datetime(1990, 5, 15, 8, 30, 0, tzinfo=timezone.utc),
            "latitude": 40.7128,
            "longitude": -74.0060,
            "timezone": "America/New_York",
            "ayanamsa": "Lahiri",
            "house_system": "Placidus",
            "user_id": user_ids[0]
        },
        {
            "date_time": datetime(1988, 10, 20, 14, 15, 0, tzinfo=timezone.utc),
            "latitude": 51.5074,
            "longitude": -0.1278,
            "timezone": "Europe/London",
            "ayanamsa": "KP",
            "house_system": "Equal",
            "user_id": user_ids[1]
        },
        {
            "date_time": datetime(1985, 3, 10, 12, 0, 0, tzinfo=timezone.utc),
            "latitude": 19.0760,
            "longitude": 72.8777,
            "timezone": "Asia/Kolkata",
            "ayanamsa": "Lahiri",
            "house_system": "Whole Sign",
            "user_id": user_ids[0]
        }
    ]
    
    chart_ids = []
    
    # Create birth charts
    for data in birth_data:
        # Calculate birth chart using calculator service
        chart_data = await calculator_service.calculate_birth_chart(
            date_time=data["date_time"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            timezone=data["timezone"],
            ayanamsa=data["ayanamsa"],
            house_system=data["house_system"]
        )
        
        # Create birth chart entity
        chart = BirthChart(
            date_time=data["date_time"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            timezone=data["timezone"],
            ayanamsa=data["ayanamsa"],
            house_system=data["house_system"],
            ascendant=chart_data["ascendant"],
            planets=chart_data["planets"],
            houses=chart_data["houses"],
            aspects=chart_data["aspects"],
            calculation_system=chart_data["calculation_system"],
            calculation_time=chart_data["calculation_time"]
        )
        
        # Add user ID
        chart.user_id = data["user_id"]
        
        # Save to repository
        chart_id = await birth_chart_repository.save(chart)
        chart_ids.append(chart_id)
        
        logger.info(f"Created birth chart with ID: {chart_id}")
        
        # Add to user's recent calculations
        await user_profile_repository.add_recent_calculation(data["user_id"], chart_id)
    
    return chart_ids


async def init_sample_data():
    """Initialize sample data."""
    try:
        # Create sample user profiles
        user_ids = await create_sample_user_profiles()
        
        # Create sample birth charts
        chart_ids = await create_sample_birth_charts(user_ids)
        
        logger.info("Sample data initialization complete!")
        logger.info(f"Created {len(user_ids)} user profiles and {len(chart_ids)} birth charts")
        
    except Exception as e:
        logger.error(f"Error initializing sample data: {str(e)}")
        raise


if __name__ == "__main__":
    # Run the initialization
    asyncio.run(init_sample_data())
