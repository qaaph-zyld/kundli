"""
Dasha Timeline Generator
This module provides functionality for generating dasha timelines for visualization.
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from ...core.entities.dasha import DashaNode, DashaTimeline, DashaLevel
from ...core.entities.birth_chart import BirthChart

# Configure logging
logger = logging.getLogger(__name__)


class DashaTimelineGenerator:
    """Class for generating dasha timelines for visualization."""
    
    def __init__(self):
        """Initialize the dasha timeline generator."""
        logger.info("Initialized dasha timeline generator")
    
    def generate_timeline(self, dasha_tree: List[DashaNode], birth_chart: BirthChart) -> DashaTimeline:
        """
        Generate dasha timeline for visualization.
        
        Args:
            dasha_tree: The dasha tree
            birth_chart: The birth chart
            
        Returns:
            DashaTimeline: The dasha timeline
        """
        logger.info(f"Generating dasha timeline for birth chart {birth_chart.id}")
        
        # Get birth date
        birth_date = datetime.fromisoformat(birth_chart.date_time.replace('Z', '+00:00'))
        
        # Get current date
        current_date = datetime.utcnow()
        
        # Calculate timeline start date (1 year before birth or earliest dasha start)
        timeline_start = birth_date - timedelta(days=365)
        for mahadasha in dasha_tree:
            if mahadasha.start_date < timeline_start:
                timeline_start = mahadasha.start_date
        
        # Calculate timeline end date (120 years after birth or latest dasha end)
        timeline_end = birth_date + timedelta(days=120*365)
        for mahadasha in dasha_tree:
            if mahadasha.end_date > timeline_end:
                timeline_end = mahadasha.end_date
        
        # Generate timeline periods
        timeline_periods = self._generate_timeline_periods(dasha_tree, current_date)
        
        # Generate significant periods
        significant_periods = self._generate_significant_periods(dasha_tree, birth_chart, current_date)
        
        # Generate upcoming transitions
        upcoming_transitions = self._generate_upcoming_transitions(dasha_tree, current_date)
        
        return DashaTimeline(
            start_date=timeline_start,
            end_date=timeline_end,
            current_date=current_date,
            periods=timeline_periods,
            significant_periods=significant_periods,
            upcoming_transitions=upcoming_transitions
        )
    
    def _generate_timeline_periods(self, dasha_tree: List[DashaNode], current_date: datetime) -> List[Dict[str, Any]]:
        """
        Generate timeline periods.
        
        Args:
            dasha_tree: The dasha tree
            current_date: The current date
            
        Returns:
            List[Dict[str, Any]]: Timeline periods
        """
        # Initialize periods
        periods = []
        
        # Process each mahadasha
        for mahadasha in dasha_tree:
            # Add mahadasha period
            periods.append({
                "level": 1,
                "planet": mahadasha.planet,
                "start_date": mahadasha.start_date,
                "end_date": mahadasha.end_date,
                "duration_years": mahadasha.duration_years,
                "is_current": mahadasha.start_date <= current_date <= mahadasha.end_date
            })
            
            # Process each antardasha
            for antardasha in mahadasha.children:
                # Add antardasha period
                periods.append({
                    "level": 2,
                    "planet": antardasha.planet,
                    "parent_planet": mahadasha.planet,
                    "start_date": antardasha.start_date,
                    "end_date": antardasha.end_date,
                    "duration_years": antardasha.duration_years,
                    "is_current": antardasha.start_date <= current_date <= antardasha.end_date
                })
                
                # Process each pratyantardasha
                for pratyantardasha in antardasha.children:
                    # Add pratyantardasha period
                    periods.append({
                        "level": 3,
                        "planet": pratyantardasha.planet,
                        "parent_planet": antardasha.planet,
                        "grand_parent_planet": mahadasha.planet,
                        "start_date": pratyantardasha.start_date,
                        "end_date": pratyantardasha.end_date,
                        "duration_years": pratyantardasha.duration_years,
                        "is_current": pratyantardasha.start_date <= current_date <= pratyantardasha.end_date
                    })
        
        return periods
    
    def _generate_significant_periods(self, dasha_tree: List[DashaNode], birth_chart: BirthChart, current_date: datetime) -> List[Dict[str, Any]]:
        """
        Generate significant periods.
        
        Args:
            dasha_tree: The dasha tree
            birth_chart: The birth chart
            current_date: The current date
            
        Returns:
            List[Dict[str, Any]]: Significant periods
        """
        # Initialize periods
        periods = []
        
        # Get benefic and malefic planets based on ascendant
        benefics, malefics = self._get_benefic_malefic_planets(birth_chart)
        
        # Process each mahadasha
        for mahadasha in dasha_tree:
            # Skip mahadashas that ended before current date
            if mahadasha.end_date < current_date:
                continue
            
            # Check if mahadasha planet is benefic or malefic
            is_benefic = mahadasha.planet in benefics
            is_malefic = mahadasha.planet in malefics
            
            # If benefic, add as significant positive period
            if is_benefic:
                periods.append({
                    "type": "positive",
                    "level": 1,
                    "planet": mahadasha.planet,
                    "start_date": mahadasha.start_date,
                    "end_date": mahadasha.end_date,
                    "description": f"Positive {mahadasha.planet} Mahadasha period"
                })
            
            # If malefic, add as significant challenging period
            if is_malefic:
                periods.append({
                    "type": "challenging",
                    "level": 1,
                    "planet": mahadasha.planet,
                    "start_date": mahadasha.start_date,
                    "end_date": mahadasha.end_date,
                    "description": f"Challenging {mahadasha.planet} Mahadasha period"
                })
            
            # Process each antardasha
            for antardasha in mahadasha.children:
                # Skip antardashas that ended before current date
                if antardasha.end_date < current_date:
                    continue
                
                # Check if antardasha planet is benefic or malefic
                is_benefic = antardasha.planet in benefics
                is_malefic = antardasha.planet in malefics
                
                # Check for benefic-benefic or malefic-malefic combinations
                if is_benefic and mahadasha.planet in benefics:
                    periods.append({
                        "type": "very_positive",
                        "level": 2,
                        "planet": antardasha.planet,
                        "parent_planet": mahadasha.planet,
                        "start_date": antardasha.start_date,
                        "end_date": antardasha.end_date,
                        "description": f"Very positive {antardasha.planet} Antardasha in {mahadasha.planet} Mahadasha"
                    })
                elif is_malefic and mahadasha.planet in malefics:
                    periods.append({
                        "type": "very_challenging",
                        "level": 2,
                        "planet": antardasha.planet,
                        "parent_planet": mahadasha.planet,
                        "start_date": antardasha.start_date,
                        "end_date": antardasha.end_date,
                        "description": f"Very challenging {antardasha.planet} Antardasha in {mahadasha.planet} Mahadasha"
                    })
        
        return periods
    
    def _generate_upcoming_transitions(self, dasha_tree: List[DashaNode], current_date: datetime) -> List[Dict[str, Any]]:
        """
        Generate upcoming transitions.
        
        Args:
            dasha_tree: The dasha tree
            current_date: The current date
            
        Returns:
            List[Dict[str, Any]]: Upcoming transitions
        """
        # Initialize transitions
        transitions = []
        
        # Process each mahadasha
        for mahadasha in dasha_tree:
            # Check if mahadasha starts in the future
            if mahadasha.start_date > current_date:
                # Add mahadasha transition
                transitions.append({
                    "level": 1,
                    "planet": mahadasha.planet,
                    "date": mahadasha.start_date,
                    "description": f"Beginning of {mahadasha.planet} Mahadasha"
                })
            
            # Process each antardasha
            for antardasha in mahadasha.children:
                # Check if antardasha starts in the future
                if antardasha.start_date > current_date:
                    # Add antardasha transition
                    transitions.append({
                        "level": 2,
                        "planet": antardasha.planet,
                        "parent_planet": mahadasha.planet,
                        "date": antardasha.start_date,
                        "description": f"Beginning of {antardasha.planet} Antardasha in {mahadasha.planet} Mahadasha"
                    })
                
                # Process each pratyantardasha
                for pratyantardasha in antardasha.children:
                    # Check if pratyantardasha starts in the future
                    if pratyantardasha.start_date > current_date:
                        # Add pratyantardasha transition
                        transitions.append({
                            "level": 3,
                            "planet": pratyantardasha.planet,
                            "parent_planet": antardasha.planet,
                            "grand_parent_planet": mahadasha.planet,
                            "date": pratyantardasha.start_date,
                            "description": f"Beginning of {pratyantardasha.planet} Pratyantardasha in {antardasha.planet} Antardasha"
                        })
        
        # Sort transitions by date
        transitions.sort(key=lambda x: x["date"])
        
        # Limit to next 10 transitions
        return transitions[:10]
    
    def _get_benefic_malefic_planets(self, birth_chart: BirthChart) -> tuple:
        """
        Get benefic and malefic planets based on ascendant.
        
        Args:
            birth_chart: The birth chart
            
        Returns:
            tuple: (benefics, malefics)
        """
        # Get ascendant sign
        ascendant_sign = birth_chart.ascendant.get("sign", "Ar")
        
        # Default benefics and malefics
        default_benefics = ["Ju", "Ve", "Mo"]
        default_malefics = ["Sa", "Ma", "Ra", "Ke"]
        
        # Natural benefics and malefics
        benefics = default_benefics.copy()
        malefics = default_malefics.copy()
        
        # Adjust based on ascendant
        if ascendant_sign in ["Ta", "Li"]:
            # Venus-ruled signs
            if "Sa" in malefics:
                malefics.remove("Sa")
                benefics.append("Sa")
        elif ascendant_sign in ["Ge", "Vi"]:
            # Mercury-ruled signs
            if "Ve" in benefics:
                benefics.remove("Ve")
                malefics.append("Ve")
        elif ascendant_sign in ["Cn"]:
            # Moon-ruled signs
            if "Sa" in malefics:
                malefics.remove("Sa")
                benefics.append("Sa")
        elif ascendant_sign in ["Le"]:
            # Sun-ruled signs
            if "Ju" in benefics:
                benefics.remove("Ju")
                malefics.append("Ju")
        elif ascendant_sign in ["Sc"]:
            # Mars-ruled signs
            if "Mo" in benefics:
                benefics.remove("Mo")
                malefics.append("Mo")
        elif ascendant_sign in ["Sg", "Pi"]:
            # Jupiter-ruled signs
            if "Mo" in benefics:
                benefics.remove("Mo")
                malefics.append("Mo")
        elif ascendant_sign in ["Cp", "Aq"]:
            # Saturn-ruled signs
            if "Ve" in benefics:
                benefics.remove("Ve")
                malefics.append("Ve")
        
        return benefics, malefics
