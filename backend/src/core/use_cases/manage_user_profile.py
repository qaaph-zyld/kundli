"""
Manage User Profile Use Case
This module defines the use case for managing user profiles.
"""
from datetime import datetime
from typing import Dict, Any, Optional, List

from ..entities.user_profile import UserProfile, SavedLocation, SavedPerson
from ..repositories.user_profile_repository import UserProfileRepository


class ManageUserProfileUseCase:
    """Use case for managing user profiles."""
    
    def __init__(self, user_profile_repository: UserProfileRepository):
        """
        Initialize the use case.
        
        Args:
            user_profile_repository: Repository for user profile data
        """
        self.user_profile_repository = user_profile_repository
    
    async def create_profile(
        self,
        username: str,
        email: str,
        user_id: str,
        initial_preferences: Optional[Dict[str, Any]] = None
    ) -> UserProfile:
        """
        Create a new user profile.
        
        Args:
            username: Username for the new profile
            email: Email address for the new profile
            user_id: User ID for the new profile
            initial_preferences: Optional initial preferences
            
        Returns:
            UserProfile: The created user profile
        """
        # Create the user profile entity
        profile = UserProfile(
            id=user_id,
            username=username,
            email=email,
            created_at=datetime.now()
        )
        
        # Set initial preferences if provided
        if initial_preferences:
            profile.update_preferences(initial_preferences)
        
        # Save the profile
        await self.user_profile_repository.save(profile)
        
        return profile
    
    async def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """
        Get a user profile by ID.
        
        Args:
            user_id: The ID of the user profile to retrieve
            
        Returns:
            Optional[UserProfile]: The user profile if found, None otherwise
        """
        return await self.user_profile_repository.get_by_id(user_id)
    
    async def update_profile(
        self,
        user_id: str,
        data: Dict[str, Any]
    ) -> Optional[UserProfile]:
        """
        Update a user profile.
        
        Args:
            user_id: The ID of the user profile to update
            data: The data to update
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        return await self.user_profile_repository.update(user_id, data)
    
    async def update_preferences(
        self,
        user_id: str,
        preferences: Dict[str, Any]
    ) -> Optional[UserProfile]:
        """
        Update user preferences.
        
        Args:
            user_id: The ID of the user profile to update
            preferences: The preferences to update
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        return await self.user_profile_repository.update_preferences(user_id, preferences)
    
    async def add_saved_location(
        self,
        user_id: str,
        name: str,
        latitude: float,
        longitude: float,
        timezone: str,
        notes: Optional[str] = None
    ) -> Optional[UserProfile]:
        """
        Add a saved location to a user profile.
        
        Args:
            user_id: The ID of the user profile to update
            name: Name of the location
            latitude: Latitude of the location
            longitude: Longitude of the location
            timezone: Timezone of the location
            notes: Optional notes about the location
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        location_data = {
            "name": name,
            "latitude": latitude,
            "longitude": longitude,
            "timezone": timezone,
            "notes": notes
        }
        
        return await self.user_profile_repository.add_saved_location(user_id, location_data)
    
    async def add_saved_person(
        self,
        user_id: str,
        name: str,
        date_of_birth: datetime,
        time_of_birth: Optional[datetime] = None,
        place_of_birth: Optional[Dict[str, Any]] = None,
        gender: Optional[str] = None,
        notes: Optional[str] = None,
        tags: List[str] = None
    ) -> Optional[UserProfile]:
        """
        Add a saved person to a user profile.
        
        Args:
            user_id: The ID of the user profile to update
            name: Name of the person
            date_of_birth: Date of birth
            time_of_birth: Optional time of birth
            place_of_birth: Optional place of birth data
            gender: Optional gender
            notes: Optional notes about the person
            tags: Optional tags for categorization
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        person_data = {
            "name": name,
            "date_of_birth": date_of_birth,
            "time_of_birth": time_of_birth,
            "place_of_birth": place_of_birth,
            "gender": gender,
            "notes": notes,
            "tags": tags or []
        }
        
        return await self.user_profile_repository.add_saved_person(user_id, person_data)
    
    async def add_recent_calculation(
        self,
        user_id: str,
        calculation_id: str
    ) -> Optional[UserProfile]:
        """
        Add a calculation ID to a user's recent calculations.
        
        Args:
            user_id: The ID of the user profile to update
            calculation_id: The calculation ID to add
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        return await self.user_profile_repository.add_recent_calculation(user_id, calculation_id)
    
    async def delete_profile(self, user_id: str) -> bool:
        """
        Delete a user profile.
        
        Args:
            user_id: The ID of the user profile to delete
            
        Returns:
            bool: True if the profile was deleted, False otherwise
        """
        return await self.user_profile_repository.delete(user_id)
