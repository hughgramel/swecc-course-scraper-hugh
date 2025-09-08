#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def show_expected_vs_actual():
    print("📊 AUT 2023 MATH - Expected vs Actual Results")
    print("=" * 60)
    
    # Expected results based on screenshots
    expected = {
        "MATH 103": {
            "18069": {"meeting_id": "A", "credits": "5", "type": "lecture", "meetings": 1}
        },
        "MATH 111": {
            "18070": {"meeting_id": "A", "credits": "5", "type": "lecture", "meetings": 1},
            "18071": {"meeting_id": "AA", "credits": "", "type": "quiz", "meetings": 1},
            "18072": {"meeting_id": "AB", "credits": "", "type": "quiz", "meetings": 1},
            "18073": {"meeting_id": "AC", "credits": "", "type": "quiz", "meetings": 1},
            "18074": {"meeting_id": "AD", "credits": "", "type": "quiz", "meetings": 1},
            "18075": {"meeting_id": "AE", "credits": "", "type": "quiz", "meetings": 1},
            "18076": {"meeting_id": "AF", "credits": "", "type": "quiz", "meetings": 1}
        },
        "MATH 125": {
            "18214": {"meeting_id": "A", "credits": "5", "type": "lecture", "meetings": 1},
            "18215": {"meeting_id": "AA", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18216": {"meeting_id": "AB", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18217": {"meeting_id": "AC", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18218": {"meeting_id": "AD", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18219": {"meeting_id": "AE", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18220": {"meeting_id": "AF", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18221": {"meeting_id": "AG", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18222": {"meeting_id": "AH", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18223": {"meeting_id": "B", "credits": "5", "type": "lecture", "meetings": 1},
            "18224": {"meeting_id": "BA", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18225": {"meeting_id": "BB", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18226": {"meeting_id": "BC", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18227": {"meeting_id": "BD", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18228": {"meeting_id": "BE", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18229": {"meeting_id": "BF", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18230": {"meeting_id": "BG", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18231": {"meeting_id": "BH", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18232": {"meeting_id": "C", "credits": "5", "type": "lecture", "meetings": 1},
            "18233": {"meeting_id": "CA", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18234": {"meeting_id": "CB", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18235": {"meeting_id": "CC", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18236": {"meeting_id": "CD", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18237": {"meeting_id": "CE", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18238": {"meeting_id": "CF", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18239": {"meeting_id": "CG", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18240": {"meeting_id": "CH", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18241": {"meeting_id": "D", "credits": "5", "type": "lecture", "meetings": 1, "time": "to be arranged"},
            "18242": {"meeting_id": "DA", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18243": {"meeting_id": "DB", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18244": {"meeting_id": "DC", "credits": "", "type": "quiz", "meetings": 2},  # Multiple times
            "18245": {"meeting_id": "DD", "credits": "", "type": "quiz", "meetings": 2}   # Multiple times
        }
    }
    
    print("📋 Expected Results (Based on Screenshots):")
    print()
    
    total_expected_meetings = 0
    for course, sections in expected.items():
        print(f"🎓 {course}:")
        for sln, details in sections.items():
            print(f"  SLN {sln}: {details['meeting_id']} - {details['type']} ({details['credits']} credits)")
            if details.get('time'):
                print(f"    Time: {details['time']}")
            print(f"    Expected meetings: {details['meetings']}")
            total_expected_meetings += details['meetings']
        print()
    
    print(f"📊 Total Expected Meetings: {total_expected_meetings}")
    print()
    
    print("🔍 Key Features to Test:")
    print("  ✅ Multiple meeting times (quiz sections have 2 meetings each)")
    print("  ✅ 'To be arranged' times (SLN 18241)")
    print("  ✅ Lecture vs Quiz classification")
    print("  ✅ Credits vs Type codes")
    print("  ✅ Enrollment restrictions (currently empty in HTML)")
    print("  ✅ Additional codes (like 'B')")
    print("  ✅ Complex instructor names")
    print("  ✅ Multiple description lines")
    print()
    
    print("📝 Notes:")
    print("  • Quiz sections (AA, AB, etc.) should have 2 meeting objects each")
    print("  • Lecture sections (A, B, C, D) should have 1 meeting object each")
    print("  • SLN 18241 should have 'to be arranged' time with empty building/room")
    print("  • All sections should have proper enrollment restriction field (empty)")
    print("  • Additional codes like 'B' should be captured when present")

def show_math_581_expected():
    print("\n📚 MATH 581 Special Topics - Expected Structure:")
    print("=" * 50)
    
    expected_581 = {
        "18424": {"id": "A", "credits": "3", "time": "MWF 9:30-10:20", "building": "PDL", "room": "C038", "instructor": "McGovern, William M", "title": "LINEAR ALGEBRAIC GROUPS", "enrolled": 4, "capacity": 15},
        "18425": {"id": "B", "credits": "3", "time": "MW 9:00-10:20", "building": "SIG", "room": "226", "instructor": "Yuan, Yu", "title": "LINEAR AND NONLINEAR ELLIPTIC EQUATIONS", "enrolled": 7, "capacity": 20},
        "18427": {"id": "D", "credits": "3", "time": "T 9:00-11:50", "building": "PDL", "room": "C038", "instructor": "Shokrieh, Farbod", "title": "CHIP-FIRING", "enrolled": 14, "capacity": 25, "additional_code": "B"},
        "18428": {"id": "E", "credits": "3", "time": "Th 9:00-11:50", "building": "PDL", "room": "C401", "instructor": "Shokrieh, Farbod", "title": "ALGEBRAIC NUMBER THEORY", "enrolled": 13, "capacity": 20, "additional_code": "B"},
        "18429": {"id": "F", "credits": "3", "time": "to be arranged", "building": "", "room": "", "instructor": "Pal, Soumik", "title": "WASSERSTEIN GRADIENT FLOWS (PIMS) SEE INSTRUCTOR FOR COURSE DAYS/TIME", "enrolled": 17, "capacity": 20},
        "18430": {"id": "G", "credits": "3", "time": "MW 1:00-2:20", "building": "GUG", "room": "218", "instructor": "Drusvyatskiy, Dmitriy", "title": "MATHEMATICS OF DATA SCIENCE", "enrolled": 37, "capacity": 40}
    }
    
    for sln, details in expected_581.items():
        print(f"SLN {sln}: {details['id']} - {details['title']}")
        print(f"  {details['time']} {details['building']} {details['room']}")
        print(f"  {details['instructor']} - {details['enrolled']}/{details['capacity']}")
        if details.get('additional_code'):
            print(f"  Additional Code: {details['additional_code']}")
        print()

if __name__ == "__main__":
    show_expected_vs_actual()
    show_math_581_expected()
    print("\n🎯 To test these expectations, run the parser on the actual HTML data")
    print("   and compare the results with these expected values.")
