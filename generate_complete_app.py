#!/usr/bin/env python3
"""
Complete script to generate app.js with all psalms from PDF
"""
import json
import re

def clean_psalm_text(lines):
    """Clean psalm lines and remove artifacts"""
    cleaned = []
    for line in lines:
        line = line.strip()
        if re.match(r'^- \d+ -$', line):
            continue
        if "Priè" in line and ("heure" in line or "aube" in line):
            continue
        line = re.sub(r'^[\*\+\=]+', '', line)
        line = re.sub(r'[\*\+\=]+$', '', line)
        line = line.replace('=', "'")
        line = line.strip()
        if line:
            cleaned.append(line)
    return cleaned

def group_into_paragraphs(lines):
    """Group lines into paragraphs - try to detect natural breaks"""
    if not lines:
        return []
    
    paragraphs = []
    current_para = []
    
    # First pass: group by empty lines
    for line in lines:
        if not line.strip():
            if current_para:
                paragraphs.append(current_para)
                current_para = []
        else:
            current_para.append(line)
    
    if current_para:
        paragraphs.append(current_para)
    
    # If no paragraphs detected, create reasonable groupings
    if len(paragraphs) == 1:
        paragraphs = []
        current_para = []
        for i, line in enumerate(lines):
            current_para.append(line)
            # Group 3-6 lines per paragraph, break at sentence endings
            if len(current_para) >= 3 and (line.endswith('.') or line.endswith('!') or line.endswith(':')):
                if len(current_para) >= 3:  # At least 3 lines
                    paragraphs.append(current_para)
                    current_para = []
        if current_para:
            paragraphs.append(current_para)
    
    return paragraphs if paragraphs else [lines]

def format_psalm_block(hour_key, psalm_num, psalm_data):
    """Format a psalm as a JavaScript block"""
    raw_lines = psalm_data.get('raw_lines', [])
    cleaned = clean_psalm_text(raw_lines)
    paragraphs = group_into_paragraphs(cleaned)
    
    js = []
    js.append(f'      {{')
    js.append(f'        id: "h{hour_key}-psalm-{psalm_num}",')
    js.append(f'        type: "psalm",')
    js.append(f'        title: "Psaume {psalm_num}",')
    js.append(f'        content: [')
    
    for i, para in enumerate(paragraphs):
        js.append('          [')
        for line in para:
            # Escape quotes in JavaScript
            line_escaped = line.replace('\\', '\\\\').replace('"', '\\"')
            js.append(f'            "{line_escaped}",')
        js.append('          ]' + (',' if i < len(paragraphs) - 1 else ''))
    
    js.append('        ]')
    js.append('      }')
    
    return '\n'.join(js)

# Load extracted psalms
with open('psalms_extracted.json', 'r', encoding='utf-8') as f:
    all_psalms = json.load(f)

# Hour structure
hours_info = {
    "1": {"title": "Première Heure", "psalms": ["1", "2", "3", "4", "5", "6", "8", "11", "12", "14", "15", "18", "24", "26", "62", "66", "69", "112", "142"]},
    "3": {"title": "Troisième Heure", "psalms": ["19", "22", "23", "25", "28", "29", "33", "40", "42", "44", "45", "46"]},
    "6": {"title": "Sixième Heure", "psalms": ["53", "56", "60", "62", "66", "69", "83", "84", "85", "86", "90", "92"]},
    "9": {"title": "Neuvième Heure", "psalms": ["95", "96", "97", "98", "99", "100", "109", "110", "111", "112", "114", "115"]},
    "11": {"title": "Onzième Heure", "psalms": ["116", "117", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128"]},
    "12": {"title": "Douzième Heure", "psalms": ["129", "130", "131", "132", "133", "136", "137", "140", "141", "145", "146", "147", "118"]},
}

# Generate code for all hours
output = []

for hour_key in ["1", "3", "6", "9", "11", "12"]:
    hour_psalms = all_psalms.get(hour_key, {})
    hour_info = hours_info[hour_key]
    
    output.append(f'\n// ===== HOUR {hour_key}: {hour_info["title"]} =====')
    output.append(f'// Psalms: {", ".join(hour_info["psalms"])}')
    output.append('')
    
    for psalm_num in hour_info["psalms"]:
        if psalm_num in hour_psalms:
            output.append(format_psalm_block(hour_key, psalm_num, hour_psalms[psalm_num]))
            output.append(',')
            output.append('')
        else:
            output.append(f'      // WARNING: Psalm {psalm_num} not found in extraction')
            output.append('')

# Write to file
with open('generated_psalms.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("Generated code written to generated_psalms.js")
print(f"Total blocks generated: {sum(len(hours_info[k]['psalms']) for k in hours_info)}")

