# Structured Implementation Prompt for Vedic Astrology Calculator

This document provides a systematic approach to implementing a web-based Vedic astrology calculator according to the provided roadmap. The implementation will proceed through modular, testable phases with clear validation criteria at each stage.

## Implementation Approach

1. **Modular Development**: Each component will be implemented as an isolated, testable module
2. **Progressive Integration**: Modules will be integrated in phases, with validation at each stage
3. **Test-Driven Development**: Each component will include comprehensive unit tests
4. **Documentation**: All code will be thoroughly documented with clear API contracts

## Phase 1: Foundation Implementation

### 1.1 Backend: Core Astronomical Engine

```
Please implement the core astronomical calculation engine for the Vedic astrology calculator with the following specifications:

1. Create a module that calculates planetary positions using the Lahiri ayanamsa
2. Implement functions for:
   - Calculating planetary longitudes for a given date, time, and location
   - Determining house cusps using the equal house system
   - Mapping planets to their respective Rashis (zodiac signs)
3. Include proper error handling for invalid inputs
4. Implement a basic caching mechanism for repeated calculations
5. Provide unit tests that verify accuracy within 1 arc minute against reference data

The implementation should be in Python and follow best practices for code organization and documentation.
```

### 1.2 Frontend: Basic Application Shell

```
Please implement the basic frontend shell for the Vedic astrology calculator with the following specifications:

1. Create a responsive React application with TypeScript
2. Implement the core state management infrastructure using Redux
3. Create basic input forms for:
   - Date and time input with validation
   - Location input with geocoding support
4. Set up the API communication layer that will connect to the backend
5. Implement a simple loading state and error display mechanism
6. Create a prototype South Indian chart visualization component that can display placeholders for planets

The implementation should follow modern React best practices, with component separation and responsive design principles.
```

### 1.3 Integration: API Layer

```
Please implement the API layer that will connect the frontend and backend components with the following specifications:

1. Create a RESTful API with endpoints for:
   - Calculating basic chart data (D1 chart)
   - Validating input parameters
2. Implement serialization/deserialization of astronomical data
3. Set up proper error handling and status codes
4. Implement basic rate limiting and request validation
5. Create documentation for the API endpoints

The implementation should use FastAPI or Flask and include OpenAPI documentation.
```

## Phase 2: Chart Visualization & Divisional Chart Framework

### 2.1 Backend: Divisional Chart Calculations

```
Please extend the astronomical calculation engine to support divisional charts with the following specifications:

1. Implement calculations for divisional charts D1-D9
2. Create functions for:
   - Determining planetary dignities (exaltation, debilitation, etc.)
   - Calculating basic planetary strengths
   - Identifying key planetary relationships
3. Enhance the caching mechanism to support divisional chart data
4. Implement proper error recovery for calculation edge cases
5. Provide unit tests that verify divisional chart accuracy against reference implementations

The implementation should maintain the modular structure established in Phase 1.
```

### 2.2 Frontend: Enhanced Chart Visualization

```
Please enhance the chart visualization component with the following specifications:

1. Implement a full South Indian style chart rendering engine using SVG
2. Create interactive elements that show detailed information on hover/click
3. Add visualizations for:
   - Planetary positions with proper symbols
   - Aspect lines between planets
   - Dignity state indicators
4. Implement client-side caching for chart data
5. Create a mechanism to switch between different divisional charts
6. Ensure responsive design that maintains legibility across device sizes

The implementation should maintain performance standards with initial render under 1 second.
```

### 2.3 Integration: Expanded API and Testing

```
Please enhance the API layer to support the expanded functionality with the following specifications:

1. Add endpoints for:
   - Calculating divisional charts (D1-D9)
   - Retrieving planetary dignity information
   - Getting detailed planet information
2. Implement comprehensive integration tests
3. Add performance monitoring for API endpoints
4. Create documentation for the new endpoints
5. Implement a mocking service for frontend development

The implementation should maintain backward compatibility with Phase 1 endpoints.
```

## Phase 3: Dasa System Implementation

### 3.1 Backend: Dasa Calculation Engine

```
Please implement the Vimshottari dasa calculation system with the following specifications:

1. Create modules for:
   - Calculating the main dasa periods
   - Determining bhukti (sub-periods)
   - Calculating antara (sub-sub-periods)
2. Implement precise boundary calculations (accuracy within 1 day)
3. Create a date-based lookup system to find current dasa periods
4. Enhance caching for dasa calculations
5. Implement error handling for temporal edge cases
6. Provide comprehensive unit tests against reference data

The implementation should maintain consistent calculation precision and performance.
```

