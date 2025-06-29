"""
Transit Routes
This module defines the API routes for transit calculations.
"""
import logging
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from ...core.entities.transit import Transit
from ...core.use_cases.calculate_transits import CalculateTransitsUseCase
from ...infrastructure.repositories.transit_repository import TransitRepository
from ...infrastructure.repositories.birth_chart_repository import BirthChartRepository
from ...infrastructure.astro.calculator_service import calculator_service
from ...infrastructure.repositories import repository_factory

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/transits", tags=["transits"])


# Request and response models
class CalculateTransitRequest(BaseModel):
    """Request model for transit calculation."""
    birth_chart_id: str
    transit_date: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "birth_chart_id": "birth-chart-12345",
                "transit_date": "2025-07-01T00:00:00Z"
            }
        }


class CalculateTransitTimelineRequest(BaseModel):
    """Request model for transit timeline calculation."""
    birth_chart_id: str
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: Optional[datetime] = None
    step_days: int = 1
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "birth_chart_id": "birth-chart-12345",
                "start_date": "2025-07-01T00:00:00Z",
                "end_date": "2025-12-31T00:00:00Z",
                "step_days": 1
            }
        }


# Dependency injection
async def get_transit_use_case() -> CalculateTransitsUseCase:
    """
    Get the transit use case.
    
    Returns:
        CalculateTransitsUseCase: Transit use case
    """
    transit_repository = repository_factory.get_repository(TransitRepository)
    birth_chart_repository = repository_factory.get_repository(BirthChartRepository)
    
    return CalculateTransitsUseCase(
        transit_repository=transit_repository,
        birth_chart_repository=birth_chart_repository,
        calculator_service=calculator_service
    )


@router.post("/calculate", response_model=Transit, status_code=201)
async def calculate_transit(
    request: CalculateTransitRequest,
    transit_use_case: CalculateTransitsUseCase = Depends(get_transit_use_case)
):
    """
    Calculate transit for a specific date.
    
    Args:
        request: Transit calculation request
        transit_use_case: Transit use case
        
    Returns:
        Transit: Calculated transit
    """
    try:
        transit = await transit_use_case.calculate_transit(
            birth_chart_id=request.birth_chart_id,
            transit_date=request.transit_date
        )
        
        return transit
    except ValueError as e:
        logger.error(f"Error calculating transit: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error calculating transit: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error calculating transit: {str(e)}")


@router.post("/calculate-timeline", response_model=Transit, status_code=201)
async def calculate_transit_timeline(
    request: CalculateTransitTimelineRequest,
    transit_use_case: CalculateTransitsUseCase = Depends(get_transit_use_case)
):
    """
    Calculate transit timeline for a date range.
    
    Args:
        request: Transit timeline calculation request
        transit_use_case: Transit use case
        
    Returns:
        Transit: Transit with timeline data
    """
    try:
        # Set default end date if not provided (6 months from start date)
        end_date = request.end_date or request.start_date + timedelta(days=180)
        
        transit = await transit_use_case.calculate_transit_timeline(
            birth_chart_id=request.birth_chart_id,
            start_date=request.start_date,
            end_date=end_date,
            step_days=request.step_days
        )
        
        return transit
    except ValueError as e:
        logger.error(f"Error calculating transit timeline: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error calculating transit timeline: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error calculating transit timeline: {str(e)}")


@router.get("/{transit_id}", response_model=Transit)
async def get_transit(
    transit_id: str,
    transit_use_case: CalculateTransitsUseCase = Depends(get_transit_use_case)
):
    """
    Get a transit by ID.
    
    Args:
        transit_id: ID of the transit
        transit_use_case: Transit use case
        
    Returns:
        Transit: Transit data
    """
    transit = await transit_use_case.get_transit(transit_id)
    
    if not transit:
        raise HTTPException(status_code=404, detail=f"Transit with ID {transit_id} not found")
    
    return transit


@router.get("/birth-chart/{birth_chart_id}", response_model=List[Transit])
async def get_transits_for_birth_chart(
    birth_chart_id: str,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    transit_use_case: CalculateTransitsUseCase = Depends(get_transit_use_case)
):
    """
    Get transits for a birth chart.
    
    Args:
        birth_chart_id: ID of the birth chart
        limit: Maximum number of transits to return
        offset: Number of transits to skip
        transit_use_case: Transit use case
        
    Returns:
        List[Transit]: List of transits
    """
    transits = await transit_use_case.get_transits_for_birth_chart(
        birth_chart_id=birth_chart_id,
        limit=limit,
        offset=offset
    )
    
    return transits


@router.get("/birth-chart/{birth_chart_id}/date-range", response_model=List[Transit])
async def get_transits_by_date_range(
    birth_chart_id: str,
    start_date: datetime,
    end_date: datetime,
    transit_use_case: CalculateTransitsUseCase = Depends(get_transit_use_case)
):
    """
    Get transits for a birth chart within a date range.
    
    Args:
        birth_chart_id: ID of the birth chart
        start_date: Start date of the range
        end_date: End date of the range
        transit_use_case: Transit use case
        
    Returns:
        List[Transit]: List of transits
    """
    transits = await transit_use_case.get_transits_by_date_range(
        birth_chart_id=birth_chart_id,
        start_date=start_date,
        end_date=end_date
    )
    
    return transits


@router.delete("/{transit_id}", status_code=204)
async def delete_transit(
    transit_id: str,
    transit_use_case: CalculateTransitsUseCase = Depends(get_transit_use_case)
):
    """
    Delete a transit.
    
    Args:
        transit_id: ID of the transit to delete
        transit_use_case: Transit use case
    """
    deleted = await transit_use_case.delete_transit(transit_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Transit with ID {transit_id} not found")
