#!/usr/bin/env python3
"""
Test the parser functions with print statements.
"""

from tests.test_blocks import get_test_block
from swecc_course_scraper.commands.parser import _parse_course_header, _parse_course_sections

def test_header_parser():
    """Test the header parser function."""
    print("🧪 TESTING HEADER PARSER")
    print("=" * 80)
    
    # Test with MATH_WIN_2023 first block
    block = get_test_block('MATH_WIN_2023', 0)
    print(f"Testing with MATH_WIN_2023 block 0 ({len(block)} characters)")
    
    header_data = _parse_course_header(block)
    print(f"\n📊 HEADER PARSER RESULT:")
    print(f"   Type: {type(header_data)}")
    print(f"   Keys: {list(header_data.keys()) if isinstance(header_data, dict) else 'N/A'}")
    print(f"   Values: {header_data}")
    
    return header_data

def test_section_parser():
    """Test the section parser function."""
    print("\n🧪 TESTING SECTION PARSER")
    print("=" * 80)
    
    # Test with MATH_WIN_2023 first block
    block = get_test_block('MATH_WIN_2023', 0)
    print(f"Testing with MATH_WIN_2023 block 0 ({len(block)} characters)")
    
    # Get course code from header first
    header_data = _parse_course_header(block)
    course_code = header_data.get('code', 'UNKNOWN')
    
    sections = _parse_course_sections(block, course_code, 'WIN', 2023)
    print(f"\n📊 SECTION PARSER RESULT:")
    print(f"   Type: {type(sections)}")
    print(f"   Count: {len(sections)}")
    print(f"   Section types: {[type(s).__name__ for s in sections]}")
    
    if sections:
        print(f"   First section: {sections[0]}")
    
    return sections

def test_multiple_blocks():
    """Test with multiple blocks from different files."""
    print("\n🧪 TESTING MULTIPLE BLOCKS")
    print("=" * 80)
    
    test_cases = [
        ('MATH_WIN_2023', 0, 'WIN', 2023),
        ('MATH_SPR_2021', 0, 'SPR', 2021),
        ('CHEM_SPR_2021', 0, 'SPR', 2021),
    ]
    
    for file_name, block_index, quarter, year in test_cases:
        print(f"\n--- Testing {file_name} block {block_index} ---")
        block = get_test_block(file_name, block_index)
        
        # Test header
        header_data = _parse_course_header(block)
        course_code = header_data.get('code', 'UNKNOWN')
        
        # Test sections
        sections = _parse_course_sections(block, course_code, quarter, year)
        
        print(f"✅ {file_name}: {course_code} - {len(sections)} sections")

if __name__ == "__main__":
    # Test header parser
    header_result = test_header_parser()
    
    # Test section parser
    section_result = test_section_parser()
    
    # Test multiple blocks
    test_multiple_blocks()
    
    print("\n🎯 SUMMARY")
    print("=" * 80)
    print("Header parser returns:", type(header_result).__name__)
    print("Section parser returns:", type(section_result).__name__)
    print("Ready for next phase!")
