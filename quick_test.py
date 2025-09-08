#!/usr/bin/env python3

import sys
import os

# Add the project to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from swecc_course_scraper.commands.parser import parse_schedule_html

def quick_test():
    print("🧪 Quick test of parser...")
    
    # Read the test file
    test_file = 'tests/test_files/math_AUT_2023.html'
    
    try:
        with open(test_file, 'r') as f:
            html = f.read()
        
        print(f"📄 Read {len(html)} characters")
        
        # Parse the HTML
        courses = parse_schedule_html(html, "AUT", 2023)
        
        print(f"✅ Successfully parsed {len(courses)} courses")
        
        if courses:
            total_meetings = sum(len(course.meetings) for course in courses)
            print(f"   Total meetings: {total_meetings}")
            
            # Show first few courses
            for i, course in enumerate(courses[:3]):
                print(f"   {i+1}. {course.course_code}: {len(course.meetings)} meetings")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = quick_test()
    if success:
        print("\n✅ Test passed!")
    else:
        print("\n❌ Test failed!")