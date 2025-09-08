#!/usr/bin/env python3

import csv
import os
from datetime import datetime

def create_sample_csv_files():
    """Create sample CSV files to demonstrate the output format."""
    print("📊 Creating Sample CSV Files")
    print("=" * 50)
    
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Sample courses data
    sample_courses = [
        {
            'course_code': 'MATH 125',
            'title': 'CALC ANALYT GEOM II',
            'prerequisites': 'Prerequisites (cancellation in effect)',
            'credits': '5',
            'credit_types': 'NSc',
            'quarter': 'AUT',
            'year': 2023,
            'meeting_count': 33
        },
        {
            'course_code': 'MATH 111',
            'title': 'ALGEBRA WITH APPLICATIONS',
            'prerequisites': 'None',
            'credits': '5',
            'credit_types': 'NSc',
            'quarter': 'AUT',
            'year': 2023,
            'meeting_count': 7
        },
        {
            'course_code': 'MATH 103',
            'title': 'INTRODUCTION TO ELEMENTARY FUNCTIONS',
            'prerequisites': 'None',
            'credits': '5',
            'credit_types': 'NSc',
            'quarter': 'AUT',
            'year': 2023,
            'meeting_count': 1
        }
    ]
    
    # Sample meetings data
    sample_meetings = [
        {
            'sln': '18214',
            'course_code': 'MATH 125',
            'meeting_id': 'A',
            'meeting_type_code': '',
            'credits': '5',
            'meeting_date': 'MWF',
            'days': 'MWF',
            'time': '830-920',
            'building': 'PCAR',
            'room': '192',
            'instructor': 'Heald,Andy M',
            'professor_name': 'Heald,Andy M',
            'status': 'Open',
            'enrolled': 227,
            'capacity': 240,
            'max_capacity': 240,
            'current_capacity': 227,
            'meeting_classification': 'lecture',
            'quarter': 'AUT',
            'year': 2023,
            'meeting_times': '830-920',
            'notes': None,
            'description': 'NO OVERLOADS',
            'additional_code': '',
            'enrl_restr': ''
        },
        {
            'sln': '18215',
            'course_code': 'MATH 125',
            'meeting_id': 'AA',
            'meeting_type_code': 'QZ',
            'credits': '',
            'meeting_date': 'T',
            'days': 'T',
            'time': '830-920',
            'building': 'LOW',
            'room': '217',
            'instructor': 'Catron,Spencer',
            'professor_name': 'Catron,Spencer',
            'status': 'Open',
            'enrolled': 27,
            'capacity': 30,
            'max_capacity': 30,
            'current_capacity': 27,
            'meeting_classification': 'quiz',
            'quarter': 'AUT',
            'year': 2023,
            'meeting_times': '830-920',
            'notes': None,
            'description': 'NO OVERLOADS',
            'additional_code': '',
            'enrl_restr': ''
        },
        {
            'sln': '18215',
            'course_code': 'MATH 125',
            'meeting_id': 'AA-1',
            'meeting_type_code': 'QZ',
            'credits': '',
            'meeting_date': 'Th',
            'days': 'Th',
            'time': '830-950',
            'building': 'CDH',
            'room': '128',
            'instructor': 'Catron,Spencer',
            'professor_name': 'Catron,Spencer',
            'status': 'Open',
            'enrolled': 27,
            'capacity': 30,
            'max_capacity': 30,
            'current_capacity': 27,
            'meeting_classification': 'quiz',
            'quarter': 'AUT',
            'year': 2023,
            'meeting_times': '830-950',
            'notes': None,
            'description': 'NO OVERLOADS',
            'additional_code': '',
            'enrl_restr': ''
        },
        {
            'sln': '18241',
            'course_code': 'MATH 125',
            'meeting_id': 'D',
            'meeting_type_code': '',
            'credits': '5',
            'meeting_date': 'to be arranged',
            'days': 'to be arranged',
            'time': 'to be arranged',
            'building': '',
            'room': '',
            'instructor': 'Conroy,Matthew',
            'professor_name': 'Conroy,Matthew',
            'status': 'Open',
            'enrolled': 100,
            'capacity': 120,
            'max_capacity': 120,
            'current_capacity': 100,
            'meeting_classification': 'lecture',
            'quarter': 'AUT',
            'year': 2023,
            'meeting_times': 'to be arranged',
            'notes': None,
            'description': 'MWF ASYNCHRONOUS REMOTE LECTURES T/TH IN-PERSON SECTIONS AND EXAMS MATH 125 CANNOT BE OVERLOADED',
            'additional_code': 'B',
            'enrl_restr': ''
        }
    ]
    
    # Sample summary data
    sample_summary = [
        {
            'course_code': 'MATH 125',
            'title': 'CALC ANALYT GEOM II',
            'quarter': 'AUT',
            'year': 2023,
            'credits': '5',
            'total_meetings': 33,
            'lectures': 4,
            'quizzes': 28,
            'labs': 0,
            'seminars': 0,
            'others': 1,
            'to_be_arranged': 1,
            'with_additional_codes': 1,
            'total_enrolled': 655,
            'total_capacity': 720
        },
        {
            'course_code': 'MATH 111',
            'title': 'ALGEBRA WITH APPLICATIONS',
            'quarter': 'AUT',
            'year': 2023,
            'credits': '5',
            'total_meetings': 7,
            'lectures': 1,
            'quizzes': 6,
            'labs': 0,
            'seminars': 0,
            'others': 0,
            'to_be_arranged': 0,
            'with_additional_codes': 0,
            'total_enrolled': 0,
            'total_capacity': 0
        }
    ]
    
    # Write courses CSV
    courses_file = f'output/courses_{timestamp}.csv'
    print(f"📝 Creating {courses_file}...")
    
    with open(courses_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['course_code', 'title', 'prerequisites', 'credits', 'credit_types', 'quarter', 'year', 'meeting_count']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sample_courses)
    print(f"✅ Created {courses_file} with {len(sample_courses)} courses")
    
    # Write meetings CSV
    meetings_file = f'output/meetings_{timestamp}.csv'
    print(f"📝 Creating {meetings_file}...")
    
    with open(meetings_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['sln', 'course_code', 'meeting_id', 'meeting_type_code', 'credits', 'meeting_date', 'days', 'time', 'building', 'room', 'instructor', 'professor_name', 'status', 'enrolled', 'capacity', 'max_capacity', 'current_capacity', 'meeting_classification', 'quarter', 'year', 'meeting_times', 'notes', 'description', 'additional_code', 'enrl_restr']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sample_meetings)
    print(f"✅ Created {meetings_file} with {len(sample_meetings)} meetings")
    
    # Write summary CSV
    summary_file = f'output/summary_{timestamp}.csv'
    print(f"📝 Creating {summary_file}...")
    
    with open(summary_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['course_code', 'title', 'quarter', 'year', 'credits', 'total_meetings', 'lectures', 'quizzes', 'labs', 'seminars', 'others', 'to_be_arranged', 'with_additional_codes', 'total_enrolled', 'total_capacity']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sample_summary)
    print(f"✅ Created {summary_file} with {len(sample_summary)} course summaries")
    
    print(f"\n🎯 Sample CSV Files Created!")
    print(f"   Files created:")
    print(f"     - {courses_file}")
    print(f"     - {meetings_file}")
    print(f"     - {summary_file}")
    print(f"\n📋 Key Features Demonstrated:")
    print(f"   ✅ Multiple meeting times (quiz sections have 2 meetings each)")
    print(f"   ✅ 'To be arranged' times (SLN 18241)")
    print(f"   ✅ Lecture vs Quiz classification")
    print(f"   ✅ Credits vs Type codes")
    print(f"   ✅ Additional codes (like 'B')")
    print(f"   ✅ Complex instructor names")
    print(f"   ✅ Multiple description lines")

if __name__ == "__main__":
    create_sample_csv_files()
