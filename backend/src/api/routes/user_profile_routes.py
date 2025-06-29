"""
User Profile Routes
This module defines API routes for user profile operations.
"""
import logging
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from pydantic import BaseModel, EmailStr

from ...core.entities.user_profile import UserProfile, SavedLocation, SavedPerson, UserPreferences
from ...core.use_cases.manage_user_profile import ManageUserProfileUseCase
from ...infrastructure.repositories import user_profile_repository

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/user-profiles", tags=["User Profiles"])


# Define request and response models
class UserProfileRequest(BaseModel):
    """Request model for creating a user profile."""
    username: str
    email: EmailStr
    preferences: Optional[Dict[str, Any]] = None


class UserProfileResponse(BaseModel):
    """Response model for user profile data."""
    id: str
    username: str
    email: str
    created_at: str
    last_login: Optional[str] = None
    preferences: Dict[str, Any]
    saved_locations: List[Dict[str, Any]]
    saved_people: List[Dict[str, Any]]
    recent_calculations: List[str]
    is_active: bool
    is_verified: bool
    roles: List[str]


class SavedLocationRequest(BaseModel):
    """Request model for adding a saved location."""
    name: str
    latitude: float
    longitude: float
    timezone: str
    notes: Optional[str] = None


class SavedPersonRequest(BaseModel):
    """Request model for adding a saved person."""
    name: str
    date_of_birth: str
    time_of_birth: str
    latitude: float
    longitude: float
    timezone: str
    gender: Optional[str] = None
    notes: Optional[str] = None


class UserPreferencesRequest(BaseModel):
    """Request model for updating user preferences."""
    ayanamsa: Optional[str] = None
    house_system: Optional[str] = None
    chart_style: Optional[str] = None
    language: Optional[str] = None
    theme: Optional[str] = None
    custom_settings: Optional[Dict[str, Any]] = None


# Define dependency for use case
async def get_manage_user_profile_use_case() -> ManageUserProfileUseCase:
    """
    Dependency for the manage user profile use case.
    
    Returns:
        ManageUserProfileUseCase: The use case instance
    """
    return ManageUserProfileUseCase(user_profile_repository=user_profile_repository)


@router.post("/", response_model=UserProfileResponse)
async def create_user_profile(
    request: UserProfileRequest,
    use_case: ManageUserProfileUseCase = Depends(get_manage_user_profile_use_case)
):
    """
    Create a new user profile.
    
    Args:
        request: The user profile data
        use_case: The use case instance
        
    Returns:
        UserProfileResponse: The created user profile
    """
    try:
        # Create preferences if provided
        preferences = UserPreferences(**request.preferences) if request.preferences else None
        
        # Execute the use case
        profile = await use_case.create_profile(
            username=request.username,
            email=request.email,
            preferences=preferences
        )
        
        # Convert to response model
        return UserProfileResponse(
            id=profile.id,
            username=profile.username,
            email=profile.email,
            created_at=profile.created_at.isoformat(),
            last_login=profile.last_login.isoformat() if profile.last_login else None,
            preferences=profile.preferences.dict() if profile.preferences else {},
            saved_locations=[location.dict() for location in profile.saved_locations],
            saved_people=[person.dict() for person in profile.saved_people],
            recent_calculations=profile.recent_calculations,
            is_active=profile.is_active,
            is_verified=profile.is_verified,
            roles=profile.roles
        )
    
    except Exception as e:
        logger.error(f"Error creating user profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating user profile: {str(e)}")


