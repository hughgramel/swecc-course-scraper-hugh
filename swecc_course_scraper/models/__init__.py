"""
Data models for the SWECC Course Scraper.

This package contains dataclasses for representing course and meeting data
extracted from UW's time schedule pages.
"""

from .course import Course, CourseMeeting

__all__ = ['Course', 'CourseMeeting']
