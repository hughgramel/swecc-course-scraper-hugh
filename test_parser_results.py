#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_parser_and_write_results():
    """Test the parser and write results to a file for analysis"""
    
    results_file = "parser_test_results.txt"
    
    try:
        with open(results_file, 'w') as f:
            f.write("🧪 Parser Test Results\n")
            f.write("=" * 50 + "\n\n")
            
            # Test imports
            f.write("Testing imports...\n")
            try:
                from swecc_course_scraper.commands.parser import _parse_course_meetings
                from tests.test_blocks import get_test_block
                f.write("✅ Imports successful\n\n")
            except Exception as e:
                f.write(f"❌ Import failed: {e}\n\n")
                return
            
            # Test MATH AUT 2023 Block 7
            f.write("Testing MATH AUT 2023 Block 7...\n")
            try:
                block = get_test_block('MATH_AUT_2023', 7)
                f.write("✅ Block loaded successfully\n")
                
                meetings = _parse_course_meetings(block, 'MATH 125', 'AUT', 2023)
                f.write(f"✅ Found {len(meetings)} total meeting objects\n\n")
                
                # Group by SLN
                meetings_by_sln = {}
                for meeting in meetings:
                    if meeting.sln not in meetings_by_sln:
                        meetings_by_sln[meeting.sln] = []
                    meetings_by_sln[meeting.sln].append(meeting)
                
                f.write("📊 Results by SLN:\n")
                for sln, sln_meetings in meetings_by_sln.items():
                    f.write(f"  SLN {sln}: {len(sln_meetings)} meeting object(s)\n")
                    for i, meeting in enumerate(sln_meetings):
                        f.write(f"    {i+1}. ID: {meeting.meeting_id}, Time: {meeting.time}\n")
                        f.write(f"       Building: {meeting.building}, Room: {meeting.room}\n")
                        f.write(f"       Instructor: {meeting.instructor}\n")
                        f.write(f"       Status: {meeting.status} ({meeting.enrolled}/{meeting.capacity})\n")
                        f.write(f"       Credits: '{meeting.credits}', Type: '{meeting.meeting_type_code}'\n")
                        f.write(f"       Enrl Restr: '{meeting.enrl_restr}'\n")
                        f.write(f"       Additional Code: '{meeting.additional_code}'\n")
                        f.write(f"       Description: '{meeting.description}'\n")
                        f.write("\n")
                
                # Expected results comparison
                f.write("📋 Expected vs Actual Comparison:\n")
                expected_results = {
                    "18214": 1,  # A lecture
                    "18215": 2,  # AA quiz with multiple times
                    "18216": 2,  # AB quiz with multiple times
                    "18223": 1,  # B lecture
                    "18224": 2,  # BA quiz with multiple times
                    "18232": 1,  # C lecture
                    "18241": 1,  # D lecture, to be arranged
                }
                
                for sln, expected_count in expected_results.items():
                    actual_count = len(meetings_by_sln.get(sln, []))
                    status = "✅" if actual_count == expected_count else "❌"
                    f.write(f"  {status} SLN {sln}: Expected {expected_count}, Got {actual_count}\n")
                
                # Check for "to be arranged" meetings
                arranged_meetings = [m for m in meetings if m.time == "to be arranged"]
                f.write(f"\n🔍 'To be arranged' meetings: {len(arranged_meetings)}\n")
                for meeting in arranged_meetings:
                    f.write(f"  SLN {meeting.sln}: {meeting.meeting_id} - {meeting.time}\n")
                    f.write(f"    Building: '{meeting.building}', Room: '{meeting.room}'\n")
                
                # Check for additional codes
                meetings_with_codes = [m for m in meetings if m.additional_code]
                f.write(f"\n🔍 Meetings with additional codes: {len(meetings_with_codes)}\n")
                for meeting in meetings_with_codes:
                    f.write(f"  SLN {meeting.sln}: Additional code '{meeting.additional_code}'\n")
                
                f.write("\n✅ Parser test completed successfully!\n")
                
            except Exception as e:
                f.write(f"❌ Parser test failed: {e}\n")
                import traceback
                f.write(traceback.format_exc())
        
        print(f"✅ Test results written to {results_file}")
        
    except Exception as e:
        print(f"❌ Failed to write test results: {e}")

if __name__ == "__main__":
    test_parser_and_write_results()

