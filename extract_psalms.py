#!/usr/bin/env python3
import re
import json

with open('pdf_text.txt', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Structure des heures et leurs psaumes
hours_structure = {
    "1": {"name": "Prière de l'aube", "psalms": ["1", "2", "3", "4", "5", "6", "8", "11", "12", "14", "15", "18", "24", "26", "62", "66", "69", "112", "142"]},
    "3": {"name": "Prière de la troisième heure", "psalms": ["19", "22", "23", "25", "28", "29", "33", "40", "42", "44", "45", "46"]},
    "6": {"name": "Prière de la sixième heure", "psalms": ["53", "56", "60", "62", "66", "69", "83", "84", "85", "86", "90", "92"]},
    "9": {"name": "Prière de la neuvième heure", "psalms": ["95", "96", "97", "98", "99", "100", "109", "110", "111", "112", "114", "115"]},
    "11": {"name": "Prière de la onzième heure", "psalms": ["116", "117", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128"]},
    "12": {"name": "Prière de la douzième heure", "psalms": ["129", "130", "131", "132", "133", "136", "137", "140", "141", "145", "146", "147", "118"]},
}

def extract_psalm_text(lines, start_idx, next_psalm_num=None, hour_end_markers=None):
    """Extract text of a psalm from lines starting at start_idx"""
    psalm_lines = []
    i = start_idx + 1  # Skip the "Psaume X" line
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Stop conditions
        if not line:
            i += 1
            continue
            
        # Check if we hit next psalm
        psalm_match = re.match(r'^Psaume (\d+)', line)
        if psalm_match:
            break
            
        # Check if we hit hour end markers
        if hour_end_markers:
            for marker in hour_end_markers:
                if marker in line:
                    return psalm_lines, i
                    
        # Check if line is just a page number
        if re.match(r'^- \d+ -$', line):
            i += 1
            continue
            
        # Check if line is "Alléluia !" or similar ending
        if line == "Alléluia !" or line == "Alléluia":
            psalm_lines.append(line)
            i += 1
            # Usually psalm ends after Alléluia
            break
            
        # Add line if it contains text
        if line and not line.startswith('*') and not line.startswith('+'):
            # Clean up the line
            line = line.replace('=', "'")  # Fix encoding issues
            psalm_lines.append(line)
            
        i += 1
    
    return psalm_lines, i

def parse_psalm_into_paragraphs(psalm_lines):
    """Parse psalm lines into paragraph structure"""
    paragraphs = []
    current_para = []
    
    for line in psalm_lines:
        line = line.strip()
        if not line:
            if current_para:
                paragraphs.append(current_para)
                current_para = []
            continue
            
        # Check if line ends a sentence (ends with . ! : or ,)
        current_para.append(line)
        
        # If line ends with . ! or :, it might be end of sentence
        # But we'll group by empty lines for now
        if line.endswith('.') or line.endswith('!') or line.endswith(':'):
            # Check if next non-empty line starts new paragraph
            pass
    
    if current_para:
        paragraphs.append(current_para)
    
    return paragraphs

# Extract all psalms
all_psalms = {}

for hour_key, hour_data in hours_structure.items():
    print(f"\nProcessing {hour_data['name']}...")
    hour_psalms = {}
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Find hour start
        if hour_data['name'] in line:
            # Look for psalms in this hour
            for psalm_num in hour_data['psalms']:
                psalm_pattern = f'^Psaume {psalm_num}'
                if re.match(psalm_pattern, line):
                    print(f"  Found Psalm {psalm_num}")
                    psalm_lines, next_idx = extract_psalm_text(lines, i)
                    if psalm_lines:
                        # Clean and structure
                        clean_lines = [l for l in psalm_lines if l and not re.match(r'^- \d+ -$', l)]
                        hour_psalms[psalm_num] = clean_lines
                    i = next_idx - 1
                    break
        i += 1
    
    all_psalms[hour_key] = hour_psalms

# Save to JSON for inspection
with open('psalms_extracted.json', 'w', encoding='utf-8') as f:
    json.dump(all_psalms, f, ensure_ascii=False, indent=2)

print("\nExtraction complete! Saved to psalms_extracted.json")
print(f"\nSummary:")
for hour_key, hour_data in hours_structure.items():
    extracted = all_psalms.get(hour_key, {})
    print(f"  Hour {hour_key}: {len(extracted)}/{len(hour_data['psalms'])} psalms extracted")

