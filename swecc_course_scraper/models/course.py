"""
Course and section data models.

This module defines the core data structures for representing course information
extracted from UW's time schedule pages.
"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class CourseSection:
    """
    Represents a single section of a course (lecture, quiz, lab, etc.).
    
    This is the most granular unit of course data, containing all the
    information needed for enrollment and scheduling.
    """
    # Core identification
    sln: str                    # Section Line Number (e.g., "12917") - unique identifier for enrollment
    course_code: str           # Course code (e.g., "CSE 122") - links to course catalog
    section_id: str            # Section identifier (e.g., "A", "AA", "QZ") - distinguishes sections
    section_type: str          # Section type (e.g., "4", "QZ") - lecture vs quiz vs lab
    
    # Scheduling information
    days: str                  # Meeting days (e.g., "TTh", "WF") - when the section meets
    time: str                  # Meeting time (e.g., "1130-1220") - start and end times
    building: str              # Building code (e.g., "MGH", "KNE") - where the section meets
    room: str                  # Room number (e.g., "130", "288") - specific room location
    
    # Personnel
    instructor: str            # Instructor name (e.g., "Natsuhara,Miya Kaye") - who teaches
    
    # Enrollment information
    status: str                # Enrollment status (e.g., "Open", "Closed") - can students enroll?
    enrolled: int              # Current enrollment count - how many students enrolled
    capacity: int              # Maximum capacity - how many students can enroll
    
    # Temporal information
    quarter: str               # Quarter (e.g., "WIN") - when this section is offered
    year: int                  # Year (e.g., 2023) - when this section is offered
    
    # Optional information
    notes: Optional[str] = None # Additional notes/restrictions (e.g., prerequisites, credit limits)


@dataclass
class Course:
    """
    Represents a complete course with all its sections.
    
    This aggregates multiple CourseSection objects and provides
    course-level metadata like title, prerequisites, and credits.
    """
    # Core identification
    course_code: str           # Course code (e.g., "CSE 122") - primary identifier
    title: str                 # Course title (e.g., "COMP PROGRAMMING II") - human-readable name
    
    # Course metadata
    prerequisites: str         # Prerequisite information - what students need before taking this course
    credits: str               # Credit information - how many credits this course is worth
    
    # Sections
    sections: List[CourseSection]  # All sections for this course - lectures, quizzes, labs, etc.
    
    # Temporal information
    quarter: str               # Quarter (e.g., "WIN") - when this course is offered
    year: int                  # Year (e.g., 2023) - when this course is offered
