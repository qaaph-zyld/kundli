# Vedic Jyotish Development Guidelines

## Core Directive
Execute Vedic astrology calculation service with maximum velocity while maintaining computational accuracy and astrological integrity. Make autonomous decisions within defined astrological systems. Proceed immediately upon validating core calculation requirements.

## Analysis & Implementation Framework

### Phase 1: Architectural Assessment
```
ANALYZE AND PROCEED:
- Calculation precision → Identify ephemeris requirements and algorithms
- Component hierarchy → Structure modular calculation systems
- Technical dependencies → Map astrological computation libraries
- Integration pathways → Define interfaces between calculation modules
- User experience architecture → Design intuitive chart visualization

ACTION: Begin implementation of D1 chart calculations immediately
```

### Phase 2: Accelerated Development
```
EXECUTE INCREMENTALLY:
- Core calculations → Implement planetary positions and house cusps first
- Modular expansion → Add divisional charts in priority sequence (D1, D9, D12)
- Parallel development → Simultaneously build Vimshottari dasha module
- Testing automation → Verify calculations against established references
- API foundation → Create standardized endpoints for each calculation type

POLICY: Prioritize computational accuracy while maintaining development velocity
```

### Phase 3: Targeted Deployment
```
DELIVER PROGRESSIVELY:
- Deploy calculation engine → Launch with validated D1 chart functionality
- Phase divisional charts → Release new chart types as validated
- Monitor performance → Optimize calculation-intensive operations
- Implement feedback loop → Focus on calculation accuracy adjustments
- Scale methodically → Prepare architecture for full D1-D60 expansion

PRIORITY: Reliable astrological calculations over comprehensive feature set
```

## Implementation Parameters

### Decision Protocol
1. Validate calculation methods against classical Vedic references
2. Prioritize features based on astrological significance and user value
3. Implement standardized interfaces between calculation modules
4. Establish clear validation criteria for each astrological component
5. Document computational approaches and their classical foundations

### Quality Assurance
- Verify planetary position accuracy to within accepted tolerances
- Confirm house cusp calculations match established systems
- Validate dasha period calculations for precision
- Ensure nakshatra and pada determinations align with classical texts
- Test transit calculations against ephemeris data

## Development Sequence
1. Planetary position calculation engine
2. House system implementation (Whole Sign initial priority)
3. Basic divisional chart framework (D1, D9, D12)
4. Vimshottari dasha calculation module
5. Nakshatra determination system
6. User interface for chart visualization
7. API endpoints for core calculations

## Critical Path Focus
- Establish accurate planetary calculation foundation before expanding features
- Implement precise time and location handling for birth data
- Develop modular interfaces between calculation systems
- Create extensible architecture for future divisional charts and dasha systems
- Build visualization components that accurately represent calculated positions

## Core Alignment Directives

- **Ayanamsa Standardization:** Implement Lahiri ayanamsa as primary calculation reference
- **House System Standardization:** Utilize exclusive Whole Sign house system in accordance with classical Vedic methodology
- **Calculation Purity:** Maintain strict adherence to traditional Parashari calculation principles throughout all computational modules

## Architectural Refinement Specification

### Calculation Core Reconfiguration

#### Ayanamsa Implementation Framework
- Primary calculation engine calibrated to Lahiri ayanamsa with 23°51' precession value
- Validation system ensuring consistent ayanamsa application across all calculation modules
- Historical ayanamsa tracking for date-specific calculations with precession adjustment

#### House System Standardization
- Exclusive Whole Sign house implementation with rashi-based boundary definitions
- House lordship determination based on classical sign-lord relationships
- House-to-house aspect calculations using traditional Whole Sign methodology
- Integrated house strength metrics within Whole Sign framework

### House System Implementation Verification
- **Current Implementation:** The system correctly uses the Whole Sign house system as specified
- **Swiss Ephemeris Configuration:** Using 'W' parameter in swe.houses_ex() calls to specify Whole Sign system
- **House Calculation Logic:** Houses are correctly determined by the sign position relative to the ascendant sign
- **Verification Process:**
  1. Confirmed house calculation in _calculate_houses() method follows Whole Sign principles
  2. Verified _get_house_number() method correctly calculates houses based on sign position
  3. Confirmed Swiss Ephemeris calls use 'W' parameter for Whole Sign system
  4. Validated that house assignments in planet data match Whole Sign expectations

## Comprehensive Testing Framework

