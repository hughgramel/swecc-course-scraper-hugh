# Parser Tests

This directory contains comprehensive tests for the HTML parser functionality.

## Test Structure

### Files

- `test_parser.py` - Main test file for all parser functions
- `test_files/` - Directory containing test data
  - `math_WIN_2023.html` - Sample HTML from UW's MATH department Winter 2023
  - `README.md` - Documentation for test files

### Test Classes

#### `TestParserFunctions`
Tests for all individual parser functions:

- `test_html_file_exists` - Validates test data is available
- `test_extract_course_tables` - Tests course table extraction
- `test_parse_course_header` - Tests course header parsing
- `test_parse_section_row` - Tests section row parsing
- `test_parse_time_and_location` - Tests time/location parsing
- `test_parse_enrollment_numbers` - Tests enrollment parsing
- `test_parse_schedule_html_integration` - Integration test for main function
- `test_html_structure_validation` - Validates HTML structure

#### `TestParserEdgeCases`
Tests for edge cases and error handling:

- `test_empty_html` - Tests with empty HTML
- `test_malformed_html` - Tests with malformed HTML
- `test_missing_data_fields` - Tests with incomplete data

## Running Tests

### Using pytest directly

```bash
# Run all tests
python -m pytest tests/test_parser.py -v

# Run specific test
python -m pytest tests/test_parser.py::TestParserFunctions::test_html_file_exists -v

# Run with coverage
python -m pytest tests/test_parser.py --cov=swecc_course_scraper.commands.parser
```

### Using the test runner script

```bash
# Run all tests
python run_parser_tests.py

# Run specific test
python run_parser_tests.py test_html_file_exists
python run_parser_tests.py test_html_structure_validation
```

## Test Data

The test uses real UW time schedule data from MATH Winter 2023, which includes:

- **Course Headers**: MATH 103, 111, 112, 120, 124, 125, 126, etc.
- **Section Data**: SLNs, section IDs, meeting times, locations
- **Instructor Information**: Names and contact details
- **Enrollment Data**: Current enrollment and capacity
- **Status Information**: Open/Closed status
- **Notes and Restrictions**: Course-specific information

## Implementation Status

Currently, most parser functions are not yet implemented, so tests are skipped with appropriate messages. As you implement each function, you can:

1. Uncomment the assertion lines in the relevant test
2. Run the specific test to validate your implementation
3. Add additional test cases as needed

## Test Development

When implementing parser functions:

1. **Start with individual function tests** - Test each helper function separately
2. **Use the provided sample data** - The test file contains real examples
3. **Add edge cases** - Test with missing data, malformed input, etc.
4. **Validate output structure** - Ensure returned data matches expected format
5. **Run integration tests** - Test the main parsing function end-to-end

## Example Test Data

The test file contains examples like:

```html
<!-- Course Header -->
<table bgcolor='#99ccff' width='100%' style='border:solid 1px #999;margin-bottom:4px'>
<tr><td width="50%"><b><A NAME=math124>MATH&nbsp;&nbsp; 124 </A>&nbsp;<A HREF=/students/crscat/math.html#math124>CALC ANALYT GEOM I</A></b></td><td width="15%"><b>(NSc,RSN)</b></td><td align="right" width="35%"></td></tr></table>

<!-- Section Row -->
<tr><td><pre>
Restr  <A HREF=https://sdb.admin.washington.edu/timeschd/uwnetid/sln.asp?QTRYR=WIN+2023&SLN=17252>17252</A> A  5       MWF    930-1020   <A HREF=/students/maps/map.cgi?FSH>FSH</A>  102      Collingwood,David H        Open    133/ 150                      
</td></tr>
```

This provides comprehensive test coverage for all parser functionality.
