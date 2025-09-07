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
    # TODO: Implement this function
    # 1. Extract course blocks from HTML using _extract_course_blocks()
    # 2. For each course block:
    #    - Parse course header using _parse_course_header()
    #    - Parse sections using _parse_course_sections()
    #    - Create Course object with parsed data
    # 3. Return list of all Course objects
    pass


def _extract_course_blocks(html: str) -> List[str]:
    """
    Extract individual course blocks from HTML.
    
    Args:
        html: Raw HTML content
        
    Returns:
        List[str]: List of HTML blocks, each containing one course and its sections
    """
    # TODO: Implement this function
    # 1. Use regex to find course header tables (bgcolor='#99ccff')
    # 2. For each header, capture the header + all following section tables
    # 3. Return list of complete course blocks
    
    # Regex pattern hint:
    # Course header: <table bgcolor='#99ccff'.*?</table>
    # Followed by: (?:<table[^>]*>.*?</table>)*
    # Use re.DOTALL flag for multiline matching
    pass


def _parse_course_header(course_block: str) -> Dict[str, str]:
    """
    Parse course header information from a course block.
    
    Args:
        course_block: HTML block containing one course and its sections
        
    Returns:
        Dict[str, str]: Dictionary with keys: 'code', 'title', 'prerequisites', 'credits'
    """
    # TODO: Implement this function
    # 1. Find course header table (bgcolor='#99ccff')
    # 2. Extract course code from <A NAME=...> tags
    # 3. Extract title from course title link
    # 4. Extract prerequisites from header text
    # 5. Extract credits from header text
    # 6. Return structured dictionary
    
    # HTML structure to parse:
    # <table bgcolor='#99ccff'>
    #     <tr><td><b><A NAME=cse122>CSE&nbsp;&nbsp; 122 </A>&nbsp;<A HREF=...>COMP PROGRAMMING II </A></b></td>
    #         <td><b>(NSc,RSN)</b></td>
    #         <td><b>Prerequisites</b></td></tr>
    # </table>
    pass


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
    # TODO: Implement this function
    # 1. Find all section tables in the course block
    # 2. For each section, extract:
    #    - SLN from href link
    #    - Section ID (A, AA, QZ, etc.)
    #    - Section type (4, QZ, etc.)
    #    - Days (TTh, WF, etc.)
    #    - Time (1130-1220, etc.)
    #    - Building and room
    #    - Instructor name
    #    - Status (Open/Closed)
    #    - Enrollment numbers
    # 3. Create CourseSection objects
    # 4. Handle edge cases (missing data, special characters, etc.)
    
    # HTML structure to parse:
    # <table><tr><td><pre>
    #     <A HREF=...>12917</A> A  4  WF  1130-1220  <A HREF=...>KNE</A>  130  Natsuhara,Miya Kaye  Open  357/376
    # </pre></td></tr></table>
    pass


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
   r'<A HREF=[^>]*>(\d+)</A>\s+(\w+)\s+(\w+)\s+(\w+)\s+(\d+-\d+)\s+<A[^>]*>(\w+)</A>\s+(\d+)\s+([^<]+?)\s+(Open|Closed)\s+(\d+)/(\d+)'

3. Course code and title:
   r'<A NAME=(\w+)>(\w+)\s+(\d+)\s*</A>.*?<A[^>]*>([^<]+)</A>'

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
