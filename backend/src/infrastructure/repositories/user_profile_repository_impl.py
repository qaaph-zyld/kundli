"""
User Profile Repository Implementation
This module implements the repository interface for user profile data.
"""
import logging
from typing import List, Optional, Dict, Any

from ...core.entities.user_profile import UserProfile, SavedLocation, SavedPerson
from ...core.repositories.user_profile_repository import UserProfileRepository

# Configure logging
logger = logging.getLogger(__name__)


class InMemoryUserProfileRepository(UserProfileRepository):
    """In-memory implementation of the user profile repository."""
    
    def __init__(self):
        """Initialize the repository."""
        self.profiles = {}
        self.username_index = {}
        self.email_index = {}
    
    async def save(self, profile: UserProfile) -> str:
        """
        Save a user profile to the repository.
        
        Args:
            profile: The user profile to save
            
        Returns:
            str: The ID of the saved profile
        """
        user_id = profile.id
        
        # Update indices
        self.username_index[profile.username] = user_id
        self.email_index[profile.email] = user_id
        
        # Store the profile
        self.profiles[user_id] = profile
        
        logger.info(f"Saved user profile with ID: {user_id}")
        return user_id
    
    async def get_by_id(self, user_id: str) -> Optional[UserProfile]:
        """
        Get a user profile by its ID.
        
        Args:
            user_id: The ID of the user profile to retrieve
            
        Returns:
            Optional[UserProfile]: The user profile if found, None otherwise
        """
        profile = self.profiles.get(user_id)
        if not profile:
            logger.warning(f"User profile with ID {user_id} not found")
        return profile
    
    async def get_by_username(self, username: str) -> Optional[UserProfile]:
        """
        Get a user profile by username.
        
        Args:
            username: The username to search for
            
        Returns:
            Optional[UserProfile]: The user profile if found, None otherwise
        """
        user_id = self.username_index.get(username)
        if not user_id:
            logger.warning(f"User profile with username {username} not found")
            return None
        
        return self.profiles.get(user_id)
    
    async def get_by_email(self, email: str) -> Optional[UserProfile]:
        """
        Get a user profile by email address.
        
        Args:
            email: The email address to search for
            
        Returns:
            Optional[UserProfile]: The user profile if found, None otherwise
        """
        user_id = self.email_index.get(email)
        if not user_id:
            logger.warning(f"User profile with email {email} not found")
            return None
        
        return self.profiles.get(user_id)
    
    async def delete(self, user_id: str) -> bool:
        """
        Delete a user profile by its ID.
        
        Args:
            user_id: The ID of the user profile to delete
            
        Returns:
            bool: True if the profile was deleted, False otherwise
        """
        if user_id not in self.profiles:
            logger.warning(f"Cannot delete: User profile with ID {user_id} not found")
            return False
        
        # Get the profile for index cleanup
        profile = self.profiles[user_id]
        
        # Remove from indices
        if profile.username in self.username_index:
            del self.username_index[profile.username]
        
        if profile.email in self.email_index:
            del self.email_index[profile.email]
        
        # Remove the profile
        del self.profiles[user_id]
        
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
        if user_id not in self.profiles:
            logger.warning(f"Cannot update: User profile with ID {user_id} not found")
            return None
        
        # Get the existing profile
        profile = self.profiles[user_id]
        
        # Check for username or email changes to update indices
        if "username" in data and data["username"] != profile.username:
            # Remove old username from index
            if profile.username in self.username_index:
                del self.username_index[profile.username]
            
            # Add new username to index
            self.username_index[data["username"]] = user_id
        
        if "email" in data and data["email"] != profile.email:
            # Remove old email from index
            if profile.email in self.email_index:
                del self.email_index[profile.email]
            
            # Add new email to index
            self.email_index[data["email"]] = user_id
        
        # Update the profile with new data
        for key, value in data.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        logger.info(f"Updated user profile with ID: {user_id}")
        return profile
    
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
        # Simple implementation for now
        results = []
        
        for profile in self.profiles.values():
            match = True
            
            # Check each query criterion
            for key, value in query.items():
                if hasattr(profile, key):
                    profile_value = getattr(profile, key)
                    
                    # Handle exact matches
                    if profile_value != value:
                        match = False
                        break
                else:
                    match = False
                    break
            
            if match:
                results.append(profile)
        
        # Apply pagination
        paginated_results = results[offset:offset + limit]
        
        return paginated_results
    
    async def update_preferences(self, user_id: str, preferences: Dict[str, Any]) -> Optional[UserProfile]:
        """
        Update user preferences.
        
        Args:
            user_id: The ID of the user profile to update
            preferences: The preferences to update
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        if user_id not in self.profiles:
            logger.warning(f"Cannot update preferences: User profile with ID {user_id} not found")
            return None
        
        # Get the existing profile
        profile = self.profiles[user_id]
        
        # Update preferences
        profile.update_preferences(preferences)
        
        logger.info(f"Updated preferences for user profile with ID: {user_id}")
        return profile
    
    async def add_saved_location(self, user_id: str, location_data: Dict[str, Any]) -> Optional[UserProfile]:
        """
        Add a saved location to a user profile.
        
        Args:
            user_id: The ID of the user profile to update
            location_data: The location data to add
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        if user_id not in self.profiles:
            logger.warning(f"Cannot add saved location: User profile with ID {user_id} not found")
            return None
        
        # Get the existing profile
        profile = self.profiles[user_id]
        
        # Create and add the saved location
        location = SavedLocation(**location_data)
        profile.add_saved_location(location)
        
        logger.info(f"Added saved location '{location.name}' to user profile with ID: {user_id}")
        return profile
    
    async def add_saved_person(self, user_id: str, person_data: Dict[str, Any]) -> Optional[UserProfile]:
        """
        Add a saved person to a user profile.
        
        Args:
            user_id: The ID of the user profile to update
            person_data: The person data to add
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        if user_id not in self.profiles:
            logger.warning(f"Cannot add saved person: User profile with ID {user_id} not found")
            return None
        
        # Get the existing profile
        profile = self.profiles[user_id]
        
        # Create and add the saved person
        person = SavedPerson(**person_data)
        profile.add_saved_person(person)
        
        logger.info(f"Added saved person '{person.name}' to user profile with ID: {user_id}")
        return profile
    
    async def add_recent_calculation(self, user_id: str, calculation_id: str) -> Optional[UserProfile]:
        """
        Add a calculation ID to a user's recent calculations.
        
        Args:
            user_id: The ID of the user profile to update
            calculation_id: The calculation ID to add
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        if user_id not in self.profiles:
            logger.warning(f"Cannot add recent calculation: User profile with ID {user_id} not found")
            return None
        
        # Get the existing profile
        profile = self.profiles[user_id]
        
        # Add the calculation ID
        profile.add_recent_calculation(calculation_id)
        
        logger.info(f"Added recent calculation to user profile with ID: {user_id}")
        return profile