@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(
    user_id: str = Path(..., description="The ID of the user profile to retrieve"),
    use_case: ManageUserProfileUseCase = Depends(get_manage_user_profile_use_case)
):
    """
    Get a user profile by ID.
    
    Args:
        user_id: The ID of the user profile to retrieve
        use_case: The use case instance
        
    Returns:
        UserProfileResponse: The user profile
    """
    try:
        # Execute the use case
        profile = await use_case.get_profile_by_id(user_id=user_id)
        
        if not profile:
            raise HTTPException(status_code=404, detail=f"User profile with ID {user_id} not found")
        
        # Convert to response model
        return UserProfileResponse(
            id=profile.id,
            username=profile.username,
            email=profile.email,
            created_at=profile.created_at.isoformat(),
            last_login=profile.last_login.isoformat() if profile.last_login else None,
            preferences=profile.preferences.dict() if profile.preferences else {},
            saved_locations=[location.dict() for location in profile.saved_locations],
            saved_people=[person.dict() for person in profile.saved_people],
            recent_calculations=profile.recent_calculations,
            is_active=profile.is_active,
            is_verified=profile.is_verified,
            roles=profile.roles
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving user profile: {str(e)}")


@router.put("/{user_id}/preferences", response_model=UserProfileResponse)
async def update_user_preferences(
    request: UserPreferencesRequest,
    user_id: str = Path(..., description="The ID of the user profile to update"),
    use_case: ManageUserProfileUseCase = Depends(get_manage_user_profile_use_case)
):
    """
    Update user preferences.
    
    Args:
        request: The preferences data
        user_id: The ID of the user profile to update
        use_case: The use case instance
        
    Returns:
        UserProfileResponse: The updated user profile
    """
    try:
        # Execute the use case
        profile = await use_case.update_preferences(
            user_id=user_id,
            preferences=request.dict(exclude_unset=True)
        )
        
        if not profile:
            raise HTTPException(status_code=404, detail=f"User profile with ID {user_id} not found")
        
        # Convert to response model
        return UserProfileResponse(
            id=profile.id,
            username=profile.username,
            email=profile.email,
            created_at=profile.created_at.isoformat(),
            last_login=profile.last_login.isoformat() if profile.last_login else None,
            preferences=profile.preferences.dict() if profile.preferences else {},
            saved_locations=[location.dict() for location in profile.saved_locations],
            saved_people=[person.dict() for person in profile.saved_people],
            recent_calculations=profile.recent_calculations,
            is_active=profile.is_active,
            is_verified=profile.is_verified,
            roles=profile.roles
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user preferences: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating user preferences: {str(e)}")


@router.post("/{user_id}/locations", response_model=UserProfileResponse)
async def add_saved_location(
    request: SavedLocationRequest,
    user_id: str = Path(..., description="The ID of the user profile to update"),
    use_case: ManageUserProfileUseCase = Depends(get_manage_user_profile_use_case)
):
    """
    Add a saved location to a user profile.
    
    Args:
        request: The location data
        user_id: The ID of the user profile to update
        use_case: The use case instance
        
    Returns:
        UserProfileResponse: The updated user profile
    """
    try:
        # Create location entity
        location = SavedLocation(
            name=request.name,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone=request.timezone,
            notes=request.notes
        )
        
        # Execute the use case
        profile = await use_case.add_saved_location(
            user_id=user_id,
            location=location
        )
        
        if not profile:
            raise HTTPException(status_code=404, detail=f"User profile with ID {user_id} not found")
        
        # Convert to response model
        return UserProfileResponse(
            id=profile.id,
            username=profile.username,
            email=profile.email,
            created_at=profile.created_at.isoformat(),
            last_login=profile.last_login.isoformat() if profile.last_login else None,
            preferences=profile.preferences.dict() if profile.preferences else {},
            saved_locations=[location.dict() for location in profile.saved_locations],
            saved_people=[person.dict() for person in profile.saved_people],
            recent_calculations=profile.recent_calculations,
            is_active=profile.is_active,
            is_verified=profile.is_verified,
            roles=profile.roles
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding saved location: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding saved location: {str(e)}")


@router.post("/{user_id}/people", response_model=UserProfileResponse)
async def add_saved_person(
    request: SavedPersonRequest,
    user_id: str = Path(..., description="The ID of the user profile to update"),
    use_case: ManageUserProfileUseCase = Depends(get_manage_user_profile_use_case)
):
    """
    Add a saved person to a user profile.
    
    Args:
        request: The person data
        user_id: The ID of the user profile to update
        use_case: The use case instance
        
    Returns:
        UserProfileResponse: The updated user profile
    """
    try:
        # Create person entity
        person = SavedPerson(
            name=request.name,
            date_of_birth=request.date_of_birth,
            time_of_birth=request.time_of_birth,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone=request.timezone,
            gender=request.gender,
            notes=request.notes
        )
        
        # Execute the use case
        profile = await use_case.add_saved_person(
            user_id=user_id,
            person=person
        )
        
        if not profile:
            raise HTTPException(status_code=404, detail=f"User profile with ID {user_id} not found")
        
        # Convert to response model
        return UserProfileResponse(
            id=profile.id,
            username=profile.username,
            email=profile.email,
            created_at=profile.created_at.isoformat(),
            last_login=profile.last_login.isoformat() if profile.last_login else None,
            preferences=profile.preferences.dict() if profile.preferences else {},
            saved_locations=[location.dict() for location in profile.saved_locations],
            saved_people=[person.dict() for person in profile.saved_people],
            recent_calculations=profile.recent_calculations,
            is_active=profile.is_active,
            is_verified=profile.is_verified,
            roles=profile.roles
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding saved person: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding saved person: {str(e)}")


@router.post("/{user_id}/calculations/{calculation_id}", response_model=UserProfileResponse)
async def add_recent_calculation(
    user_id: str = Path(..., description="The ID of the user profile to update"),
    calculation_id: str = Path(..., description="The ID of the calculation to add"),
    use_case: ManageUserProfileUseCase = Depends(get_manage_user_profile_use_case)
):
    """
    Add a calculation ID to a user's recent calculations.
    
    Args:
        user_id: The ID of the user profile to update
        calculation_id: The ID of the calculation to add
        use_case: The use case instance
        
    Returns:
        UserProfileResponse: The updated user profile
    """
    try:
        # Execute the use case
        profile = await use_case.add_recent_calculation(
            user_id=user_id,
            calculation_id=calculation_id
        )
        
        if not profile:
            raise HTTPException(status_code=404, detail=f"User profile with ID {user_id} not found")
        
        # Convert to response model
        return UserProfileResponse(
            id=profile.id,
            username=profile.username,
            email=profile.email,
            created_at=profile.created_at.isoformat(),
            last_login=profile.last_login.isoformat() if profile.last_login else None,
            preferences=profile.preferences.dict() if profile.preferences else {},
            saved_locations=[location.dict() for location in profile.saved_locations],
            saved_people=[person.dict() for person in profile.saved_people],
            recent_calculations=profile.recent_calculations,
            is_active=profile.is_active,
            is_verified=profile.is_verified,
            roles=profile.roles
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding recent calculation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding recent calculation: {str(e)}")


@router.delete("/{user_id}", response_model=dict)
async def delete_user_profile(
    user_id: str = Path(..., description="The ID of the user profile to delete"),
    use_case: ManageUserProfileUseCase = Depends(get_manage_user_profile_use_case)
):
    """
    Delete a user profile.
    
    Args:
        user_id: The ID of the user profile to delete
        use_case: The use case instance
        
    Returns:
        dict: A success message
    """
    try:
        # Execute the use case
        success = await use_case.delete_profile(user_id=user_id)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"User profile with ID {user_id} not found")
        
        return {"message": f"User profile with ID {user_id} deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting user profile: {str(e)}")
