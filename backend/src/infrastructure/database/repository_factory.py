"""
Repository Factory
This module provides a factory for creating repository instances.
"""
import logging
from typing import Optional

from sqlalchemy.orm import Session

from ...core.repositories.birth_chart_repository import BirthChartRepository
from ...core.repositories.user_profile_repository import UserProfileRepository
from .repositories.birth_chart_repository_db import SQLAlchemyBirthChartRepository
from .repositories.user_profile_repository_db import SQLAlchemyUserProfileRepository
from .connection import get_db

# Configure logging
logger = logging.getLogger(__name__)


class RepositoryFactory:
    """Factory for creating repository instances."""
    
    def __init__(self, db_session: Optional[Session] = None):
        """
        Initialize the factory.
        
        Args:
            db_session: SQLAlchemy database session (optional)
        """
        self.db_session = db_session
    
    def get_birth_chart_repository(self) -> BirthChartRepository:
        """
        Get a birth chart repository instance.
        
        Returns:
            BirthChartRepository: A birth chart repository
        """
        if self.db_session:
            logger.info("Creating SQLAlchemy birth chart repository")
            return SQLAlchemyBirthChartRepository(self.db_session)
        else:
            # Use the next session from the generator
            logger.info("Creating SQLAlchemy birth chart repository with new session")
            db = next(get_db())
            return SQLAlchemyBirthChartRepository(db)
    
    def get_user_profile_repository(self) -> UserProfileRepository:
        """
        Get a user profile repository instance.
        
        Returns:
            UserProfileRepository: A user profile repository
        """
        if self.db_session:
            logger.info("Creating SQLAlchemy user profile repository")
            return SQLAlchemyUserProfileRepository(self.db_session)
        else:
            # Use the next session from the generator
            logger.info("Creating SQLAlchemy user profile repository with new session")
            db = next(get_db())
            return SQLAlchemyUserProfileRepository(db)


# Create a singleton instance
repository_factory = RepositoryFactory()
