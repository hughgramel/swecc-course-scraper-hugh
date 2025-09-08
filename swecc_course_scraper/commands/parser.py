"""
HTML parser for UW time schedule pages.

This module contains functions to parse raw HTML from UW's time schedule
pages into structured Course and CourseMeeting objects.
"""

import re
from typing import List, Dict, Optional
from ..models.course import Course, CourseMeeting


# =============================================================================
# SAMPLE OUTPUT - What your functions should return
# =============================================================================

"""
Example of what parse_schedule_html() should return:

[
    Course(
        course_code="CSE 122",
        title="COMP PROGRAMMING II",
        prerequisites="CSE 121 or equivalent",
        credits="5",
        quarter="WIN",
        year=2023,
        meetings=[
            CourseMeeting(
                sln="12924",
                course_code="CSE 122",
                meeting_id="A",
                meeting_type_code="",
                credits="4",
                meeting_date="WF",
                days="WF",
                time="1130-1220",
                building="KNE",
                room="130",
                instructor="Natsuhara,Miya Kaye",
                professor_name="Natsuhara,Miya Kaye",
                status="Open",
                enrolled=357,
                capacity=376,
                max_capacity=376,
                current_capacity=357,
                meeting_classification="lecture",
                quarter="WIN",
                year=2023,
                meeting_times="1130-1220",
                notes="NO CREDIT FOR STUDENTS WHO HAVE COMPLETED CSE 143",
                description="",
                additional_code="",
                enrl_restr=""
            ),
            CourseMeeting(
                sln="12925",
                course_code="CSE 122",
                meeting_id="AA",
                meeting_type_code="QZ",
                credits="",
                meeting_date="TTh",
                days="TTh",
                time="830-920",
                building="MGH",
                room="288",
                instructor="Lin,Melissa",
                professor_name="Lin,Melissa",
                status="Open",
                enrolled=17,
                capacity=21,
                max_capacity=21,
                current_capacity=17,
                meeting_classification="quiz",
                quarter="WIN",
                year=2023,
                meeting_times="830-920",
                notes=None,
                description="",
                additional_code="",
                enrl_restr=""
            )
        ]
    ),
    Course(
        course_code="CSE 142",
        title="COMPUTER PROGRAMMING I",
        prerequisites="None",
        credits="5",
        quarter="WIN",
        year=2023,
        meetings=[
            # ... more meetings
        ]
    )
]
"""


# =============================================================================
# IMPLEMENTATION SECTION - Complete these functions
# =============================================================================

def parse_schedule_html(html: str, quarter: str, year: int) -> List[Course]:
    """
    Parse UW schedule HTML into structured Course objects.
    
    Args:
        html: Raw HTML content from UW time schedule page
        quarter: Quarter code (e.g., "WIN", "SPR", "SUM", "AUT")
        year: Year (e.g., 2023)
    
    Returns:
        List[Course]: List of parsed Course objects with all sections
    """
    print("=" * 80)
    print("PARSING SCHEDULE HTML")
    print("=" * 80)
    print(f"📅 Quarter: {quarter} {year}")
    print(f"📄 HTML length: {len(html)} characters")
    
    # Step 1: Extract course blocks from HTML
    print("\n🔍 Step 1: Extracting course blocks...")
    course_blocks = _extract_course_blocks(html)
    print(f"✅ Found {len(course_blocks)} course blocks")
    
    courses = []
    
    # Step 2: Process each course block
    print(f"\n🔍 Step 2: Processing {len(course_blocks)} course blocks...")
    
    for i, course_block in enumerate(course_blocks):
        # Parse course header first to get course code
        header_data = _parse_course_header(course_block, show_debug=False)
        
        if not header_data or not header_data.get('code'):
            continue
        
        course_code = header_data['code']
        is_math116 = "116" in course_code
        
        # Only show output for MATH 116 courses
        if is_math116:
            print(f"\n--- Processing Course Block {i+1}/{len(course_blocks)} ---")
            print("📋 Parsing course header...")
            # Re-parse header with debug output for MATH 116
            _parse_course_header(course_block, show_debug=True)
            print(f"✅ Header parsed: {course_code}")
            print("📋 Parsing course meetings...")
        
        # Parse course meetings
        meetings = _parse_course_meetings(course_block, course_code, quarter, year)
        
        if is_math116:
            print(f"✅ Found {len(meetings)} meetings")
            print("📋 Creating Course object...")
        course = Course(
            course_code=header_data['code'],
            title=header_data['title'],
            prerequisites=header_data['prerequisites'],
            credits=header_data['credits'],
            credit_types=header_data['credit_types'],
            quarter=quarter,
            year=year,
            meetings=meetings
        )
        
        courses.append(course)
        
        if is_math116:
            print(f"✅ Course created: {course_code} with {len(meetings)} meetings")
    
    print(f"\n🎯 PARSING COMPLETE")
    print(f"   Total courses parsed: {len(courses)}")
    print(f"   Total meetings: {sum(len(course.meetings) for course in courses)}")
    print("=" * 80)
    
    return courses


