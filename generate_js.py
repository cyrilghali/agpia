#!/usr/bin/env python3
"""
Script to generate JavaScript code for app.js from extracted psalms
"""
import json
import re

def clean_psalm_text(lines):
    """Clean psalm lines and remove artifacts"""
    cleaned = []
    for line in lines:
        line = line.strip()
        # Remove page numbers
        if re.match(r'^- \d+ -$', line):
            continue
        # Remove hour markers
        if "Priè" in line and ("heure" in line or "aube" in line):
            continue
        # Remove formatting markers
        line = re.sub(r'^[\*\+\=]+', '', line)
        line = re.sub(r'[\*\+\=]+$', '', line)
        # Fix encoding
        line = line.replace('=', "'")
        line = line.strip()
        if line:
            cleaned.append(line)
    return cleaned

def group_into_paragraphs(lines):
    """Group lines into paragraphs based on sentence structure"""
    paragraphs = []
    current_para = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            if current_para:
                paragraphs.append(current_para)
                current_para = []
            continue
        
        current_para.append(line)
        
        # Check if this might be end of paragraph
        # If line ends with punctuation and next line starts with capital or is empty
        if i < len(lines) - 1:
            next_line = lines[i + 1].strip()
            if (line.endswith('.') or line.endswith('!') or line.endswith(':')) and \
               (not next_line or next_line[0].isupper()):
                # Might be paragraph break, but we'll be conservative
                pass
    
    if current_para:
        paragraphs.append(current_para)
    
    # If we didn't detect paragraphs well, try grouping by sentence endings
    if len(paragraphs) == 1 and len(paragraphs[0]) > 10:
        # Re-group more aggressively
        paragraphs = []
        current_para = []
        for line in lines:
            if not line.strip():
                if current_para:
                    paragraphs.append(current_para)
                    current_para = []
                continue
            current_para.append(line)
            # Group 3-5 lines per paragraph roughly
            if len(current_para) >= 4 and (line.endswith('.') or line.endswith('!') or line.endswith(':')):
                paragraphs.append(current_para)
                current_para = []
        if current_para:
            paragraphs.append(current_para)
    
    return paragraphs if paragraphs else [lines]

def format_psalm_for_js(psalm_num, psalm_data):
    """Format a psalm for JavaScript code"""
    raw_lines = psalm_data.get('raw_lines', [])
    cleaned = clean_psalm_text(raw_lines)
    paragraphs = group_into_paragraphs(cleaned)
    
    # Format as JavaScript array structure
    js_lines = []
    js_lines.append(f'        {{')
    js_lines.append(f'          id: "h1-psalm-{psalm_num}",')
    js_lines.append(f'          type: "psalm",')
    js_lines.append(f'          title: "Psaume {psalm_num}",')
    js_lines.append(f'          content: [')
    
    for para in paragraphs:
        if len(paragraphs) == 1 and len(para) <= 4:
            # Single paragraph, format as array
            js_lines.append('            [')
            for line in para:
                js_lines.append(f'              "{line}",')
            js_lines.append('            ]')
        else:
            # Multiple paragraphs
            js_lines.append('            [')
            for line in para:
                js_lines.append(f'              "{line}",')
            js_lines.append('            ]' + (',' if para != paragraphs[-1] else ''))
    
    js_lines.append('          ]')
    js_lines.append('        }' + ',')
    
    return '\n'.join(js_lines)

# Load extracted psalms
with open('psalms_extracted.json', 'r', encoding='utf-8') as f:
    all_psalms = json.load(f)

# Generate code for first hour as example
print("Generating code for Hour 1 (first 3 psalms as example)...\n")
hour_1_psalms = all_psalms.get('1', {})

for psalm_num in ['1', '2', '3']:
    if psalm_num in hour_1_psalms:
        print(f"// Psalm {psalm_num}")
        print(format_psalm_for_js(psalm_num, hour_1_psalms[psalm_num]))
        print()

