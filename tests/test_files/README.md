# Test Files

This directory contains test data files used by the parser tests.

## Files

- `math_WIN_2023.html` - Sample HTML from UW's MATH department Winter 2023 time schedule
  - Contains course data for MATH 103, 111, 112, 120, 124, 125, 126, and many others
  - Includes section data with SLNs, instructors, times, locations, enrollment
  - Used to test all parser functions with real UW data

## Usage

These files are used by the test suite in `test_parser.py` to validate that the HTML parser
functions work correctly with actual UW time schedule data.

## Data Structure

The HTML file contains:
- Course headers with course codes, titles, and credits
- Section rows with SLN, section ID, meeting times, locations, instructors
- Enrollment data (enrolled/capacity)
- Status information (Open/Closed)
- Notes and restrictions

This provides comprehensive test coverage for all parser functions.
