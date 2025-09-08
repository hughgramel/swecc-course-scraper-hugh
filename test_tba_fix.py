#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from swecc_course_scraper.commands.parser import parse_schedule_html

def test_to_be_arranged_fix():
    print("🧪 Testing 'to be arranged' fix...")
    
    # Load the full test file that contains SLN 18241
    with open('tests/test_files/math_AUT_2023.html', 'r') as f:
        html = f.read()
    
    # Parse the HTML
    courses = parse_schedule_html(html, "AUT", 2023)
    
    # Find SLN 18241
    found_18241 = False
    for course in courses:
        for meeting in course.meetings:
            if meeting.sln == "18241":
                found_18241 = True
                print(f"✅ Found SLN 18241!")
                print(f"   Meeting ID: {meeting.meeting_id}")
                print(f"   Credits: {meeting.credits}")
                print(f"   Time: {meeting.time}")
                print(f"   Building: {meeting.building}")
                print(f"   Room: {meeting.room}")
                print(f"   Instructor: {meeting.instructor}")
                print(f"   Status: {meeting.status}")
                print(f"   Enrollment: {meeting.enrolled}/{meeting.capacity}")
                print(f"   Additional Code: {meeting.additional_code}")
                print(f"   Description: {meeting.description}")
                break
        if found_18241:
            break
    
    if not found_18241:
        print("❌ SLN 18241 not found - fix didn't work")
        return False
    
    print("✅ 'To be arranged' fix successful!")
    return True

if __name__ == "__main__":
    test_to_be_arranged_fix()
