#!/usr/bin/env python3

import re

# The actual text from the HTML
text = 'Restr  <A HREF=https://sdb.admin.washington.edu/timeschd/uwnetid/sln.asp?QTRYR=AUT+2023&SLN=18241>18241</A> D  5       to be arranged                  Conroy,Matthew             Open    100/ 120                B'

print("Text to parse:")
print(repr(text))
print()

# New pattern that accounts for "to be arranged" being multiple words and no meeting date
pattern_arranged = r'Restr\s+<A HREF=[^>]*>(\d+)</A>\s+(\w+)\s+(\w+)\s+(\w+)\s+(to be arranged)\s+([^<]+?)\s+(Open|Closed)\s+(\d+)/(\s*\d+)(?:\s+(\w+))?'

print("New pattern:")
print(pattern_arranged)
print()

match = re.search(pattern_arranged, text)
if match:
    print("✅ Match found!")
    print("Groups:")
    for i, group in enumerate(match.groups()):
        print(f"  {i+1}: {repr(group)}")
else:
    print("❌ No match found")
    
    # Let's try a pattern that doesn't require a meeting date field
    print("\nTrying pattern without meeting date requirement...")
    pattern_no_date = r'Restr\s+<A HREF=[^>]*>(\d+)</A>\s+(\w+)\s+(\w+)\s+(to be arranged)\s+([^<]+?)\s+(Open|Closed)\s+(\d+)/(\s*\d+)(?:\s+(\w+))?'
    match2 = re.search(pattern_no_date, text)
    if match2:
        print("✅ No-date match found!")
        for i, group in enumerate(match2.groups()):
            print(f"  {i+1}: {repr(group)}")
    else:
        print("❌ Still no match")
        
        # Let's try to understand the structure better
        print("\nAnalyzing structure...")
        # Split by spaces and see what we get
        parts = text.split()
        print("Parts:", parts)
        
        # Find the position of "to be arranged"
        try:
            tba_pos = parts.index("to")
            print(f"'to' found at position {tba_pos}")
            print(f"Parts around 'to': {parts[tba_pos-2:tba_pos+5]}")
        except ValueError:
            print("'to' not found in parts")