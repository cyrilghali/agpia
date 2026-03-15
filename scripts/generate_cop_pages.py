#!/usr/bin/env python3
"""Generate Coptic prayer HTML pages from coptic_raw.json."""

import json
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
COP_DIR = os.path.join(PROJECT_DIR, "cop")
JSON_PATH = os.path.join(SCRIPT_DIR, "coptic_raw.json")


def has_unicode_coptic(line):
    """Check if a line contains Unicode Coptic characters (U+2C80+)."""
    return any(ord(c) >= 0x2C80 for c in line)


def classify_line(line):
    """Classify a line as 'unicode-coptic', 'coptic-text' (CS/ASCII), or 'french'."""
    stripped = line.strip()
    if not stripped:
        return None
    if has_unicode_coptic(stripped):
        return "unicode-coptic"
    # Check if it looks like French (Latin with accents, common French words)
    # CS-encoded Coptic uses ASCII chars but with special patterns (backticks, @, etc.)
    # French text is typically longer sentences with spaces and accented chars
    # A heuristic: if it has backticks or @ or specific Coptic CS markers, it's CS Coptic
    cs_markers = ['`', '@', '[', ']', '=']
    has_cs = any(m in stripped for m in cs_markers)
    # Common French/section header patterns
    french_patterns = [
        r'^PSAUME\s',
        r'^PSAUMES\s',
        r'^Psaumes?\s',
        r'^TIERCE',
        r'^SEXTE',
        r'^NONE',
        r'^VÊPRES',
        r'^COMPLIES',
        r'^PRIÈRE',
        r'^Allons',
        r'^\d+\.\s*[….]',
        r'^Fais-nous',
        r'^Et fais-nous',
    ]
    for pat in french_patterns:
        if re.match(pat, stripped):
            return "french"

    if has_cs:
        return "coptic-text"

    # No CS markers - check if it's French text
    # French accented characters are a strong signal
    has_accents = bool(re.search(r'[àâéèêëïîôùûüçÀÂÉÈÊËÏÎÔÙÛÜÇ]', stripped))
    if has_accents:
        return "french"

    # Check for common French words
    french_words = {'et', 'le', 'la', 'les', 'de', 'du', 'des', 'un', 'une', 'en',
                    'qui', 'que', 'nous', 'vous', 'ils', 'car', 'par', 'pour', 'sur',
                    'avec', 'dans', 'tout', 'ses', 'aux', 'mon', 'ton', 'son',
                    'mes', 'tes', 'nos', 'vos', 'leur', 'leurs', 'au', 'est',
                    'sa', 'se', 'ce', 'ne', 'pas', 'plus', 'si', 'ou', 'sont',
                    'ta', 'ma', 'il', 'elle', 'ont', 'toi', 'moi', 'lui',
                    'tous', 'ces', 'vers', 'tes', 'nos', 'ils', 'eux',
                    'bien', 'mais', 'comme', 'des', 'sur', 'sous', 'sans'}
    words = stripped.lower().split()
    french_count = sum(1 for w in words if w.rstrip('.,;:!?*') in french_words)

    # Even short phrases: if any French word is found and no CS markers
    if french_count >= 1 and len(words) <= 8:
        return "french"
    if len(words) > 3 and french_count >= 2:
        return "french"

    # Lines with spaces but no CS markers and only ASCII - likely French
    # CS Coptic without markers is very rare
    if len(words) >= 3 and all(ord(c) < 128 for c in stripped):
        return "french"

    return "coptic-text"


