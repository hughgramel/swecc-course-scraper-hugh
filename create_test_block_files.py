#!/usr/bin/env python3
"""
Create individual test block files for easier inspection.
"""

import os
from tests.test_blocks import get_all_blocks

def create_test_block_files():
    """Create individual test block files for each course."""
    
    test_files = [
        'MATH_WIN_2023',
        'MATH_SPR_2021', 
        'MATH_SUM_2023',
        'MATH_AUT_2023',
        'CHEM_SPR_2021'
    ]
    
    # Create test_blocks directory
    os.makedirs('test_blocks', exist_ok=True)
    
    for file_name in test_files:
        print(f"Creating test block files for {file_name}...")
        
        blocks = get_all_blocks(file_name)
        print(f"  Found {len(blocks)} blocks")
        
        # Create directory for this file
        file_dir = f'test_blocks/{file_name.lower()}'
        os.makedirs(file_dir, exist_ok=True)
        
        # Write each block to a separate file
        for i, block in enumerate(blocks):
            block_file = f'{file_dir}/block_{i:02d}.html'
            with open(block_file, 'w', encoding='utf-8') as f:
                f.write(block)
        
        print(f"  Created {len(blocks)} block files in {file_dir}/")
    
    print(f"\n✅ Created test block files in test_blocks/ directory")
    print("You can now inspect individual course blocks easily!")

if __name__ == "__main__":
    create_test_block_files()
