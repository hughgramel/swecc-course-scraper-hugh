"""
Data models for the SWECC Course Scraper.

This package contains dataclasses for representing course and section data
extracted from UW's time schedule pages.
"""

from .course import Course, CourseSection

__all__ = ['Course', 'CourseSection']