### 3.2 Frontend: Dasa Visualization

```
Please implement the dasa period visualization components with the following specifications:

1. Create a timeline interface showing dasa periods
2. Implement hierarchical navigation controls for bhukti and antara periods
3. Add date-based lookup functionality
4. Create a persistent display configuration system
5. Implement visual indicators for current dasa period
6. Ensure responsive design for the timeline interface

The implementation should follow established design patterns and maintain performance standards.
```

### 3.3 Integration: Dasa API and Testing

```
Please enhance the API layer to support dasa calculations with the following specifications:

1. Add endpoints for:
   - Calculating complete dasa hierarchy
   - Looking up dasa periods for specific dates
   - Retrieving detailed dasa information
2. Implement comprehensive integration tests
3. Add performance monitoring for dasa calculation endpoints
4. Create documentation for the new endpoints
5. Enhance error handling for dasa-specific edge cases

The implementation should maintain backward compatibility with previous phases.
```

## Phase 4: Advanced Feature Implementation

### 4.1 Backend: Advanced Calculations

```
Please implement advanced Jyotish calculations with the following specifications:

1. Complete the remaining divisional charts (D10-D60)
2. Implement a comprehensive yoga identification system
3. Create a complete planetary strength calculation framework
4. Enhance dignity evaluation with detailed rules
5. Implement an advanced caching strategy
6. Create comprehensive error management with recovery strategies
7. Provide unit tests for all new calculations

The implementation should maintain calculation accuracy and performance standards.
```

### 4.2 Frontend: Advanced Visualization

```
Please implement advanced visualization features with the following specifications:

1. Create interfaces for all divisional charts (D10-D60)
2. Implement yoga identification displays
3. Add strength calculation visualizations
4. Create chart comparison interfaces
5. Implement guided interpretation views
6. Add printable report generation
7. Create custom view configurations with persistence

The implementation should maintain performance standards and responsive design principles.
```

### 4.3 Integration: Complete System

```
Please finalize the API integration with the following specifications:

1. Complete all remaining API endpoints
2. Implement comprehensive system testing
3. Add detailed error reporting and monitoring
4. Create complete API documentation
5. Implement performance optimizations for all endpoints
6. Add system health monitoring

The implementation should ensure consistent performance under load and graceful degradation.
```

## Phase 5: Integration, Optimization & Finalization

### 5.1 System Optimization

```
Please implement system-wide optimizations with the following specifications:

1. Perform frontend optimizations:
   - Code splitting
   - Asset preloading
   - Animation tuning
   - Bundle size reduction
2. Implement backend optimizations:
   - Query optimization
   - Caching strategy refinement
   - Resource utilization improvements
3. Enhance overall system performance:
   - End-to-end response time tuning
   - Memory usage optimization
   - Throughput improvements

The implementation should meet or exceed all performance targets defined in the roadmap.
```

### 5.2 Final Integration and Testing

```
Please perform final system integration and testing with the following specifications:

1. Conduct comprehensive end-to-end testing
2. Perform cross-browser and device compatibility testing
3. Implement accessibility improvements to meet WCAG 2.1 AA standards
4. Conduct performance testing under varied load conditions
5. Create comprehensive system documentation
6. Prepare production deployment configurations

The implementation should validate against all criteria specified in the roadmap.
```

## Validation Framework

After each implementation step, please provide:

1. **Functional Evidence**: Screenshots or output examples demonstrating the implemented functionality
2. **Test Results**: Summary of unit/integration test results
3. **Performance Metrics**: Measurements against the defined performance targets
4. **Code Documentation**: Clear documentation of API contracts and component interfaces
5. **Next Steps**: Clear identification of what will be implemented next

## Technical Constraints

- **Frontend**: React with TypeScript, SVG for visualization
- **Backend**: Python for astronomical calculations
- **API**: RESTful endpoints with proper documentation
- **Validation**: Test coverage >80%, adherence to performance targets
- **Documentation**: Comprehensive API documentation and usage examples

## Adherence to Jyotish Principles

All implementations must strictly adhere to traditional Vedic astrology principles:
- Exclusive use of Lahiri ayanamsa
- Equal house system
- Traditional rules for Rashi, Nakshatra, dignity states, and yoga identification
- No incorporation of Western astrological concepts

## Implementation Readiness

Please confirm readiness to begin implementation of Phase 1 components, and specify any questions or clarifications needed before proceeding.