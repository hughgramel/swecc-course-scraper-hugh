#!/usr/bin/env python3
"""
Test the parser functions to see if we're passing data correctly.
"""

from tests.test_blocks import get_test_block
from swecc_course_scraper.commands.parser import _parse_course_header, _parse_course_sections

def test_parser_functions():
    """Test both parser functions with debug output."""
    print("🧪 TESTING PARSER FUNCTIONS")
    print("=" * 80)
    
    # Test with MATH_WIN_2023 first block
    print("📋 Getting test block...")
    block = get_test_block('MATH_WIN_2023', 0)
    print(f"   Block length: {len(block)} characters")
    print(f"   Block preview: {block[:200]}...")
    print()
    
    # Test header parser
    print("🔍 TESTING HEADER PARSER")
    print("-" * 40)
    header_data = _parse_course_header(block)
    print(f"Header result: {header_data}")
    print()
    
    # Test section parser
    print("🔍 TESTING SECTION PARSER")
    print("-" * 40)
    course_code = header_data.get('code', 'UNKNOWN')
    sections = _parse_course_sections(block, course_code, 'WIN', 2023)
    print(f"Section result: {len(sections)} sections found")
    if sections:
        print(f"First section: {sections[0]}")
    print()
    
    # Test with a different block
    print("🔍 TESTING WITH CHEM_SPR_2021")
    print("-" * 40)
    chem_block = get_test_block('CHEM_SPR_2021', 0)
    print(f"   Block length: {len(chem_block)} characters")
    
    chem_header = _parse_course_header(chem_block)
    print(f"   Header result: {chem_header}")
    
    chem_sections = _parse_course_sections(chem_block, chem_header.get('code', 'UNKNOWN'), 'SPR', 2021)
    print(f"   Section result: {len(chem_sections)} sections found")

if __name__ == "__main__":
    test_parser_functions()