def _extract_course_blocks(html: str) -> List[str]:
    """
    Extract individual course blocks from HTML.
    
    New approach:
    1. Extract everything between </P> and <P> tags
    2. Remove the first table (header area) and the first <br> after it
    3. Every remaining table is either a course header or contains section information
    
    Args:
        html: Raw HTML content
        
    Returns:
        List[str]: List of HTML blocks, each containing one complete course and its sections
    """
    print("Extracting course blocks...")
    
    # Determine the background color based on quarter
    quarter_colors = {
        'WIN': '#99ccff',  # Winter - light blue
        'SPR': '#ccffcc',  # Spring - light green  
        'SUM': '#ffffcc',  # Summer - light yellow
        'AUT': '#ffcccc',  # Autumn - light pink
    }
    
    # Try to detect quarter from HTML content
    bgcolor = '#99ccff'  # Default to winter
    for quarter, color in quarter_colors.items():
        if f'bgcolor="{color}"' in html or f"bgcolor='{color}'" in html:
            bgcolor = color
            print(f"Detected {quarter} quarter (color: {color})")
            break
    
    # Step 1: Extract everything between </P> and <P> tags (or <p> and <P>)
    # Try to find </P> first, then fall back to <p>
    p_close_match = re.search(r'</P>', html)
    if not p_close_match:
        p_close_match = re.search(r'<p>', html)
    
    p_open_match = re.search(r'<P>', html)
    if not p_open_match:
        p_open_match = re.search(r'<p>', html)
    
    if not p_close_match or not p_open_match:
        print("Warning: Could not find </P> (or <p>) and <P> boundaries")
        return []
    
    # Extract content between the closing tag and <P> (including both tags)
    start_pos = p_close_match.start()  # Start at </P> or <p>
    end_pos = p_open_match.start()     # End before <P>
    course_schedule_html = html[start_pos:end_pos]
    
    print(f"Extracted content between </P> and <P>: {len(course_schedule_html)} characters")
    
    # Step 2: Remove the first table (header area) and the first <br> after it
    # Find the first table in the extracted content
    first_table_match = re.search(r'<table[^>]*>.*?</table>', course_schedule_html, re.DOTALL)
    if not first_table_match:
        print("Warning: Could not find first table to remove")
        return []
    
    # Find the first <br> after the first table
    after_first_table = course_schedule_html[first_table_match.end():]
    first_br_match = re.search(r'<br>', after_first_table)
    
    if not first_br_match:
        print("Warning: Could not find <br> after first table")
        return []
    
    # Remove the first table and the first <br> after it
    # Keep everything after the first <br> following the first table
    br_end_pos = first_table_match.end() + first_br_match.end()
    cleaned_html = course_schedule_html[br_end_pos:]
    
    print(f"After removing first table and <br>: {len(cleaned_html)} characters")
    
    # Step 3: Extract course blocks from the cleaned content
    # Pattern: course header table + everything until next course header
    pattern = f'(<table bgcolor=[\'"]{re.escape(bgcolor)}[\'"].*?</table>.*?)(?=<table bgcolor=[\'"]{re.escape(bgcolor)}[\'"]|$)'
    course_blocks = re.findall(pattern, cleaned_html, re.DOTALL)
    
    print(f"Found {len(course_blocks)} course blocks")
    return course_blocks


