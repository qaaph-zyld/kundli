"""
Database Models
This module defines SQLAlchemy models for database entities.
"""
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class BirthChartModel(Base):
    """SQLAlchemy model for birth charts."""
    __tablename__ = "birth_charts"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("user_profiles.id"), nullable=True)
    
    # Birth data
    date_time = Column(DateTime, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timezone = Column(String(50), nullable=False)
    
    # Chart data
    ayanamsa = Column(String(50), default="Lahiri")
    house_system = Column(String(50), default="Placidus")
    ascendant = Column(Float, nullable=True)
    
    # JSON data
    planets = Column(JSON, default=dict)
    houses = Column(JSON, default=dict)
    aspects = Column(JSON, default=list)
    divisional_charts = Column(JSON, default=dict)
    dashas = Column(JSON, default=dict)
    yogas = Column(JSON, default=list)
    
    # Calculation metadata
    calculation_system = Column(String(50), default="")
    calculation_time = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("UserProfileModel", back_populates="birth_charts")


class UserProfileModel(Base):
    """SQLAlchemy model for user profiles."""
    __tablename__ = "user_profiles"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    # User metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # User data
    preferences = Column(JSON, default=dict)
    saved_locations = Column(JSON, default=list)
    saved_people = Column(JSON, default=list)
    recent_calculations = Column(JSON, default=list)
    
    # User permissions
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    roles = Column(JSON, default=list)
    
    # Relationships
    birth_charts = relationship("BirthChartModel", back_populates="user")


class AstronomicalCalculationMetricsModel(Base):
    """SQLAlchemy model for astronomical calculation metrics."""
    __tablename__ = "astronomical_calculation_metrics"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    calculator_name = Column(String(50), nullable=False)
    calculation_type = Column(String(50), nullable=False)
    execution_time = Column(Float, default=0.0)
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Additional data
    input_parameters = Column(JSON, default=dict)
    result_summary = Column(JSON, default=dict)