def detect_sections(content, hour_key):
    """Split content into sections based on detected headers."""
    lines = content.split('\n')
    sections = []
    current_title = None
    current_lines = []

    # Section header patterns
    section_patterns = [
        (r'^PSAUME\s+(\d+)', lambda m: f"Psaume {m.group(1)}"),
        (r'^PSAUMES\s+(.+)', lambda m: f"Psaumes {m.group(1)}"),
        (r'^Psaumes?\s+(.+)', lambda m: f"Psaumes {m.group(1)}"),
        (r'^TIERCE\s*\(.*\)', lambda m: "Tierce (troisième heure)"),
        (r'^SEXTE\s*\(.*\)', lambda m: "Sexte (sixième heure)"),
        (r'^NONE\s*\(.*\)', lambda m: "None (neuvième heure)"),
        (r'^VÊPRES\s*\(.*\)', lambda m: "Vêpres (onzième heure)"),
        (r'^COMPLIES\s*\(.*\)', lambda m: "Complies (douzième heure)"),
    ]

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current_lines and current_lines[-1] != '':
                current_lines.append('')
            continue

        matched = False
        for pattern, title_fn in section_patterns:
            m = re.match(pattern, stripped, re.IGNORECASE)
            if m:
                # Save previous section
                if current_lines:
                    sections.append((current_title, current_lines))
                current_title = title_fn(m)
                current_lines = []
                matched = True
                break

        if not matched:
            current_lines.append(stripped)

    if current_lines:
        sections.append((current_title, current_lines))

    return sections


def render_paragraphs(lines):
    """Group consecutive lines of the same type into paragraphs and render HTML."""
    html_parts = []
    current_type = None
    current_group = []

    for line in lines:
        if not line:  # Empty line = paragraph break
            if current_group:
                html_parts.append(render_group(current_type, current_group))
                current_group = []
                current_type = None
            continue

        line_type = classify_line(line)
        if line_type is None:
            continue

        if line_type != current_type and current_group:
            html_parts.append(render_group(current_type, current_group))
            current_group = []

        current_type = line_type
        current_group.append(line)

    if current_group:
        html_parts.append(render_group(current_type, current_group))

    return '\n'.join(html_parts)


def render_group(line_type, lines):
    """Render a group of lines as an HTML div."""
    if line_type == "french":
        # French text - no special font class needed, just prayer-text
        text = '<br>\n'.join(lines)
        return f'<div class="prayer-text">\n{text}\n</div>'
    elif line_type == "unicode-coptic":
        text = '<br>\n'.join(lines)
        return f'<div class="prayer-text unicode-coptic">\n{text}\n</div>'
    else:  # coptic-text (CS/ASCII)
        text = '<br>\n'.join(lines)
        return f'<div class="prayer-text coptic-text">\n{text}\n</div>'


# Hour metadata
HOURS = {
    'prime': {
        'title': 'Prime',
        'time': 'First Hour · 6:00 AM',
        'sections_from': ['introduction', 'thanksgiving', 'psalm50', 'prime'],
    },
    'terce': {
        'title': 'Terce',
        'time': 'Third Hour · 9:00 AM',
        'sections_from': ['terce'],
    },
    'sext': {
        'title': 'Sext',
        'time': 'Sixth Hour · 12:00 PM',
        'sections_from': ['sext'],
    },
    'none': {
        'title': 'None',
        'time': 'Ninth Hour · 3:00 PM',
        'sections_from': ['none'],
    },
    'vespers': {
        'title': 'Vespers',
        'time': 'Eleventh Hour · 5:00 PM',
        'sections_from': ['vespers'],
    },
    'compline': {
        'title': 'Compline',
        'time': 'Twelfth Hour · 7:00 PM',
        'sections_from': ['compline'],
    },
    'midnight': {
        'title': 'Midnight',
        'time': 'Midnight Prayer · 12:00 AM',
        'sections_from': ['midnight'],
    },
    'veil': {
        'title': 'Veil',
        'time': 'Prayer of the Veil',
        'sections_from': ['veil'],
    },
    'other': {
        'title': 'Other',
        'time': 'Other Prayers',
        'sections_from': ['other'],
    },
}

# French section titles for each source key
SOURCE_TITLES = {
    'introduction': "Introduction de chaque heure",
    'thanksgiving': "Prière d'action de grâce",
    'psalm50': "Psaume 50",
}

NAV_HOURS = [
    ('prime.html', 'Prime'),
    ('terce.html', 'Terce'),
    ('sext.html', 'Sext'),
    ('none.html', 'None'),
    ('vespers.html', 'Vespers'),
    ('compline.html', 'Compline'),
    ('midnight.html', 'Midnight'),
    ('veil.html', 'Veil'),
    ('other.html', 'Other'),
    ('about.html', 'About'),
]


