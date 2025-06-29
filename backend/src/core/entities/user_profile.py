"""
User Profile Entity
This module defines the core domain entity for user profiles in the system.
"""
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, EmailStr


class UserPreferences(BaseModel):
    """Model for user preferences."""
    preferred_ayanamsa: str = "Lahiri"
    preferred_house_system: str = "Placidus"
    preferred_language: str = "en"
    preferred_time_format: str = "24h"
    preferred_date_format: str = "YYYY-MM-DD"
    preferred_coordinate_format: str = "decimal"
    preferred_color_theme: str = "light"
    show_aspects: bool = True
    show_divisional_charts: bool = True
    show_dashas: bool = True
    show_yogas: bool = True
    show_shadbala: bool = True
    show_interpretations: bool = True
    calculator_performance_profile: str = "balanced"


class SavedLocation(BaseModel):
    """Model for saved locations."""
    name: str
    latitude: float
    longitude: float
    timezone: str
    notes: Optional[str] = None


class SavedPerson(BaseModel):
    """Model for saved person data."""
    name: str
    date_of_birth: datetime
    time_of_birth: Optional[datetime] = None
    place_of_birth: Optional[SavedLocation] = None
    gender: Optional[str] = None
    notes: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class UserProfile(BaseModel):
    """Core domain entity for user profiles."""
    # User identification
    id: str
    username: str
    email: EmailStr
    
    # User metadata
    created_at: datetime
    last_login: Optional[datetime] = None
    
    # User data
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    saved_locations: List[SavedLocation] = Field(default_factory=list)
    saved_people: List[SavedPerson] = Field(default_factory=list)
    recent_calculations: List[str] = Field(default_factory=list)
    
    # User permissions
    is_active: bool = True
    is_verified: bool = False
    roles: List[str] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True
    
    def add_saved_location(self, location: SavedLocation) -> None:
        """Add a saved location to the user profile."""
        # Check if location with same name exists
        for i, loc in enumerate(self.saved_locations):
            if loc.name == location.name:
                # Update existing location
                self.saved_locations[i] = location
                return
        
        # Add new location
        self.saved_locations.append(location)
    
    def add_saved_person(self, person: SavedPerson) -> None:
        """Add a saved person to the user profile."""
        # Check if person with same name exists
        for i, p in enumerate(self.saved_people):
            if p.name == person.name:
                # Update existing person
                self.saved_people[i] = person
                return
        
        # Add new person
        self.saved_people.append(person)
    
    def add_recent_calculation(self, calculation_id: str, max_recent: int = 10) -> None:
        """Add a calculation ID to recent calculations."""
        # Remove if already exists
        if calculation_id in self.recent_calculations:
            self.recent_calculations.remove(calculation_id)
        
        # Add to front of list
        self.recent_calculations.insert(0, calculation_id)
        
        # Trim list if needed
        if len(self.recent_calculations) > max_recent:
            self.recent_calculations = self.recent_calculations[:max_recent]
    
    def has_role(self, role: str) -> bool:
        """Check if user has a specific role."""
        return role in self.roles
    
    def update_preferences(self, preferences: Dict[str, Any]) -> None:
        """Update user preferences."""
        # Get current preferences as dict
        current_prefs = self.preferences.dict()
        
        # Update with new preferences
        current_prefs.update(preferences)
        
        # Create new preferences object
        self.preferences = UserPreferences(**current_prefs)