def _parse_course_header(course_block: str, show_debug: bool = True) -> Dict[str, str]:
    """
    Parse course header information from a course block.
    
    Args:
        course_block: HTML block containing one course and its sections
        
    Returns:
        Dict[str, str]: Dictionary with keys: 'code', 'title', 'prerequisites', 'credits'
    """
    if show_debug:
        print("=" * 60)
        print("PARSING COURSE HEADER")
        print("=" * 60)

    # Find the course header table (with background color)
    header_pattern = r'<table[^>]*bgcolor=[\'"][^\'\"]*[\'"][^>]*>.*?</table>'
    header_match = re.search(header_pattern, course_block, re.DOTALL)
    
    if not header_match:
        if show_debug:
            print("❌ No course header table found")
        return {}
    
    header_html = header_match.group(0)
    if show_debug:
        print(f"📋 Found course header table:")
        print(f"   Length: {len(header_html)} characters")
        print(f"   Preview: {header_html[:200]}...")
    
    # Extract course code from <A NAME=...> tags
    code_pattern = r'<A NAME=([^>]*)>([^<]+)</A>'
    code_match = re.search(code_pattern, header_html)
    
    if code_match:
        course_code = code_match.group(2).strip()
        # Clean up HTML entities
        course_code = course_code.replace('&nbsp;', ' ').replace('  ', ' ').strip()
        if show_debug:
            print(f"📚 Course Code: '{course_code}'")
    else:
        if show_debug:
            print("❌ No course code found")
        course_code = ""
    
    # Extract title from course title link
    title_pattern = r'<A HREF=[^>]*>([^<]+)</A>'
    title_match = re.search(title_pattern, header_html)
    
    if title_match:
        title = title_match.group(1).strip()
        if show_debug:
            print(f"📖 Title: '{title}'")
    else:
        if show_debug:
            print("❌ No title found")
        title = ""
    
    # Extract prerequisites from header text
    prereq_pattern = r'Prerequisites[:\s]*([^<\n]+)'
    prereq_match = re.search(prereq_pattern, header_html, re.IGNORECASE)
    
    if prereq_match:
        prerequisites = prereq_match.group(1).strip()
        if show_debug:
            print(f"📋 Prerequisites: '{prerequisites}'")
    else:
        if show_debug:
            print("ℹ️  No prerequisites found")
        prerequisites = ""
    
    # Extract credits from header text
    credits_pattern = r'(\d+)\s*credits?'
    credits_match = re.search(credits_pattern, header_html, re.IGNORECASE)
    
    if credits_match:
        credits = credits_match.group(1)
        if show_debug:
            print(f"🎓 Credits: '{credits}'")
    else:
        if show_debug:
            print("ℹ️  No credits found")
        credits = ""
    
    # Extract credit types from parentheses (e.g., "(NSc,RSN)")
    credit_types_pattern = r'\(([^)]+)\)'
    credit_types_match = re.search(credit_types_pattern, header_html)
    
    if credit_types_match:
        credit_types = credit_types_match.group(1)
        if show_debug:
            print(f"🏷️  Credit Types: '{credit_types}'")
    else:
        if show_debug:
            print("ℹ️  No credit types found")
        credit_types = ""
    
    result = {
        'code': course_code,
        'title': title,
        'prerequisites': prerequisites,
        'credits': credits,
        'credit_types': credit_types
    }
    
    if show_debug:
        print(f"✅ Header parsing complete:")
        print(f"   Result: {result}")
        print("=" * 60)
    
    return result


