#!/usr/bin/env python3
"""
Script to integrate all psalms into app.js
"""
import re
import json

# Read the generated psalms
with open('generated_psalms.js', 'r', encoding='utf-8') as f:
    generated = f.read()

# Read app.js
with open('app.js', 'r', encoding='utf-8') as f:
    app_content = f.read()

# Extract psalm blocks by hour and number
def extract_psalm_blocks(content):
    """Extract all psalm blocks from generated content"""
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
                
                # Extract complete block
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

psalm_blocks = extract_psalm_blocks(generated)

# Clean problematic psalms (5 and 142 for hour 1)
# For now, we'll keep them as is and let user clean manually

# Function to replace psalm blocks in app.js
def replace_psalms_in_hour(app_content, hour_key, psalm_blocks_for_hour):
    """Replace all psalm blocks for a specific hour"""
    # Find the hour section
    hour_pattern = rf'("1":\s*{{[^}}]*"blocks":\s*\[)'
    
    # Find all psalm blocks in this hour
    pattern = rf'(id: "h{hour_key}-psalm-\d+".*?}},?\s*\n)'
    matches = list(re.finditer(pattern, app_content, re.DOTALL))
    
    # Get expected psalms for this hour
    expected_psalms = {
        "1": ["1", "2", "3", "4", "5", "6", "8", "11", "12", "14", "15", "18", "24", "26", "62", "66", "69", "112", "142"],
        "3": ["19", "22", "23", "25", "28", "29", "33", "40", "42", "44", "45", "46"],
        "6": ["53", "56", "60", "62", "66", "69", "83", "84", "85", "86", "90", "92"],
        "9": ["95", "96", "97", "98", "99", "100", "109", "110", "111", "112", "114", "115"],
        "11": ["116", "117", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128"],
        "12": ["129", "130", "131", "132", "133", "136", "137", "140", "141", "145", "146", "147", "118"],
    }
    
    if hour_key not in expected_psalms:
        return app_content
    
    # Find where psalms start and end for this hour
    # Look for first psalm block
    first_psalm_pattern = rf'(id: "h{hour_key}-psalm-(\d+)"'
    first_match = re.search(first_psalm_pattern, app_content)
    if not first_match:
        return app_content
    
    # Find the conclusion block for this hour
    conclusion_pattern = rf'(id: "h{hour_key}-conclusion"'
    conclusion_match = re.search(conclusion_pattern, app_content)
    
    if not conclusion_match:
        return app_content
    
    # Find the start of first psalm and end of last psalm before conclusion
    start_pos = first_match.start()
    # Go back to find the opening brace of the first psalm block
    while start_pos > 0 and app_content[start_pos] not in ['{', ',']:
        start_pos -= 1
    if app_content[start_pos] == ',':
        start_pos += 1
    
    # Find end of last psalm before conclusion
    # Look backwards from conclusion to find last psalm block end
    end_pos = conclusion_match.start()
    # Go back to find the closing of the last psalm block
    while end_pos > start_pos and app_content[end_pos:end_pos+2] != '},':
        end_pos -= 1
    end_pos += 2  # Include the '},\n'
    
    # Build replacement: all psalms in order
    replacement_parts = []
    for psalm_num in expected_psalms[hour_key]:
        if psalm_num in psalm_blocks_for_hour:
            block = psalm_blocks_for_hour[psalm_num]
            replacement_parts.append('      ' + block + ',')
        else:
            replacement_parts.append(f'      // WARNING: Psalm {psalm_num} not found')
    
    replacement = '\n\n'.join(replacement_parts) + '\n'
    
    # Replace
    new_content = app_content[:start_pos] + replacement + app_content[end_pos:]
    return new_content

# For each hour, replace psalms
for hour_key in ["1", "3", "6", "9", "11", "12"]:
    if hour_key in psalm_blocks:
        print(f"Processing hour {hour_key}...")
        app_content = replace_psalms_in_hour(app_content, hour_key, psalm_blocks[hour_key])

# Write updated app.js
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_content)

print("Integration complete! app.js has been updated.")

