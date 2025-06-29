"""
User Profile Repository Interface
This module defines the repository interface for user profile data.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from ..entities.user_profile import UserProfile


class UserProfileRepository(ABC):
    """Repository interface for user profile data."""
    
    @abstractmethod
    async def save(self, profile: UserProfile) -> str:
        """
        Save a user profile to the repository.
        
        Args:
            profile: The user profile to save
            
        Returns:
            str: The ID of the saved profile
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[UserProfile]:
        """
        Get a user profile by its ID.
        
        Args:
            user_id: The ID of the user profile to retrieve
            
        Returns:
            Optional[UserProfile]: The user profile if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[UserProfile]:
        """
        Get a user profile by username.
        
        Args:
            username: The username to search for
            
        Returns:
            Optional[UserProfile]: The user profile if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserProfile]:
        """
        Get a user profile by email address.
        
        Args:
            email: The email address to search for
            
        Returns:
            Optional[UserProfile]: The user profile if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """
        Delete a user profile by its ID.
        
        Args:
            user_id: The ID of the user profile to delete
            
        Returns:
            bool: True if the profile was deleted, False otherwise
        """
        pass
    
    @abstractmethod
    async def update(self, user_id: str, data: Dict[str, Any]) -> Optional[UserProfile]:
        """
        Update a user profile with new data.
        
        Args:
            user_id: The ID of the user profile to update
            data: The data to update
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    async def update_preferences(self, user_id: str, preferences: Dict[str, Any]) -> Optional[UserProfile]:
        """
        Update user preferences.
        
        Args:
            user_id: The ID of the user profile to update
            preferences: The preferences to update
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def add_saved_location(self, user_id: str, location_data: Dict[str, Any]) -> Optional[UserProfile]:
        """
        Add a saved location to a user profile.
        
        Args:
            user_id: The ID of the user profile to update
            location_data: The location data to add
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def add_saved_person(self, user_id: str, person_data: Dict[str, Any]) -> Optional[UserProfile]:
        """
        Add a saved person to a user profile.
        
        Args:
            user_id: The ID of the user profile to update
            person_data: The person data to add
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def add_recent_calculation(self, user_id: str, calculation_id: str) -> Optional[UserProfile]:
        """
        Add a calculation ID to a user's recent calculations.
        
        Args:
            user_id: The ID of the user profile to update
            calculation_id: The calculation ID to add
            
        Returns:
            Optional[UserProfile]: The updated user profile if found, None otherwise
        """
        pass
