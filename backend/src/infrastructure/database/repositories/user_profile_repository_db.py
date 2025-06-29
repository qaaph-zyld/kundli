"""
User Profile Repository Database Implementation
This module implements the repository interface for user profile data using SQLAlchemy.
"""
import logging
from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy import desc

from ....core.entities.user_profile import UserProfile, SavedLocation, SavedPerson, UserPreferences
from ....core.repositories.user_profile_repository import UserProfileRepository
from ..models import UserProfileModel

# Configure logging
logger = logging.getLogger(__name__)


class SQLAlchemyUserProfileRepository(UserProfileRepository):
    """SQLAlchemy implementation of the user profile repository."""
    
    def __init__(self, db_session: Session):
        """
        Initialize the repository.
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db = db_session
    
    async def save(self, profile: UserProfile) -> str:
        """
        Save a user profile to the repository.
        
        Args:
            profile: The user profile to save
            
        Returns:
            str: The ID of the saved profile
        """
        # Create model instance
        profile_model = UserProfileModel(
            id=profile.id,
            username=profile.username,
            email=profile.email,
            created_at=profile.created_at,
            last_login=profile.last_login,
            preferences=profile.preferences.dict() if profile.preferences else {},
            saved_locations=[location.dict() for location in profile.saved_locations],
            saved_people=[person.dict() for person in profile.saved_people],
            recent_calculations=profile.recent_calculations,
            is_active=profile.is_active,
            is_verified=profile.is_verified,
            roles=profile.roles
        )
        
        # Add to database
        self.db.add(profile_model)
        self.db.commit()
        self.db.refresh(profile_model)
        
        logger.info(f"Saved user profile with ID: {profile.id}")
        return profile.id
    
    async def get_by_id(self, user_id: str) -> Optional[UserProfile]:
        """
        Get a user profile by its ID.
        
        Args:
            user_id: The ID of the user profile to retrieve
            
        Returns:
            Optional[UserProfile]: The user profile if found, None otherwise
        """
        # Query the database
        profile_model = self.db.query(UserProfileModel).filter(UserProfileModel.id == user_id).first()
        
        if not profile_model:
            logger.warning(f"User profile with ID {user_id} not found")
            return None
        
        # Convert to domain entity
        return self._model_to_entity(profile_model)
    
    async def get_by_username(self, username: str) -> Optional[UserProfile]:
        """
        Get a user profile by username.
        
        Args:
            username: The username to search for
            
        Returns:
            Optional[UserProfile]: The user profile if found, None otherwise
        """
        # Query the database
        profile_model = self.db.query(UserProfileModel).filter(UserProfileModel.username == username).first()
        
        if not profile_model:
            logger.warning(f"User profile with username {username} not found")
            return None
        
        # Convert to domain entity
        return self._model_to_entity(profile_model)
    
    async def get_by_email(self, email: str) -> Optional[UserProfile]:
        """
        Get a user profile by email address.
        
        Args:
            email: The email address to search for
            
        Returns:
            Optional[UserProfile]: The user profile if found, None otherwise
        """
        # Query the database
        profile_model = self.db.query(UserProfileModel).filter(UserProfileModel.email == email).first()
        
        if not profile_model:
            logger.warning(f"User profile with email {email} not found")
            return None
        
        # Convert to domain entity
        return self._model_to_entity(profile_model)
    
    async def delete(self, user_id: str) -> bool:
        """
        Delete a user profile by its ID.
        
        Args:
            user_id: The ID of the user profile to delete
            
        Returns:
            bool: True if the profile was deleted, False otherwise
        """
        # Query the database
        profile_model = self.db.query(UserProfileModel).filter(UserProfileModel.id == user_id).first()
        
        if not profile_model:
            logger.warning(f"Cannot delete: User profile with ID {user_id} not found")
            return False
        
        # Delete from database
        self.db.delete(profile_model)
        self.db.commit()
        
        logger.info(f"Deleted user profile with ID: {user_id}")
        return True
    
    async def update(self, user_id: str, data: Dict[str, Any]) -> Optional[UserProfile]:
        """
        Update a user profile with new data.
        
        Args:
            user_id: The ID of the user profile to update
            data: The data to update
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        # Query the database
        profile_model = self.db.query(UserProfileModel).filter(UserProfileModel.id == user_id).first()
        
        if not profile_model:
            logger.warning(f"Cannot update: User profile with ID {user_id} not found")
            return None
        
        # Update the model with new data
        for key, value in data.items():
            if hasattr(profile_model, key):
                # Handle special cases for JSON fields
                if key == "preferences" and isinstance(value, dict):
                    profile_model.preferences = value
                elif key == "saved_locations" and isinstance(value, list):
                    profile_model.saved_locations = [location.dict() for location in value]
                elif key == "saved_people" and isinstance(value, list):
                    profile_model.saved_people = [person.dict() for person in value]
                elif key == "recent_calculations" and isinstance(value, list):
                    profile_model.recent_calculations = value
                elif key == "roles" and isinstance(value, list):
                    profile_model.roles = value
                else:
                    setattr(profile_model, key, value)
        
        # Commit changes
        self.db.commit()
        self.db.refresh(profile_model)
        
        logger.info(f"Updated user profile with ID: {user_id}")
        
        # Convert to domain entity
        return self._model_to_entity(profile_model)
    
    async def search(self, query: Dict[str, Any], limit: int = 10, offset: int = 0) -> List[UserProfile]:
        """
        Search for user profiles matching query criteria.
        
        Args:
            query: The search criteria
            limit: Maximum number of profiles to return
            offset: Number of profiles to skip
            
        Returns:
            List[UserProfile]: List of matching user profiles
        """
        # Start with a base query
        db_query = self.db.query(UserProfileModel)
        
        # Apply filters based on query criteria
        for key, value in query.items():
            if hasattr(UserProfileModel, key):
                db_query = db_query.filter(getattr(UserProfileModel, key) == value)
        
        # Apply pagination
        profile_models = db_query.order_by(desc(UserProfileModel.created_at)).offset(offset).limit(limit).all()
        
        # Convert to domain entities
        return [self._model_to_entity(profile_model) for profile_model in profile_models]
    
    async def update_preferences(self, user_id: str, preferences: Dict[str, Any]) -> Optional[UserProfile]:
        """
        Update user preferences.
        
        Args:
            user_id: The ID of the user profile to update
            preferences: The preferences to update
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        # Query the database
        profile_model = self.db.query(UserProfileModel).filter(UserProfileModel.id == user_id).first()
        
        if not profile_model:
            logger.warning(f"Cannot update preferences: User profile with ID {user_id} not found")
            return None
        
        # Update preferences
        current_preferences = profile_model.preferences or {}
        current_preferences.update(preferences)
        profile_model.preferences = current_preferences
        
        # Commit changes
        self.db.commit()
        self.db.refresh(profile_model)
        
        logger.info(f"Updated preferences for user profile with ID: {user_id}")
        
        # Convert to domain entity
        return self._model_to_entity(profile_model)
    
    async def add_saved_location(self, user_id: str, location_data: Dict[str, Any]) -> Optional[UserProfile]:
        """
        Add a saved location to a user profile.
        
        Args:
            user_id: The ID of the user profile to update
            location_data: The location data to add
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        # Query the database
        profile_model = self.db.query(UserProfileModel).filter(UserProfileModel.id == user_id).first()
        
        if not profile_model:
            logger.warning(f"Cannot add saved location: User profile with ID {user_id} not found")
            return None
        
        # Get current saved locations
        saved_locations = profile_model.saved_locations or []
        
        # Check if location with same name exists
        location_name = location_data.get("name")
        for i, location in enumerate(saved_locations):
            if location.get("name") == location_name:
                # Update existing location
                saved_locations[i] = location_data
                break
        else:
            # Add new location
            saved_locations.append(location_data)
        
        # Update model
        profile_model.saved_locations = saved_locations
        
        # Commit changes
        self.db.commit()
        self.db.refresh(profile_model)
        
        logger.info(f"Added saved location to user profile with ID: {user_id}")
        
        # Convert to domain entity
        return self._model_to_entity(profile_model)
    
    async def add_saved_person(self, user_id: str, person_data: Dict[str, Any]) -> Optional[UserProfile]:
        """
        Add a saved person to a user profile.
        
        Args:
            user_id: The ID of the user profile to update
            person_data: The person data to add
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        # Query the database
        profile_model = self.db.query(UserProfileModel).filter(UserProfileModel.id == user_id).first()
        
        if not profile_model:
            logger.warning(f"Cannot add saved person: User profile with ID {user_id} not found")
            return None
        
        # Get current saved people
        saved_people = profile_model.saved_people or []
        
        # Check if person with same name exists
        person_name = person_data.get("name")
        for i, person in enumerate(saved_people):
            if person.get("name") == person_name:
                # Update existing person
                saved_people[i] = person_data
                break
        else:
            # Add new person
            saved_people.append(person_data)
        
        # Update model
        profile_model.saved_people = saved_people
        
        # Commit changes
        self.db.commit()
        self.db.refresh(profile_model)
        
        logger.info(f"Added saved person to user profile with ID: {user_id}")
        
        # Convert to domain entity
        return self._model_to_entity(profile_model)
    
    async def add_recent_calculation(self, user_id: str, calculation_id: str) -> Optional[UserProfile]:
        """
        Add a calculation ID to a user's recent calculations.
        
        Args:
            user_id: The ID of the user profile to update
            calculation_id: The calculation ID to add
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        # Query the database
        profile_model = self.db.query(UserProfileModel).filter(UserProfileModel.id == user_id).first()
        
        if not profile_model:
            logger.warning(f"Cannot add recent calculation: User profile with ID {user_id} not found")
            return None
        
        # Get current recent calculations
        recent_calculations = profile_model.recent_calculations or []
        
        # Remove if already exists
        if calculation_id in recent_calculations:
            recent_calculations.remove(calculation_id)
        
        # Add to front of list
        recent_calculations.insert(0, calculation_id)
        
        # Trim list if needed
        max_recent = 10
        if len(recent_calculations) > max_recent:
            recent_calculations = recent_calculations[:max_recent]
        
        # Update model
        profile_model.recent_calculations = recent_calculations
        
        # Commit changes
        self.db.commit()
        self.db.refresh(profile_model)
        
        logger.info(f"Added recent calculation to user profile with ID: {user_id}")
        
        # Convert to domain entity
        return self._model_to_entity(profile_model)
    
    def _model_to_entity(self, model: UserProfileModel) -> UserProfile:
        """
        Convert a database model to a domain entity.
        
        Args:
            model: The database model
            
        Returns:
            UserProfile: The domain entity
        """
        # Create preferences
        preferences = UserPreferences(**model.preferences) if model.preferences else UserPreferences()
        
        # Create saved locations
        saved_locations = []
        for location_data in model.saved_locations or []:
            saved_locations.append(SavedLocation(**location_data))
        
        # Create saved people
        saved_people = []
        for person_data in model.saved_people or []:
            saved_people.append(SavedPerson(**person_data))
        
        # Create user profile
        profile = UserProfile(
            id=model.id,
            username=model.username,
            email=model.email,
            created_at=model.created_at,
            last_login=model.last_login,
            preferences=preferences,
            saved_locations=saved_locations,
            saved_people=saved_people,
            recent_calculations=model.recent_calculations or [],
            is_active=model.is_active,
            is_verified=model.is_verified,
            roles=model.roles or []
        )
        
        return profile