def generate_nav():
    """Generate the nav-hours HTML."""
    parts = ['<nav class="nav-hours">']
    for href, label in NAV_HOURS:
        parts.append(f'<a class="nav-hour" href="{href}">')
        parts.append(f'<div>{label}</div>')
        parts.append('</a>')
    parts.append('</nav>')
    return '\n'.join(parts)


def generate_page(hour_key, data):
    """Generate a complete HTML page for an hour."""
    meta = HOURS[hour_key]
    title = meta['title']
    time_str = meta['time']

    # Build all sections
    all_sections_html = []

    for source_key in meta['sections_from']:
        source_data = data[source_key]
        content = source_data['content']

        sections = detect_sections(content, source_key)

        for section_title, section_lines in sections:
            # Use a specific title if this is a known source
            if section_title is None and source_key in SOURCE_TITLES:
                section_title = SOURCE_TITLES[source_key]
            elif section_title is None:
                section_title = source_data.get('title', title)

            paragraphs_html = render_paragraphs(section_lines)
            if not paragraphs_html.strip():
                continue

            section_html = f'''<section class="section">
<h2 class="section-title">{section_title}</h2>
{paragraphs_html}
</section>'''
            all_sections_html.append(section_html)

    sections_content = '\n'.join(all_sections_html)
    nav_html = generate_nav()

    page = f'''<!DOCTYPE html>

<html lang="cop">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0, viewport-fit=cover" name="viewport"/>
<title>{title} | Agpia</title>
<link href="../agpeya-style.css" rel="stylesheet"/>
<meta name="description" content="Pray the Agpia (Coptic Book of Hours) in Coptic.">
<meta property="og:title" content="{title} | Agpia">
<meta property="og:description" content="Pray the Agpia (Coptic Book of Hours) in Coptic.">
<meta property="og:image" content="https://agpia.fr/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="https://agpia.fr/cop/{hour_key}.html">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Agpia">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://agpia.fr/og-image.png">
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#fdfdf9">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <link rel="apple-touch-icon" href="/icons/icon-192.png">
    <script>
        window.va = window.va || function () {{ (window.vaq = window.vaq || []).push(arguments); }};
    </script>
    <script defer src="/_vercel/insights/script.js"></script>
</head>
<body>
<main class="container">
<div class="hour-header">
<div class="header-crosses">
<img alt="Coptic Cross" src="../coptic-cross.png"/>
</div>
<h1 class="hour-title">{title}</h1>
<p class="hour-time">{time_str}</p>
</div>
<div class="prayer-content">
<div class="ornament">
<img alt="Coptic Cross" class="ornament-cross" src="../coptic-cross.png"/>
<img alt="Coptic Cross" class="ornament-cross" src="../coptic-cross.png"/>
<img alt="Coptic Cross" class="ornament-cross" src="../coptic-cross.png"/>
</div>
{sections_content}
<div class="ornament">
<img alt="Coptic Cross" class="ornament-cross" src="../coptic-cross.png"/>
<img alt="Coptic Cross" class="ornament-cross" src="../coptic-cross.png"/>
<img alt="Coptic Cross" class="ornament-cross" src="../coptic-cross.png"/>
</div>
</div>
{nav_html}
</main>
<script src="../agpeya.js"></script>
<script>
        // Initialize jump to gospel functionality
        initJumpToGospel();
    </script>
    <script>
        window.si = window.si || function () {{ (window.siq = window.siq || []).push(arguments); }};
    </script>
    <script defer src="/_vercel/speed-insights/script.js"></script>
</body>
</html>'''

    return page


def main():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    os.makedirs(COP_DIR, exist_ok=True)

    for hour_key in HOURS:
        page_html = generate_page(hour_key, data)
        output_path = os.path.join(COP_DIR, f"{hour_key}.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(page_html)
        print(f"Generated {output_path}")

    print("\nDone! Generated 9 Coptic prayer pages.")


if __name__ == '__main__':
    main()
