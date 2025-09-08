#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from swecc_course_scraper.commands.parser import _parse_course_meetings
from tests.test_blocks import get_test_block

def test_to_be_arranged():
    print("🧪 Testing 'To Be Arranged' Meeting Times")
    print("=" * 50)
    
    try:
        # Test with MATH AUT 2023 Block 7 which has "to be arranged" meetings
        block = get_test_block('MATH_AUT_2023', 7)
        meetings = _parse_course_meetings(block, 'MATH 125', 'AUT', 2023)
        
        print(f"✅ Found {len(meetings)} total meeting objects")
        print()
        
        # Find "to be arranged" meetings
        arranged_meetings = [m for m in meetings if m.time == "to be arranged"]
        
        if arranged_meetings:
            print(f"✅ Found {len(arranged_meetings)} 'to be arranged' meeting(s):")
            print()
            
            for i, meeting in enumerate(arranged_meetings):
                print(f"Meeting {i+1} (SLN: {meeting.sln}):")
                print(f"  Meeting ID: {meeting.meeting_id}")
                print(f"  Credits: '{meeting.credits}'")
                print(f"  Meeting Type Code: '{meeting.meeting_type_code}'")
                print(f"  Meeting Date: '{meeting.meeting_date}'")
                print(f"  Time: '{meeting.time}'")
                print(f"  Building: '{meeting.building}'")
                print(f"  Room: '{meeting.room}'")
                print(f"  Instructor: '{meeting.instructor}'")
                print(f"  Status: {meeting.status}")
                print(f"  Enrollment: {meeting.enrolled}/{meeting.capacity}")
                print(f"  Additional Code: '{meeting.additional_code}'")
                print(f"  Meeting Classification: {meeting.meeting_classification}")
                print(f"  Description: '{meeting.description}'")
                print()
                
                # Verify that building and room are empty for "to be arranged"
                if meeting.building == "" and meeting.room == "":
                    print("  ✅ Building and room correctly empty for 'to be arranged'")
                else:
                    print(f"  ❌ Building and room should be empty but got: building='{meeting.building}', room='{meeting.room}'")
                print()
        else:
            print("ℹ️  No 'to be arranged' meetings found in this block")
            
        # Test regular meetings for comparison
        regular_meetings = [m for m in meetings if m.time != "to be arranged"]
        if regular_meetings:
            print(f"📊 Regular meetings (non-'to be arranged'): {len(regular_meetings)}")
            print("  Sample regular meeting:")
            sample = regular_meetings[0]
            print(f"    SLN: {sample.sln}")
            print(f"    Time: {sample.time}")
            print(f"    Building: {sample.building}")
            print(f"    Room: {sample.room}")
            
    except Exception as e:
        print(f"❌ Error testing 'to be arranged' meetings: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_to_be_arranged()
