#!/usr/bin/env python3

import os
import sys

# Add the project to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from swecc_course_scraper.commands.parser import parse_schedule_html

def test_simple():
    print("🧪 Testing simple parser functionality...")
    
    # Read a small test file
    test_file = 'tests/test_files/math_AUT_2023.html'
    
    try:
        with open(test_file, 'r') as f:
            html = f.read()
        
        print(f"📄 Read {len(html)} characters from {test_file}")
        
        # Parse the full HTML
        courses = parse_schedule_html(html, "AUT", 2023)  # Full HTML
        
        print(f"✅ Successfully parsed {len(courses)} courses")
        
        for course in courses[:3]:  # Show first 3 courses
            print(f"   Course: {course.course_code} - {len(course.meetings)} meetings")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple()
