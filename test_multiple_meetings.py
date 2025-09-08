#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from swecc_course_scraper.commands.parser import _parse_course_meetings
from tests.test_blocks import get_test_block

def test_multiple_meetings():
    print("🧪 Testing Multiple Meeting Objects Approach")
    print("=" * 60)
    
    # Test with MATH AUT 2023 Block 7 (has multiple meeting times)
    print("\n📚 Testing MATH AUT 2023 Block 7 (Multiple Meeting Times):")
    print("-" * 50)
    
    try:
        block = get_test_block('MATH_AUT_2023', 7)
        meetings = _parse_course_meetings(block, 'MATH 125', 'AUT', 2023)
        
        print(f"✅ Found {len(meetings)} total meeting objects")
        print()
        
        # Group meetings by SLN to see how multiple times are handled
        meetings_by_sln = {}
        for meeting in meetings:
            if meeting.sln not in meetings_by_sln:
                meetings_by_sln[meeting.sln] = []
            meetings_by_sln[meeting.sln].append(meeting)
        
        print("📊 Meeting Objects by SLN:")
        for sln, sln_meetings in meetings_by_sln.items():
            print(f"  SLN {sln}: {len(sln_meetings)} meeting object(s)")
            for i, meeting in enumerate(sln_meetings):
                print(f"    {i+1}. ID: {meeting.meeting_id}, Time: {meeting.time}, Building: {meeting.building}, Room: {meeting.room}")
        
        print()
        
        # Test specific cases
        print("🔍 Detailed Analysis:")
        
        # Find a section with multiple meeting times
        multi_time_sections = {sln: meetings for sln, meetings in meetings_by_sln.items() if len(meetings) > 1}
        
        if multi_time_sections:
            print(f"✅ Found {len(multi_time_sections)} sections with multiple meeting times")
            
            # Show first multi-time section
            first_sln = list(multi_time_sections.keys())[0]
            first_meetings = multi_time_sections[first_sln]
            
            print(f"\n📋 Example: SLN {first_sln} ({len(first_meetings)} meeting objects):")
            for i, meeting in enumerate(first_meetings):
                print(f"  Meeting {i+1}:")
                print(f"    Meeting ID: {meeting.meeting_id}")
                print(f"    Meeting Date: {meeting.meeting_date}")
                print(f"    Time: {meeting.time}")
                print(f"    Building: {meeting.building}")
                print(f"    Room: {meeting.room}")
                print(f"    Instructor: {meeting.instructor}")
                print(f"    Status: {meeting.status}")
                print(f"    Enrollment: {meeting.enrolled}/{meeting.capacity}")
                print(f"    Description: {meeting.description}")
                print()
        else:
            print("ℹ️  No sections with multiple meeting times found in this block")
        
        # Test "to be arranged" case
        arranged_meetings = [m for m in meetings if m.time == "to be arranged"]
        if arranged_meetings:
            print(f"✅ Found {len(arranged_meetings)} 'to be arranged' meeting(s)")
            for meeting in arranged_meetings:
                print(f"  SLN {meeting.sln}: {meeting.meeting_id} - {meeting.time}")
                print(f"    Instructor: {meeting.instructor}")
                print(f"    Description: {meeting.description}")
        else:
            print("ℹ️  No 'to be arranged' meetings found in this block")
            
    except Exception as e:
        print(f"❌ Error testing MATH AUT 2023 Block 7: {e}")
        import traceback
        traceback.print_exc()

def test_simple_meetings():
    print("\n📚 Testing MATH SPR 2021 Block 1 (Simple Case):")
    print("-" * 50)
    
    try:
        block = get_test_block('MATH_SPR_2021', 1)
        meetings = _parse_course_meetings(block, 'MATH 112', 'SPR', 2021)
        
        print(f"✅ Found {len(meetings)} total meeting objects")
        print()
        
        # Show all meetings
        for i, meeting in enumerate(meetings):
            print(f"Meeting {i+1}:")
            print(f"  SLN: {meeting.sln}")
            print(f"  Meeting ID: {meeting.meeting_id}")
            print(f"  Credits: '{meeting.credits}'")
            print(f"  Meeting Type Code: '{meeting.meeting_type_code}'")
            print(f"  Meeting Date: '{meeting.meeting_date}'")
            print(f"  Time: '{meeting.time}'")
            print(f"  Building: {meeting.building}")
            print(f"  Room: {meeting.room}")
            print(f"  Instructor: '{meeting.instructor}'")
            print(f"  Status: {meeting.status}")
            print(f"  Enrollment: {meeting.enrolled}/{meeting.capacity}")
            print(f"  Additional Code: '{meeting.additional_code}'")
            print(f"  Meeting Classification: {meeting.meeting_classification}")
            print(f"  Description: '{meeting.description}'")
            print()
            
    except Exception as e:
        print(f"❌ Error testing MATH SPR 2021 Block 1: {e}")
        import traceback
        traceback.print_exc()

def test_data_consistency():
    print("\n🔍 Testing Data Consistency:")
    print("-" * 30)
    
    try:
        # Test with a block that has multiple meeting times
        block = get_test_block('MATH_AUT_2023', 7)
        meetings = _parse_course_meetings(block, 'MATH 125', 'AUT', 2023)
        
        # Group by SLN
        meetings_by_sln = {}
        for meeting in meetings:
            if meeting.sln not in meetings_by_sln:
                meetings_by_sln[meeting.sln] = []
            meetings_by_sln[meeting.sln].append(meeting)
        
        print("✅ Data Consistency Checks:")
        
        for sln, sln_meetings in meetings_by_sln.items():
            if len(sln_meetings) > 1:
                # Check that all meetings for the same SLN have consistent data
                first_meeting = sln_meetings[0]
                
                consistent_fields = [
                    'sln', 'course_code', 'meeting_type_code', 'credits', 
                    'status', 'enrolled', 'capacity', 'description', 'additional_code'
                ]
                
                for field in consistent_fields:
                    values = [getattr(m, field) for m in sln_meetings]
                    if len(set(values)) > 1:
                        print(f"  ⚠️  SLN {sln}: Inconsistent {field}: {values}")
                    else:
                        print(f"  ✅ SLN {sln}: Consistent {field}: {values[0]}")
                
                # Check that meeting IDs are unique
                meeting_ids = [m.meeting_id for m in sln_meetings]
                if len(set(meeting_ids)) == len(meeting_ids):
                    print(f"  ✅ SLN {sln}: Unique meeting IDs: {meeting_ids}")
                else:
                    print(f"  ❌ SLN {sln}: Duplicate meeting IDs: {meeting_ids}")
                
                break  # Only check first multi-meeting section
        
    except Exception as e:
        print(f"❌ Error in data consistency test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_multiple_meetings()
    test_simple_meetings()
    test_data_consistency()
    print("\n🎉 All tests completed!")
