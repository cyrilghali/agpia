#!/usr/bin/env python3
"""Generate Coptic HTML pages from coptic_extracted.json."""

import json
import os
import html

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
JSON_PATH = os.path.join(SCRIPT_DIR, "coptic_extracted.json")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "cop")

# Hour keys in display order (for nav)
HOUR_KEYS = ["prime", "terce", "sext", "none", "vespers", "compline", "midnight", "veil", "other"]

# Shared sections prepended to prime only
SHARED_KEYS = ["introduction", "thanksgiving", "psalm50"]

# Hour time descriptions
HOUR_TIMES = {
    "prime": "6:00",
    "terce": "9:00",
    "sext": "12:00",
    "none": "15:00",
    "vespers": "18:00",
    "compline": "21:00",
    "midnight": "0:00",
    "veil": "",
    "other": "",
}

# Short nav labels (will be overridden by Coptic titles from JSON)
NAV_LABELS_FALLBACK = {
    "prime": "ϣⲱⲣⲡ",
    "terce": "ϣⲟⲙⲧ",
    "sext": "ⲥⲟⲟⲩ",
    "none": "ⲯⲓⲥ",
    "vespers": "ⲣⲟⲩϩⲓ",
    "compline": "ⲉⲛⲕⲟⲧ",
    "midnight": "ⲉϫⲱⲣϩ",
    "veil": "ⲕⲁⲧⲁⲡⲉⲧⲁⲥⲙⲁ",
    "other": "ⲛⲓⲡⲣⲟⲥⲉⲩⲭⲏ",
    "about": "ⲉⲑⲃⲉ",
}


def escape(text):
    """HTML-escape text and convert newlines to <br>."""
    return html.escape(text).replace("\n", "<br>\n")


def render_section(section):
    """Render a single section as HTML."""
    sec_type = section.get("type", "prayer")
    title = section.get("title", "")
    content = section.get("content", "")

    parts = []

    # Determine id and class
    section_id = ' id="gospel"' if sec_type == "gospel" else ""
    parts.append(f'<section class="section"{section_id}>')

    if title:
        parts.append(f'<h2 class="section-title">{escape(title)}</h2>')

    if sec_type == "psalm":
        # Split into verses by numbered lines or double newlines
        verses = split_psalm_verses(content)
        for i, verse in enumerate(verses):
            cls = "psalm-verse drop-cap" if i == 0 else "psalm-verse"
            verse_html = escape(verse.strip())
            parts.append(f'<div class="{cls} coptic-text">')
            parts.append(f"                    {verse_html}")
            parts.append("                </div>")
        # Add alleluia at the end
        parts.append('<div class="psalm-verse coptic-text">')
        parts.append('                    <span class="alleluia">Ⲁⲗⲗⲏⲗⲟⲩⲓⲁ.</span>')
        parts.append("                </div>")
    else:
        # prayer, gospel, tropaire, absolution, creed, litany
        content_html = escape(content.strip())
        parts.append(f'<div class="prayer-text coptic-text">')
        parts.append(f"                    {content_html}")
        parts.append("                </div>")

    parts.append("</section>")
    return "\n".join(parts)


def split_psalm_verses(text):
    """Split psalm text into verses. Use numbered verse markers or paragraph breaks."""
    import re
    # Split on verse numbers like "2 " at start of line or after newline
    # First, split by lines that start with a digit
    lines = text.strip().split("\n")
    verses = []
    current = []

    for line in lines:
        stripped = line.strip()
        # Check if line starts with a verse number (digit followed by space)
        if re.match(r"^\d+\s", stripped) and current:
            verses.append("\n".join(current))
            current = [stripped]
        else:
            current.append(stripped)

    if current:
        verses.append("\n".join(current))

    # If we only got one verse, try splitting on double newlines
    if len(verses) <= 1:
        verses = [v.strip() for v in text.split("\n\n") if v.strip()]

    return verses if verses else [text]


