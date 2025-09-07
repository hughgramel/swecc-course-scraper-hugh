"""
HTML parser for UW time schedule pages.

This module contains functions to parse raw HTML from UW's time schedule
pages into structured Course and CourseSection objects.
"""

import re
from typing import List, Dict, Optional
from ..models.course import Course, CourseSection


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
        sections=[
            CourseSection(
                sln="12924",
                course_code="CSE 122",
                section_id="A",
                section_type="4",
                days="WF",
                time="1130-1220",
                building="KNE",
                room="130",
                instructor="Natsuhara,Miya Kaye",
                status="Open",
                enrolled=357,
                capacity=376,
                quarter="WIN",
                year=2023,
                notes="NO CREDIT FOR STUDENTS WHO HAVE COMPLETED CSE 143"
            ),
            CourseSection(
                sln="12925",
                course_code="CSE 122",
                section_id="AA",
                section_type="QZ",
                days="TTh",
                time="830-920",
                building="MGH",
                room="288",
                instructor="Lin,Melissa",
                status="Open",
                enrolled=17,
                capacity=21,
                quarter="WIN",
                year=2023,
                notes=None
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
        sections=[
            # ... more sections
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
        print(f"\n--- Processing Course Block {i+1}/{len(course_blocks)} ---")
        
        # Parse course header
        print("📋 Parsing course header...")
        header_data = _parse_course_header(course_block)
        
        if not header_data or not header_data.get('code'):
            print(f"❌ Skipping block {i+1} - no valid header data")
            continue
        
        course_code = header_data['code']
        print(f"✅ Header parsed: {course_code}")
        
        # Parse course sections
        print("📋 Parsing course sections...")
        sections = _parse_course_sections(course_block, course_code, quarter, year)
        print(f"✅ Found {len(sections)} sections")
        
        # Create Course object
        print("📋 Creating Course object...")
        course = Course(
            course_code=header_data['code'],
            title=header_data['title'],
            prerequisites=header_data['prerequisites'],
            credits=header_data['credits'],
            quarter=quarter,
            year=year,
            sections=sections
        )
        
        courses.append(course)
        print(f"✅ Course created: {course_code} with {len(sections)} sections")
    
    print(f"\n🎯 PARSING COMPLETE")
    print(f"   Total courses parsed: {len(courses)}")
    print(f"   Total sections: {sum(len(course.sections) for course in courses)}")
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


def _parse_course_header(course_block: str) -> Dict[str, str]:
    """
    Parse course header information from a course block.
    
    Args:
        course_block: HTML block containing one course and its sections
        
    Returns:
        Dict[str, str]: Dictionary with keys: 'code', 'title', 'prerequisites', 'credits'
    """
    print("=" * 60)
    print("PARSING COURSE HEADER")
    print("=" * 60)

    # Find the course header table (with background color)
    header_pattern = r'<table[^>]*bgcolor=[\'"][^\'\"]*[\'"][^>]*>.*?</table>'
    header_match = re.search(header_pattern, course_block, re.DOTALL)
    
    if not header_match:
        print("❌ No course header table found")
        return {}
    
    header_html = header_match.group(0)
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
        print(f"📚 Course Code: '{course_code}'")
    else:
        print("❌ No course code found")
        course_code = ""
    
    # Extract title from course title link
    title_pattern = r'<A HREF=[^>]*>([^<]+)</A>'
    title_match = re.search(title_pattern, header_html)
    
    if title_match:
        title = title_match.group(1).strip()
        print(f"📖 Title: '{title}'")
    else:
        print("❌ No title found")
        title = ""
    
    # Extract prerequisites from header text
    prereq_pattern = r'Prerequisites[:\s]*([^<\n]+)'
    prereq_match = re.search(prereq_pattern, header_html, re.IGNORECASE)
    
    if prereq_match:
        prerequisites = prereq_match.group(1).strip()
        print(f"📋 Prerequisites: '{prerequisites}'")
    else:
        print("ℹ️  No prerequisites found")
        prerequisites = ""
    
    # Extract credits from header text
    credits_pattern = r'(\d+)\s*credits?'
    credits_match = re.search(credits_pattern, header_html, re.IGNORECASE)
    
    if credits_match:
        credits = credits_match.group(1)
        print(f"🎓 Credits: '{credits}'")
    else:
        print("ℹ️  No credits found")
        credits = ""
    
    result = {
        'code': course_code,
        'title': title,
        'prerequisites': prerequisites,
        'credits': credits
    }
    
    print(f"✅ Header parsing complete:")
    print(f"   Result: {result}")
    print("=" * 60)
    
    return result


def _parse_course_sections(course_block: str, course_code: str, quarter: str, year: int) -> List[CourseSection]:
    """
    Parse individual sections from a course block.
    
    Args:
        course_block: HTML block containing one course and its sections
        course_code: Course code (e.g., "CSE 122")
        quarter: Quarter code (e.g., "WIN")
        year: Year (e.g., 2023)
        
    Returns:
        List[CourseSection]: List of parsed section objects


        
    """
    print("=" * 60)
    print("PARSING COURSE SECTIONS")
    print("=" * 60)
    print(f"📚 Course: {course_code}")
    print(f"📅 Quarter: {quarter} {year}")
    
    # Find all section tables (tables without background color)
    section_pattern = r'<table[^>]*(?!bgcolor)[^>]*>.*?</table>'
    section_tables = re.findall(section_pattern, course_block, re.DOTALL)
    
    print(f"🔍 Found {len(section_tables)} section tables")
    
    sections = []
    
    for i, section_html in enumerate(section_tables):
        print(f"\n--- Section {i+1} ---")
        print(f"📋 Section HTML length: {len(section_html)} characters")
        print(f"📋 Section preview: {section_html[:150]}...")
        
        # Extract section data from <pre> tags (they don't have closing </pre> tags)
        pre_pattern = r'<pre[^>]*>(.*?)(?=</td></tr></table>)'
        pre_match = re.search(pre_pattern, section_html, re.DOTALL)
        
        if not pre_match:
            print("❌ No <pre> tag found in section")
            continue
        
        section_text = pre_match.group(1).strip()
        print(f"📝 Section text: '{section_text}'")
        
        # Parse section data using regex
        # Pattern: <A HREF=...>SLN</A> SectionID SectionType Days Time Building Room Instructor Status Enrolled/Capacity
        # The format is: SLN SectionID SectionType Days Time * * Instructor Status Enrolled/Capacity
        section_pattern = r'<A HREF=[^>]*>(\d+)</A>\s+(\w+)\s+(\w+)\s+(\w+)\s+([^\s]+)\s+\*\s+\*\s+([^<]+?)\s+(Open|Closed)\s+(\d+)/(\d+)'
        section_match = re.search(section_pattern, section_text)
        
        if section_match:
            sln = section_match.group(1)
            section_id = section_match.group(2)
            section_type = section_match.group(3)
            days = section_match.group(4)
            time = section_match.group(5)
            # Building and room are marked as * * in this format
            building = "*"
            room = "*"
            instructor = section_match.group(6).strip()
            status = section_match.group(7)
            enrolled = int(section_match.group(8))
            capacity = int(section_match.group(9))
            
            print(f"✅ Parsed section data:")
            print(f"   SLN: {sln}")
            print(f"   Section ID: {section_id}")
            print(f"   Section Type: {section_type}")
            print(f"   Days: {days}")
            print(f"   Time: {time}")
            print(f"   Building: {building}")
            print(f"   Room: {room}")
            print(f"   Instructor: {instructor}")
            print(f"   Status: {status}")
            print(f"   Enrollment: {enrolled}/{capacity}")
            
            # Create CourseSection object (placeholder for now)
            section = CourseSection(
                sln=sln,
                course_code=course_code,
                section_id=section_id,
                section_type=section_type,
                days=days,
                time=time,
                building=building,
                room=room,
                instructor=instructor,
                status=status,
                enrolled=enrolled,
                capacity=capacity,
                quarter=quarter,
                year=year,
                notes=None
            )
            sections.append(section)
            
        else:
            print("❌ Could not parse section data")
            print(f"   Raw text: '{section_text}'")
    
    print(f"\n✅ Section parsing complete:")
    print(f"   Found {len(sections)} valid sections")
    print("=" * 60)
    
    return sections


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
   sections = []                   # Create empty list
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

2. Section data:
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
   print(f"Section data: {section_data}")

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
