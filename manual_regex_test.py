#!/usr/bin/env python3

import re

# Test the regex pattern with actual HTML data
test_line = "Restr  <A HREF=https://sdb.admin.washington.edu/timeschd/uwnetid/sln.asp?QTRYR=AUT+2023&SLN=18214>18214</A> A  5       MWF    830-920    <A HREF=/students/maps/map.cgi?PCAR>PCAR</A> 192      Heald,Andy M               Open    227/ 240"

print("Testing regex pattern with actual HTML data:")
print(f"Input: {test_line}")
print()

# Test the normal pattern
pattern_normal = r'Restr\s+<A HREF=[^>]*>(\d+)</A>\s+(\w+)\s+(\w+)\s+(\w+)\s+([^\s]+)\s+<A[^>]*>(\w+)</A>\s+(\w+)\s+([^<]+?)\s+(Open|Closed)\s+(\d+)/(\s*\d+)(?:\s+(\w+))?'
match = re.search(pattern_normal, test_line)

if match:
    print("✅ Pattern matched successfully!")
    print("Groups:")
    for i, group in enumerate(match.groups()):
        print(f"  Group {i+1}: {repr(group)}")
    
    print()
    print("Parsed data:")
    print(f"  SLN: {match.group(1)}")
    print(f"  Meeting ID: {match.group(2)}")
    print(f"  Credits/Type: {match.group(3)}")
    print(f"  Meeting Date: {match.group(4)}")
    print(f"  Time: {match.group(5)}")
    print(f"  Building: {match.group(6)}")
    print(f"  Room: {match.group(7)}")
    print(f"  Instructor: {match.group(8).strip()}")
    print(f"  Status: {match.group(9)}")
    print(f"  Enrolled: {match.group(10)}")
    print(f"  Capacity: {match.group(11).strip()}")
    if match.group(12):
        print(f"  Additional Code: {match.group(12)}")
    else:
        print(f"  Additional Code: (none)")
else:
    print("❌ Pattern did not match")
    
    # Try a simpler pattern to debug
    print("\nTrying simpler pattern...")
    simple_pattern = r'<A HREF=[^>]*>(\d+)</A>\s+(\w+)\s+(\w+)'
    simple_match = re.search(simple_pattern, test_line)
    if simple_match:
        print("✅ Simple pattern matched:")
        for i, group in enumerate(simple_match.groups()):
            print(f"  Group {i+1}: {repr(group)}")
    else:
        print("❌ Even simple pattern failed")