def _parse_course_meetings(course_block: str, course_code: str, quarter: str, year: int) -> List[CourseMeeting]:
    """
    Parse individual meetings from a course block.
    
    Args:
        course_block: HTML block containing one course and its meetings
        course_code: Course code (e.g., "CSE 122")
        quarter: Quarter code (e.g., "WIN")
        year: Year (e.g., 2023)
        
    Returns:
        List[CourseMeeting]: List of parsed meeting objects


        
    """
    # Only show debug output for MATH 116
    is_math116 = "116" in course_code
    if is_math116:
        print("=" * 60)
        print("PARSING COURSE MEETINGS")
        print("=" * 60)
        print(f"📚 Course: {course_code}")
        print(f"📅 Quarter: {quarter} {year}")
    
    # Find all meeting tables (tables without background color)
    meeting_pattern = r'<table[^>]*(?!bgcolor)[^>]*>.*?</table>'
    meeting_tables = re.findall(meeting_pattern, course_block, re.DOTALL)
    
    if is_math116:
        print(f"🔍 Found {len(meeting_tables)} meeting tables")
    
    meetings = []
    
    for i, meeting_html in enumerate(meeting_tables):
        if is_math116:
            print(f"\n--- Meeting {i+1} ---")
            print(f"📋 Meeting HTML length: {len(meeting_html)} characters")
            print(f"📋 Meeting preview: {meeting_html[:150]}...")
        
        # Extract meeting data from <pre> tags (they don't have closing </pre> tags)
        pre_pattern = r'<pre[^>]*>(.*?)(?=</td></tr></table>)'
        pre_match = re.search(pre_pattern, meeting_html, re.DOTALL)
        
        if not pre_match:
            if is_math116:
                print("❌ No <pre> tag found in meeting")
            continue
        
        meeting_text = pre_match.group(1).strip()
        if is_math116:
            print(f"📝 Meeting text: '{meeting_text}'")
        
        # Parse meeting data using a more flexible approach
        # The structure is: SLN MeetingID Credits/TypeCode MeetingDate Time Building Room Instructor Status Enrolled/Capacity [AdditionalCodes]
        # But we need to handle:
        # 1. Multiple meeting times (additional lines)
        # 2. "to be arranged" times
        # 3. Additional codes after capacity (like "B")
        # 4. Complex professor names with spaces/commas
        # 5. Multiple description lines
        
        # First, extract the main line (first line of the meeting)
        lines = meeting_text.split('\n')
        main_line = lines[0].strip()
        additional_lines = [line.strip() for line in lines[1:] if line.strip()]
        
        if is_math116:
            print(f"🔍 Main line: '{main_line}'")
            print(f"🔍 Additional lines: {additional_lines}")
        
        # Parse the main line with multiple patterns to handle different cases
        # Use more flexible spacing patterns to handle variable whitespace
        # Case 1: Normal time format with "Restr" prefix
        # Structure: Restr <A HREF=...>SLN</A> MeetingID Credits/Type MeetingDate Time <A HREF=...>Building</A> Room Instructor Status Enrolled/Capacity [AdditionalCode]
        pattern_normal_restr = r'Restr\s+<A HREF=[^>]*>(\d+)</A>\s+(\w+)\s+(\w+)\s+(\w+)\s+([^\s]+)\s+<A[^>]*>(\w+)</A>\s+(\w+)\s+([^<]+?)\s+(Open|Closed)\s+(\d+)/(\s*\d+E?)(?:\s+(\w+))?'
        
        # Case 2: "to be arranged" time format with "Restr" prefix
        # Structure: Restr <A HREF=...>SLN</A> MeetingID Credits/Type MeetingDate "to be arranged" [Building/Room] Instructor Status Enrolled/Capacity [AdditionalCode]
        pattern_arranged_restr = r'Restr\s+<A HREF=[^>]*>(\d+)</A>\s+(\w+)\s+(\w+)\s+(\w+)\s+(to be arranged)\s+([^*]+?)\s+([^<]+?)\s+(Open|Closed)\s+(\d+)/(\s*\d+E?)(?:\s+(\w+))?'
        
        # Case 3: Normal time format without "Restr" prefix (like block_04.html)
        # Structure: [>] <A HREF=...>SLN</A> MeetingID Credits/Type MeetingDate Time [Building/Room] Instructor Status Enrolled/Capacity [AdditionalCode]
        pattern_normal_no_restr = r'[>\s]*<A HREF=[^>]*>(\d+)</A>\s+(\w+)\s+(\w+)\s+(\w+)\s+([^\s]+)\s+([^<]+?)\s+(Open|Closed)\s+(\d+)/(\s*\d+E?)(?:\s+(\w+))?'
        
        # Case 4: "to be arranged" time format without "Restr" prefix
        # Structure: [>] <A HREF=...>SLN</A> MeetingID Credits/Type MeetingDate "to be arranged" [Building/Room] Instructor Status Enrolled/Capacity [AdditionalCode]
        # Building/Room can be "*    *" or empty
        pattern_arranged_no_restr = r'[>\s]*<A HREF=[^>]*>(\d+)</A>\s+(\w+)\s+(\w+)\s+(\w+)\s+(to be arranged)\s+([^*]*?)\s+([^<]+?)\s+(Open|Closed)\s+(\d+)/(\s*\d+E?)(?:\s+([^<]+?))?'
        
        # Case 5: "to be arranged" time format without "Restr" prefix and without Status field
        # Structure: [>] <A HREF=...>SLN</A> MeetingID Credits/Type MeetingDate "to be arranged" [Building/Room] Instructor Enrolled/Capacity [CreditType] [AdditionalCode]
        pattern_arranged_no_restr_no_status = r'[>\s]*<A HREF=[^>]*>(\d+)</A>\s+(\w+)\s+(\w+)\s+(\w+)\s+(to be arranged)\s+([^*]*?)\s+([^<]+?)\s+(\d+)/(\s*\d+E?)(?:\s+([^<]+?))?(?:\s+([^<]+?))?'
        
        # Try patterns in order of preference
        meeting_match = None
        pattern_type = None
        has_restr = False
        
        if is_math116:
            print(f"🔍 Testing regex patterns on main line: '{main_line}'")
        
        # Try normal pattern with "Restr" first
        meeting_match = re.search(pattern_normal_restr, main_line)
        if meeting_match:
            pattern_type = "normal"
            has_restr = True
            if is_math116:
                print(f"✅ Matched pattern_normal_restr with {len(meeting_match.groups())} groups")
        
        if not meeting_match:
            # Try normal pattern without "Restr"
            meeting_match = re.search(pattern_normal_no_restr, main_line)
            if meeting_match:
                pattern_type = "normal"
                has_restr = False
                if is_math116:
                    print(f"✅ Matched pattern_normal_no_restr with {len(meeting_match.groups())} groups")
        
        if not meeting_match:
            # Try "to be arranged" pattern with "Restr"
            meeting_match = re.search(pattern_arranged_restr, main_line)
            if meeting_match:
                pattern_type = "arranged"
                has_restr = True
                if is_math116:
                    print(f"✅ Matched pattern_arranged_restr with {len(meeting_match.groups())} groups")
        
        if not meeting_match:
            # Try "to be arranged" pattern without "Restr"
            meeting_match = re.search(pattern_arranged_no_restr, main_line)
            if meeting_match:
                pattern_type = "arranged"
                has_restr = False
                if is_math116:
                    print(f"✅ Matched pattern_arranged_no_restr with {len(meeting_match.groups())} groups")
        
        if not meeting_match:
            # Try "to be arranged" pattern without "Restr" and without Status field
            meeting_match = re.search(pattern_arranged_no_restr_no_status, main_line)
            if meeting_match:
                pattern_type = "arranged_no_status"
                has_restr = False
                if is_math116:
                    print(f"✅ Matched pattern_arranged_no_restr_no_status with {len(meeting_match.groups())} groups")
        
        if meeting_match:
            if is_math116:
                print(f"🎯 Using pattern: {pattern_type} (has_restr: {has_restr})")
                print(f"📊 Groups captured: {len(meeting_match.groups())}")
                for i, group in enumerate(meeting_match.groups(), 1):
                    print(f"   Group {i}: '{group}'")
            
            # Set enrollment restriction code based on whether "Restr" was found
            enrl_restr = "Restr" if has_restr else ""
            sln = meeting_match.group(1)
            meeting_id = meeting_match.group(2)
            credits_or_type = meeting_match.group(3)  # This could be credits (single digit) or type code (like QZ)
            meeting_date = meeting_match.group(4)     # Meeting date (e.g., "T", "Th", "MWF")
            time = meeting_match.group(5)             # Time (can be "to be arranged" or specific times)
            
            if pattern_type == "normal":
                if has_restr:
                    # With Restr: Restr <A HREF=...>SLN</A> MeetingID Credits/Type MeetingDate Time <A HREF=...>Building</A> Room Instructor Status Enrolled/Capacity [AdditionalCode]
                    building = meeting_match.group(6)         # Building code (from <A HREF=...>Building</A>)
                    room = meeting_match.group(7)             # Room number (after </A>)
                    instructor = (meeting_match.group(8) or "").strip()  # Instructor name (can have spaces/commas)
                    status = meeting_match.group(9)           # Open/Closed
                    enrolled = int(meeting_match.group(10))   # Enrolled count
                    capacity_str = (meeting_match.group(11) or "").strip()  # Capacity (may have E suffix)
                    additional_code = meeting_match.group(12) if meeting_match.lastindex >= 12 and meeting_match.group(12) else ""  # Additional codes like "B"
                else:
                    # Without Restr: [>] <A HREF=...>SLN</A> MeetingID Credits/Type MeetingDate Time [Building/Room] Instructor Status Enrolled/Capacity [AdditionalCode]
                    building_room = (meeting_match.group(6) or "").strip()  # Building/Room info (may be "* *" for to be arranged)
                    instructor = (meeting_match.group(7) or "").strip()  # Instructor name (can have spaces/commas)
                    status = meeting_match.group(8)           # Open/Closed
                    enrolled = int(meeting_match.group(9))   # Enrolled count
                    capacity_str = (meeting_match.group(10) or "").strip()  # Capacity (may have E suffix)
                    additional_code = meeting_match.group(11) if meeting_match.lastindex >= 11 and meeting_match.group(11) else ""  # Additional codes like "B"
                    
                    # Parse building/room for non-Restr entries
                    if building_room == "* *":
                        building = ""
                        room = ""
                    else:
                        # Try to extract building and room from the combined string
                        building = ""
                        room = ""
            else:  # pattern_type == "arranged"
                if has_restr:
                    # With Restr: Restr <A HREF=...>SLN</A> MeetingID Credits/Type MeetingDate "to be arranged" [Building/Room] Instructor Status Enrolled/Capacity [AdditionalCode]
                    building_room = (meeting_match.group(6) or "").strip()  # Building/Room info (may be "* *" for to be arranged)
                    instructor = (meeting_match.group(7) or "").strip()  # Instructor name (can have spaces/commas)
                    status = meeting_match.group(8)           # Open/Closed
                    enrolled = int(meeting_match.group(9))   # Enrolled count
                    capacity_str = (meeting_match.group(10) or "").strip()  # Capacity (may have E suffix)
                    additional_code = meeting_match.group(11) if meeting_match.lastindex >= 11 and meeting_match.group(11) else ""  # Additional codes like "B"
                    
                    # Parse building/room for "to be arranged" entries with Restr
                    if building_room == "* *" or building_room.strip() == "":
                        building = ""
                        room = ""
                    else:
                        # Try to extract building and room from the combined string
                        building = ""
                        room = ""
                else:
                    # Without Restr: [>] <A HREF=...>SLN</A> MeetingID Credits/Type MeetingDate "to be arranged" [Building/Room] Instructor Status Enrolled/Capacity [AdditionalCode]
                    # Group structure: SLN(1) MeetingID(2) Credits(3) MeetingDate(4) "to be arranged"(5) Building/Room(6) Instructor(7) Status(8) Enrolled(9) Capacity(10) AdditionalCode(11)
                    building_room = (meeting_match.group(6) or "").strip()  # Building/Room info (may be "* *" for to be arranged)
                    instructor = (meeting_match.group(7) or "").strip()  # Instructor name (can have spaces/commas)
                    status = meeting_match.group(8)           # Open/Closed
                    enrolled = int(meeting_match.group(9))   # Enrolled count
                    capacity_str = (meeting_match.group(10) or "").strip()  # Capacity (may have E suffix)
                    additional_code = meeting_match.group(11) if meeting_match.lastindex >= 11 and meeting_match.group(11) else ""  # Additional codes like "B"
            
            # Parse capacity and check for estimated enrollment
            estimated_enrollment = capacity_str.endswith('E')
            if estimated_enrollment:
                try:
                    capacity = int(capacity_str[:-1])  # Remove 'E' suffix
                except ValueError:
                    # If capacity can't be parsed, it might be part of additional_code
                    if is_math116:
                        print(f"⚠️ Warning: Could not parse capacity '{capacity_str[:-1]}' for SLN {sln}")
                    capacity = 0
            else:
                try:
                    capacity = int(capacity_str)
                except ValueError:
                    # If capacity can't be parsed, it might be part of additional_code
                    if is_math116:
                        print(f"⚠️ Warning: Could not parse capacity '{capacity_str}' for SLN {sln}")
                    # Try to extract the actual capacity if it contains non-numeric characters
                    # Look for patterns like "120 B" where B is the additional code
                    capacity_match = re.search(r'(\d+)', capacity_str)
                    if capacity_match:
                        capacity = int(capacity_match.group(1))
                        # The remaining part might be the additional code
                        remaining = capacity_str.replace(capacity_match.group(1), '').strip()
                        if remaining and not additional_code:
                            additional_code = remaining
                    else:
                        # If no numeric capacity found, this might be a credit type or additional code
                        # Set capacity to 0 and treat the whole string as additional info
                        capacity = 0
                        if not additional_code:
                            additional_code = capacity_str
            
            days = meeting_date  # For now, set days same as meeting_date
            
            # Determine if this is credits or meeting type code based on meeting_id length
            if len(meeting_id) == 1:
                # Single character meeting ID = lecture, next field is credits
                credits = credits_or_type
                meeting_type_code = ""  # Lectures don't have type codes
            else:
                # Double character meeting ID = other type, next field is type code
                credits = ""  # Non-lectures don't have credits in this field
                meeting_type_code = credits_or_type
            
            # Process additional lines for multiple meeting times and descriptions
            additional_meeting_times = []
            description_lines = []
            
            for line in additional_lines:
                # Check if this line contains additional meeting time information
                # Pattern: Day Time Building Room Instructor
                time_pattern = r'^(\w+)\s+([^\s]+)\s+<A[^>]*>(\w+)</A>\s+(\w+)\s+(.+)$'
                time_match = re.search(time_pattern, line)
                
                if time_match:
                    # This is an additional meeting time
                    additional_day = time_match.group(1)
                    additional_time = time_match.group(2)
                    additional_building = time_match.group(3)
                    additional_room = time_match.group(4)
                    additional_instructor = time_match.group(5).strip()
                    
                    additional_meeting_times.append({
                        'day': additional_day,
                        'time': additional_time,
                        'building': additional_building,
                        'room': additional_room,
                        'instructor': additional_instructor
                    })
                else:
                    # This is a description line
                    description_lines.append(line)
            
            # Combine all description lines
            description = ' '.join(description_lines).strip()
            
            # Create the first CourseMeeting object (main meeting)
            main_meeting = CourseMeeting(
                sln=sln,
                course_code=course_code,
                meeting_id=meeting_id,
                meeting_type_code=meeting_type_code,
                credits=credits,
                meeting_date=meeting_date,
                days=days,
                time=time,
                building=building,
                room=room,
                instructor=instructor,
                professor_name=instructor,  # Keep for compatibility but they're the same
                status=status,
                enrolled=enrolled,
                capacity=capacity,
                max_capacity=capacity,
                current_capacity=enrolled,
                meeting_classification="",  # Remove this field from CSV output
                quarter=quarter,
                year=year,
                meeting_times=time,
                notes=None,
                description=description,
                additional_code=additional_code,
                enrl_restr=enrl_restr,
                estimated_enrollment=estimated_enrollment
            )
            meetings.append(main_meeting)
            
            # Create additional CourseMeeting objects for each additional meeting time
            for i, add_time in enumerate(additional_meeting_times):
                # Create a unique meeting ID for additional times (e.g., "AA-1", "AA-2")
                additional_meeting_id = f"{meeting_id}-{i+1}"
                
                additional_meeting = CourseMeeting(
                    sln=sln,  # Same SLN as main meeting
                    course_code=course_code,
                    meeting_id=additional_meeting_id,
                    meeting_type_code=meeting_type_code,
                    credits=credits,
                    meeting_date=add_time['day'],
                    days=add_time['day'],
                    time=add_time['time'],
                    building=add_time['building'],
                    room=add_time['room'],
                    instructor=add_time['instructor'],
                    professor_name=add_time['instructor'],  # Keep for compatibility
                    status=status,  # Same status as main meeting
                    enrolled=enrolled,  # Same enrollment as main meeting
                    capacity=capacity,  # Same capacity as main meeting
                    max_capacity=capacity,
                    current_capacity=enrolled,
                    meeting_classification="",  # Remove this field from CSV output
                    quarter=quarter,
                    year=year,
                    meeting_times=add_time['time'],
                    notes=None,
                    description=description,  # Same description as main meeting
                    additional_code=additional_code,
                    enrl_restr=enrl_restr,  # Same enrollment restriction as main meeting
                    estimated_enrollment=estimated_enrollment  # Same estimated enrollment as main meeting
                )
                meetings.append(additional_meeting)
            
            if is_math116:
                print(f"✅ Parsed meeting data:")
                print(f"   Main Meeting - SLN: {sln}, ID: {meeting_id}, Credits: {credits}")
                print(f"   Meeting Type Code: {meeting_type_code}, Date: {meeting_date}")
                print(f"   Time: {time}, Building: {building}, Room: {room}")
                print(f"   Instructor: {instructor}, Status: {status}")
                print(f"   Enrollment: {enrolled}/{capacity}, Additional Code: {additional_code}")
                print(f"   Enrollment Restriction: {enrl_restr}")
                print(f"   Estimated Enrollment: {estimated_enrollment}")
                print(f"   Description: {description}")
            
            if additional_meeting_times and is_math116:
                print(f"   Created {len(additional_meeting_times)} additional meeting objects:")
                for i, add_time in enumerate(additional_meeting_times):
                    print(f"     {i+1}. {add_time['day']} {add_time['time']} {add_time['building']} {add_time['room']} {add_time['instructor']}")
            
            if is_math116:
                print(f"   Total meetings created for this section: {1 + len(additional_meeting_times)}")
            
        else:
            if is_math116:
                print("❌ Could not parse meeting data")
                print(f"   Raw text: '{meeting_text}'")
                print("🔍 No regex pattern matched the main line")
    
    if is_math116:
        print(f"\n✅ Meeting parsing complete:")
        print(f"   Found {len(meetings)} valid meetings")
        print("=" * 60)
    
    return meetings