### Core Validation Principles
- Astrological computational integrity
- Vedic methodology adherence
- Cross-module consistency validation
- Edge case identification and verification

### Planetary Calculation Verification Protocol

#### Position Accuracy Validation
1. **Ephemeris Comparison Testing**
   - Validate planetary longitudes against Swiss Ephemeris with Lahiri ayanamsa
   - Verify degree/minute/second precision across 100-year test range
   - Confirm proper retrograde status identification across planetary cycles
   - Validate proper combustion state detection with solar proximity thresholds

2. **Nakshatra Placement Verification**
   - Test accurate nakshatra determination for all planets
   - Validate pada calculations with precise boundary recognition
   - Confirm correct lord assignment across nakshatra transitions
   - Verify degree-specific attributes within nakshatra segments

### Divisional Chart Testing Framework

#### Chart Generation Validation
1. **D1 Chart Verification**
   - Validate sign placement accuracy for all planets
   - Confirm Whole Sign house assignment integrity
   - Test house lordship identification for all charts
   - Verify correct ascendant calculation with precise degree

2. **Higher Harmonic Chart Testing**
   - Validate mathematical accuracy of all divisional chart calculations (D1-D60)
   - Test internal consistency between related divisional charts
   - Confirm proper lordship assignments across all divisions
   - Verify special divisional rules application (e.g., Navamsha variance)

### Predictive System Validation

#### Dasha Calculation Testing
1. **Vimshottari Dasha Verification**
   - Validate accurate calculation of main dasha sequence
   - Test precise timing of dasha transitions to minute level
   - Confirm proper sub-period (antardasha) calculations
   - Verify accurate chaining of multi-level dasha periods (pratyantardasha, etc.)

### Strength Calculation Validation

#### Shadbala Testing Suite
1. **Six-fold Strength Verification**
   - Test Sthana Bala (positional strength) calculations
   - Validate Dig Bala (directional strength) metrics
   - Confirm Kala Bala (temporal strength) computations
   - Verify Chesta Bala (motional strength) values
   - Test Naisargika Bala (natural strength) assignments
   - Validate Drig Bala (aspectual strength) calculations

2. **Ashtakavarga Validation**
   - Test individual planet bindu calculations
   - Validate complete Sarvashtakavarga computations
   - Confirm transit bindu accumulation metrics
   - Verify kakshya-level bindu distributions

## Integration Testing Architecture

### Cross-Module Consistency Validation

#### Comprehensive System Testing
1. **End-to-End Chart Generation**
   - Validate complete chart generation pipeline from birth data input to final chart output
   - Test ayanamsa consistency across all generated charts and calculations
   - Confirm proper data persistence through all calculation stages
   - Verify accurate final presentation of calculated values

2. **Reference Chart Comparison**
   - Test system outputs against manually calculated reference charts
   - Validate alignment with established classical calculation methodologies
   - Confirm proper handling of edge cases and special conditions
   - Verify results against published charts from authoritative sources

### User Interface Integration Testing

#### Visualization Validation
1. **Chart Rendering Accuracy**
   - Test proper symbolic representation of planetary positions
   - Validate accurate house boundary visualization
   - Confirm correct aspect line rendering
   - Verify proper display of calculated metrics and values

2. **Interactive Feature Testing**
   - Test drill-down functionality for detailed planetary information
   - Validate proper behavior of interactive chart elements
   - Confirm accurate data presentation in tooltips and information panels
   - Verify proper state management during user interaction

## Performance Testing Framework

### Computational Efficiency Validation

#### Processing Optimization Testing
1. **Calculation Speed Benchmarking**
   - Test calculation performance across varying chart complexities
   - Validate response time for complete chart generation workflow
   - Confirm efficient processing of multiple concurrent chart calculations
   - Verify optimal resource utilization during intensive calculations

2. **Memory Utilization Optimization**
   - Test efficient memory management during complex calculations
   - Validate proper cleanup of temporary calculation artifacts
   - Confirm absence of memory leaks during extended operation
   - Verify proper handling of large dataset operations

## Implementation Guidelines

1. Follow the existing Development Protocol for all implementation work
2. Maintain compatibility between frontend and backend features
3. Implement features in the order specified by the roadmap
4. Test each feature thoroughly before moving to the next phase
5. Update documentation as features are completed
6. Only Vedic astrology features will be added (no Western astrology)
7. Maintain existing capabilities when adding new features
8. Run the application after each feature addition for verification
9. Update GitHub repository after each confirmed feature