def build_nav_hours(data):
    """Build the nav-hours HTML block."""
    parts = ['<nav class="nav-hours">']
    for key in HOUR_KEYS:
        if key in data:
            title = data[key].get("title", NAV_LABELS_FALLBACK.get(key, key))
        else:
            title = NAV_LABELS_FALLBACK.get(key, key)
        # Use short form from title - take last meaningful word(s)
        label = title
        parts.append(f'<a class="nav-hour" href="{key}.html">')
        parts.append(f"<div>{escape(label)}</div>")
        parts.append("</a>")

    # About page
    parts.append('<a class="nav-hour" href="about.html">')
    parts.append(f"<div>{escape(NAV_LABELS_FALLBACK['about'])}</div>")
    parts.append("</a>")
    parts.append("</nav>")
    return "\n".join(parts)


def build_head(title, page_filename):
    """Build the <head> section."""
    og_url = f"https://agpia.fr/cop/{page_filename}"
    og_description = "Coptic Agpeya - The Book of Hours in Coptic."
    return f"""<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0, viewport-fit=cover" name="viewport"/>
<title>{escape(title)} | Agpia</title>
<link href="../agpeya-style.css" rel="stylesheet"/>
<meta name="description" content="{og_description}">
<meta property="og:title" content="{escape(title)} | Agpia">
<meta property="og:description" content="{og_description}">
<meta property="og:image" content="https://agpia.fr/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{og_url}">
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
</head>"""


def build_ornament():
    """Build the ornament divider."""
    return """<div class="ornament">
<img alt="Coptic Cross" class="ornament-cross" src="../coptic-cross.png"/>
<img alt="Coptic Cross" class="ornament-cross" src="../coptic-cross.png"/>
<img alt="Coptic Cross" class="ornament-cross" src="../coptic-cross.png"/>
</div>"""


def build_prayer_page(hour_key, data):
    """Build a complete prayer hour page."""
    hour_data = data[hour_key]
    title = hour_data["title"]
    time_str = HOUR_TIMES.get(hour_key, "")

    sections_to_render = []

    # For prime, prepend shared sections
    if hour_key == "prime":
        for shared_key in SHARED_KEYS:
            if shared_key in data:
                shared = data[shared_key]
                # Add a section header for the shared block
                shared_title = shared.get("title", shared_key)
                sections_to_render.append({
                    "title": shared_title,
                    "type": "prayer",
                    "content": "",
                    "_is_header": True,
                })
                for s in shared["sections"]:
                    sections_to_render.append(s)

    # Add the hour's own sections
    sections_to_render.extend(hour_data["sections"])

    # Check if this hour has a gospel section
    has_gospel = any(s.get("type") == "gospel" for s in sections_to_render)

    # Render sections
    sections_html_parts = []
    for section in sections_to_render:
        if section.get("_is_header"):
            # Render as a titled section with no content
            sections_html_parts.append(f'<section class="section">')
            sections_html_parts.append(f'<h2 class="section-title">{escape(section["title"])}</h2>')
            sections_html_parts.append("</section>")
        else:
            sections_html_parts.append(render_section(section))

    sections_html = "\n".join(sections_html_parts)
    nav_html = build_nav_hours(data)

    time_display = f" · {time_str}" if time_str else ""

    page = f"""<!DOCTYPE html>

<html lang="cop">
{build_head(title, f'{hour_key}.html')}
<body>
<main class="container">
<div class="hour-header">
<div class="header-crosses">
<img alt="Coptic Cross" src="../coptic-cross.png"/>
</div>
<h1 class="hour-title">{escape(title)}</h1>
<p class="hour-time">{escape(title)}{time_display}</p>
</div>
<div class="prayer-content">
{build_ornament()}
{sections_html}
{build_ornament()}
</div>
{nav_html}
</main>
<script src="../agpeya.js"></script>
<script>
        initJumpToGospel();
    </script>
    <script>
        window.si = window.si || function () {{ (window.siq = window.siq || []).push(arguments); }};
    </script>
    <script defer src="/_vercel/speed-insights/script.js"></script>
</body>
</html>
"""
    return page


