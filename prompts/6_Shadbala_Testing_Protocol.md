# Shadbala Testing Protocol

## Overview
This document outlines the comprehensive testing protocol for the Shadbala calculation system in the Vedic Kundli Calculator. The testing framework ensures that all six strength components are accurately calculated according to classical Parashari principles.

## Test Objectives
1. Verify the accuracy of each Shadbala component calculation
2. Validate the total Shadbala values against reference charts
3. Confirm proper integration with the main calculation engine
4. Ensure correct display of Shadbala data in the user interface

## Test Cases

### 1. Component-Level Testing

#### 1.1 Sthana Bala Tests
- **TC-SB-01**: Verify Uchcha Bala calculation for exalted planets
- **TC-SB-02**: Verify Uchcha Bala calculation for debilitated planets
- **TC-SB-03**: Verify Saptavargaja Bala calculation for planets in own signs
- **TC-SB-04**: Verify Ojayugmarasyamsa Bala calculation for male/female planets
- **TC-SB-05**: Verify Kendradi Bala calculation for planets in different house positions
- **TC-SB-06**: Verify Drekkana Bala calculation for planets in different decanates

#### 1.2 Dig Bala Tests
- **TC-DB-01**: Verify Dig Bala for Jupiter in the 1st house (North)
- **TC-DB-02**: Verify Dig Bala for Venus in the 1st house (North)
- **TC-DB-03**: Verify Dig Bala for Mercury in the 7th house (West)
- **TC-DB-04**: Verify Dig Bala for Saturn in the 4th house (South)
- **TC-DB-05**: Verify Dig Bala for Mars in the 10th house (East)
- **TC-DB-06**: Verify Dig Bala for Moon in the 10th house (East)
- **TC-DB-07**: Verify Dig Bala for Sun in the 4th house (South)

#### 1.3 Kala Bala Tests
- **TC-KB-01**: Verify Natonnata Bala for diurnal planets during day
- **TC-KB-02**: Verify Natonnata Bala for nocturnal planets during night
- **TC-KB-03**: Verify Paksha Bala for Moon in Shukla Paksha
- **TC-KB-04**: Verify Paksha Bala for Moon in Krishna Paksha
- **TC-KB-05**: Verify Tribhaga Bala calculation
- **TC-KB-06**: Verify Ayana Bala for benefic planets during Uttarayana
- **TC-KB-07**: Verify Ayana Bala for malefic planets during Dakshinayana
- **TC-KB-08**: Verify Yuddha Bala for planets in planetary war

#### 1.4 Chesta Bala Tests
- **TC-CB-01**: Verify Chesta Bala for direct motion planets
- **TC-CB-02**: Verify Chesta Bala for retrograde planets
- **TC-CB-03**: Verify Chesta Bala for combust planets

#### 1.5 Naisargika Bala Tests
- **TC-NB-01**: Verify Naisargika Bala values for all planets

#### 1.6 Drik Bala Tests
- **TC-DRB-01**: Verify Drik Bala for planets with benefic aspects
- **TC-DRB-02**: Verify Drik Bala for planets with malefic aspects
- **TC-DRB-03**: Verify Drik Bala for planets with mixed aspects

### 2. Integration Testing

#### 2.1 Calculation Engine Integration
- **TC-INT-01**: Verify Shadbala data is correctly included in the API response
- **TC-INT-02**: Verify Shadbala calculation is triggered during chart calculation
- **TC-INT-03**: Verify Shadbala data structure matches expected format

#### 2.2 UI Integration
- **TC-UI-01**: Verify Shadbala tab is correctly displayed in the UI
- **TC-UI-02**: Verify Shadbala summary table shows correct data
- **TC-UI-03**: Verify detailed Shadbala components are displayed correctly
- **TC-UI-04**: Verify interactive elements function as expected

### 3. Reference Chart Validation

#### 3.1 Known Chart Tests
- **TC-REF-01**: Validate Shadbala calculations against reference chart #1
- **TC-REF-02**: Validate Shadbala calculations against reference chart #2
- **TC-REF-03**: Validate Shadbala calculations against reference chart #3

## Test Data
The following test data will be used for validation:

### Reference Charts
1. **Reference Chart #1**: January 15, 1980, 10:30 AM, New Delhi, India
2. **Reference Chart #2**: May 5, 1990, 3:45 PM, Mumbai, India
3. **Reference Chart #3**: October 10, 1985, 8:15 PM, Chennai, India

### Expected Values
Detailed expected values for each test case are documented in the accompanying Excel spreadsheet: `shadbala_test_values.xlsx`

## Test Execution

### Prerequisites
1. Development environment set up with all dependencies
2. Test data loaded into the system
3. Testing tools configured

### Execution Steps
1. Run component-level tests for each Shadbala type
2. Execute integration tests to verify proper system integration
3. Validate calculations against reference charts
4. Document any discrepancies or issues

## Acceptance Criteria
1. All component-level tests pass with expected values
2. Shadbala data is correctly integrated with the calculation engine
3. UI displays Shadbala data accurately and responsively
4. Reference chart validation shows less than 1% deviation from expected values

## Issue Tracking
Any issues identified during testing will be documented with:
1. Test case ID
2. Expected vs. actual results
3. Severity level
4. Proposed resolution

## Conclusion
This testing protocol ensures that the Shadbala implementation meets the high standards of accuracy and reliability required for the Vedic Kundli Calculator. Successful completion of these tests will validate that the Shadbala calculations follow classical Parashari principles and provide valuable insights into planetary strengths.
