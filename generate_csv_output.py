#!/usr/bin/env python3

import sys
import os
import csv
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from swecc_course_scraper.commands.parser import parse_schedule_html

def generate_csv_output():
    """Generate CSV files from parsed course data."""
    print("📊 Generating CSV Output")
    print("=" * 50)
    
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)
    
    # Test files to process
    test_files = [
        ('tests/test_files/math_AUT_2023.html', 'AUT', 2023, 'math_aut_2023'),
        ('tests/test_files/math_WIN_2023.html', 'WIN', 2023, 'math_win_2023'),
        ('tests/test_files/math_SPR_2021.html', 'SPR', 2021, 'math_spr_2021'),
        ('tests/test_files/math_SUM_2023.html', 'SUM', 2023, 'math_sum_2023'),
        ('tests/test_files/chem_SPR_2021.html', 'SPR', 2021, 'chem_spr_2021'),
    ]
    
    all_courses = []
    all_meetings = []
    
    for file_path, quarter, year, prefix in test_files:
        if not os.path.exists(file_path):
            print(f"⚠️  Skipping {file_path} - file not found")
            continue
            
        print(f"\n📚 Processing {file_path}...")
        
        try:
            with open(file_path, 'r') as f:
                html = f.read()
            
            courses = parse_schedule_html(html, quarter, year)
            print(f"✅ Parsed {len(courses)} courses with {sum(len(course.meetings) for course in courses)} meetings")
            
            # Add to combined lists
            for course in courses:
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
                
                for meeting in course.meetings:
                    meeting_data = {
                        'sln': meeting.sln,
                        'course_code': meeting.course_code,
                        'meeting_id': meeting.meeting_id,
                        'meeting_type_code': meeting.meeting_type_code,
                        'credits': meeting.credits,
                        'meeting_date': meeting.meeting_date,
                        'days': meeting.days,
                        'time': meeting.time,
                        'building': meeting.building,
                        'room': meeting.room,
                        'instructor': meeting.instructor,
                        'professor_name': meeting.professor_name,
                        'status': meeting.status,
                        'enrolled': meeting.enrolled,
                        'capacity': meeting.capacity,
                        'max_capacity': meeting.max_capacity,
                        'current_capacity': meeting.current_capacity,
                        'meeting_classification': meeting.meeting_classification,
                        'quarter': meeting.quarter,
                        'year': meeting.year,
                        'meeting_times': meeting.meeting_times,
                        'notes': meeting.notes,
                        'description': meeting.description,
                        'additional_code': meeting.additional_code,
                        'enrl_restr': meeting.enrl_restr
                    }
                    all_meetings.append(meeting_data)
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            continue
    
    # Generate CSV files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Courses CSV
    courses_file = f'output/courses_{timestamp}.csv'
    print(f"\n📝 Writing courses to {courses_file}...")
    
    if all_courses:
        with open(courses_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['course_code', 'title', 'prerequisites', 'credits', 'credit_types', 'quarter', 'year', 'meeting_count']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_courses)
        print(f"✅ Wrote {len(all_courses)} courses to {courses_file}")
    else:
        print("⚠️  No courses to write")
    
    # Meetings CSV
    meetings_file = f'output/meetings_{timestamp}.csv'
    print(f"\n📝 Writing meetings to {meetings_file}...")
    
    if all_meetings:
        with open(meetings_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['sln', 'course_code', 'meeting_id', 'meeting_type_code', 'credits', 'meeting_date', 'days', 'time', 'building', 'room', 'instructor', 'professor_name', 'status', 'enrolled', 'capacity', 'max_capacity', 'current_capacity', 'meeting_classification', 'quarter', 'year', 'meeting_times', 'notes', 'description', 'additional_code', 'enrl_restr']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_meetings)
        print(f"✅ Wrote {len(all_meetings)} meetings to {meetings_file}")
    else:
        print("⚠️  No meetings to write")
    
    # Summary CSV
    summary_file = f'output/summary_{timestamp}.csv'
    print(f"\n📝 Writing summary to {summary_file}...")
    
    summary_data = []
    for course in all_courses:
        course_meetings = [m for m in all_meetings if m['course_code'] == course['course_code']]
        
        # Count different types of meetings
        lectures = len([m for m in course_meetings if m['meeting_classification'] == 'lecture'])
        quizzes = len([m for m in course_meetings if m['meeting_classification'] == 'quiz'])
        labs = len([m for m in course_meetings if m['meeting_classification'] == 'lab'])
        seminars = len([m for m in course_meetings if m['meeting_classification'] == 'seminar'])
        others = len([m for m in course_meetings if m['meeting_classification'] == 'other'])
        
        # Count "to be arranged" meetings
        tba_meetings = len([m for m in course_meetings if m['time'] == 'to be arranged'])
        
        # Count meetings with additional codes
        additional_codes = len([m for m in course_meetings if m['additional_code']])
        
        summary_data.append({
            'course_code': course['course_code'],
            'title': course['title'],
            'quarter': course['quarter'],
            'year': course['year'],
            'credits': course['credits'],
            'total_meetings': len(course_meetings),
            'lectures': lectures,
            'quizzes': quizzes,
            'labs': labs,
            'seminars': seminars,
            'others': others,
            'to_be_arranged': tba_meetings,
            'with_additional_codes': additional_codes,
            'total_enrolled': sum(m['enrolled'] for m in course_meetings if m['meeting_classification'] == 'lecture'),
            'total_capacity': sum(m['capacity'] for m in course_meetings if m['meeting_classification'] == 'lecture')
        })
    
    if summary_data:
        with open(summary_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['course_code', 'title', 'quarter', 'year', 'credits', 'total_meetings', 'lectures', 'quizzes', 'labs', 'seminars', 'others', 'to_be_arranged', 'with_additional_codes', 'total_enrolled', 'total_capacity']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(summary_data)
        print(f"✅ Wrote {len(summary_data)} course summaries to {summary_file}")
    else:
        print("⚠️  No summary data to write")
    
    print(f"\n🎯 CSV Generation Complete!")
    print(f"   Total courses: {len(all_courses)}")
    print(f"   Total meetings: {len(all_meetings)}")
    print(f"   Files created:")
    print(f"     - {courses_file}")
    print(f"     - {meetings_file}")
    print(f"     - {summary_file}")

if __name__ == "__main__":
    generate_csv_output()
