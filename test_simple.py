#!/usr/bin/env python3

print("Testing basic execution...")

try:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from swecc_course_scraper.commands.parser import parse_schedule_html
    
    print("Parser imported successfully")
    
    # Test with a small file
    with open('tests/test_files/math_AUT_2023.html', 'r') as f:
        html = f.read()
    
    print(f"HTML loaded: {len(html)} characters")
    
    courses = parse_schedule_html(html, "AUT", 2023)
    print(f"Parsed {len(courses)} courses")
    
    if courses:
        print(f"First course: {courses[0].course_code}")
        print(f"First course meetings: {len(courses[0].meetings)}")
        if courses[0].meetings:
            meeting = courses[0].meetings[0]
            print(f"First meeting SLN: {meeting.sln}")
            print(f"First meeting enrl_restr: '{meeting.enrl_restr}'")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
