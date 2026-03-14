#!/usr/bin/env python3
"""
Extract Coptic text from agpia.pdf and output structured JSON.

The PDF uses two Coptic encodings:
  1. Unicode Coptic (ArialCoptic font) - U+2C80-2CFF / U+03E2-03EF ranges
  2. CS Avva Shenouda legacy font - ASCII mapped to Coptic glyphs

This script:
  - Extracts characters by font, keeping only Coptic-font text
  - Converts CS-encoded ASCII to proper Unicode Coptic
  - Passes through already-Unicode Coptic as-is
  - Organises output by prayer hour
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import pdfplumber

PDF_PATH = Path(__file__).resolve().parent.parent / "agpia.pdf"
OUTPUT_PATH = Path(__file__).resolve().parent / "coptic_extracted.json"

# ---------------------------------------------------------------------------
# CS Avva Shenouda -> Unicode Coptic mapping
# ---------------------------------------------------------------------------

CS_LOWER = {
    'a': '\u2C81',  # ⲁ
    'b': '\u2C83',  # ⲃ
    'g': '\u2C85',  # ⲅ
    'd': '\u2C87',  # ⲇ
    'e': '\u2C89',  # ⲉ
    'z': '\u2C8D',  # ⲍ
    'y': '\u2C8F',  # ⲏ
    'i': '\u2C93',  # ⲓ
    'k': '\u2C95',  # ⲕ
    'l': '\u2C97',  # ⲗ
    'm': '\u2C99',  # ⲙ
    'n': '\u2C9B',  # ⲛ
    'x': '\u2C9D',  # ⲝ
    'o': '\u2C9F',  # ⲟ
    'p': '\u2CA1',  # ⲡ
    'r': '\u2CA3',  # ⲣ
    'c': '\u2CA5',  # ⲥ
    't': '\u2CA7',  # ⲧ
    'u': '\u2CA9',  # ⲩ
    'v': '\u2CAB',  # ⲫ
    'w': '\u2CB1',  # ⲱ
    # Coptic-only letters
    's': '\u03E3',  # ϣ  (Coptic Sha)
    'f': '\u03E5',  # ϥ  (Coptic Fai)
    'h': '\u03E9',  # ϩ  (Coptic Hori)
    'q': '\u03E7',  # ϧ  (Coptic Khai)
    'j': '\u03EB',  # ϫ  (Coptic Gangia)
    # Bracket-mapped
    '[': '\u03ED',  # ϭ  (Coptic Shima)
    ']': '\u03EF',  # ϯ  (Coptic Dei)
    # Special chars
    ';': '\u2C91',  # ⲑ  (Theta)
    ',': '\u2CAD',  # ⲭ  (Chi)
    '<': '\u2CAD',  # ⲭ  (Chi alternate)
}

CS_UPPER = {
    'A': '\u2C80',  # Ⲁ
    'B': '\u2C82',  # Ⲃ
    'G': '\u2C84',  # Ⲅ
    'D': '\u2C86',  # Ⲇ
    'E': '\u2C88',  # Ⲉ
    'Z': '\u2C8C',  # Ⲍ
    'Y': '\u2C8E',  # Ⲏ
    'I': '\u2C92',  # Ⲓ
    'K': '\u2C94',  # Ⲕ
    'L': '\u2C96',  # Ⲗ
    'M': '\u2C98',  # Ⲙ
    'N': '\u2C9A',  # Ⲛ
    'X': '\u2C9C',  # Ⲝ
    'O': '\u2C9E',  # Ⲟ
    'P': '\u2CA0',  # Ⲡ
    'R': '\u2CA2',  # Ⲣ
    'C': '\u2CA4',  # Ⲥ
    'T': '\u2CA6',  # Ⲧ
    'U': '\u2CA8',  # Ⲩ
    'V': '\u2CAA',  # Ⲫ
    'W': '\u2CB0',  # Ⲱ
    # Coptic-only uppercase
    'S': '\u03E2',  # Ϣ
    'F': '\u03E4',  # Ϥ
    'H': '\u03E8',  # Ϩ
    'Q': '\u03E6',  # Ϧ
    'J': '\u03EA',  # Ϫ
}

# Merge both maps
CS_MAP = {}
CS_MAP.update(CS_LOWER)
CS_MAP.update(CS_UPPER)

# Characters to strip (supralinear stroke, nomina sacra marker)
CS_STRIP = {'`', '='}

# @ = verse/line separator -> newline
CS_VERSE_SEP = '@'

# ---------------------------------------------------------------------------
# Greek liturgical phrase detection
# ---------------------------------------------------------------------------

GREEK_MARKERS = [
    'Kuri', 'Doxa', 'Patri', 'Pneumati', 'agiou', 'euaggeliou',
    'anagnwcma', 'Iwannyn', 'Ma;;eon', 'Kurie', 'eulogycon',
    'ele`ycon', 'eleycon', 'ke Uiw', 'ke nun', 'twn `e`wnwn',
    'touc e', 'Kata', 'Pieuaggelion', 'piagion',
]


def is_greek_line(text: str) -> bool:
    """Detect lines that are Greek liturgical phrases (not Coptic)."""
    for marker in GREEK_MARKERS:
        if marker in text:
            return True
    return False


# ---------------------------------------------------------------------------
# CS -> Unicode conversion
# ---------------------------------------------------------------------------

def convert_cs_char(ch: str) -> str:
    """Convert a single CS-encoded character to Unicode Coptic."""
    if ch in CS_STRIP:
        return ''  # remove supralinear strokes and nomina sacra markers
    if ch == CS_VERSE_SEP:
        return '\n'
    if ch in CS_MAP:
        return CS_MAP[ch]
    # Pass through spaces, colons, periods, digits, etc.
    return ch


def convert_cs_text(text: str) -> str:
    """Convert a full CS-encoded string to Unicode Coptic."""
    return ''.join(convert_cs_char(ch) for ch in text)


# ---------------------------------------------------------------------------
# PDF extraction
# ---------------------------------------------------------------------------

def is_coptic_font(fontname: str) -> bool:
    return 'CSAvva' in fontname or 'ArialCoptic' in fontname


def is_cs_font(fontname: str) -> bool:
    return 'CSAvva' in fontname


def is_unicode_coptic_font(fontname: str) -> bool:
    return 'ArialCoptic' in fontname


def is_page_number_line(text: str) -> bool:
    """Detect page number lines like '- 6 -'."""
    return bool(re.match(r'^-\s*\d+\s*-\s*$', text.strip()))


def is_title_font(fontname: str) -> bool:
    return 'Constantia' in fontname or ('Garamond-Bold' in fontname)


def extract_coptic_from_page(page) -> list[dict]:
    """
    Extract Coptic text lines from a single PDF page.

    Returns a list of dicts:
      { 'text': str, 'font_type': 'cs'|'unicode', 'y': float, 'is_title': bool }
    """
    chars = page.chars
    if not chars:
        return []

    # Group characters by approximate y-position (line)
    lines_by_y = defaultdict(list)
    for c in chars:
        y_key = round(c['top'], 0)
        lines_by_y[y_key].append(c)

    results = []
    for y in sorted(lines_by_y.keys()):
        line_chars = sorted(lines_by_y[y], key=lambda c: c['x0'])

        # Separate Coptic chars from non-Coptic
        coptic_chars = [c for c in line_chars if is_coptic_font(c.get('fontname', ''))]
        if not coptic_chars:
            continue

        # Check if this is a page number line (entire line)
        full_text = ''.join(c['text'] for c in line_chars)
        if is_page_number_line(full_text):
            continue

        raw_text = ''.join(c['text'] for c in coptic_chars)

        # Skip empty/whitespace lines
        if not raw_text.strip():
            continue

        # Determine font type
        font_types = set()
        for c in coptic_chars:
            fn = c.get('fontname', '')
            if is_cs_font(fn):
                font_types.add('cs')
            elif is_unicode_coptic_font(fn):
                font_types.add('unicode')

        # If mixed, process each segment separately
        if len(font_types) > 1:
            # Split into runs by font type
            segments = []
            current_type = None
            current_text = []
            for c in coptic_chars:
                fn = c.get('fontname', '')
                ft = 'cs' if is_cs_font(fn) else 'unicode'
                if ft != current_type:
                    if current_text:
                        segments.append((current_type, ''.join(current_text)))
                    current_type = ft
                    current_text = [c['text']]
                else:
                    current_text.append(c['text'])
            if current_text:
                segments.append((current_type, ''.join(current_text)))

            converted_parts = []
            for ft, seg_text in segments:
                if ft == 'cs':
                    converted_parts.append(convert_cs_text(seg_text))
                else:
                    converted_parts.append(seg_text)
            final_text = ''.join(converted_parts)
        else:
            font_type = font_types.pop() if font_types else 'unicode'
            if font_type == 'cs':
                # Check for Greek liturgical phrases before converting
                if is_greek_line(raw_text):
                    final_text = raw_text  # preserve Greek as-is
                else:
                    final_text = convert_cs_text(raw_text)
            else:
                final_text = raw_text

        # Detect if any char in this line uses a title/bold font
        is_title = any(
            is_title_font(c.get('fontname', ''))
            for c in line_chars
            if is_coptic_font(c.get('fontname', ''))
        )

        results.append({
            'text': final_text.strip(),
            'y': y,
            'is_title': is_title,
        })

    return results


# ---------------------------------------------------------------------------
# Prayer hour organisation
# ---------------------------------------------------------------------------

HOUR_PAGES = {
    'introduction': (6, 6),
    'thanksgiving': (7, 7),
    'psalm50': (8, 8),
    'prime': (9, 32),
    'terce': (33, 46),
    'sext': (47, 59),
    'none': (60, 71),
    'vespers': (72, 82),
    'compline': (83, 95),
    'veil': (96, 98),
    'midnight': (99, 123),
    'other': (124, 137),
}

HOUR_TITLES = {
    'introduction': 'ϧⲉⲛ ⲫⲣⲁⲛ ⲙⲫⲓⲱⲧ',
    'thanksgiving': 'ⲡϣⲉⲡϩⲙⲟⲧ',
    'psalm50': 'ⲯⲁⲗⲙⲟⲥ ⲛ̅',
    'prime': 'ⲡⲣⲟⲥⲉⲩⲭⲏ ⲛⲧⲉ ϯⲛⲁⲩ ⲛϣⲱⲣⲡ',
    'terce': 'ⲡⲣⲟⲥⲉⲩⲭⲏ ⲛⲧⲉ ϯⲛⲁⲩ ⲙⲙⲁϩϣⲟⲙⲧ',
    'sext': 'ⲡⲣⲟⲥⲉⲩⲭⲏ ⲛⲧⲉ ϯⲛⲁⲩ ⲙⲙⲁϩⲥⲟⲟⲩ',
    'none': 'ⲡⲣⲟⲥⲉⲩⲭⲏ ⲛⲧⲉ ϯⲛⲁⲩ ⲙⲙⲁϩⲯⲓⲥ',
    'vespers': 'ⲡⲣⲟⲥⲉⲩⲭⲏ ⲛⲧⲉ ϯⲛⲁⲩ ⲛⲣⲟⲩϩⲓ',
    'compline': 'ⲡⲣⲟⲥⲉⲩⲭⲏ ⲛⲧⲉ ϯⲛⲁⲩ ⲛⲉⲛⲕⲟⲧ',
    'veil': 'ⲡⲣⲟⲥⲉⲩⲭⲏ ⲛⲧⲉ ⲡⲓⲕⲁⲧⲁⲡⲉⲧⲁⲥⲙⲁ',
    'midnight': 'ⲡⲣⲟⲥⲉⲩⲭⲏ ⲛⲧⲉ ϯⲛⲁⲩ ⲛⲉϫⲱⲣϩ',
    'other': 'ⲛⲓⲡⲣⲟⲥⲉⲩⲭⲏ',
}


def classify_section_type(text: str) -> str:
    """Heuristic to classify a section's content type."""
    lower = text.lower()
    if any(w in lower for w in ['ⲯⲁⲗⲙⲟⲥ', 'ⲁⲗⲗⲏⲗⲟⲩⲓⲁ', 'allelouia']):
        return 'psalm'
    if any(w in lower for w in ['euaggeliou', 'ⲉⲩⲁⲅⲅⲉⲗⲓⲟⲛ', 'pieuaggelion', 'Kata']):
        return 'gospel'
    if any(w in lower for w in ['ⲧⲣⲟⲡⲁⲣⲓⲟⲛ', 'tropaire']):
        return 'tropaire'
    if any(w in lower for w in ['ⲗⲓⲧⲁⲛⲓⲁ', 'litany']):
        return 'litany'
    if any(w in lower for w in ['ⲡⲓⲥⲧⲉⲩⲱ', 'ⲡⲓⲛⲁϩϯ']):
        return 'creed'
    return 'prayer'


