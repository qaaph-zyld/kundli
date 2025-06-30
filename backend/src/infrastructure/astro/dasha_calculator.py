"""
Dasha Calculator Service
This module provides functionality for calculating dashas (planetary periods) in Vedic astrology.
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple

from ...core.entities.dasha import (
    DashaAnalysis, DashaLevel, DashaNode, DashaPhala, 
    DashaSystem, DashaTimeline
)
from ...core.entities.birth_chart import BirthChart
from .vimshottari_dasha import VimshottariDasha
from .yogini_dasha import YoginiDasha
from .dasha_phala_generator import DashaPhalagenerator
from .dasha_timeline_generator import DashaTimelineGenerator

# Configure logging
logger = logging.getLogger(__name__)


class DashaCalculator:
    """Service for calculating dashas (planetary periods) in Vedic astrology."""
    
    def __init__(self, calculator_service=None):
        """
        Initialize the dasha calculator.
        
        Args:
            calculator_service: Optional calculator service for astronomical calculations
        """
        self.calculator_service = calculator_service
        logger.info("Initialized dasha calculator")
        self.phala_generator = DashaPhalagenerator()
        self.timeline_generator = DashaTimelineGenerator()
        
        # Define dasha systems
        self.dasha_systems = {
            "vimshottari": {
                "name": "Vimshottari",
                "description": "The most commonly used dasha system in Vedic astrology.",
                "levels": 5,  # Maha, Antar, Pratyantar, Sookshma, Prana
                "total_years": 120.0,
                "planet_order": ["Ke", "Ve", "Su", "Mo", "Ma", "Ra", "Ju", "Sa", "Me"],
                "planet_years": {"Ke": 7, "Ve": 20, "Su": 6, "Mo": 10, "Ma": 7, "Ra": 18, "Ju": 16, "Sa": 19, "Me": 17}
            },
            "yogini": {
                "name": "Yogini",
                "description": "An 8-year cycle dasha system related to the Yogini goddesses.",
                "levels": 3,  # Maha, Antar, Pratyantar
                "total_years": 36.0,
                "planet_order": ["Ma", "Me", "Sa", "Mo", "Ve", "Su", "Ra", "Ju"],
                "planet_years": {"Ma": 1, "Me": 2, "Sa": 3, "Mo": 4, "Ve": 5, "Su": 6, "Ra": 7, "Ju": 8}
            },
            "jaimini": {
                "name": "Jaimini Chara",
                "description": "A dasha system based on Jaimini astrology principles.",
                "levels": 3,  # Maha, Antar, Pratyantar
                "total_years": 120.0,
                "planet_order": ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"],
                "planet_years": {
                    "Ar": 10, "Ta": 10, "Ge": 10, "Cn": 10, "Le": 10, "Vi": 10,
                    "Li": 10, "Sc": 10, "Sg": 10, "Cp": 10, "Aq": 10, "Pi": 10
                }
            }
        }
    
    def calculate_dasha(self, birth_chart: BirthChart, dasha_system: str = "vimshottari") -> DashaAnalysis:
        """
        Calculate dasha for a birth chart.
        
        Args:
            birth_chart: The birth chart
            dasha_system: The dasha system to use
            
        Returns:
            DashaAnalysis: The dasha analysis
        """
        logger.info(f"Calculating {dasha_system} dasha for birth chart {birth_chart.id}")
        
        # Validate dasha system
        if dasha_system not in self.dasha_systems:
            logger.error(f"Invalid dasha system: {dasha_system}")
            raise ValueError(f"Invalid dasha system: {dasha_system}")
        
        # Record start time for execution time calculation
        start_time = datetime.now()
        
        # Calculate dasha based on system
        if dasha_system == "vimshottari":
            dasha_tree, current_levels = self._calculate_vimshottari_dasha(birth_chart)
        elif dasha_system == "yogini":
            dasha_tree, current_levels = self._calculate_yogini_dasha(birth_chart)
        elif dasha_system == "jaimini":
            dasha_tree, current_levels = self._calculate_jaimini_dasha(birth_chart)
        else:
            # This should never happen due to validation above
            logger.error(f"Unsupported dasha system: {dasha_system}")
            raise ValueError(f"Unsupported dasha system: {dasha_system}")
        
        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Create dasha system info
        system_info = DashaSystem(
            name=self.dasha_systems[dasha_system]["name"],
            description=self.dasha_systems[dasha_system]["description"],
            levels=self.dasha_systems[dasha_system]["levels"],
            total_years=self.dasha_systems[dasha_system]["total_years"]
        )
        
        # Extract current levels
        current_mahadasha = current_levels.get("mahadasha")
        current_antardasha = current_levels.get("antardasha")
        current_pratyantardasha = current_levels.get("pratyantardasha")
        
        # Generate dasha phala (effects)
        current_dasha_phala = self._generate_phala(dasha_tree, birth_chart)
        
        # Generate timeline
        timeline = self._generate_dasha_timeline(birth_chart, dasha_tree, dasha_system)
        
        # Generate upcoming significant periods
        upcoming_periods = self._generate_upcoming_significant_periods(birth_chart, dasha_tree)
        
        # Create dasha analysis
        dasha_analysis = DashaAnalysis(
            id=f"dasha-{birth_chart.id}-{dasha_system}",
            birth_chart_id=birth_chart.id,
            calculation_time=datetime.utcnow(),
            calculation_system=birth_chart.calculation_system,
            execution_time=execution_time,
            dasha_system=dasha_system,
            current_mahadasha=current_mahadasha,
            current_antardasha=current_antardasha,
            current_pratyantardasha=current_pratyantardasha,
            dasha_tree=dasha_tree,
            timeline=timeline,
            current_dasha_phala=current_dasha_phala,
            upcoming_significant_periods=upcoming_periods
        )
        
        logger.info(f"Calculated {dasha_system} dasha for birth chart {birth_chart.id} in {execution_time:.2f} seconds")
        return dasha_analysis
    
    def _calculate_vimshottari_dasha(self, birth_chart: BirthChart) -> Tuple[List[DashaNode], Dict[str, DashaLevel]]:
        """
        Calculate Vimshottari dasha for a birth chart.
        
        Args:
            birth_chart: The birth chart
            
        Returns:
            Tuple[List[DashaNode], Dict[str, DashaLevel]]: The dasha tree and current levels
        """
        logger.info(f"Calculating Vimshottari dasha for birth chart {birth_chart.id}")
        
        # Use the VimshottariDasha class for calculations
        vimshottari_calculator = VimshottariDasha()
        return vimshottari_calculator.calculate(birth_chart)
    
    def _calculate_yogini_dasha(self, birth_chart: BirthChart) -> Tuple[List[DashaNode], Dict[str, DashaLevel]]:
        """
        Calculate Yogini dasha for a birth chart.
        
        Args:
            birth_chart: The birth chart
            
        Returns:
            Tuple[List[DashaNode], Dict[str, DashaLevel]]: The dasha tree and current levels
        """
        logger.info(f"Calculating Yogini dasha for birth chart {birth_chart.id}")
        
        # Use the YoginiDasha class for calculations
        yogini_calculator = YoginiDasha()
        return yogini_calculator.calculate(birth_chart)
    
    def _calculate_jaimini_dasha(self, birth_chart: BirthChart) -> Tuple[List[DashaNode], Dict[str, DashaLevel]]:
        """
        Calculate Jaimini Chara dasha for a birth chart.
        
        Args:
            birth_chart: The birth chart
            
        Returns:
            Tuple[List[DashaNode], Dict[str, DashaLevel]]: The dasha tree and current levels
        """
        logger.info(f"Calculating Jaimini Chara dasha for birth chart {birth_chart.id}")
        
        # Placeholder implementation - will be expanded in future steps
        # This will be replaced with actual Jaimini dasha calculation logic
        
        # For now, return empty tree and levels
        return [], {}
    
    def _generate_phala(self, dasha_tree: List[DashaNode], birth_chart: BirthChart) -> List[DashaPhala]:
        """
        Generate dasha phala (effects) for dasha tree.
        
        Args:
            dasha_tree: The dasha tree
            birth_chart: The birth chart
            
        Returns:
            List[DashaPhala]: The dasha phala (effects)
        """
        logger.info(f"Generating dasha phala for birth chart {birth_chart.id}")
        
        # Use the phala generator to generate effects for each node
        phala_list = []
        
        # Process each mahadasha
        for mahadasha in dasha_tree:
            # Generate phala for mahadasha
            mahadasha_phala = self.phala_generator.generate_phala(mahadasha, birth_chart)
            phala_list.append(mahadasha_phala)
            
            # Process each antardasha
            for antardasha in mahadasha.children:
                # Set parent planet for context
                if not hasattr(antardasha, 'parent_planet'):
                    antardasha.parent_planet = mahadasha.planet
                    
                # Generate phala for antardasha
                antardasha_phala = self.phala_generator.generate_phala(antardasha, birth_chart)
                phala_list.append(antardasha_phala)
                
                # Process each pratyantardasha
                for pratyantardasha in antardasha.children:
                    # Set parent planet for context
                    if not hasattr(pratyantardasha, 'parent_planet'):
                        pratyantardasha.parent_planet = antardasha.planet
                        
                    # Generate phala for pratyantardasha
                    pratyantardasha_phala = self.phala_generator.generate_phala(pratyantardasha, birth_chart)
                    phala_list.append(pratyantardasha_phala)
        
        return phala_list
    
    def _generate_dasha_timeline(self, birth_chart: BirthChart, dasha_tree: List[DashaNode], dasha_system: DashaSystem) -> DashaTimeline:
        """
        Generate dasha timeline for visualization.
        
        Args:
            birth_chart: The birth chart
            dasha_tree: The dasha tree
            dasha_system: The dasha system
            
        Returns:
            DashaTimeline: The dasha timeline
        """
        logger.info(f"Generating dasha timeline for birth chart {birth_chart.id}")
        
        # Use the timeline generator to generate the timeline
        return self.timeline_generator.generate_timeline(dasha_tree, birth_chart)
    
    def _generate_upcoming_significant_periods(
        self, 
        birth_chart: BirthChart, 
        dasha_tree: List[DashaNode]
    ) -> List[Dict[str, Any]]:
        """
        Generate upcoming significant periods.
        
        Args:
            birth_chart: The birth chart
            dasha_tree: The dasha tree
            
        Returns:
            List[Dict[str, Any]]: The upcoming significant periods
        """
        logger.info(f"Generating upcoming significant periods for birth chart {birth_chart.id}")
        
        # Placeholder implementation - will be expanded in future steps
        # This will be replaced with actual upcoming significant periods generation logic
        
        # For now, return empty list
        return []
