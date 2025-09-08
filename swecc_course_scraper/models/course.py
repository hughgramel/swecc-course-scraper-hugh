"""
Course and meeting data models.

This module defines the core data structures for representing course information
extracted from UW's time schedule pages.
"""

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class CourseMeeting:
    """
    Represents a single scheduled meeting of a course (lecture, quiz, lab, seminar, etc.).
    
    This is the most granular unit of course data, containing all the
    information needed for enrollment and scheduling.
    """
    # Core identification
    sln: str = ""                    # Student Line Number (e.g., "12917") - unique identifier for enrollment
    course_code: str = ""           # Course code (e.g., "CSE 122") - links to course catalog
    meeting_id: str = ""            # Meeting identifier (e.g., "A", "AA") - distinguishes meetings
    meeting_type_code: str = ""     # Meeting type code (e.g., "QZ", "LB") - actual codes from schedule
    credits: str = ""               # Credit amount (e.g., "5") - number of credits for this meeting
    meeting_date: str = ""          # Meeting date (e.g., "T", "Th", "MWF", "to be arranged") - when the meeting occurs
    
    # Scheduling information
    days: str = ""                  # Meeting days (e.g., "TTh", "WF") - when the meeting occurs
    time: str = ""                  # Meeting time (e.g., "1130-1220") - start and end times
    building: str = ""              # Building code (e.g., "MGH", "KNE") - where the meeting occurs
    room: str = ""                  # Room number (e.g., "130", "288") - specific room location
    meeting_date: str = ""          # Meeting date information - handles days correctly
    
    # Personnel
    instructor: str = ""            # Instructor name (e.g., "Natsuhara,Miya Kaye") - who teaches
    professor_name: str = ""        # Professor name field (alternative to instructor)
    
    # Enrollment information
    status: str = ""                # Enrollment status (e.g., "Open", "Closed") - can students enroll?
    enrolled: int = 0               # Current enrollment count - how many students enrolled
    capacity: int = 0               # Maximum capacity - how many students can enroll
    max_capacity: int = 0           # Maximum capacity field (alternative to capacity)
    current_capacity: int = 0       # Current capacity field (alternative to enrolled)
    
    # Meeting classification
    meeting_classification: str = "" # Meeting classification (e.g., "lecture", "quiz", "lab", "seminar")
    
    # Temporal information
    quarter: str = ""               # Quarter (e.g., "WIN") - when this meeting is offered
    year: int = 0                   # Year (e.g., 2023) - when this meeting is offered
    meeting_times: str = ""         # Meeting times field - detailed time information
    
    # Optional information
    notes: Optional[str] = None     # Additional notes/restrictions (e.g., prerequisites, credit limits)
    description: str = ""           # Description text (e.g., "NO OVERLOADS", "MWF ASYNCHRONOUS REMOTE LECTURES")
    additional_code: str = ""       # Additional codes (e.g., "B") that appear after capacity
    enrl_restr: str = ""           # Enrollment restriction codes (e.g., "A 5", "AA QZ", "Restr")
    estimated_enrollment: bool = False  # True if capacity has "E" suffix indicating estimated enrollment


@dataclass
class Course:
    """
    Represents a complete course with all its scheduled meetings.
    
    This aggregates multiple CourseMeeting objects and provides
    course-level metadata like title, prerequisites, and credits.
    """
    # Core identification
    course_code: str           # Course code (e.g., "CSE 122") - primary identifier
    title: str                 # Course title (e.g., "COMP PROGRAMMING II") - human-readable name
    
    # Course metadata
    prerequisites: str         # Prerequisite information - what students need before taking this course
    credits: str               # Credit information - how many credits this course is worth
    credit_types: str          # Credit types (e.g., "NSc,RSN") - from course header
    
    # Meetings
    meetings: List[CourseMeeting]  # All meetings for this course - lectures, quizzes, labs, seminars, etc.
    
    # Temporal information
    quarter: str               # Quarter (e.g., "WIN") - when this course is offered
    year: int                  # Year (e.g., 2023) - when this course is offered
