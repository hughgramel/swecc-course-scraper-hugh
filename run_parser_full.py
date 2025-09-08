#!/usr/bin/env python3

import sys
import os
import csv
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from swecc_course_scraper.commands.parser import parse_schedule_html

def run_parser_full(quarter="AUT", year=2023, subject="MATH"):
    """Run the parser on the specified quarter/year/subject and generate full CSV output."""
    print(f"🚀 Running Parser on {subject} {quarter} {year}")
    print("=" * 60)
    
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)
    
    # Construct file path
    file_path = f'tests/test_files/{subject.lower()}_{quarter}_{year}.html'
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    print(f"📁 Loading: {file_path}")
    
    try:
        with open(file_path, 'r') as f:
            html = f.read()
        
        print(f"📄 HTML loaded: {len(html)} characters")
        
        # Parse the HTML
        print(f"🔍 Parsing {subject} {quarter} {year}...")
        courses = parse_schedule_html(html, quarter, year)
        
        print(f"✅ Parsed {len(courses)} courses with {sum(len(course.meetings) for course in courses)} total meetings")
        
        # Generate timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Prepare data for CSV files
        all_courses = []
        all_meetings = []
        
        for course in courses:
            # Course data
            course_data = {
                'course_code': course.course_code,
                'title': course.title,
                'prerequisites': course.prerequisites,
                'credits': course.credits,
                'credit_types': course.credit_types,
                'quarter': course.quarter,
                'year': course.year,
                'meeting_count': len(course.meetings)
            }
            all_courses.append(course_data)
            
            # Meeting data
            for meeting in course.meetings:
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
                all_meetings.append(meeting_data)
        
        # Generate CSV file (meetings only)
        print(f"\n📝 Generating CSV file...")
        
        # Meetings CSV only
        meetings_file = f'output/{subject.lower()}_{quarter.lower()}_{year}_meetings_{timestamp}.csv'
        print(f"   Creating: {meetings_file}")
        
        with open(meetings_file, 'w', newline='', encoding='utf-8') as f:
            # Remove duplicate fields - only keep unique fields
            fieldnames = ['sln', 'course_code', 'meeting_id', 'meeting_type_code', 'credits', 'meeting_date', 'time', 'building', 'room', 'instructor', 'status', 'enrolled', 'capacity', 'current_capacity', 'quarter', 'year', 'meeting_times', 'notes', 'description', 'additional_code', 'enrl_restr', 'estimated_enrollment']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_meetings)
        
        # Print results summary
        print(f"\n🎯 PARSING COMPLETE!")
        print(f"   Subject: {subject}")
        print(f"   Quarter: {quarter} {year}")
        print(f"   Total Courses: {len(all_courses)}")
        print(f"   Total Meetings: {len(all_meetings)}")
        print(f"\n📁 File Created:")
        print(f"   - {meetings_file}")
        
        # Validation: Check CSV row count matches meeting count
        print(f"\n🔍 VALIDATION:")
        print(f"   Parsed meetings: {len(all_meetings)}")
        
        # Count CSV rows (excluding header)
        with open(meetings_file, 'r', encoding='utf-8') as f:
            csv_lines = f.readlines()
            csv_row_count = len(csv_lines) - 1  # Subtract header row
            print(f"   CSV rows: {csv_row_count}")
        
        if len(all_meetings) == csv_row_count:
            print(f"   ✅ VALIDATION PASSED: Meeting count matches CSV row count")
        else:
            print(f"   ❌ VALIDATION FAILED: Meeting count ({len(all_meetings)}) != CSV row count ({csv_row_count})")
        
        # Show some key statistics
        print(f"\n📊 Key Statistics:")
        lectures = len([m for m in all_meetings if m['meeting_type_code'] == ''])
        quizzes = len([m for m in all_meetings if m['meeting_type_code'] == 'QZ'])
        labs = len([m for m in all_meetings if m['meeting_type_code'] == 'LB'])
        tba = len([m for m in all_meetings if m['time'] == 'to be arranged'])
        with_codes = len([m for m in all_meetings if m['additional_code']])
        with_restr = len([m for m in all_meetings if m['enrl_restr']])
        with_estimated = len([m for m in all_meetings if m['estimated_enrollment']])
        
        print(f"   - Lectures: {lectures}")
        print(f"   - Quizzes: {quizzes}")
        print(f"   - Labs: {labs}")
        print(f"   - 'To be arranged': {tba}")
        print(f"   - With additional codes: {with_codes}")
        print(f"   - With enrollment restrictions: {with_restr}")
        print(f"   - With estimated enrollment: {with_estimated}")
        
        # Show sample of courses
        print(f"\n📚 Sample Courses:")
        for i, course in enumerate(all_courses[:5]):  # Show first 5 courses
            print(f"   {i+1}. {course['course_code']}: {course['title']} ({course['meeting_count']} meetings)")
        
        if len(all_courses) > 5:
            print(f"   ... and {len(all_courses) - 5} more courses")
        
        return {
            'meetings_file': meetings_file,
            'total_courses': len(all_courses),
            'total_meetings': len(all_meetings)
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Default to MATH AUT 2023, but allow command line arguments
    quarter = sys.argv[1] if len(sys.argv) > 1 else "AUT"
    year = int(sys.argv[2]) if len(sys.argv) > 2 else 2023
    subject = sys.argv[3] if len(sys.argv) > 3 else "MATH"
    
    result = run_parser_full(quarter, year, subject)
    
    if result:
        print(f"\n✅ Success! Check the output/ directory for your CSV files.")
    else:
        print(f"\n❌ Failed to generate CSV files.")
