# Vedic Jyotish Calculation Service: Refined Architectural Framework

## Core Alignment Directives

- **Ayanamsa Standardization:** Implement Lahiri ayanamsa as primary calculation reference with optional Raman and Krishnamurti systems available as configuration parameters
- **House System Standardization:** Utilize exclusive Whole Sign house system in accordance with classical Vedic methodology
- **Calculation Purity:** Maintain strict adherence to traditional Parashari calculation principles throughout all computational modules

## Architectural Refinement Specification

### Calculation Core Reconfiguration (Priority Module)

#### Ayanamsa Implementation Framework
- Primary calculation engine calibrated to Lahiri ayanamsa with 23°51' precession value
- Configurable ayanamsa selection module with standardized offset implementation
- Validation system ensuring consistent ayanamsa application across all calculation modules
- Historical ayanamsa tracking for date-specific calculations with precession adjustment

#### House System Standardization
- Exclusive Whole Sign house implementation with rashi-based boundary definitions
- House lordship determination based on classical sign-lord relationships
- House-to-house aspect calculations using traditional Whole Sign methodology
- Integrated house strength metrics within Whole Sign framework

### Computational Module Realignment

#### Chart Generation System
- Rashi-oriented D1 chart structure with Whole Sign house overlay
- Planetary placement mapped strictly to Whole Sign houses with accurate degree positioning
- Inter-house relationship mapping using classical Whole Sign ruleset
- House significance determination using traditional Bhava indicators within Whole Sign framework

#### Divisional Chart Hierarchy
- Implement all divisional charts (D1-D60) using consistent Whole Sign methodology
- Ensure divisional lordships maintain classical Whole Sign relationship patterns
- Standardize aspect calculations across all divisional charts using Whole Sign parameters
- Maintain consistent house strength evaluation metrics within Whole Sign system

### Predictive Framework Standardization

#### Dasha Calculation Engine
- Calibrate all dasha calculations to selected ayanamsa configuration
- Ensure nakshatra boundary determinations align with specified ayanamsa parameters
- Implement consistent dasha commencement timing based on standardized ayanamsa
- Maintain temporal precision in dasha transitions accounting for ayanamsa considerations

#### Transit Progression Framework
- Apply consistent ayanamsa correction to all transit calculations
- Implement Whole Sign transit analysis with house-based activation metrics
- Develop transit-to-natal comparison system using standardized ayanamsa values
- Create temporal progression engine with consistent ayanamsa application

### Analytical Module Adjustment

#### Strength Calculation System
- Reconfigure Shadbala calculations to align with Whole Sign methodology
- Adapt Ashtakavarga system to utilize Whole Sign house boundaries
- Implement consistent planetary strength metrics within Whole Sign framework
- Ensure dignity calculations reflect traditional Whole Sign placement parameters

#### Yoga Identification Framework
- Adjust yoga detection algorithms to Whole Sign house placements
- Implement consistent ayanamsa application in yogas involving specific degrees
- Validate yoga formation criteria against classical texts using standardized parameters
- Ensure yoga strength evaluations maintain consistency with selected ayanamsa

## Implementation Verification Protocol

### Calculation Validation Framework
- Develop test suite comparing results against classical reference charts
- Implement automated verification of planetary positions against standard ephemeris
- Create house placement validation system confirming accurate Whole Sign implementation
- Establish continuous monitoring system for calculation consistency across modules

### Reference Integration System
- Document explicit ayanamsa and house system parameters in all calculation outputs
- Provide classical textual references supporting implemented methodologies
- Create detailed technical documentation explaining ayanamsa application across modules
- Develop comprehensive system architecture documentation highlighting Whole Sign implementation

## User Interface Adaptation

### Configuration Management Interface
- Implement clear ayanamsa selection with current Lahiri default
- Provide informational context explaining ayanamsa significance and selection rationale
- Display current ayanamsa and house system parameters in all chart visualizations
- Create educational resources explaining traditional Whole Sign methodology

### Visualization Framework
- Adapt chart rendering to emphasize Whole Sign house boundaries
- Implement visual indicators for ayanamsa-sensitive chart components
- Design information hierarchy highlighting traditional Vedic interpretative elements
- Create consistent symbolic language maintaining classical Vedic representations

### House System Implementation Verification
- **Current Implementation:** The system correctly uses the Whole Sign house system as specified in MVP_Roadmap_1.2
- **Swiss Ephemeris Configuration:** Using 'W' parameter in swe.houses_ex() calls to specify Whole Sign system
- **House Calculation Logic:** Houses are correctly determined by the sign position relative to the ascendant sign
- **Verification Process:**
  1. Confirmed house calculation in _calculate_houses() method follows Whole Sign principles
  2. Verified _get_house_number() method correctly calculates houses based on sign position
  3. Confirmed Swiss Ephemeris calls use 'W' parameter for Whole Sign system
  4. Validated that house assignments in planet data match Whole Sign expectations

This verification confirms that our implementation adheres to the Whole Sign house system as required, where the sign containing the ascendant becomes the 1st house, and subsequent signs follow in order as houses 2-12.

This architectural framework ensures strict alignment with classical Vedic Jyotish principles by standardizing all calculations on Lahiri ayanamsa and the Whole Sign house system while maintaining computational accuracy and authentic methodological integrity throughout the system.