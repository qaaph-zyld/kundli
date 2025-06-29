"""
Repositories Package
This package contains repository implementations for domain entities.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Determine which repository implementation to use based on environment
USE_DATABASE = os.getenv("USE_DATABASE", "False").lower() == "true"

if USE_DATABASE:
    # Use database repositories
    from ..database.repository_factory import repository_factory
    
    # Get repository instances from factory
    birth_chart_repository = repository_factory.get_birth_chart_repository()
    user_profile_repository = repository_factory.get_user_profile_repository()
else:
    # Use in-memory repositories
    from .birth_chart_repository_impl import InMemoryBirthChartRepository
    from .user_profile_repository_impl import InMemoryUserProfileRepository
    
    # Create singleton instances
    birth_chart_repository = InMemoryBirthChartRepository()
    user_profile_repository = InMemoryUserProfileRepository()