def build_sections(lines: list[dict]) -> list[dict]:
    """
    Group extracted lines into sections.
    A new section starts when there's a significant y-gap or a title line.
    """
    if not lines:
        return []

    sections = []
    current_section = {
        'title': '',
        'type': 'prayer',
        'lines': [],
    }

    prev_y = None
    for line in lines:
        # Start new section on title lines or large vertical gaps
        is_new_section = False
        if line['is_title'] and line['text'].strip():
            is_new_section = True
        elif prev_y is not None and (line['y'] - prev_y) > 30:
            is_new_section = True

        if is_new_section and current_section['lines']:
            content = '\n'.join(current_section['lines'])
            current_section['content'] = content
            current_section['type'] = classify_section_type(content)
            del current_section['lines']
            sections.append(current_section)
            current_section = {
                'title': '',
                'type': 'prayer',
                'lines': [],
            }

        if line['is_title'] and not current_section['lines']:
            current_section['title'] = line['text']
        else:
            current_section['lines'].append(line['text'])

        prev_y = line['y']

    # Flush last section
    if current_section['lines']:
        content = '\n'.join(current_section['lines'])
        current_section['content'] = content
        current_section['type'] = classify_section_type(content)
        del current_section['lines']
        sections.append(current_section)

    return sections


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Opening {PDF_PATH} ...")
    pdf = pdfplumber.open(str(PDF_PATH))
    total_pages = len(pdf.pages)
    print(f"  {total_pages} pages")

    output = {}

    for hour_name, (start_page, end_page) in HOUR_PAGES.items():
        print(f"\nProcessing {hour_name} (pages {start_page}-{end_page}) ...")
        all_lines = []

        for page_num in range(start_page, min(end_page + 1, total_pages + 1)):
            page = pdf.pages[page_num - 1]  # 0-indexed
            lines = extract_coptic_from_page(page)
            if lines:
                # Add a gap marker between pages
                if all_lines:
                    last_y = all_lines[-1]['y']
                    lines[0] = {**lines[0], 'y': last_y + 50}
                all_lines.extend(lines)

        sections = build_sections(all_lines)
        print(f"  Found {len(all_lines)} lines -> {len(sections)} sections")

        # Add verse splitting for psalm sections
        for section in sections:
            if section['type'] == 'psalm' and 'content' in section:
                verses = [v.strip() for v in section['content'].split('\n') if v.strip()]
                section['verses'] = verses

        output[hour_name] = {
            'title': HOUR_TITLES.get(hour_name, hour_name),
            'sections': sections,
        }

    pdf.close()

    # Write JSON
    print(f"\nWriting {OUTPUT_PATH} ...")
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Validation
    print("\n--- Validation ---")

    # Check Psalm 50
    ps50 = output.get('psalm50', {})
    ps50_sections = ps50.get('sections', [])
    if ps50_sections:
        first_content = ps50_sections[0].get('content', '')
        print(f"Psalm 50 starts with: {first_content[:60]}")
        if 'Ⲛⲁⲓ' in first_content:
            print("  [OK] Contains expected 'Ⲛⲁⲓ'")
        else:
            print("  [WARN] Expected 'Ⲛⲁⲓ' not found")

    # Check Introduction (CS conversion)
    intro = output.get('introduction', {})
    intro_sections = intro.get('sections', [])
    if intro_sections:
        first_content = intro_sections[0].get('content', '')
        print(f"Introduction starts with: {first_content[:60]}")
        if 'ϧⲉⲛ' in first_content:
            print("  [OK] 'Qen' correctly converted to 'ϧⲉⲛ'")
        else:
            print("  [WARN] Expected 'ϧⲉⲛ' not found")
        if 'ⲫⲣⲁⲛ' in first_content:
            print("  [OK] 'vran' correctly converted to 'ⲫⲣⲁⲛ'")
        else:
            print("  [WARN] Expected 'ⲫⲣⲁⲛ' not found")

    # Check La Foi de l'Eglise
    prime = output.get('prime', {})
    prime_sections = prime.get('sections', [])
    for s in prime_sections:
        content = s.get('content', '')
        if 'Ⲟⲩⲁⲓ' in content or 'ⲟⲩⲁⲓ' in content.lower():
            print(f"La Foi: {content[:80]}")
            if 'Ⲫⲛⲟⲩϯ' in content:
                print("  [OK] 'Vnou]' correctly converted to 'Ⲫⲛⲟⲩϯ'")
            else:
                print("  [WARN] Expected 'Ⲫⲛⲟⲩϯ' not found in La Foi section")
            break

    # Summary stats
    total_sections = sum(len(h['sections']) for h in output.values())
    total_text = sum(
        len(s.get('content', ''))
        for h in output.values()
        for s in h['sections']
    )
    print(f"\nTotal: {total_sections} sections, {total_text} characters of Coptic text")
    print("Done!")


if __name__ == '__main__':
    main()
