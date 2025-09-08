#!/usr/bin/env python3

# Simple test to verify the parser works
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_parser():
    try:
        print("Testing parser import...")
        from swecc_course_scraper.commands.parser import _parse_course_meetings
        from tests.test_blocks import get_test_block
        print("✓ Imports successful")
        
        print("Loading test block...")
        block = get_test_block('MATH_AUT_2023', 7)
        print("✓ Block loaded")
        
        print("Parsing meetings...")
        meetings = _parse_course_meetings(block, 'MATH 125', 'AUT', 2023)
        print(f"✓ Found {len(meetings)} meetings")
        
        if meetings:
            print("\nFirst few meetings:")
            for i, m in enumerate(meetings[:3]):
                print(f"  {i+1}. SLN: {m.sln}, ID: {m.meeting_id}")
                print(f"     Credits: '{m.credits}', Type: '{m.meeting_type_code}'")
                print(f"     Time: {m.time}, Building: {m.building}, Room: {m.room}")
                print(f"     Instructor: {m.instructor}")
                print(f"     Status: {m.status} ({m.enrolled}/{m.capacity})")
                print(f"     Enrl Restr: '{m.enrl_restr}'")
                print(f"     Additional Code: '{m.additional_code}'")
                print(f"     Description: '{m.description}'")
                print()
        
        print("✅ Parser test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_parser()

