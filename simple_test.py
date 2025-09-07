#!/usr/bin/env python3
"""
Simple test of the parser functions.
"""

from tests.test_blocks import get_test_block
from swecc_course_scraper.commands.parser import _parse_course_header, _parse_course_sections

# Test with CHEM_SPR_2021 first block
block = get_test_block('CHEM_SPR_2021', 0)
print(f"Block length: {len(block)} characters")

# Test header parser
print("\n=== HEADER PARSER ===")
header_data = _parse_course_header(block)
print(f"Header result: {header_data}")

# Test section parser
print("\n=== SECTION PARSER ===")
course_code = header_data.get('code', 'UNKNOWN')
sections = _parse_course_sections(block, course_code, 'SPR', 2021)
print(f"Found {len(sections)} sections")