def _clean_instructor_name(instructor: str) -> str:
    """
    Clean and normalize instructor names.
    
    Args:
        instructor: Raw instructor name from HTML
        
    Returns:
        str: Cleaned instructor name
    """
    # TODO: Implement this function
    # 1. Strip leading/trailing whitespace
    # 2. Normalize multiple spaces to single space
    # 3. Handle special characters (commas, periods, etc.)
    # 4. Return clean, consistent format
    pass


def _parse_time_slot(time_str: str) -> str:
    """
    Parse and normalize time slot information.
    
    Args:
        time_str: Raw time string from HTML
        
    Returns:
        str: Normalized time string
    """
    # TODO: Implement this function
    # 1. Handle various time formats (1130-1220, 9:30-10:20, etc.)
    # 2. Normalize to consistent format
    # 3. Handle edge cases (TBA, TBD, etc.)
    # 4. Return clean time string
    pass


def _parse_enrollment_numbers(enrollment_str: str) -> tuple[int, int]:
    """
    Parse enrollment numbers from strings like "357/376".
    
    Args:
        enrollment_str: Raw enrollment string (e.g., "357/376")
        
    Returns:
        tuple[int, int]: (enrolled, capacity)
    """
    # TODO: Implement this function
    # 1. Split on "/" character
    # 2. Convert to integers
    # 3. Handle edge cases (missing data, invalid formats)
    # 4. Return tuple of (enrolled, capacity)
    pass


