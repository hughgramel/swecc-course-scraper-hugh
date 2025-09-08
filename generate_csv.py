#!/usr/bin/env python3

import sys
import os
import csv
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def generate_csv():
    print("Generating CSV for MATH AUT 2023...")
    
    try:
        from swecc_course_scraper.commands.parser import parse_schedule_html
    except Exception as e:
        print(f"Import error: {e}")
        return False
    
    # Read the HTML file
    html_file = 'tests/test_files/math_AUT_2023.html'
    if not os.path.exists(html_file):
        print(f"HTML file not found: {html_file}")
        return False
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse the schedule
    courses = parse_schedule_html(html_content, "AUT", 2023)
    
    # Flatten all meetings
    all_meetings = []
    for course in courses:
        all_meetings.extend(course.meetings)
    
    # Generate CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = f'output/math_aut_2023_meetings_{timestamp}.csv'
    
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)
    
    # Write CSV
    fieldnames = ['sln', 'course_code', 'meeting_id', 'meeting_type_code', 'credits', 'meeting_date', 'time', 'building', 'room', 'instructor', 'status', 'enrolled', 'capacity', 'current_capacity', 'quarter', 'year', 'meeting_times', 'notes', 'description', 'additional_code', 'enrl_restr', 'estimated_enrollment']
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for meeting in all_meetings:
            meeting_data = {
                'sln': meeting.sln,
                'course_code': meeting.course_code,
                'meeting_id': meeting.meeting_id,
                'meeting_type_code': meeting.meeting_type_code,
                'credits': meeting.credits,
                'meeting_date': meeting.meeting_date,
                'time': meeting.time,
                'building': meeting.building,
                'room': meeting.room,
                'instructor': meeting.instructor,
                'status': meeting.status,
                'enrolled': meeting.enrolled,
                'capacity': meeting.capacity,
                'current_capacity': meeting.current_capacity,
                'quarter': meeting.quarter,
                'year': meeting.year,
                'meeting_times': meeting.meeting_times,
                'notes': meeting.notes,
                'description': meeting.description,
                'additional_code': meeting.additional_code,
                'enrl_restr': meeting.enrl_restr,
                'estimated_enrollment': meeting.estimated_enrollment
            }
            writer.writerow(meeting_data)
    
    print(f"CSV generated: {csv_file}")
    print(f"Total meetings: {len(all_meetings)}")
    
    # Validation
    with open(csv_file, 'r', encoding='utf-8') as f:
        csv_lines = f.readlines()
        csv_row_count = len(csv_lines) - 1  # Subtract header
    
    print(f"Validation: {len(all_meetings)} meetings = {csv_row_count} CSV rows")
    
    if len(all_meetings) == csv_row_count:
        print("✅ VALIDATION PASSED")
    else:
        print("❌ VALIDATION FAILED")
    
    # Statistics
    lectures = len([m for m in all_meetings if m.meeting_type_code == ''])
    quizzes = len([m for m in all_meetings if m.meeting_type_code == 'QZ'])
    with_estimated = len([m for m in all_meetings if m.estimated_enrollment])
    with_restr = len([m for m in all_meetings if m.enrl_restr])
    
    print(f"Statistics: {lectures} lectures, {quizzes} quizzes, {with_estimated} estimated, {with_restr} restricted")
    
    return csv_file

if __name__ == "__main__":
    generate_csv()
