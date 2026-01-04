#!/usr/bin/env python3
"""
Script to replace all psalm blocks in app.js with real psalms from PDF
"""
import re
import json

# Read generated psalms
with open('generated_psalms.js', 'r', encoding='utf-8') as f:
    generated_content = f.read()

# Parse generated psalms by hour and psalm number
psalms_by_hour = {}
current_hour = None

for line in generated_content.split('\n'):
    if 'HOUR' in line:
        match = re.search(r'HOUR (\d+)', line)
        if match:
            current_hour = match.group(1)
            psalms_by_hour[current_hour] = {}
    elif 'id: "h' in line and 'psalm-' in line:
        match = re.search(r'id: "h(\d+)-psalm-(\d+)"', line)
        if match:
            hour = match.group(1)
            psalm_num = match.group(2)
            # Extract the full block
            pass

# Better approach: extract blocks directly
def extract_psalm_blocks(content):
    """Extract complete psalm blocks from generated content"""
    blocks = {}
    lines = content.split('\n')
    i = 0
    current_hour = None
    
    while i < len(lines):
        line = lines[i]
        
        # Detect hour
        if 'HOUR' in line:
            match = re.search(r'HOUR (\d+)', line)
            if match:
                current_hour = match.group(1)
                if current_hour not in blocks:
                    blocks[current_hour] = {}
        
        # Detect psalm block start
        if 'id: "h' in line and 'psalm-' in line:
            match = re.search(r'id: "h(\d+)-psalm-(\d+)"', line)
            if match:
                hour = match.group(1)
                psalm_num = match.group(2)
                
                # Extract complete block until closing brace
                block_lines = [line]
                brace_count = line.count('{') - line.count('}')
                i += 1
                
                while i < len(lines) and brace_count > 0:
                    block_lines.append(lines[i])
                    brace_count += lines[i].count('{') - lines[i].count('}')
                    i += 1
                
                # Remove trailing comma if present
                if block_lines and block_lines[-1].strip() == ',':
                    block_lines.pop()
                
                blocks[hour][psalm_num] = '\n'.join(block_lines)
                continue
        
        i += 1
    
    return blocks

psalm_blocks = extract_psalm_blocks(generated_content)

# Read app.js
with open('app.js', 'r', encoding='utf-8') as f:
    app_content = f.read()

# For each hour, replace psalm blocks
for hour_key in ['1', '3', '6', '9', '11', '12']:
    if hour_key not in psalm_blocks:
        continue
    
    # Find all psalm blocks for this hour in app.js
    pattern = rf'(id: "h{hour_key}-psalm-\d+".*?}},?\s*\n)'
    matches = list(re.finditer(pattern, app_content, re.DOTALL))
    
    # Replace each match
    for match in reversed(matches):  # Reverse to maintain positions
        full_match = match.group(1)
        # Extract psalm number
        psalm_match = re.search(rf'id: "h{hour_key}-psalm-(\d+)"', full_match)
        if psalm_match:
            psalm_num = psalm_match.group(1)
            if psalm_num in psalm_blocks[hour_key]:
                # Replace with real psalm
                replacement = psalm_blocks[hour_key][psalm_num] + ',\n'
                app_content = app_content[:match.start()] + replacement + app_content[match.end():]

# Also need to add missing psalms. For now, let's write the updated content
# and manually add missing ones
with open('app_updated.js', 'w', encoding='utf-8') as f:
    f.write(app_content)

print("Updated app.js written to app_updated.js")
print("Note: You may need to manually add missing psalms and adjust structure")