# =============================================================================
# ASSIGNMENT HINTS - Functions you should and should NOT use
# =============================================================================
"""
FUNCTIONS YOU SHOULD USE:

1. BeautifulSoup (for HTML parsing):
   from bs4 import BeautifulSoup
   soup = BeautifulSoup(html, 'html.parser')
   tables = soup.find_all('table', bgcolor='#99ccff')
   links = soup.find_all('a')
   text = soup.get_text()

2. Regular Expressions (for pattern matching):
   import re
   matches = re.findall(pattern, text, re.DOTALL)
   match = re.search(pattern, text)
   groups = match.groups() if match else None

3. String Methods (for text processing):
   text.strip()                    # Remove whitespace
   text.split('/')                 # Split on delimiter
   text.replace('&nbsp;', ' ')     # Replace HTML entities
   ' '.join(text.split())          # Normalize whitespace

4. Type Conversion:
   int('123')                      # Convert to integer
   str(123)                        # Convert to string

5. List/Data Structure Methods:
   courses.append(course)          # Add to list
   meetings = []                   # Create empty list
   course_dict = {}                # Create empty dict

FUNCTIONS YOU SHOULD NOT USE:

1. External HTML parsing libraries (other than BeautifulSoup):
   ❌ lxml (unless you want to use it as BeautifulSoup backend)
   ❌ html.parser (use BeautifulSoup instead)
   ❌ xml.etree.ElementTree

2. Complex data manipulation libraries:
   ❌ pandas (overkill for this task)
   ❌ numpy (not needed)
   ❌ requests (already handled by schedule.py)

3. Advanced regex features (keep it simple):
   ❌ Complex lookahead/lookbehind assertions
   ❌ Recursive patterns
   ❌ Advanced group naming

4. File I/O (not needed in parser):
   ❌ open(), read(), write()
   ❌ csv module
   ❌ json module

5. Network/HTTP functions:
   ❌ requests.get()
   ❌ urllib
   ❌ httpx

USEFUL REGEX PATTERNS:

1. Course blocks:
   r'<table bgcolor=\'#99ccff\'.*?</table>(?:<table[^>]*>.*?</table>)*'

2. Meeting data:
   r'<A HREF=[^>]*>(+)</A>\s+(\w+)\s+(\w+)\s+(\w+)\s+(+-+)\s+<A[^>]*>(\w+)</A>\s+(+)\s+([^<]+?)\s+(Open|Closed)\s+(+)/(+)'

3. Course code and title:
   r'<A NAME=(\w+)>(\w+)\s+(+)\s*</A>.*?<A[^>]*>([^<]+)</A>'

4. HTML entities:
   r'&nbsp;' -> ' '
   r'&amp;' -> '&'
   r'&lt;' -> '<'
   r'&gt;' -> '>'

TESTING TIPS:

1. Start with simple functions:
   _parse_enrollment_numbers("357/376") -> (357, 376)

2. Test with real data:
   with open('output/cse_WIN_2023.html', 'r') as f:
       html = f.read()

3. Use print statements for debugging:
   print(f"Found {len(courses)} courses")
   print(f"Meeting data: {meeting_data}")

4. Handle edge cases:
   - Empty strings
   - Missing data
   - Special characters
   - Malformed HTML

COMMON MISTAKES TO AVOID:

1. Don't over-engineer - keep it simple
2. Don't forget to handle edge cases
3. Don't use complex regex when simple string methods work
4. Don't forget to strip whitespace from extracted text
5. Don't assume HTML structure is always perfect
6. Don't forget to convert strings to integers where needed
"""
