#!/usr/bin/env python3
import re

with open('pdf_text.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all hours and their psalms
hours = {
    "1": {"name": "Prière de l'aube", "psalms": []},
    "3": {"name": "Prière de la troisième heure", "psalms": []},
    "6": {"name": "Prière de la sixième heure", "psalms": []},
    "9": {"name": "Prière de la neuvième heure", "psalms": []},
    "11": {"name": "Prière de la onzième heure", "psalms": []},
    "12": {"name": "Prière de la douzième heure", "psalms": []},
}

# Find psalm numbers and their positions
psalm_pattern = r'^Psaume (\d+)'
lines = content.split('\n')

current_hour = None
for i, line in enumerate(lines):
    # Detect hour changes
    if "Prière de l'aube" in line and i > 200:  # Skip early mentions
        current_hour = "1"
    elif "Prière de la troisième heure" in line and i > 1200:
        current_hour = "3"
    elif "Prière de la sixième heure" in line and i > 1800:
        current_hour = "6"
    elif "Prière de la neuvième heure" in line and i > 2400:
        current_hour = "9"
    elif "Prière de la onzième heure" in line and i > 2900:
        current_hour = "11"
    elif "Prière de la douzième heure" in line and i > 3300:
        current_hour = "12"
    
    # Find psalms
    match = re.match(psalm_pattern, line.strip())
    if match and current_hour:
        psalm_num = match.group(1)
        if psalm_num not in hours[current_hour]["psalms"]:
            hours[current_hour]["psalms"].append(psalm_num)

# Print structure
for hour_key, hour_data in hours.items():
    print(f"\n{hour_data['name']} (Hour {hour_key}):")
    print(f"  Psalms: {', '.join(hour_data['psalms'])}")
    print(f"  Total: {len(hour_data['psalms'])} psalms")

