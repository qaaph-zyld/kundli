"""
Birth Chart Routes
This module defines the API routes for birth chart operations.
"""
from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from ...core.use_cases.calculate_birth_chart import CalculateBirthChartUseCase
from ...infrastructure.astro.calculator_service import calculator_service
from ...infrastructure.repositories import birth_chart_repository


# Define request and response models
class BirthChartRequest(BaseModel):
    """Request model for birth chart calculation."""
    date: str
    time: str
    latitude: float
    longitude: float
    timezone: str
    ayanamsa: str = "Lahiri"
    house_system: str = "Placidus"
    calculation_options: Optional[Dict[str, Any]] = None


class BirthChartResponse(BaseModel):
    """Response model for birth chart calculation."""
    chart_id: Optional[str] = None
    date_time: str
    latitude: float
    longitude: float
    timezone: str
    ayanamsa: str
    house_system: str
    ascendant: Optional[float] = None
    planets: Dict[str, Any]
    houses: Dict[str, Any]
    aspects: Optional[list] = None
    calculation_system: str
    calculation_time: float
    calculation_validation: Optional[Dict[str, Any]] = None


# Create router
router = APIRouter(
    prefix="/birth-charts",
    tags=["birth-charts"],
    responses={404: {"description": "Not found"}},
)


# Define dependency for use case
async def get_calculate_birth_chart_use_case() -> CalculateBirthChartUseCase:
    """
    Dependency for the calculate birth chart use case.
    
    Returns:
        CalculateBirthChartUseCase: The use case instance
    """
    # In a real implementation, we would use proper dependency injection
    # For now, we use the singleton repository instance
    return CalculateBirthChartUseCase(
        birth_chart_repository=birth_chart_repository,
        calculator_service=calculator_service
    )


@router.post("/", response_model=BirthChartResponse)
async def calculate_birth_chart(
    request: BirthChartRequest,
    use_case: CalculateBirthChartUseCase = Depends(get_calculate_birth_chart_use_case),
    user_id: Optional[str] = Query(None, description="Optional user ID to associate with the chart")
):
    """
    Calculate a birth chart.
    
    Args:
        request: The birth chart request
        use_case: The calculate birth chart use case
        
    Returns:
        BirthChartResponse: The calculated birth chart
    """
    try:
        # Parse date and time
        date_time = datetime.fromisoformat(f"{request.date}T{request.time}")
        
        # Execute the use case
        birth_chart = await use_case.execute(
            date_time=date_time,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone=request.timezone,
            ayanamsa=request.ayanamsa,
            house_system=request.house_system,
            user_id=user_id,
            calculation_options=request.calculation_options
        )
        
        # Convert to response model
        response = BirthChartResponse(
            date_time=birth_chart.date_time.isoformat(),
            latitude=birth_chart.latitude,
            longitude=birth_chart.longitude,
            timezone=birth_chart.timezone,
            ayanamsa=birth_chart.ayanamsa,
            house_system=birth_chart.house_system,
            ascendant=birth_chart.ascendant,
            planets=birth_chart.planets,
            houses=birth_chart.houses,
            aspects=[aspect.dict() for aspect in birth_chart.aspects] if birth_chart.aspects else [],
            calculation_system=birth_chart.calculation_system,
            calculation_time=birth_chart.calculation_time
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate birth chart: {str(e)}"
        )


@router.get("/config", response_model=Dict[str, Any])
async def get_calculator_config():
    """
    Get calculator configuration and metrics.
    
    Returns:
        Dict[str, Any]: Calculator configuration and metrics
    """
    try:
        metrics = calculator_service.get_metrics()
        
        return {
            "metrics": metrics,
            "performance_profile": metrics.get("performance_profile", "balanced")
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get calculator configuration: {str(e)}"
        )


@router.post("/config", response_model=Dict[str, Any])
async def set_calculator_config(profile: str = Query(..., description="Performance profile")):
    """
    Set calculator configuration.
    
    Args:
        profile: Performance profile to set
        
    Returns:
        Dict[str, Any]: Updated calculator configuration
    """
    try:
        success = calculator_service.set_performance_profile(profile)
        
        if not success:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid performance profile: {profile}"
            )
        
        return {
            "status": "success",
            "message": f"Set performance profile to {profile}",
            "performance_profile": profile
        }
        
    except HTTPException:
        raise
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to set calculator configuration: {str(e)}"
        )
