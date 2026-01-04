#!/usr/bin/env python3
import re
import json

with open('pdf_text.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Structure des heures et leurs psaumes
hours_structure = {
    "1": {"name": "Prière de l'aube", "psalms": ["1", "2", "3", "4", "5", "6", "8", "11", "12", "14", "15", "18", "24", "26", "62", "66", "69", "112", "142"]},
    "3": {"name": "Prière de la troisième heure", "psalms": ["19", "22", "23", "25", "28", "29", "33", "40", "42", "44", "45", "46"]},
    "6": {"name": "Prière de la sixième heure", "psalms": ["53", "56", "60", "62", "66", "69", "83", "84", "85", "86", "90", "92"]},
    "9": {"name": "Prière de la neuvième heure", "psalms": ["95", "96", "97", "98", "99", "100", "109", "110", "111", "112", "114", "115"]},
    "11": {"name": "Prière de la onzième heure", "psalms": ["116", "117", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128"]},
    "12": {"name": "Prière de la douzième heure", "psalms": ["129", "130", "131", "132", "133", "136", "137", "140", "141", "145", "146", "147", "118"]},
}

def clean_line(line):
    """Clean a line from PDF artifacts"""
    line = line.strip()
    # Remove page numbers
    if re.match(r'^- \d+ -$', line):
        return None
    # Remove formatting markers at start
    line = re.sub(r'^[\*\+\=]+', '', line)
    line = re.sub(r'[\*\+\=]+$', '', line)
    # Fix encoding issues
    line = line.replace('=', "'")
    # Remove hour markers that appear in middle
    if "Priè" in line and "heure" in line:
        return None
    return line.strip() if line.strip() else None

def extract_psalm(lines, start_idx):
    """Extract a complete psalm starting at start_idx"""
    psalm_lines = []
    i = start_idx + 1  # Skip "Psaume X" line
    
    while i < len(lines):
        line = lines[i]
        original_line = line.strip()
        
        # Stop if we hit next psalm
        if re.match(r'^Psaume \d+', original_line):
            break
            
        # Clean the line
        cleaned = clean_line(original_line)
        if cleaned:
            psalm_lines.append(cleaned)
        elif original_line == "Alléluia !" or original_line == "Alléluia":
            psalm_lines.append(original_line)
            # Usually ends after Alléluia
            i += 1
            break
            
        i += 1
    
    return psalm_lines, i

def group_into_paragraphs(psalm_lines):
    """Group psalm lines into paragraphs based on structure"""
    paragraphs = []
    current_para = []
    
    for line in psalm_lines:
        if not line:
            if current_para:
                paragraphs.append(current_para)
                current_para = []
            continue
            
        current_para.append(line)
        
        # If line ends with punctuation and next might be new paragraph
        # We'll use double line breaks as paragraph markers
        # For now, group sentences that flow together
        
    if current_para:
        paragraphs.append(current_para)
    
    # If no paragraphs detected, treat all as one
    if not paragraphs:
        paragraphs = [psalm_lines]
    
    return paragraphs

# Find all psalms
all_psalms = {}

for hour_key, hour_data in hours_structure.items():
    print(f"\nProcessing {hour_data['name']}...")
    hour_psalms = {}
    
    # Find psalms for this hour
    for psalm_num in hour_data['psalms']:
        pattern = f'^Psaume {psalm_num}'
        for i, line in enumerate(lines):
            if re.match(pattern, line.strip()):
                print(f"  Found Psalm {psalm_num} at line {i}")
                psalm_lines, next_idx = extract_psalm(lines, i)
                if psalm_lines:
                    paragraphs = group_into_paragraphs(psalm_lines)
                    hour_psalms[psalm_num] = {
                        "raw_lines": psalm_lines,
                        "paragraphs": paragraphs
                    }
                break
    
    all_psalms[hour_key] = hour_psalms

# Save to JSON
with open('psalms_extracted.json', 'w', encoding='utf-8') as f:
    json.dump(all_psalms, f, ensure_ascii=False, indent=2)

print("\nExtraction complete!")
for hour_key, hour_data in hours_structure.items():
    extracted = all_psalms.get(hour_key, {})
    print(f"  Hour {hour_key}: {len(extracted)}/{len(hour_data['psalms'])} psalms")