def build_index_page(data):
    """Build the cop/index.html page."""
    hour_cards = []
    for key in HOUR_KEYS:
        if key not in data:
            continue
        title = data[key]["title"]
        time_str = HOUR_TIMES.get(key, "")
        time_display = time_str if time_str else ""
        hour_cards.append(f"""<a class="hour-card" href="{key}.html"> <div class="hour-info">
<h3 class="hour-name">{escape(title)}</h3>
<div class="hour-time">{time_display}</div>
</div>
<div class="hour-arrow">\u2192</div>
</a>""")

    # About card
    hour_cards.append(f"""<a class="hour-card" href="about.html"> <div class="hour-info">
<h3 class="hour-name">{escape(NAV_LABELS_FALLBACK['about'])}</h3>
<div class="hour-time"></div>
</div>
<div class="hour-arrow">\u2192</div>
</a>""")

    cards_html = "\n".join(hour_cards)

    page = f"""<!DOCTYPE html>

<html lang="cop">
{build_head("Agpia - Coptic", "index.html")}
<body>
<main class="container">
<section class="hero">
<div class="hero-title-en">Agpia</div>
<div class="hero-title-coptic">%agpia</div>
<img alt="Coptic Cross" class="hero-cross" src="../coptic-cross.png"/>
<h1>\u2ce0\u2c85\u2c81\u2c85\u2ca3\u2c89\u2ca5\u2c89\u2cab\u2c87\u2c8f \u2c99\u2c99\u2c81\u2ca9 \u2c99\u2ca3\u2c8f\u2c99\u2ca3\u2c8f</h1>
<a class="cta" href="prime.html" id="beginPrayerBtn">\u2ca3\u2c89\u2ca5\u2c85\u2c89\u2cab\u2c87\u2c8f \u2192</a>
</section>
<section class="hours">
{cards_html}
</section>
</main>
<script src="../agpeya.js"></script>
    <script>
        window.si = window.si || function () {{ (window.siq = window.siq || []).push(arguments); }};
    </script>
    <script defer src="/_vercel/speed-insights/script.js"></script>
</body>
</html>
"""
    return page


def build_about_page(data):
    """Build the cop/about.html page."""
    page = f"""<!DOCTYPE html>

<html lang="cop">
{build_head(NAV_LABELS_FALLBACK['about'], "about.html")}
<body>
<main class="container">
<div class="hour-header">
<div class="header-crosses">
<img alt="Coptic Cross" src="../coptic-cross.png"/>
</div>
<h1 class="hour-title">{escape(NAV_LABELS_FALLBACK['about'])}</h1>
</div>
<div class="prayer-content">
{build_ornament()}
<section class="section">
<h2 class="section-title">Agpia</h2>
<div class="prayer-text coptic-text">
                    \u2ce0\u2c85\u2c81\u2c85\u2ca3\u2c89\u2ca5\u2c89\u2cab\u2c87\u2c8f \u2c99\u2c99\u2c81\u2ca9 \u2c99\u2ca3\u2c8f\u2c99\u2ca3\u2c8f
                </div>
<div class="prayer-text">
                    The Agpeya (Book of Hours) is the Coptic Orthodox prayer book containing the seven canonical hours of prayer, plus additional prayers. This edition presents the prayers in their original Coptic language.
                </div>
</section>
{build_ornament()}
</div>
{build_nav_hours(data)}
</main>
<script src="../agpeya.js"></script>
    <script>
        window.si = window.si || function () {{ (window.siq = window.siq || []).push(arguments); }};
    </script>
    <script defer src="/_vercel/speed-insights/script.js"></script>
</body>
</html>
"""
    return page


def main():
    # Load JSON
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate prayer hour pages
    for hour_key in HOUR_KEYS:
        if hour_key not in data:
            print(f"WARNING: '{hour_key}' not found in JSON, skipping.")
            continue
        page_html = build_prayer_page(hour_key, data)
        out_path = os.path.join(OUTPUT_DIR, f"{hour_key}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"Generated {out_path}")

    # Generate index page
    index_html = build_index_page(data)
    index_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"Generated {index_path}")

    # Generate about page
    about_html = build_about_page(data)
    about_path = os.path.join(OUTPUT_DIR, "about.html")
    with open(about_path, "w", encoding="utf-8") as f:
        f.write(about_html)
    print(f"Generated {about_path}")

    print(f"\nDone! Generated {len(HOUR_KEYS) + 2} files in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
