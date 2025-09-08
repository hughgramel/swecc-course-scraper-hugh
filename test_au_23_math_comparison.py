#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from swecc_course_scraper.commands.parser import _parse_course_meetings
from tests.test_blocks import get_test_block

def test_au_23_math_comparison():
    print("🧪 Testing AUT 2023 MATH - Actual vs Expected Results")
    print("=" * 70)
    
    # Expected results based on the screenshots provided
    expected_results = {
        # MATH 103 sections
        "18069": {
            "meeting_id": "A",
            "credits": "5",
            "meeting_type_code": "",
            "enrl_restr": "",
            "expected_meetings": 1
        },
        
        # MATH 111 sections
        "18070": {
            "meeting_id": "A", 
            "credits": "5",
            "meeting_type_code": "",
            "enrl_restr": "",
            "expected_meetings": 1
        },
        "18071": {
            "meeting_id": "AA",
            "credits": "",
            "meeting_type_code": "QZ",
            "enrl_restr": "",
            "expected_meetings": 1
        },
        "18072": {
            "meeting_id": "AB",
            "credits": "",
            "meeting_type_code": "QZ", 
            "enrl_restr": "",
            "expected_meetings": 1
        },
        "18073": {
            "meeting_id": "AC",
            "credits": "",
            "meeting_type_code": "QZ",
            "enrl_restr": "",
            "expected_meetings": 1
        },
        "18074": {
            "meeting_id": "AD",
            "credits": "",
            "meeting_type_code": "QZ",
            "enrl_restr": "",
            "expected_meetings": 1
        },
        "18075": {
            "meeting_id": "AE",
            "credits": "",
            "meeting_type_code": "QZ",
            "enrl_restr": "",
            "expected_meetings": 1
        },
        "18076": {
            "meeting_id": "AF",
            "credits": "",
            "meeting_type_code": "QZ",
            "enrl_restr": "",
            "expected_meetings": 1
        },
        
        # MATH 125 sections (from block 7)
        "18214": {
            "meeting_id": "A",
            "credits": "5",
            "meeting_type_code": "",
            "enrl_restr": "",
            "expected_meetings": 1
        },
        "18215": {
            "meeting_id": "AA",
            "credits": "",
            "meeting_type_code": "QZ",
            "enrl_restr": "",
            "expected_meetings": 2  # Has multiple meeting times
        },
        "18241": {
            "meeting_id": "D",
            "credits": "5",
            "meeting_type_code": "",
            "enrl_restr": "",
            "time": "to be arranged",
            "expected_meetings": 1
        }
    }
    
    try:
        # Test with MATH AUT 2023 Block 7 (MATH 125)
        print("\n📚 Testing MATH AUT 2023 Block 7 (MATH 125):")
        print("-" * 50)
        
        block = get_test_block('MATH_AUT_2023', 7)
        meetings = _parse_course_meetings(block, 'MATH 125', 'AUT', 2023)
        
        print(f"✅ Found {len(meetings)} total meeting objects")
        print()
        
        # Group meetings by SLN
        meetings_by_sln = {}
        for meeting in meetings:
            if meeting.sln not in meetings_by_sln:
                meetings_by_sln[meeting.sln] = []
            meetings_by_sln[meeting.sln].append(meeting)
        
        # Compare with expected results
        print("📊 Comparison Results:")
        print()
        
        for sln, expected in expected_results.items():
            if sln in meetings_by_sln:
                actual_meetings = meetings_by_sln[sln]
                actual_count = len(actual_meetings)
                expected_count = expected["expected_meetings"]
                
                print(f"SLN {sln}:")
                print(f"  Expected meetings: {expected_count}")
                print(f"  Actual meetings: {actual_count}")
                
                if actual_count == expected_count:
                    print("  ✅ Meeting count matches")
                else:
                    print("  ❌ Meeting count mismatch")
                
                # Check first meeting details
                if actual_meetings:
                    first_meeting = actual_meetings[0]
                    
                    # Check meeting ID
                    if first_meeting.meeting_id == expected["meeting_id"]:
                        print(f"  ✅ Meeting ID: {first_meeting.meeting_id}")
                    else:
                        print(f"  ❌ Meeting ID: expected '{expected['meeting_id']}', got '{first_meeting.meeting_id}'")
                    
                    # Check credits
                    if first_meeting.credits == expected["credits"]:
                        print(f"  ✅ Credits: '{first_meeting.credits}'")
                    else:
                        print(f"  ❌ Credits: expected '{expected['credits']}', got '{first_meeting.credits}'")
                    
                    # Check meeting type code
                    if first_meeting.meeting_type_code == expected["meeting_type_code"]:
                        print(f"  ✅ Meeting Type Code: '{first_meeting.meeting_type_code}'")
                    else:
                        print(f"  ❌ Meeting Type Code: expected '{expected['meeting_type_code']}', got '{first_meeting.meeting_type_code}'")
                    
                    # Check enrollment restriction
                    if first_meeting.enrl_restr == expected["enrl_restr"]:
                        print(f"  ✅ Enrollment Restriction: '{first_meeting.enrl_restr}'")
                    else:
                        print(f"  ❌ Enrollment Restriction: expected '{expected['enrl_restr']}', got '{first_meeting.enrl_restr}'")
                    
                    # Check time for special cases
                    if "time" in expected:
                        if first_meeting.time == expected["time"]:
                            print(f"  ✅ Time: '{first_meeting.time}'")
                        else:
                            print(f"  ❌ Time: expected '{expected['time']}', got '{first_meeting.time}'")
                    
                    # Show additional details
                    print(f"  📋 Details: {first_meeting.meeting_date} {first_meeting.time} {first_meeting.building} {first_meeting.room}")
                    print(f"  👨‍🏫 Instructor: {first_meeting.instructor}")
                    print(f"  📊 Status: {first_meeting.status} ({first_meeting.enrolled}/{first_meeting.capacity})")
                    print(f"  📝 Description: {first_meeting.description}")
                    
                    # Show additional meetings if any
                    if len(actual_meetings) > 1:
                        print(f"  🔄 Additional meetings:")
                        for i, meeting in enumerate(actual_meetings[1:], 1):
                            print(f"    {i}. {meeting.meeting_id}: {meeting.meeting_date} {meeting.time} {meeting.building} {meeting.room}")
                
                print()
            else:
                print(f"SLN {sln}: ❌ Not found in parsed results")
                print()
        
        # Summary
        print("📈 Summary:")
        total_expected = sum(expected["expected_meetings"] for expected in expected_results.values())
        total_actual = len(meetings)
        print(f"  Total expected meetings: {total_expected}")
        print(f"  Total actual meetings: {total_actual}")
        
        if total_actual == total_expected:
            print("  ✅ Total meeting count matches expected")
        else:
            print("  ❌ Total meeting count mismatch")
            
    except Exception as e:
        print(f"❌ Error in comparison test: {e}")
        import traceback
        traceback.print_exc()

def test_enrollment_restrictions():
    print("\n🔍 Testing Enrollment Restrictions:")
    print("-" * 40)
    
    try:
        block = get_test_block('MATH_AUT_2023', 7)
        meetings = _parse_course_meetings(block, 'MATH 125', 'AUT', 2023)
        
        # Check for enrollment restrictions
        restrictions_found = {}
        for meeting in meetings:
            if meeting.enrl_restr:
                if meeting.enrl_restr not in restrictions_found:
                    restrictions_found[meeting.enrl_restr] = []
                restrictions_found[meeting.enrl_restr].append(meeting.sln)
        
        if restrictions_found:
            print("✅ Found enrollment restrictions:")
            for restriction, slns in restrictions_found.items():
                print(f"  '{restriction}': SLNs {slns}")
        else:
            print("ℹ️  No enrollment restrictions found (all empty)")
            
    except Exception as e:
        print(f"❌ Error testing enrollment restrictions: {e}")

if __name__ == "__main__":
    test_au_23_math_comparison()
    test_enrollment_restrictions()
    print("\n🎉 Comparison tests completed!")

