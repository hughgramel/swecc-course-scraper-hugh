#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from swecc_course_scraper.commands.parser import _parse_course_meetings
from tests.test_blocks import get_test_block

def test_math_581_sections():
    print("🧪 Testing MATH 581 Special Topics Sections")
    print("=" * 50)
    
    # Expected results based on the MATH 581 screenshot
    expected_math_581 = {
        "18424": {
            "meeting_id": "A",
            "credits": "3",
            "meeting_type_code": "",
            "enrl_restr": "",
            "time": "MWF 9:30-10:20",
            "building": "PDL",
            "room": "C038",
            "instructor": "McGovern, William M",
            "title": "LINEAR ALGEBRAIC GROUPS",
            "status": "Open",
            "enrolled": 4,
            "capacity": 15,
            "expected_meetings": 1
        },
        "18425": {
            "meeting_id": "B",
            "credits": "3",
            "meeting_type_code": "",
            "enrl_restr": "",
            "time": "MW 9:00-10:20",
            "building": "SIG",
            "room": "226",
            "instructor": "Yuan, Yu",
            "title": "LINEAR AND NONLINEAR ELLIPTIC EQUATIONS",
            "status": "Open",
            "enrolled": 7,
            "capacity": 20,
            "expected_meetings": 1
        },
        "18427": {
            "meeting_id": "D",
            "credits": "3",
            "meeting_type_code": "",
            "enrl_restr": "",
            "time": "T 9:00-11:50",
            "building": "PDL",
            "room": "C038",
            "instructor": "Shokrieh, Farbod",
            "title": "CHIP-FIRING",
            "status": "Open",
            "enrolled": 14,
            "capacity": 25,
            "additional_code": "B",
            "expected_meetings": 1
        },
        "18428": {
            "meeting_id": "E",
            "credits": "3",
            "meeting_type_code": "",
            "enrl_restr": "",
            "time": "Th 9:00-11:50",
            "building": "PDL",
            "room": "C401",
            "instructor": "Shokrieh, Farbod",
            "title": "ALGEBRAIC NUMBER THEORY",
            "status": "Open",
            "enrolled": 13,
            "capacity": 20,
            "additional_code": "B",
            "expected_meetings": 1
        },
        "18429": {
            "meeting_id": "F",
            "credits": "3",
            "meeting_type_code": "",
            "enrl_restr": "",
            "time": "to be arranged",
            "building": "",
            "room": "",
            "instructor": "Pal, Soumik",
            "title": "WASSERSTEIN GRADIENT FLOWS (PIMS) SEE INSTRUCTOR FOR COURSE DAYS/TIME",
            "status": "Open",
            "enrolled": 17,
            "capacity": 20,
            "expected_meetings": 1
        },
        "18430": {
            "meeting_id": "G",
            "credits": "3",
            "meeting_type_code": "",
            "enrl_restr": "",
            "time": "MW 1:00-2:20",
            "building": "GUG",
            "room": "218",
            "instructor": "Drusvyatskiy, Dmitriy",
            "title": "MATHEMATICS OF DATA SCIENCE",
            "status": "Open",
            "enrolled": 37,
            "capacity": 40,
            "expected_meetings": 1
        }
    }
    
    print("📋 Expected MATH 581 Sections:")
    for sln, details in expected_math_581.items():
        print(f"  SLN {sln}: {details['meeting_id']} - {details['title']}")
        print(f"    {details['time']} {details['building']} {details['room']}")
        print(f"    {details['instructor']} - {details['status']} ({details['enrolled']}/{details['capacity']})")
        if details.get('additional_code'):
            print(f"    Additional Code: {details['additional_code']}")
        print()
    
    print("ℹ️  Note: These sections are not in our current test blocks.")
    print("   This test shows the expected structure based on the screenshot.")
    print("   To test these, we would need the actual HTML data for MATH 581.")

def test_math_116_section():
    print("\n🧪 Testing MATH 116 Section Structure")
    print("=" * 40)
    
    # Expected results based on the MATH 116 screenshot
    expected_math_116 = {
        "23241": {
            "meeting_id": "A",
            "credits": "1",  # Based on section number 1
            "meeting_type_code": "",
            "enrl_restr": "",
            "time": "to be arranged",
            "building": "",
            "room": "",
            "instructor": "Su, Zhixu",
            "title": "INTRO TAYLOR SERIES",
            "status": "Open",
            "enrolled": 8,
            "capacity": 15,
            "additional_code": "E",  # CR/NC grading
            "description": "ENROLLMENT OPEN ONLY TO THOSE APPROVED THROUGH MATH TRANSFER EQUIVALENCY REVIEW PROCESS. EMAIL ADVISING@MATH.WASHINGTON.EDU WITH QUESTIONS.",
            "expected_meetings": 1
        }
    }
    
    print("📋 Expected MATH 116 Section:")
    for sln, details in expected_math_116.items():
        print(f"  SLN {sln}: {details['meeting_id']} - {details['title']}")
        print(f"    {details['time']} {details['building']} {details['room']}")
        print(f"    {details['instructor']} - {details['status']} ({details['enrolled']}/{details['capacity']})")
        print(f"    Credits: {details['credits']}")
        if details.get('additional_code'):
            print(f"    Additional Code: {details['additional_code']}")
        print(f"    Description: {details['description']}")
        print()
    
    print("ℹ️  Note: This section is not in our current test blocks.")
    print("   This test shows the expected structure based on the screenshot.")

if __name__ == "__main__":
    test_math_581_sections()
    test_math_116_section()
    print("\n🎉 MATH 581 and 116 structure tests completed!")

