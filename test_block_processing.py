#!/usr/bin/env python3
"""
Test the individual block processing functions to see the data structure.
"""

from tests.test_blocks import get_test_block
from swecc_course_scraper.commands.parser import _parse_course_header, _parse_course_sections

def test_block_processing():
    """Test processing individual course blocks."""
    print("🧪 TESTING BLOCK PROCESSING FUNCTIONS")
    print("=" * 80)
    
    # Test with different blocks from different files
    test_cases = [
        ('MATH_WIN_2023', 0, 'WIN', 2023),
        ('CHEM_SPR_2021', 0, 'SPR', 2021),
        ('MATH_AUT_2023', 0, 'AUT', 2023),
    ]
    
    for file_name, block_index, quarter, year in test_cases:
        print(f"\n{'='*60}")
        print(f"TESTING: {file_name} Block {block_index}")
        print(f"{'='*60}")
        
        # Get the test block
        block = get_test_block(file_name, block_index)
        print(f"📋 Block length: {len(block)} characters")
        
        # Test header parsing
        print(f"\n🔍 PARSING HEADER...")
        header_data = _parse_course_header(block)
        print(f"📊 Header Result:")
        print(f"   Type: {type(header_data)}")
        print(f"   Keys: {list(header_data.keys()) if isinstance(header_data, dict) else 'N/A'}")
        print(f"   Values: {header_data}")
        
        # Test section parsing
        print(f"\n🔍 PARSING SECTIONS...")
        course_code = header_data.get('code', 'UNKNOWN')
        sections = _parse_course_sections(block, course_code, quarter, year)
        print(f"📊 Section Result:")
        print(f"   Type: {type(sections)}")
        print(f"   Count: {len(sections)}")
        print(f"   Section types: {[type(s).__name__ for s in sections]}")
        
        if sections:
            print(f"   First section: {sections[0]}")
            print(f"   First section attributes: {dir(sections[0])}")
        
        print(f"\n✅ {file_name} Block {block_index} processing complete")
        print(f"   Course: {header_data.get('code', 'UNKNOWN')}")
        print(f"   Sections found: {len(sections)}")

def show_data_structure():
    """Show the data structure we're working with."""
    print(f"\n{'='*80}")
    print("DATA STRUCTURE OVERVIEW")
    print(f"{'='*80}")
    
    print("\n📋 HEADER DATA STRUCTURE:")
    print("   _parse_course_header() returns:")
    print("   Dict[str, str] = {")
    print("       'code': 'MATH 103',           # Course code")
    print("       'title': 'INTRO ELEM FUNCTION', # Course title") 
    print("       'prerequisites': '',          # Prerequisites")
    print("       'credits': ''                 # Credits")
    print("   }")
    
    print("\n📋 SECTION DATA STRUCTURE:")
    print("   _parse_course_sections() returns:")
    print("   List[CourseSection] = [")
    print("       CourseSection(")
    print("           sln='17215',              # Student Line Number")
    print("           course_code='MATH 103',   # Course code")
    print("           section_id='A',           # Section ID")
    print("           section_type='5',         # Section type")
    print("           days='MTWThF',            # Days")
    print("           time='1030-1120',         # Time")
    print("           building='ICT',           # Building")
    print("           room='226',               # Room")
    print("           instructor='Skov,Christopher', # Instructor")
    print("           status='Open',            # Status")
    print("           enrolled=15,              # Enrolled count")
    print("           capacity=30,              # Capacity")
    print("           quarter='WIN',            # Quarter")
    print("           year=2023,                # Year")
    print("           notes=None                # Notes")
    print("       ),")
    print("       # ... more sections")
    print("   ]")
    
    print("\n📋 FINAL COURSE OBJECT STRUCTURE:")
    print("   parse_schedule_html() should return:")
    print("   List[Course] = [")
    print("       Course(")
    print("           course_code='MATH 103',   # From header")
    print("           title='INTRO ELEM FUNCTION', # From header")
    print("           prerequisites='',         # From header")
    print("           credits='',               # From header")
    print("           quarter='WIN',            # Parameter")
    print("           year=2023,                # Parameter")
    print("           sections=[...]            # From _parse_course_sections()")
    print("       ),")
    print("       # ... more courses")
    print("   ]")

if __name__ == "__main__":
    test_block_processing()
    show_data_structure()
