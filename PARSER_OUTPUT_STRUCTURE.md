# Parser Output Structure Documentation

## Overview

The `_extract_course_blocks()` function extracts and returns a list of course blocks from UW time schedule HTML pages. Each course block represents one complete course with all its sections.

## What is a "Course Block"?

A **course block** is a complete HTML section that contains:

1. **One course header table** (with quarter-specific background color)
2. **All section tables** that belong to that course (without background color)
3. **Any content between tables** (including `<br>` tags, notes, etc.)

### Example Course Block Structure:
```html
<!-- Course Header Table -->
<table bgcolor='#99ccff' width='100%'>
<tr><td><b><A NAME=math103>MATH&nbsp;&nbsp; 103 </A>&nbsp;<A HREF=...>INTRO ELEM FUNCTION </A></b></td></tr>
</table>

<!-- Section Table 1 -->
<table width="100%"><tr><td><pre>
<A HREF=...>17215</A> A  5  MTWThF 1030-1120  ICT  226  Skov,Christopher  15/30
</pre></td></tr></table>

<!-- Section Table 2 -->
<table width="100%"><tr><td><pre>
<A HREF=...>17216</A> AA QZ  TTh  1230-120  KNE  110  PANDYA,NIKHIL  37/40
</pre></td></tr></table>
```

## Function Output

### Return Type
```python
List[str]  # List of HTML strings, each containing one complete course block
```

### Data Structure for Next Pipeline

Each course block string contains structured HTML that can be parsed into:

```python
{
    "course_header": {
        "html": "<table bgcolor='...'>...</table>",
        "course_code": "MATH 103",
        "title": "INTRO ELEM FUNCTION",
        "prerequisites": "...",
        "credits": "5"
    },
    "sections": [
        {
            "html": "<table width='100%'>...</table>",
            "sln": "17215",
            "section_id": "A",
            "section_type": "5",
            "days": "MTWThF",
            "time": "1030-1120",
            "building": "ICT",
            "room": "226",
            "instructor": "Skov,Christopher",
            "enrolled": 15,
            "capacity": 30
        },
        {
            "html": "<table width='100%'>...</table>",
            "sln": "17216",
            "section_id": "AA",
            "section_type": "QZ",
            "days": "TTh",
            "time": "1230-120",
            "building": "KNE",
            "room": "110",
            "instructor": "PANDYA,NIKHIL",
            "enrolled": 37,
            "capacity": 40
        }
    ]
}
```

## Current Implementation Status

### ✅ Completed
- **Course block extraction** - Working perfectly
- **Table counting** - All test files pass with correct counts
- **HTML structure parsing** - Extracts between `</P>` and `<P>` tags
- **Header table identification** - Correctly identifies course headers by background color

### 🔄 Next Steps Required

1. **Parse course header information** (`_parse_course_header()`)
   - Extract course code from `<A NAME=...>` tags
   - Extract title from course title link
   - Extract prerequisites and credits from header text

2. **Parse section information** (`_parse_course_sections()`)
   - Extract SLN from href links
   - Parse section ID, type, days, time
   - Extract building, room, instructor
   - Parse enrollment numbers and status

3. **Create Course and CourseSection objects**
   - Use the existing model classes in `swecc_course_scraper.models.course`
   - Return structured data instead of raw HTML

## Test Results Summary

All test files now pass with perfect accuracy:

| File | Headers | Sections | Total | Status |
|------|---------|----------|-------|---------|
| math_WIN_2023.html | 65 | 248 | 313 | ✅ PASS |
| math_SPR_2021.html | 57 | 186 | 243 | ✅ PASS |
| math_SUM_2023.html | 36 | 63 | 99 | ✅ PASS |
| math_AUT_2023.html | 57 | 276 | 333 | ✅ PASS |
| chem_SPR_2021.html | 54 | 229 | 283 | ✅ PASS |

## Analysis Files

Complete course block analysis files are available in `table_analysis/` folder:
- `course_blocks_math_WIN_2023.txt`
- `course_blocks_math_SPR_2021.txt`
- `course_blocks_math_SUM_2023.txt`
- `course_blocks_math_AUT_2023.txt`
- `course_blocks_chem_SPR_2021.txt`

These files show the complete structure of each course block with headers and sections grouped together.

## Next Pipeline Requirements

The next pipeline should:

1. **Take course block HTML strings** from `_extract_course_blocks()`
2. **Parse each block** into structured data using `_parse_course_header()` and `_parse_course_sections()`
3. **Create Course objects** with lists of CourseSection objects
4. **Return List[Course]** as specified in the function documentation

The foundation is solid - the course blocks are correctly extracted and contain all the necessary information for parsing into structured data.
