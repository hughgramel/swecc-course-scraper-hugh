#!/usr/bin/env python3

import re

# Test the regex pattern with the MATH 116 meeting text
meeting_text = "><A HREF=https://sdb.admin.washington.edu/timeschd/uwnetid/sln.asp?QTRYR=AUT+2023&SLN=23241>23241</A> A  1       to be arranged    *    *        Su,Zhixu                             8/  15E CR/NC         %A"

print("Testing MATH 116 regex pattern:")
print(f"Text: {meeting_text}")
print()

# Current pattern for "to be arranged" without "Restr"
pattern_arranged_no_restr = r'[>\s]*<A HREF=[^>]*>(\d+)</A>\s+(\w+)\s+(\w+)\s+(\w+)\s+(to be arranged)\s+(.+?)\s+(\d+)/(\s*\d+E?)(?:\s+([^<]+?))?'

print(f"Pattern: {pattern_arranged_no_restr}")
print()

match = re.search(pattern_arranged_no_restr, meeting_text)
if match:
    print("✅ Match found!")
    print(f"Groups: {match.groups()}")
    print(f"Number of groups: {len(match.groups())}")
    print(f"Last index: {match.lastindex}")
    for i, group in enumerate(match.groups(), 1):
        print(f"  Group {i}: '{group}'")
        
    # Test capacity parsing
    capacity_str = match.group(8).strip()
    print(f"\nCapacity string: '{capacity_str}'")
    
    # Test the capacity cleaning logic
    estimated_enrollment = capacity_str.endswith('E')
    if estimated_enrollment:
        capacity = int(capacity_str[:-1])  # Remove 'E' suffix
        print(f"Estimated enrollment: True, Capacity: {capacity}")
    else:
        capacity_clean = capacity_str.strip()
        capacity_match = re.match(r'(\d+)', capacity_clean)
        if capacity_match:
            capacity = int(capacity_match.group(1))
            print(f"Parsed capacity: {capacity}")
        else:
            print(f"Could not parse capacity from '{capacity_clean}'")
else:
    print("❌ No match found")
    
    # Try a simpler pattern
    print("\nTrying simpler pattern...")
    simple_pattern = r'[>\s]*<A HREF=[^>]*>(\d+)</A>\s+(\w+)\s+(\w+)\s+(\w+)\s+(to be arranged)\s+(.+?)\s+(\d+)/(\s*\d+E?)'
    simple_match = re.search(simple_pattern, meeting_text)
    if simple_match:
        print("✅ Simple match found!")
        print(f"Groups: {simple_match.groups()}")
        for i, group in enumerate(simple_match.groups(), 1):
            print(f"  Group {i}: '{group}'")
    else:
        print("❌ Simple pattern also failed")
