"""
Tests for the HTML parser module.

This module tests all parser functions using the MATH WIN 2023 HTML file.
"""

import os
import pytest
from pathlib import Path

# Import the parser functions (they may not be implemented yet)
try:
    from swecc_course_scraper.commands.parser import (
        parse_schedule_html,
        _extract_course_tables,
        _parse_course_header,
        _parse_section_row,
        _parse_time_and_location,
        _parse_enrollment_numbers
    )
    PARSER_AVAILABLE = True
except ImportError:
    # Functions not yet implemented
    PARSER_AVAILABLE = False

from swecc_course_scraper.models.course import Course, CourseSection


class TestParserFunctions:
    """Test class for all parser functions."""
    
    @classmethod
    def setup_class(cls):
        """Set up test data once for all tests."""
        # Get the path to the test HTML file
        test_file_path = Path(__file__).parent / "test_files" / "math_WIN_2023.html"
        
        # Read the HTML content
        with open(test_file_path, 'r', encoding='utf-8') as f:
            cls.html_content = f.read()
        
        # Store file path for reference
        cls.test_file_path = test_file_path
    
    def test_html_file_exists(self):
        """Test that the test HTML file exists and is readable."""
        assert self.test_file_path.exists(), f"Test file not found: {self.test_file_path}"
        assert len(self.html_content) > 0, "HTML content is empty"
        assert "MATH" in self.html_content, "HTML should contain MATH department data"
        assert "Winter Quarter 2023" in self.html_content, "HTML should contain Winter 2023 data"
    
    def test_extract_course_tables(self):
        """Test the _extract_course_tables function."""
        if not PARSER_AVAILABLE:
            pytest.skip("Parser functions not yet implemented")
        
        # TODO: Implement this test once the function is implemented
        # Expected: Should return a list of BeautifulSoup table elements
        # Each table should have bgcolor='#99ccff' and contain course data
        
        # For now, just test that the function exists and can be called
        try:
            result = _extract_course_tables(self.html_content)
            # Once implemented, add proper assertions:
            # assert isinstance(result, list)
            # assert len(result) > 0
            # for table in result:
            #     assert table.get('bgcolor') == '#99ccff'
        except NotImplementedError:
            pytest.skip("Function not yet implemented")
    
    def test_parse_course_header(self):
        """Test the _parse_course_header function."""
        if not PARSER_AVAILABLE:
            pytest.skip("Parser functions not yet implemented")
        
        # TODO: Implement this test once the function is implemented
        # Expected: Should extract course code, title, and credits from header
        
        # Sample header HTML from the file:
        sample_header = """
        <table bgcolor='#99ccff' width='100%' style='border:solid 1px #999;margin-bottom:4px'>
        <tr><td width="50%"><b><A NAME=math124>MATH&nbsp;&nbsp; 124 </A>&nbsp;<A HREF=/students/crscat/math.html#math124>CALC ANALYT GEOM I</A></b></td><td width="15%"><b>(NSc,RSN)</b></td><td align="right" width="35%"></td></tr></table>
        """
        
        try:
            result = _parse_course_header(sample_header)
            # Once implemented, add proper assertions:
            # assert result['course_code'] == 'MATH 124'
            # assert result['title'] == 'CALC ANALYT GEOM I'
            # assert result['credits'] == '5'  # or whatever the default is
        except NotImplementedError:
            pytest.skip("Function not yet implemented")
    
    def test_parse_section_row(self):
        """Test the _parse_section_row function."""
        if not PARSER_AVAILABLE:
            pytest.skip("Parser functions not yet implemented")
        
        # TODO: Implement this test once the function is implemented
        # Expected: Should extract all section data from a table row
        
        # Sample section row from the file:
        sample_row = """
        <tr><td><pre>
        Restr  <A HREF=https://sdb.admin.washington.edu/timeschd/uwnetid/sln.asp?QTRYR=WIN+2023&SLN=17252>17252</A> A  5       MWF    930-1020   <A HREF=/students/maps/map.cgi?FSH>FSH</A>  102      Collingwood,David H        Open    133/ 150                      
                        MATH 124 CANNOT BE OVERLOADED                               <br/>                        TAKE GUIDED SELF-PLACEMENT BEFORE                           <br/>                        REGISTERING FOR COURSE                                      <br/>                        HTTPS://TINYURL.COM/UWMATHEXAMS                             <br/></td></tr>
        """
        
        try:
            result = _parse_section_row(sample_row)
            # Once implemented, add proper assertions:
            # assert result['sln'] == '17252'
            # assert result['section_id'] == 'A'
            # assert result['credits'] == '5'
            # assert result['days'] == 'MWF'
            # assert result['time'] == '930-1020'
            # assert result['building'] == 'FSH'
            # assert result['room'] == '102'
            # assert result['instructor'] == 'Collingwood,David H'
            # assert result['status'] == 'Open'
            # assert result['enrolled'] == 133
            # assert result['capacity'] == 150
        except NotImplementedError:
            pytest.skip("Function not yet implemented")
    
    def test_parse_time_and_location(self):
        """Test the _parse_time_and_location function."""
        if not PARSER_AVAILABLE:
            pytest.skip("Parser functions not yet implemented")
        
        # TODO: Implement this test once the function is implemented
        # Expected: Should parse time and location strings
        
        test_cases = [
            ("MWF    930-1020   FSH  102", ("MWF", "930-1020", "FSH", "102")),
            ("TTh    1230-120   KNE  110", ("TTh", "1230-120", "KNE", "110")),
            ("to be arranged", ("", "", "", "")),
        ]
        
        for input_str, expected in test_cases:
            try:
                result = _parse_time_and_location(input_str)
                # Once implemented, add proper assertions:
                # assert result == expected
            except NotImplementedError:
                pytest.skip("Function not yet implemented")
                break
    
    def test_parse_enrollment_numbers(self):
        """Test the _parse_enrollment_numbers function."""
        if not PARSER_AVAILABLE:
            pytest.skip("Parser functions not yet implemented")
        
        # TODO: Implement this test once the function is implemented
        # Expected: Should parse enrollment strings like "133/150"
        
        test_cases = [
            ("133/150", (133, 150)),
            ("0/120", (0, 120)),
            ("357/376", (357, 376)),
            ("", (0, 0)),  # Handle empty string
        ]
        
        for input_str, expected in test_cases:
            try:
                result = _parse_enrollment_numbers(input_str)
                # Once implemented, add proper assertions:
                # assert result == expected
            except NotImplementedError:
                pytest.skip("Function not yet implemented")
                break
    
    def test_parse_schedule_html_integration(self):
        """Test the main parse_schedule_html function (integration test)."""
        if not PARSER_AVAILABLE:
            pytest.skip("Parser functions not yet implemented")
        
        # TODO: Implement this test once all functions are implemented
        # Expected: Should return a list of Course objects with all sections parsed
        
        try:
            result = parse_schedule_html(self.html_content, "WIN", 2023)
            # Once implemented, add proper assertions:
            # assert isinstance(result, list)
            # assert len(result) > 0
            # 
            # # Check that we have some expected courses
            # course_codes = [course.course_code for course in result]
            # assert "MATH 124" in course_codes
            # assert "MATH 125" in course_codes
            # 
            # # Check that courses have sections
            # for course in result:
            #     assert len(course.sections) > 0
            #     for section in course.sections:
            #         assert isinstance(section, CourseSection)
            #         assert section.sln is not None
            #         assert section.course_code is not None
        except NotImplementedError:
            pytest.skip("Function not yet implemented")
    
    def test_html_structure_validation(self):
        """Test that the HTML has the expected structure for parsing."""
        # This test validates the HTML structure without calling parser functions
        
        # Check for course tables
        assert "bgcolor='#99ccff'" in self.html_content, "Should contain course tables"
        
        # Check for course headers
        assert "MATH&nbsp;&nbsp; 124" in self.html_content, "Should contain MATH 124"
        assert "MATH&nbsp;&nbsp; 125" in self.html_content, "Should contain MATH 125"
        
        # Check for section data
        assert "17252" in self.html_content, "Should contain SLN 17252"
        assert "Collingwood,David H" in self.html_content, "Should contain instructor names"
        
        # Check for enrollment data
        assert "133/ 150" in self.html_content, "Should contain enrollment data"
        
        # Check for time/location data
        assert "MWF    930-1020" in self.html_content, "Should contain meeting times"
        assert "FSH</A>  102" in self.html_content, "Should contain building/room data"


class TestParserEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_html(self):
        """Test parser behavior with empty HTML."""
        if not PARSER_AVAILABLE:
            pytest.skip("Parser functions not yet implemented")
        
        try:
            result = parse_schedule_html("", "WIN", 2023)
            # Should return empty list or handle gracefully
            assert isinstance(result, list)
        except NotImplementedError:
            pytest.skip("Function not yet implemented")
    
    def test_malformed_html(self):
        """Test parser behavior with malformed HTML."""
        if not PARSER_AVAILABLE:
            pytest.skip("Parser functions not yet implemented")
        
        malformed_html = "<html><body><table><tr><td>Incomplete"
        
        try:
            result = parse_schedule_html(malformed_html, "WIN", 2023)
            # Should handle gracefully without crashing
            assert isinstance(result, list)
        except NotImplementedError:
            pytest.skip("Function not yet implemented")
    
    def test_missing_data_fields(self):
        """Test parser behavior when expected data fields are missing."""
        if not PARSER_AVAILABLE:
            pytest.skip("Parser functions not yet implemented")
        
        # This would test individual functions with incomplete data
        # For example, a section row missing instructor or enrollment data
        
        incomplete_row = """
        <tr><td><pre>
        Restr  <A HREF=...>17252</A> A  5       MWF    930-1020   FSH  102      Open    133/ 150
        """
        
        try:
            result = _parse_section_row(incomplete_row)
            # Should handle missing instructor gracefully
            # assert result['instructor'] == "" or result['instructor'] is None
        except NotImplementedError:
            pytest.skip("Function not yet implemented")


if __name__ == "__main__":
    # Run tests with: python -m pytest tests/test_parser.py -v
    # Or run individual tests: python -m pytest tests/test_parser.py::TestParserFunctions::test_html_file_exists -v
    pytest.main([__file__, "-v"])
