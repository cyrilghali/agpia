#!/usr/bin/env python3
"""Fetch Arabic Agpeya from St-Takla.org, parse into structured sections,
output JSON, and optionally fill ar/ HTML from en/ templates."""

import json, os, re, sys, time
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = os.path.dirname(os.path.abspath(__file__))

# ===================================================================
# 1. St-Takla URLs and Arabic-to-Psalm-number mapping
# ===================================================================

URLS = {
    'prime':    'https://st-takla.org/Agpeya/Agbeya_01_Prime_.html',
    'terce':    'https://st-takla.org/Agpeya/Agbeya_03_Terce_.html',
    'sext':     'https://st-takla.org/Agpeya/Agbeya_06_Sext_.html',
    'none':     'https://st-takla.org/Agpeya/Agbeya_09_None_.html',
    'vespers':  'https://st-takla.org/Agpeya/Agbeya_11_Vespers_.html',
    'compline': 'https://st-takla.org/Agpeya/Agbeya_12_Compline_.html',
    'midnight': 'https://st-takla.org/Agpeya/Agbeya_Midnight_.html',
    'veil':     'https://st-takla.org/Agpeya/Agbeya_Viel_.html',
}

AR_ORDINAL_TO_NUM = {
    'الأول': 1, 'الثاني': 2, 'الثالث': 3, 'الرابع': 4,
    'الخامس': 5, 'السادس': 6, 'السابع': 7, 'الثامن': 8,
    'التاسع': 9, 'العاشر': 10,
    'الحادي عشر': 11, 'الثاني عشر': 12, 'الثالث عشر': 13,
    'الرابع عشر': 14, 'الخامس عشر': 15, 'السادس عشر': 16,
    'السابع عشر': 17, 'الثامن عشر': 18, 'التاسع عشر': 19,
    'العشرون': 20, 'العشرين': 20,
    'الحادي والعشرون': 21, 'الحادي والعشرين': 21,
    'الثاني والعشرون': 22, 'الثاني والعشرين': 22,
    'الثالث والعشرون': 23, 'الثالث والعشرين': 23,
    'الرابع والعشرون': 24, 'الرابع والعشرين': 24,
    'الخامس والعشرون': 25, 'الخامس والعشرين': 25,
    'السادس والعشرون': 26, 'السادس والعشرين': 26,
    'السابع والعشرون': 27, 'السابع والعشرين': 27,
    'الثامن والعشرون': 28, 'الثامن والعشرين': 28,
    'التاسع والعشرون': 29, 'التاسع والعشرين': 29,
    'الثلاثون': 30, 'الثلاثين': 30,
    'الحادي والثلاثون': 31, 'الحادي والثلاثين': 31,
    'الثاني والثلاثون': 32, 'الثاني والثلاثين': 32,
    'الثالث والثلاثون': 33, 'الثالث والثلاثين': 33,
    'الرابع والثلاثون': 34, 'الرابع والثلاثين': 34,
    'الخامس والثلاثون': 35, 'الخامس والثلاثين': 35,
    'السادس والثلاثون': 36, 'السادس والثلاثين': 36,
    'السابع والثلاثون': 37, 'السابع والثلاثين': 37,
    'الثامن والثلاثون': 38, 'الثامن والثلاثين': 38,
    'التاسع والثلاثون': 39, 'التاسع والثلاثين': 39,
    'الأربعون': 40, 'الأربعين': 40,
    'الحادي والأربعون': 41, 'الحادي والأربعين': 41,
    'الثاني والأربعون': 42, 'الثاني والأربعين': 42,
    'الثالث والأربعون': 43, 'الثالث والأربعين': 43,
    'الرابع والأربعون': 44, 'الرابع والأربعين': 44,
    'الخامس والأربعون': 45, 'الخامس والأربعين': 45,
    'السادس والأربعون': 46, 'السادس والأربعين': 46,
    'السابع والأربعون': 47, 'السابع والأربعين': 47,
    'الخمسون': 50, 'الخمسين': 50,
    'الثالث والخمسون': 53, 'الثالث والخمسين': 53,
    'السادس والخمسون': 56, 'السادس والخمسين': 56,
    'الستون': 60, 'الستين': 60,
    'الثاني والستون': 62, 'الثاني والستين': 62,
    'السادس والستون': 66, 'السادس والستين': 66,
    'التاسع والستون': 69, 'التاسع والستين': 69,
    'الثالث والثمانون': 83, 'الثالث والثمانين': 83,
    'الرابع والثمانون': 84, 'الرابع والثمانين': 84,
    'الخامس والثمانون': 85, 'الخامس والثمانين': 85,
    'السادس والثمانون': 86, 'السادس والثمانين': 86,
    'التسعون': 90, 'التسعين': 90,
    'الثاني والتسعون': 92, 'الثاني والتسعين': 92,
    'الخامس والتسعون': 95, 'الخامس والتسعين': 95,
    'السادس والتسعون': 96, 'السادس والتسعين': 96,
    'السابع والتسعون': 97, 'السابع والتسعين': 97,
    'الثامن والتسعون': 98, 'الثامن والتسعين': 98,
    'التاسع والتسعون': 99, 'التاسع والتسعين': 99,
    'المائة': 100,
    'المائة والتاسع': 109,
    'المائة والعاشر': 110,
    'المائة والحادي عشر': 111,
    'المائة والثاني عشر': 112,
    'المائة والثامن عشر': 118,
    'المائة والرابع عشر': 114,
    'المائة والخامس عشر': 115,
    'المائة والسادس عشر': 116,
    'المائة والسابع عشر': 117,
    'المائة والتاسع عشر': 119,
    'المائة والعشرون': 120, 'المائة والعشرين': 120,
    'المائة والحادي والعشرون': 121, 'المائة والحادي والعشرين': 121,
    'المائة والثاني والعشرون': 122, 'المائة والثاني والعشرين': 122,
    'المائة والثالث والعشرون': 123, 'المائة والثالث والعشرين': 123,
    'المائة والرابع والعشرون': 124, 'المائة والرابع والعشرين': 124,
    'المائة والخامس والعشرون': 125, 'المائة والخامس والعشرين': 125,
    'المائة والسادس والعشرون': 126, 'المائة والسادس والعشرين': 126,
    'المائة والسابع والعشرون': 127, 'المائة والسابع والعشرين': 127,
    'المائة والثامن والعشرون': 128, 'المائة والثامن والعشرين': 128,
    'المائة والتاسع والعشرون': 129, 'المائة والتاسع والعشرين': 129,
    'المائة والثلاثون': 130, 'المائة والثلاثين': 130,
    'المائة والحادي والثلاثون': 131, 'المائة والحادي والثلاثين': 131,
    'المائة والثاني والثلاثون': 132, 'المائة والثاني والثلاثين': 132,
    'المائة والثالث والثلاثون': 133, 'المائة والثالث والثلاثين': 133,
    'المائة والسادس والثلاثون': 136, 'المائة والسادس والثلاثين': 136,
    'المائة والسابع والثلاثون': 137, 'المائة والسابع والثلاثين': 137,
    'المائة والأربعون': 140, 'المائة والأربعين': 140,
    'المائة والحادي والأربعون': 141, 'المائة والحادي والأربعين': 141,
    'المائة والثاني والأربعون': 142, 'المائة والثاني والأربعين': 142,
    'المائة والخامس والأربعون': 145, 'المائة والخامس والأربعين': 145,
    'المائة والسادس والأربعون': 146, 'المائة والسادس والأربعين': 146,
    'المائة والسابع والأربعون': 147, 'المائة والسابع والأربعين': 147,
}

def arabic_psalm_number(title):
    """Extract psalm number from an Arabic psalm title like '(1) المزمور الأول'."""
    cleaned = re.sub(r'^\(\d+\)\s*', '', title).strip()
    cleaned = re.sub(r'^المزمور\s+', '', cleaned).strip()
    cleaned = re.sub(r'^من المزمور\s+', '', cleaned).strip()
    if cleaned in AR_ORDINAL_TO_NUM:
        return AR_ORDINAL_TO_NUM[cleaned]
    for key in sorted(AR_ORDINAL_TO_NUM, key=len, reverse=True):
        if key in cleaned:
            return AR_ORDINAL_TO_NUM[key]
    return None

# ===================================================================
# 2. Fetch and decode St-Takla pages
# ===================================================================

def fetch_page(url):
    """Fetch a St-Takla page (windows-1256 encoded) and return decoded text."""
    import urllib.request
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()
    return raw.decode('windows-1256', errors='replace')

def get_bodytext(html_text):
    """Extract the #bodytext div content."""
    soup = BeautifulSoup(html_text, 'html.parser')
    body = soup.find(id='bodytext')
    if not body:
        return soup
    return body

# ===================================================================
# 3. Parse sections from a St-Takla page
# ===================================================================

def normalize_text(text):
    """Clean up extracted text: collapse whitespace, strip."""
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.replace('\xa0', ' ')
    return text

def is_heading(tag):
    return tag.name in ('h1', 'h2', 'h3') if isinstance(tag, Tag) else False

def extract_sections(body_el):
    """Walk the bodytext and split into sections by heading tags.
    Returns a list of {title, tag_level, paragraphs}."""
    sections = []
    current_title = None
    current_level = None
    current_paras = []

    skip_titles = {'الأجبية', 'إخفاء/إظهار الصور والجداول'}

    for el in body_el.descendants:
        if not isinstance(el, Tag):
            continue
        if el.name in ('h1', 'h2', 'h3'):
            text = normalize_text(el.get_text())
            text = re.sub(r'^[\s\u200f\u200e]+|[\s\u200f\u200e]+$', '', text)
            if not text or text in skip_titles:
                continue
            if 'Ajpia' in text or 'كتاب الصلاة' in text:
                continue

            if current_title is not None:
                sections.append({
                    'title': current_title,
                    'level': current_level,
                    'paragraphs': current_paras,
                })
            current_title = text
            current_level = el.name
            current_paras = []

        elif el.name == 'p' and current_title is not None:
            if el.find_parent(['h1', 'h2', 'h3']):
                continue
            text = normalize_text(el.get_text())
            if text and text != '\xa0' and len(text) > 1:
                current_paras.append(text)

    if current_title is not None:
        sections.append({
            'title': current_title,
            'level': current_level,
            'paragraphs': current_paras,
        })

    return sections

# ===================================================================
# 4. Section title mapping: St-Takla Arabic → en/ canonical titles
# ===================================================================

COMMON_SECTION_MAP = {
    'مقدمة كل ساعة': 'Introduction to Every Hour',
    'الصلاة الربانية': "The Lord's Prayer",
    'صلاة الشكر': 'The Prayer of Thanksgiving',
    'المزمور الخمسون': 'Psalm 50',
    'تسبحة الملائكة': 'The Gloria',
    'الثلاث تقديسات': 'The Trisagion',
    'السلام لك': 'Hail to Saint Mary',
    'بدء قانون الإيمان': 'Introduction to the Creed',
    'قانون الإيمان المقدس الأرثوذكسي': 'The Orthodox Creed',
    'قدوس قدوس قدوس': 'Holy Holy Holy',
    'طلبة تصلى آخر كل ساعة': 'Conclusion of Every Hour',
    'تفضل يا رب': 'Graciously Accord, O Lord',
    'لتكن طلبتي': 'Let My Supplication',
}

HOUR_SECTION_MAP = {
    'prime': {
        'هلم نسجد': 'Come Let Us Kneel Down',
        'هلم نسجد:': 'Come Let Us Kneel Down',
        'البولس من رسالة أفسس (4: 1-5)': 'The Pauline Epistle (Ephesians 4:1-5)',
        'من إيمان الكنيسة': 'The Faith of the Church',
        '(إنجيل يوحنا 1: 1ـ17)': 'The Holy Gospel According to Saint John (1:1-17)',
        'القطع': 'Litanies',
        'التحليل': 'First Absolution',
        'تحليل آخر': 'Second Absolution',
    },
    'terce': {
        '(إنجيل يوحنا 14: 26ـ15: 3)': 'The Holy Gospel (John 14:26-31 & 15:1-4)',
        'القطع': 'Litanies',
        'التحليل': 'Absolution',
    },
    'sext': {
        '(إنجيل متى 5: 1ـ16)': 'The Holy Gospel (Matthew 5:1-16)',
        'القطع': 'Litanies',
        'التحليل': 'Absolution',
    },
    'none': {
        '(إنجيل لوقا 9: 10-17)': 'The Holy Gospel (Luke 9:10-17)',
        'القطع': 'Litanies',
        'التحليل': 'Absolution',
    },
    'vespers': {
        '(إنجيل لوقا 4: 38-41)': 'The Holy Gospel (Luke 4:38-41)',
        'القطع': 'Litanies',
        'التحليل': 'Absolution',
    },
    'compline': {
        '(إنجيل لوقا 2: 25-32)': 'The Holy Gospel (St. Luke 2:25-32)',
        'القطع': 'Litanies',
        'التحليل': 'Absolution',
    },
    'veil': {
        '(إنجيل يوحنا6: 15-23)': 'The Holy Gospel (John 6:15-23)',
        '(إنجيل يوحنا 6: 15-23)': 'The Holy Gospel (John 6:15-23)',
        'القطع': 'Litanies',
        'التحليل': 'Absolution',
    },
    'midnight': {
        'الخدمة الأولى': 'The First Watch',
        'الخدمة الثانية': 'The Second Watch',
        'الخدمة الثالثة': 'The Third Watch',
        'قوموا يا بني النور': 'Opening Prayer',
        '(إنجيل متى 25: 1-13)': 'The Holy Gospel (Matthew 25:1-13)',
        '(إنجيل لوقا 7: 36-50)': 'The Holy Gospel (Luke 7:36-50)',
        '(إنجيل لوقا 12: 32-46)': 'The Holy Gospel (Luke 12:32-46)',
        'فصل من إنجيل لوقا ص2: 29-32': 'The Holy Gospel (Luke 2:29-32)',
        'القطع': 'Litanies',
        'التحليل': 'Absolution',
        'التحليل الكبير لنصف الليل: تحليل الكهنة بعد صلاة نصف الليل': 'Absolution',
    },
}

SKIP_SECTIONS = {
    'بدء الصلاة',
    'بدء صلاة باكر',
    'بدء الصلاة (هلم نسجد - البولس - من إيمان الكنيسة):-',
    'صلاة باكر',
    'صلاة الساعة الثالثة',
    'صلاة الساعة السادسة',
    'صلاة الساعة التاسعة',
    'صلاة الغروب',
    'صلاة النوم',
    'صلاة نصف الليل',
    'صلاة السِّتار',
    'صلاة السِتار',
    'صلاة الستار',
}

def map_section_title(ar_title, hour):
    """Map an Arabic section title to the canonical English title."""
    stripped = re.sub(r'[\u064B-\u065F\u0610-\u061A\u0670\u06D6-\u06ED]', '', ar_title)
    if ar_title in SKIP_SECTIONS or stripped in SKIP_SECTIONS:
        return '__skip__'
    if ar_title in COMMON_SECTION_MAP:
        return COMMON_SECTION_MAP[ar_title]
    hour_map = HOUR_SECTION_MAP.get(hour, {})
    if ar_title in hour_map:
        return hour_map[ar_title]
    pn = arabic_psalm_number(ar_title)
    if pn is not None:
        return f'Psalm {pn}'
    if 'إنجيل' in ar_title:
        return f'Gospel: {ar_title}'
    return None

# ===================================================================
# 5. Build structured data for all hours
# ===================================================================

def fetch_and_parse_hour(hour, url, cache_dir=None):
    """Fetch, parse, and return structured sections for one hour."""
    if cache_dir:
        cache_file = os.path.join(cache_dir, f'{hour}.html')
        if os.path.exists(cache_file):
            print(f"  Using cached {hour}")
            with open(cache_file, 'r', encoding='utf-8') as f:
                html_text = f.read()
        else:
            print(f"  Fetching {hour}...")
            html_text = fetch_page(url)
            os.makedirs(cache_dir, exist_ok=True)
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(html_text)
    else:
        print(f"  Fetching {hour}...")
        html_text = fetch_page(url)

    body = get_bodytext(html_text)
    raw_sections = extract_sections(body)

    mapped = []
    for sec in raw_sections:
        en_title = map_section_title(sec['title'], hour)
        if en_title == '__skip__':
            continue
        entry = {
            'ar_title': sec['title'],
            'en_title': en_title,
            'paragraphs': sec['paragraphs'],
        }
        if en_title and en_title.startswith('Psalm '):
            entry['psalm_num'] = int(en_title.split()[1])
        mapped.append(entry)

    return mapped

def fetch_all_hours(cache_dir=None):
    """Fetch and parse all hours. Returns {hour: [sections]}."""
    all_data = {}
    for hour, url in URLS.items():
        sections = fetch_and_parse_hour(hour, url, cache_dir)
        all_data[hour] = sections
        unmapped = [s for s in sections if s['en_title'] is None]
        if unmapped:
            print(f"    WARN: {len(unmapped)} unmapped sections in {hour}:")
            for s in unmapped:
                print(f"      - {s['ar_title']}")
        time.sleep(1)
    return all_data

# ===================================================================
# 6. Build psalm lookup from parsed data
# ===================================================================

def build_arabic_psalm_lookup(all_data):
    """Build {psalm_number: [arabic paragraphs]} from all parsed hours."""
    psalms = {}
    for hour, sections in all_data.items():
        for sec in sections:
            pn = sec.get('psalm_num')
            if pn and pn not in psalms and sec['paragraphs']:
                psalms[pn] = sec['paragraphs']
    return psalms

# ===================================================================
# 7. HTML replacement helpers (mirrors fill_french.py)
# ===================================================================

SP = '\n                    '
SP_END = '\n                '

def set_text(el, text):
    el.clear()
    el.append(NavigableString(SP + text + SP_END))

def set_em(el, text):
    el.clear()
    em = Tag(name='em')
    em.string = text
    el.append(em)

def distribute(paras, n):
    if n <= 0 or not paras:
        return []
    if len(paras) <= n:
        return paras + [''] * (n - len(paras))
    result = []
    base = len(paras) // n
    extra = len(paras) % n
    idx = 0
    for i in range(n):
        count = base + (1 if i < extra else 0)
        result.append(' '.join(paras[idx:idx + count]))
        idx += count
    return result

def replace_psalm_ar(section_el, ar_paras):
    """Replace psalm verse divs with Arabic text."""
    divs = section_el.find_all('div', class_='psalm-verse')
    if not divs or not ar_paras:
        return
    paras = [p for p in ar_paras if p.strip()]
    last_para = paras[-1] if paras else ''
    has_hallelujah = 'هلليلويا' in last_para
    if has_hallelujah:
        paras[-1] = re.sub(r'\s*هلليلويا\.?\s*$', '', paras[-1]).strip()

    if len(paras) > len(divs):
        paras = distribute(paras, len(divs))

    for i, div in enumerate(divs):
        if i >= len(paras):
            break
        had_alleluia = div.find('span', class_='alleluia')
        is_last = (i == len(divs) - 1)
        div.clear()
        div.append(NavigableString(SP + paras[i] + ' '))
        if (had_alleluia or is_last) and has_hallelujah:
            al = Tag(name='span')
            al['class'] = ['alleluia']
            al.string = 'هلليلويا.'
            div.append(al)
        div.append(NavigableString(SP_END))

def replace_prayer_ar(section_el, ar_paras):
    """Replace prayer-text divs with Arabic text."""
    divs = section_el.find_all('div', class_='prayer-text')
    if not divs or not ar_paras:
        return
    paras = [p for p in ar_paras if p.strip()]
    if len(paras) > len(divs):
        paras = distribute(paras, len(divs))
    for i, div in enumerate(divs):
        if i >= len(paras):
            break
        em_child = div.find('em')
        if em_child and len(list(div.children)) <= 2:
            set_em(div, paras[i])
        else:
            set_text(div, paras[i])

def replace_gospel_ar(section_el, ar_paras):
    """Replace gospel section with Arabic text."""
    if not ar_paras:
        return
    verse_divs = section_el.find_all('div', class_='psalm-verse')
    other_divs = [d for d in section_el.find_all('div', class_='prayer-text')
                  if 'doxology' not in d.get('class', [])]

    body = list(ar_paras)
    intro = None
    if body and ('من إنجيل' in body[0] or 'بركاته' in body[0]):
        intro = body.pop(0)

    outro = 'والمجد لله دائمًا أبديًا أمين.'
    if body and ('والمجد لله' in body[-1] or 'المجد لله' in body[-1]):
        outro = body.pop()

    if verse_divs:
        if len(body) > len(verse_divs):
            body = distribute(body, len(verse_divs))
        for i, div in enumerate(verse_divs):
            if i < len(body):
                div.clear()
                div.append(NavigableString(SP + body[i] + SP_END))

    for div in section_el.find_all('div'):
        classes = div.get('class', [])
        if 'doxology' in classes:
            eng = div.find('span', class_='doxology-english')
            if eng:
                eng.string = 'نسجد لك أيها المسيح مع أبيك الصالح والروح القدس لأنك أتيت وخلصتنا فارحمنا.'
            continue
        em_child = div.find('em')
        if em_child and 'psalm-verse' not in classes:
            txt = div.get_text(strip=True)
            if intro and ('Glory' in txt or 'Holy' in txt or 'reading' in txt.lower() or 'From the' in txt):
                set_em(div, intro)
                intro = None
            elif 'Glory to God forever' in txt or 'glory' in txt.lower()[:20]:
                set_text(div, outro)

def replace_litanies_ar(section_el, ar_paras):
    """Replace litany section with Arabic text."""
    if not ar_paras:
        return
    lit_idx = 0
    for div in section_el.find_all('div', class_='prayer-text'):
        classes = div.get('class', [])
        if 'doxology' in classes:
            continue
        num = div.find('span', class_='litany-number')
        if num and lit_idx < len(ar_paras):
            num_html = str(num)
            div.clear()
            div.append(BeautifulSoup(num_html, 'html.parser'))
            div.append(NavigableString(' ' + ar_paras[lit_idx]))
            lit_idx += 1
        elif lit_idx < len(ar_paras):
            set_text(div, ar_paras[lit_idx])
            lit_idx += 1

# ===================================================================
# 8. Arabic common section text (hard-coded from St-Takla)
# ===================================================================

INTRO_AR = [
    "باسم الآب والابن والروح القدس الإله الواحد آمين.",
    "يا رب ارحم. يا رب ارحم. يا رب بارك. آمين.",
    "المجد للآب والابن والروح القدس الآن وكل أوان وإلى دهر الدهور آمين.",
]

LORDS_PRAYER_AR = [
    ("em", "اللهم اجعلنا مستحقين أن نقول بشكر:"),
    ("text", "أبانا الذي في السموات. ليتقدس اسمك. ليأت ملكوتك. لتكن مشيئتك. كما في السماء كذلك على الأرض. خبزنا الذي للغد أعطنا اليوم."),
    ("text", "وأغفر لنا ذنوبنا كما نغفر نحن أيضا للمذنبين إلينا. ولا تدخلنا في تجربة. لكن نجنا من الشرير. بالمسيح يسوع ربنا لأن لك الملك والقوة والمجد إلى الأبد. آمين."),
]

THANKSGIVING_AR = [
    "فلنشكر صانع الخيرات الرحوم الله، أبا ربنا وإلهنا ومخلصنا يسوع المسيح، لأنه سترنا وأعاننا، وحفظنا، وقبلنا إليه وأشفق علينا وعضدنا، وأتى بنا إلى هذه الساعة. هو أيضا فلنسأله أن يحفظنا في هذا اليوم المقدس وكل أيام حياتنا بكل سلام. الضابط الكل الرب إلهنا.",
    "أيها السيد الإله ضابط الكل أبو ربنا وإلهنا ومخلصنا يسوع المسيح، نشكرك على كل حال ومن أجل كل حال، وفى كل حال، لأنك سترتنا، وأعنتنا، وحفظتنا، وقبلتنا إليك، وأشفقت علينا، وعضدتنا، وأتيت بنا إلى هذه الساعة.",
    "من أجل هذا نسأل ونطلب من صلاحك يا محب البشر، امنحنا أن نكمل هذا اليوم المقدس وكل أيام حياتنا بكل سلام مع خوفك. كل حسد، وكل تجربة وكل فعل الشيطان ومؤامرة الناس الأشرار، وقيام الأعداء الخفيين والظاهريين، انزعها عنا وعن سائر شعبك، وعن موضعك المقدس هذا. أما الصالحات والنافعات فارزقنا إياها.",
    "لأنك أنت الذي أعطيتنا السلطان أن ندوس الحيات والعقارب وكل قوة العدو. ولا تدخلنا في تجربة، لكن نجنا من الشرير.",
    "بالنعمة والرأفات ومحبة البشر اللواتي لابنك الوحيد ربنا وإلهنا ومخلصنا يسوع المسيح. هذا الذي من قبله المجد والإكرام والعزة والسجود تليق بك معه مع الروح القدس المحيي المساوي لك الآن وكل أوان وإلى دهر الدهور آمين.",
]

KYRIE_AR = [
    ("em", "يصلي المؤمن:"),
    ("text", "يا رب استمع لنا وارحمنا واغفر لنا خطايانا. آمين."),
    ("em", "(يا رب ارحم) 41 مرة"),
]

HOLY_HOLY_AR = [
    "قدوس، قدوس، قدوس، رب الصباؤوت. السماء والأرض مملوءتان من مجدك وكرامتك. ارحمنا يا الله الآب ضابط الكل. أيها الثالوث القدوس ارحمنا. أيها الرب إله القوات كن معنا، لأنه ليس لنا معين في شدائدنا وضيقاتنا سواك.",
    "حل واغفر واصفح لنا يا الله عن سيئاتنا، التي صنعناها بإرادتنا والتي صنعناها بغير إرادتنا، التي فعلناها بمعرفة والتي فعلناها بغير معرفة، الخفية والظاهرة. يا رب اغفرها لنا، من أجل اسمك القدوس الذي دعي علينا. كرحمتك يا رب وليس كخطايانا.",
]

CONCLUSION_AR = [
    "ارحمنا يا الله ثم ارحمنا. يا من في كل وقت وكل ساعة، في السماء وعلى الأرض، مسجود له وممجد. المسيح إلهنا الصالح، الطويل الروح، الكثير الرحمة، الجزيل التحنن، الذي يحب الصديقين ويرحم الخطاة الذين أولهم أنا. الذي لا يشاء موت الخاطئ مثل ما يرجع ويحيا. الداعي الكل إلى الخلاص لأجل الموعد بالخيرات المنتظرة.",
    "يا رب اقبل منا في هذه الساعة وكل ساعة طلباتنا. سهل حياتنا، وأرشدنا إلى العمل بوصاياك. قدس أرواحنا. طهر أجسامنا. قوم أفكارنا. نق نياتنا. اشف أمراضنا واغفر خطايانا. ونجنا من كل حزن رديء ووجع قلب. أحطنا بملائكتك القديسين، لكي نكون بمعسكرهم محفوظين ومرشدين، لنصل إلى اتحاد الإيمان وإلى معرفة مجدك غير المحسوس وغير المحدود، فإنك مبارك إلى الأبد. آمين.",
]

CREED_AR = [
    "بالحقيقة نؤمن بإله واحد، الله الآب، ضابط الكل، خالق السماء والأرض، ما يُرَى وما لا يرى.",
    "نؤمن برب واحد يسوع المسيح، ابن الله الوحيد، المولود من الآب قبل كل الدهور، نور من نور، إله حق من إله حق، مولود غير مخلوق، مساو للآب في الجوهر، الذي به كان كل شيء. هذا الذي من أجلنا نحن البشر، ومن أجل خلاصنا، نزل من السماء، وتجسد من الروح القدس ومن مريم العذراء، وتأنس. وصلب عنا على عهد بيلاطس البنطي. وتألم وقبر وقام من بين الأموات في اليوم الثالث كما في الكتب، وصعد إلى السموات، وجلس عن يمين أبيه، وأيضا يأتي في مجده ليدين الأحياء والأموات، الذي ليس لملكه انقضاء.",
    "نعم نؤمن بالروح القدس، الرب المحيى المنبثق من الآب. نسجد له ونمجده مع الآب والابن، الناطق في الأنبياء.",
    "وبكنيسة واحدة مقدسة جامعة رسولية.",
    "ونعترف بمعمودية واحدة لمغفرة الخطايا.",
    "وننتظر قيامة الأموات وحياة الدهر الآتي. آمين.",
]

CREED_INTRO_AR = [
    "نعظمك يا أم النور الحقيقي، ونمجدك أيتها العذراء القديسة، والدة الإله، لأنك ولدت لنا مخلص العالم، أتى وخلص نفوسنا.",
    "المجد لكَ يا سيدنا وملكنا المسيح، فخر الرسل، إكليل الشهداء تهليل الصديقين، ثبات الكنائس، غفران الخطايا.",
    "نبشر بالثالوث القدوس، لاهوت واحد، نسجد له ونمجده. يا رب ارحم. يا رب ارحم. يا رب بارك. آمين.",
]

VIRGIN_AR = [
    "السلام لك. نسألك أيتها القديسة الممتلئة مجدا العذراء كل حين، والدة الإله أم المسيح، أصعدي صلواتنا إلى ابنك الحبيب ليغفر لنا خطايانا.",
    "السلام للتي ولدت لنا النور الحقيقي المسيح إلهنا، العذراء القديسة، اسألي الرب عنا، ليصنع رحمة مع نفوسنا، ويغفر لنا خطايانا.",
    "أيتها العذراء مريم والدة الإله، القديسة الشفيعة الأمينة لجنس البشرية، اشفعي فينا أمام المسيح الذي ولدته لكي ينعم علينا بغفران خطايانا.",
    "السلام لك أيتها العذراء الملكة الحقيقية، السلام لفخر جنسنا، ولدت لنا عمانوئيل. نسألك: اذكرينا، أيتها الشفيعة المؤتمنة، أمام ربنا يسوع المسيح، ليغفر لنا خطايانا.",
]

TRISAGION_AR = [
    "قدوس الله، قدوس القوى، قدوس الحي الذي لا يموت، الذي ولد من العذراء، ارحمنا. قدوس الله، قدوس القوى، قدوس الحي الذي لا يموت، الذي صلب عنا، ارحمنا. قدوس الله، قدوس القوى، قدوس الحي الذي لا يموت، الذي قام من الأموات وصعد إلى السموات، ارحمنا. المجد للآب والابن والروح القدس، الآن وكل أوان وإلى دهر الدهور. أمين. أيها الثالوث القدوس ارحمنا. أيها الثالوث القدوس ارحمنا. أيها الثالوث القدوس ارحمنا.",
    "يا رب اغفر لنا خطايانا. يا رب اغفر لنا آثامنا. يا رب اغفر لنا زلاتنا. يا رب افتقد مرضى شعبك، اشفهم من أجل اسمك القدوس. آباؤنا وإخوتنا الذين رقدوا، يا رب نيح نفوسهم. يا من هو بلا خطية، يا رب ارحمنا. يا من بلا خطية، يا رب أعنا، واقبل طلباتنا إليك. لأن لك المجد والعزة والتقديس المثلث. يا رب ارحم. يا رب ارحم يا رب بارك. أمين.",
]

GLORIA_AR = [
    "فلنسبح مع الملائكة قائلين: المجد لله في الأعالي وعلى الأرض السلام وفى الناس المسرة. نسبحك. نباركك. نخدمك. نسجد لك. نعترف لك. ننطق بمجدك. نشكرك من أجل عظم مجدك، أيها الرب المالك على السموات، الله الآب ضابط الكل، والرب الابن الواحد الوحيد يسوع المسيح، والروح القدس.",
    "أيها الرب الإله، حمل الله، ابن الآب، رافع خطية العالم، ارحمنا. يا حامل خطية العالم، اقبل طلباتنا إليك. أيها الجالس عن يمين أبيه، ارحمنا. أنت وحدك القدوس. أنت وحدك العالي يا ربى يسوع المسيح والروح القدس. مجدا لله الآب أمين.",
    "أباركك كل يوم، وأسبح اسمك القدوس إلى الأبد. وإلى أبد الأبد. أمين. منذ الليل روحي تبكر إليك يا إلهي، لأن أوامرك هي نور على الأرض. كنت أتلو في طرقك، لأنك صرت لي معينا. باكرا يا رب تسمع صوتي، بالغداة أقف أمامك وتراني.",
]

GRACIOUSLY_AR = [
    "تفضل يا رب أن تحفظنا في هذه الليلة بغير خطية. مبارك أنت يا رب إله آبائنا، ومبارك ومتعالي ومتمجد هو اسمك إلى الأبد. آمين.",
    "فلتكن رحمتك يا رب علينا حسب اتكالنا عليك. لأن عيون الجميع تنتظرك وأنت تعطيهم طعامهم في حينه. اسمعنا أيها الإله مخلصنا رجاء كل أقاصي الأرض. وأنت يا رب أنقذنا من هذا الجيل وإلى الأبد. آمين.",
    "مبارك أنت يا رب علمني عدلك. مبارك أنت يا سيدي فهمني حقوقك. مبارك أنت يا قدوس أنرني ببرك. رحمتك يا رب إلى الأبد وأعمال يديك لا ترفضها. لك التسبيح. لك التمجيد. لك التعظيم يا أبا الآب والابن والروح القدس من الآن وإلى الأبد. آمين.",
]

HOUR_INTRO_AR = {
    'prime':    "صلاة باكر من النهار المبارك، أقدمها للمسيح ملكي وإلهي، وأرجوه أن يغفر لي خطاياي.",
    'terce':    "صلاة الساعة الثالثة من النهار المبارك، أقدمها للمسيح ملكي وإلهي، وأرجوه أن يغفر لي خطاياي.",
    'sext':     "صلاة الساعة السادسة من النهار المبارك، أقدمها للمسيح ملكي وإلهي، وأرجوه أن يغفر لي خطاياي.",
    'none':     "صلاة الساعة التاسعة من النهار المبارك، أقدمها للمسيح ملكي وإلهي، وأرجوه أن يغفر لي خطاياي.",
    'vespers':  "صلاة الغروب من النهار المبارك، أقدمها للمسيح ملكي وإلهي، وأرجوه أن يغفر لي خطاياي.",
    'compline': "صلاة النوم من النهار المبارك، أقدمها للمسيح ملكي وإلهي، وأرجوه أن يغفر لي خطاياي.",
    'veil':     "صلاة ستار الظلمة من النهار المبارك، أقدمها للمسيح ملكي وإلهي، وأرجوه أن يغفر لي خطاياي.",
    'midnight-1': "صلاة الخدمة الأولى المباركة، أقدمها للمسيح ملكي وإلهي، وأرجوه أن يغفر لي خطاياي.",
    'midnight-2': "صلاة الخدمة الثانية المباركة، أقدمها للمسيح ملكي وإلهي، وأرجوه أن يغفر لي خطاياي.",
    'midnight-3': "صلاة الخدمة الثالثة المباركة، أقدمها للمسيح ملكي وإلهي، وأرجوه أن يغفر لي خطاياي.",
}

PSALMS_INTRO_AR = "من مزامير معلمنا داود النبي بركاته علينا أمين."

GLOBAL_EM_REPLACEMENTS_AR = {
    'The worshipper says:': 'يصلي المؤمن:',
    'The following psalms are selected from the 1st hour:': 'المزامير التالية مختارة من الساعة الأولى:',
    'The following psalms are selected from the 3rd hour:': 'المزامير التالية مختارة من الساعة الثالثة:',
    'The following psalms are selected from the 6th hour:': 'المزامير التالية مختارة من الساعة السادسة:',
    'The following psalms are selected from the 9th hour:': 'المزامير التالية مختارة من الساعة التاسعة:',
    'The following psalms are selected from Vespers:': 'المزامير التالية مختارة من الغروب:',
    'The following psalms are selected from Compline:': 'المزامير التالية مختارة من النوم:',
    'The following psalms are selected from Midnight:': 'المزامير التالية مختارة من نصف الليل:',
}

GLOBAL_TEXT_REPLACEMENTS_AR = {
    'Glory be to God forever. Amen.': 'والمجد لله دائمًا أبديًا آمين.',
    'Glory to God forever. Amen.': 'والمجد لله دائمًا أبديًا آمين.',
}

GLOBAL_DOX_REPLACEMENTS_AR = {
    'Glory to You, the Lover of mankind.': 'المجد لك يا محب البشر.',
}

# ===================================================================
# 9. Section processing for ar/ HTML fill
# ===================================================================

def process_section_ar(section_el, title, ar_data_by_en, ar_psalms, hour):
    """Process one <section> in the en/ template and fill with Arabic."""
    pm = re.match(r'Psalm (\d+)(?:\s*\(([IVXLC]+)\))?', title)
    if pm:
        num = int(pm.group(1))
        if num in ar_psalms:
            replace_psalm_ar(section_el, ar_psalms[num])
        return

    if title == 'Introduction to Every Hour':
        replace_prayer_ar(section_el, INTRO_AR)
        return
    if title == "The Lord's Prayer":
        divs = section_el.find_all('div', class_='prayer-text')
        for i, div in enumerate(divs):
            if i < len(LORDS_PRAYER_AR):
                item = LORDS_PRAYER_AR[i]
                if isinstance(item, tuple):
                    kind, txt = item
                    if kind == 'em':
                        set_em(div, txt)
                    else:
                        set_text(div, txt)
                else:
                    set_text(div, item)
        return
    if title == 'The Prayer of Thanksgiving':
        replace_prayer_ar(section_el, THANKSGIVING_AR)
        return
    if title == '41 Kyrie Eleison':
        divs = section_el.find_all('div', class_='prayer-text')
        for i, div in enumerate(divs):
            if i < len(KYRIE_AR):
                item = KYRIE_AR[i]
                if isinstance(item, tuple):
                    kind, txt = item
                    if kind == 'em':
                        set_em(div, txt)
                    else:
                        set_text(div, txt)
                else:
                    set_text(div, item)
        return
    if title == 'Holy Holy Holy':
        replace_prayer_ar(section_el, HOLY_HOLY_AR)
        return
    if title == 'Conclusion of Every Hour':
        replace_prayer_ar(section_el, CONCLUSION_AR)
        return
    if title == 'The Orthodox Creed':
        replace_prayer_ar(section_el, CREED_AR)
        return
    if title == 'Introduction to the Creed':
        replace_prayer_ar(section_el, CREED_INTRO_AR)
        return
    if title in ('Hail to Saint Mary', 'Hail to You'):
        replace_prayer_ar(section_el, VIRGIN_AR)
        return
    if title == 'The Trisagion':
        replace_prayer_ar(section_el, TRISAGION_AR)
        return
    if title == 'The Gloria':
        replace_prayer_ar(section_el, GLORIA_AR)
        return
    if title == 'Graciously Accord, O Lord':
        replace_prayer_ar(section_el, GRACIOUSLY_AR)
        return
    if title == 'Let My Supplication':
        let_my_supplication_ar = [
            "لتقترب طلبتي قدامك يا رب. فهمني حسب قولك. ليدخل تضرعي قدامك. أحيني حسب قولك. لتنطق شفتاي بتسبحتك لأنك علمتني حقوقك. لينطق لساني بأقوالك لأن كل وصاياك عدل. لتكن يدك خلاصي لأني اشتهيت وصاياك. اشتهيت خلاصك يا رب وناموسك هو تلاوتي. تحيا نفسي وتسبحك وأحكامك تعينني. ضللت كخروف ضائع فاطلب عبدك لأنني لم أنس وصاياك.",
            "المجد للآب والابن والروح القدس الآن وكل أوان وإلى دهر الدهور آمين.",
            "المجد للآب والابن والروح القدس الآن وكل أوان وإلى دهر الدهور آمين.",
            "المجد لك يا صالح ومحب البشر. السلام لأمك العذراء ولجميع قديسيك. المجد لك أيها الثالوث القدوس ارحمنا.",
            "ليقم الله وليتبدد أعداؤه وليهرب من قدام وجهه كل مبغضي اسمه القدوس. وشعبك فليكن بالبركة ألوف الألوف وربوات الربوات يصنعون مشيئتك. يا رب افتح شفتي فيخبر فمي بتسبيحك آمين.",
        ]
        replace_prayer_ar(section_el, let_my_supplication_ar)
        return
    if title in ('The First Watch', 'The Second Watch', 'The Third Watch'):
        return
    if title == 'Psalm 50':
        if 50 in ar_psalms:
            replace_psalm_ar(section_el, ar_psalms[50])
        return

    ar_sec = ar_data_by_en.get(title)
    if ar_sec and ar_sec['paragraphs']:
        if 'Gospel' in title or 'إنجيل' in title:
            replace_gospel_ar(section_el, ar_sec['paragraphs'])
        elif title == 'Litanies':
            replace_litanies_ar(section_el, ar_sec['paragraphs'])
        else:
            replace_prayer_ar(section_el, ar_sec['paragraphs'])
        return

def global_replacements_ar(soup):
    for div in soup.find_all('div', class_='prayer-text'):
        txt = div.get_text(strip=True)
        for eng, ar in GLOBAL_EM_REPLACEMENTS_AR.items():
            if eng in txt:
                set_em(div, ar)
                break
        for eng, ar in GLOBAL_TEXT_REPLACEMENTS_AR.items():
            if txt.strip() == eng:
                set_text(div, ar)
                break
        eng_span = div.find('span', class_='doxology-english')
        if eng_span:
            span_txt = eng_span.get_text(strip=True)
            for eng, ar in GLOBAL_DOX_REPLACEMENTS_AR.items():
                if eng in span_txt:
                    eng_span.string = ar
                    break

def replace_hour_intros_ar(soup, hour_name):
    hymn = HOUR_INTRO_AR.get(hour_name)
    if not hymn:
        return
    for sec in soup.find_all('section', class_='section'):
        for div in sec.find_all('div', class_='prayer-text'):
            txt = div.get_text(strip=True)
            if 'beseeching Him to forgive' in txt or 'beseeching him to forgive' in txt.lower():
                set_em(div, hymn)
            elif 'From the Psalms of our father David' in txt:
                set_em(div, PSALMS_INTRO_AR)

# ===================================================================
# 10. Arabic UI translation (section titles, page chrome)
# ===================================================================

AR_TITLE_MAP = {
    'Introduction to Every Hour': 'مقدمة كل ساعة',
    "The Lord's Prayer": 'الصلاة الربانية',
    'The Prayer of Thanksgiving': 'صلاة الشكر',
    'Psalm 50': 'المزمور الخمسون',
    '41 Kyrie Eleison': 'كيرياليسون 41 مرة',
    'Holy Holy Holy': 'قدوس قدوس قدوس',
    'The Orthodox Creed': 'قانون الإيمان المقدس الأرثوذكسي',
    'Introduction to the Creed': 'بدء قانون الإيمان',
    'Conclusion of Every Hour': 'طلبة تصلى آخر كل ساعة',
    'First Absolution': 'التحليل',
    'Second Absolution': 'تحليل آخر',
    'Hail to Saint Mary': 'السلام لك',
    'Hail to You': 'السلام لك',
    'The Trisagion': 'الثلاث تقديسات',
    'The Gloria': 'تسبحة الملائكة',
    'Graciously Accord, O Lord': 'تفضل يا رب',
    'Let My Supplication': 'لتكن طلبتي',
    'Opening Prayer': 'قوموا يا بني النور',
    'Come Let Us Kneel Down': 'هلم نسجد',
    'The Faith of the Church': 'من إيمان الكنيسة',
    'The First Watch': 'الخدمة الأولى',
    'The Second Watch': 'الخدمة الثانية',
    'The Third Watch': 'الخدمة الثالثة',
    'The Pauline Epistle (Ephesians 4:1-5)': 'البولس من رسالة أفسس (٤: ١-٥)',
    'The Holy Gospel According to Saint John (1:1-17)': 'إنجيل يوحنا (١: ١-١٧)',
    'The Holy Gospel (John 14:26-31 & 15:1-4)': 'إنجيل يوحنا (١٤: ٢٦ - ١٥: ٣)',
    'The Holy Gospel (Matthew 5:1-16)': 'إنجيل متى (٥: ١-١٦)',
    'The Holy Gospel (Luke 9:10-17)': 'إنجيل لوقا (٩: ١٠-١٧)',
    'The Holy Gospel (Luke 4:38-41)': 'إنجيل لوقا (٤: ٣٨-٤١)',
    'The Holy Gospel (St. Luke 2:25-32)': 'إنجيل لوقا (٢: ٢٥-٣٢)',
    'The Holy Gospel (Matthew 25:1-13)': 'إنجيل متى (٢٥: ١-١٣)',
    'The Holy Gospel (Luke 7:36-50)': 'إنجيل لوقا (٧: ٣٦-٥٠)',
    'The Holy Gospel (Luke 12:32-46)': 'إنجيل لوقا (١٢: ٣٢-٤٦)',
    'The Holy Gospel (Luke 2:29-32)': 'نشيد سمعان الشيخ',
    'The Holy Gospel (John 6:15-23)': 'إنجيل يوحنا (٦: ١٥-٢٣)',
    'Litanies': 'القطع',
    'Absolution': 'التحليل',
    'Prayer Before Confession': 'صلاة قبل الاعتراف',
    'Prayer After Confession': 'صلاة بعد الاعتراف',
    'Prayer Before Communion 1': 'صلاة قبل التناول ١',
    'Prayer Before Communion 2': 'صلاة قبل التناول ٢',
    'Prayer After Communion 1': 'صلاة بعد التناول ١',
    'Prayer After Communion 2': 'صلاة بعد التناول ٢',
    'Prayer Before Meals 1': 'صلاة قبل الطعام ١',
    'Prayer Before Meals 2': 'صلاة قبل الطعام ٢',
    'Prayer After Meals': 'صلاة بعد الطعام',
    'Prayer Before Studying': 'صلاة قبل المذاكرة',
    'Prayer After Studying': 'صلاة بعد المذاكرة',
}

AR_PSALM_ORDINALS = {
    1: 'الأول', 2: 'الثاني', 3: 'الثالث', 4: 'الرابع',
    5: 'الخامس', 6: 'السادس', 8: 'الثامن',
    11: 'الحادي عشر', 12: 'الثاني عشر', 14: 'الرابع عشر',
    15: 'الخامس عشر', 18: 'الثامن عشر', 19: 'التاسع عشر',
    22: 'الثاني والعشرون', 23: 'الثالث والعشرون',
    24: 'الرابع والعشرون', 25: 'الخامس والعشرون',
    26: 'السادس والعشرون', 28: 'الثامن والعشرون',
    29: 'التاسع والعشرون', 33: 'الثالث والثلاثون',
    40: 'الأربعون', 42: 'الثاني والأربعون',
    44: 'الرابع والأربعون', 45: 'الخامس والأربعون',
    46: 'السادس والأربعون', 50: 'الخمسون',
    53: 'الثالث والخمسون', 56: 'السادس والخمسون',
    60: 'الستون', 62: 'الثاني والستون',
    66: 'السادس والستون', 69: 'التاسع والستون',
    83: 'الثالث والثمانون', 84: 'الرابع والثمانون',
    85: 'الخامس والثمانون', 86: 'السادس والثمانون',
    90: 'التسعون', 92: 'الثاني والتسعون',
    95: 'الخامس والتسعون', 96: 'السادس والتسعون',
    97: 'السابع والتسعون', 98: 'الثامن والتسعون',
    99: 'التاسع والتسعون', 100: 'المائة',
    109: 'المائة والتاسع', 110: 'المائة والعاشر',
    111: 'المائة والحادي عشر', 112: 'المائة والثاني عشر',
    114: 'المائة والرابع عشر', 115: 'المائة والخامس عشر',
    116: 'المائة والسادس عشر', 117: 'المائة والسابع عشر',
    118: 'المائة والثامن عشر', 119: 'المائة والتاسع عشر',
    120: 'المائة والعشرون', 121: 'المائة والحادي والعشرون',
    122: 'المائة والثاني والعشرون', 123: 'المائة والثالث والعشرون',
    124: 'المائة والرابع والعشرون', 125: 'المائة والخامس والعشرون',
    126: 'المائة والسادس والعشرون', 127: 'المائة والسابع والعشرون',
    128: 'المائة والثامن والعشرون', 129: 'المائة والتاسع والعشرون',
    130: 'المائة والثلاثون', 131: 'المائة والحادي والثلاثون',
    132: 'المائة والثاني والثلاثون', 133: 'المائة والثالث والثلاثون',
    136: 'المائة والسادس والثلاثون', 137: 'المائة والسابع والثلاثون',
    140: 'المائة والأربعون', 141: 'المائة والحادي والأربعون',
    142: 'المائة والثاني والأربعون', 145: 'المائة والخامس والأربعون',
    146: 'المائة والسادس والأربعون', 147: 'المائة والسابع والأربعون',
}

PAGE_TITLES_AR = {
    'Prime | Agpeya': 'صلاة باكر | الأجبية',
    'Terce | Agpeya': 'الساعة الثالثة | الأجبية',
    'Sext | Agpeya': 'الساعة السادسة | الأجبية',
    'None | Agpeya': 'الساعة التاسعة | الأجبية',
    'Vespers | Agpeya': 'صلاة الغروب | الأجبية',
    'Compline | Agpeya': 'صلاة النوم | الأجبية',
    'Midnight Prayer | Agpeya': 'صلاة نصف الليل | الأجبية',
    'Prayer of the Veil | Agpeya': 'صلاة الستار | الأجبية',
    'Other Prayers | Agpeya': 'صلوات أخرى | الأجبية',
    'About | Agpeya': 'عن الأجبية | الأجبية',
    'Agpeya - The Coptic Book of Hours': 'الأجبية - كتاب السبع صلوات',
}

H1_MAP_AR = {
    'Prime': 'صلاة باكر',
    'Terce': 'الساعة الثالثة',
    'Sext': 'الساعة السادسة',
    'None': 'الساعة التاسعة',
    'Vespers': 'صلاة الغروب',
    'Compline': 'صلاة النوم',
    'Midnight Prayer': 'صلاة نصف الليل',
    'Prayer of the Veil': 'صلاة الستار',
    'Other Prayers': 'صلوات أخرى',
    'About the Agpeya': 'عن الأجبية',
}

HOUR_DESC_AR = {
    'prime': "في هذه الصلاة نشكر الله على انقضاء الليل بسلام، ونطلب من أجل نهار مضيء بالأعمال الصالحة، وفيها نذكر قيامة السيد المسيح في باكر النهار فنمجده على قيامته.",
    'terce': "تعني هذه الصلاة بتذكيرنا بثلاثة أحداث رئيسية: محاكمة الرب يسوع عن طريق بيلاطس البنطي، وصعود السيد المسيح إلى السماوات، وحلول الروح القدس الذي يُطهر قلوبنا ويُجدد حياتنا.",
    'sext': "تُذكرنا هذه الساعة بصلب السيد المسيح وآلامه، طالبين أنه من خلال آلامه المقدسة، يُنقذ عقولنا من الشهوات، ويحول أفكارنا لتذكُر وصاياه، ويجعلنا نورًا للعالم وملحًا للأرض.",
    'none': "هذه الصلاة تُذكرنا بموت المسيح الخلاصي بالجسد على الصليب، وقبوله توبة اللص اليمين. ونطلب منه أن يميت شهواتنا الجسدية، ويجعلنا شركاء لمجده، وأن يقبل صلواتنا.",
    'vespers': "صلاة الغروب أو الساعة الحادية عشر تتحدث عن إنزال جسد السيد المسيح من على الصليب. وفي نهاية اليوم نعطي الشكر على عناية الله، ونقر بخطايانا.",
    'compline': "صلاة النوم نتذكر فيها دفن السيد المسيح، والعالم الفاني والحساب الأخير، مُتَيَقظين لقدوم الله الوشيك والوقوف قدامه، ونطلب الصفح عن خطايانا، والحماية خلال الليل.",
    'midnight': "صلاة نصف الليل تتحدث عن المجيء الثاني لإلهنا ومخلصنا السيد المسيح، وتنقسم تلك الصلاة لثلاث خدمات.",
    'veil': "صلاة ساعة المساء التي تُدْعَى ساعة حجاب الظلمة أو سِتار الظلمة وهي خاصة بالآباء الكهنة والآباء الرهبان.",
    'other': "مجموعة صلوات روحية من التقليد القبطي الأرثوذكسي.",
}

HOUR_DROPDOWN_AR = [
    {'short': 'الرئيسية', 'long': 'الرئيسية', 'text': 'الرئيسية'},
    {'short': 'الساعة ١', 'long': 'الساعة الأولى - باكر', 'text': 'الساعة الأولى - باكر'},
    {'short': 'الساعة ٣', 'long': 'الساعة الثالثة', 'text': 'الساعة الثالثة'},
    {'short': 'الساعة ٦', 'long': 'الساعة السادسة', 'text': 'الساعة السادسة'},
    {'short': 'الساعة ٩', 'long': 'الساعة التاسعة', 'text': 'الساعة التاسعة'},
    {'short': 'الساعة ١١', 'long': 'الساعة الحادية عشر - الغروب', 'text': 'الساعة الحادية عشر - الغروب'},
    {'short': 'الساعة ١٢', 'long': 'الساعة الثانية عشر - النوم', 'text': 'الساعة الثانية عشر - النوم'},
    {'short': 'نصف الليل', 'long': 'نصف الليل', 'text': 'نصف الليل'},
    {'short': 'الستار', 'long': 'صلاة الستار', 'text': 'صلاة الستار'},
    {'short': 'أخرى', 'long': 'صلوات أخرى', 'text': 'صلوات أخرى'},
    {'short': 'عن', 'long': 'عن الأجبية', 'text': 'عن الأجبية'},
]

def translate_ui_ar(soup, hour_name=None):
    """Translate all visible UI elements to Arabic."""
    for h2 in soup.find_all('h2', class_='section-title'):
        title = h2.get_text(strip=True)
        if title in AR_TITLE_MAP:
            h2.string = AR_TITLE_MAP[title]
        else:
            m = re.match(r'Psalm (\d+)(?:\s*\(([IVXLC]+)\))?', title)
            if m:
                num = int(m.group(1))
                roman = m.group(2)
                ar_name = AR_PSALM_ORDINALS.get(num, str(num))
                label = f'المزمور {ar_name}'
                if roman:
                    label += f' ({roman})'
                h2.string = label

    h1 = soup.find('h1', class_='hour-title')
    if h1:
        txt = h1.get_text(strip=True)
        if txt in H1_MAP_AR:
            h1.string = H1_MAP_AR[txt]

    title_tag = soup.find('title')
    if title_tag:
        txt = title_tag.get_text(strip=True)
        if txt in PAGE_TITLES_AR:
            title_tag.string = PAGE_TITLES_AR[txt]

    if hour_name and hour_name in HOUR_DESC_AR:
        p_desc = soup.find('p', class_='hour-desc')
        if p_desc:
            p_desc.string = HOUR_DESC_AR[hour_name]

    dropdown = soup.find('select', id='hourDropdown')
    if dropdown:
        options = dropdown.find_all('option')
        for opt, ar_data in zip(options, HOUR_DROPDOWN_AR):
            opt['data-short'] = ar_data['short']
            opt['data-long'] = ar_data['long']
            opt.string = ar_data['text']

    light_btn = soup.find('button', id='lightModeBtn')
    if light_btn and light_btn.get_text(strip=True) == 'Light':
        light_btn.string = 'فاتح'
    dark_btn = soup.find('button', id='darkModeBtn')
    if dark_btn and dark_btn.get_text(strip=True) == 'Dark':
        dark_btn.string = 'داكن'

    sec_dropdown = soup.find('select', id='sectionDropdown')
    if sec_dropdown:
        top_opt = sec_dropdown.find('option', value='')
        if top_opt and top_opt.get_text(strip=True) == 'Top':
            top_opt.string = 'أعلى'

    footer = soup.find('footer')
    if footer:
        for child in footer.descendants:
            if isinstance(child, NavigableString) and 'Coptic Book of Hours' in child:
                child.replace_with(child.replace('Coptic Book of Hours', 'كتاب السبع صلوات'))

# ===================================================================
# 11. Process each hour file
# ===================================================================

def build_en_title_lookup(hour_sections):
    """Build {en_title: section_data} from parsed hour sections."""
    lookup = {}
    for sec in hour_sections:
        if sec['en_title'] and sec['en_title'] not in lookup:
            lookup[sec['en_title']] = sec
    return lookup

def process_hour_ar(en_path, ar_path, hour_sections, ar_psalms, hour_name):
    """Load en/ template and fill with Arabic content, write to ar/."""
    with open(en_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = 'ar'
        html_tag['dir'] = 'rtl'

    ar_by_en = build_en_title_lookup(hour_sections)

    for sec in soup.find_all('section', class_='section'):
        h2 = sec.find('h2', class_='section-title')
        if not h2:
            continue
        title = h2.get_text(strip=True)
        process_section_ar(sec, title, ar_by_en, ar_psalms, hour_name)

    replace_hour_intros_ar(soup, hour_name)
    global_replacements_ar(soup)
    translate_ui_ar(soup, hour_name)

    with open(ar_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"  Wrote {os.path.basename(ar_path)}")

def process_midnight_ar(en_path, ar_path, hour_sections, ar_psalms):
    """Process midnight with its 3 watches."""
    with open(en_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = 'ar'
        html_tag['dir'] = 'rtl'

    ar_by_en = build_en_title_lookup(hour_sections)
    watch = 0

    for sec in soup.find_all('section', class_='section'):
        h2 = sec.find('h2', class_='section-title')
        if not h2:
            continue
        title = h2.get_text(strip=True)

        if title == 'The First Watch':
            watch = 1
        elif title == 'The Second Watch':
            watch = 2
        elif title == 'The Third Watch':
            watch = 3

        process_section_ar(sec, title, ar_by_en, ar_psalms, 'midnight')

    for sec in soup.find_all('section', class_='section'):
        for div in sec.find_all('div', class_='prayer-text'):
            txt = div.get_text(strip=True)
            if 'beseeching Him to forgive' in txt or 'beseeching him to forgive' in txt.lower():
                if 'first watch' in txt.lower():
                    set_em(div, HOUR_INTRO_AR['midnight-1'])
                elif 'second watch' in txt.lower():
                    set_em(div, HOUR_INTRO_AR['midnight-2'])
                elif 'third watch' in txt.lower():
                    set_em(div, HOUR_INTRO_AR['midnight-3'])
            elif 'From the Psalms of our father David' in txt:
                set_em(div, PSALMS_INTRO_AR)

    global_replacements_ar(soup)
    translate_ui_ar(soup, 'midnight')

    with open(ar_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"  Wrote midnight.html")

# ===================================================================
# 12. Main
# ===================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Parse St-Takla Arabic Agpeya')
    parser.add_argument('--cache-dir', default=os.path.join(ROOT, '.st-takla-cache'),
                        help='Directory to cache fetched HTML')
    parser.add_argument('--json-out', default=os.path.join(ROOT, 'st-takla-arabic.json'),
                        help='Output JSON file path')
    parser.add_argument('--fill-ar', action='store_true',
                        help='Fill ar/ HTML files from en/ templates')
    args = parser.parse_args()

    print("Fetching and parsing St-Takla Arabic Agpeya...")
    all_data = fetch_all_hours(cache_dir=args.cache_dir)

    print(f"\nWriting JSON to {args.json_out}...")
    with open(args.json_out, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print("  Done.")

    total_sections = sum(len(v) for v in all_data.values())
    total_paras = sum(len(s['paragraphs']) for secs in all_data.values() for s in secs)
    print(f"\n  {total_sections} sections, {total_paras} paragraphs across {len(all_data)} hours")

    if args.fill_ar:
        print("\nFilling ar/ HTML files...")
        ar_psalms = build_arabic_psalm_lookup(all_data)
        print(f"  {len(ar_psalms)} unique psalms collected")

        os.makedirs(os.path.join(ROOT, 'ar'), exist_ok=True)

        for hour in ['prime', 'terce', 'sext', 'none', 'vespers', 'compline', 'veil']:
            en = os.path.join(ROOT, 'en', f'{hour}.html')
            ar = os.path.join(ROOT, 'ar', f'{hour}.html')
            if not os.path.exists(en):
                print(f"  SKIP {hour} (no en/ template)")
                continue
            print(f"  Processing {hour}...")
            process_hour_ar(en, ar, all_data.get(hour, []), ar_psalms, hour)

        mn_en = os.path.join(ROOT, 'en', 'midnight.html')
        mn_ar = os.path.join(ROOT, 'ar', 'midnight.html')
        if os.path.exists(mn_en):
            print("  Processing midnight...")
            process_midnight_ar(mn_en, mn_ar, all_data.get('midnight', []), ar_psalms)

        print("\nDone filling ar/ HTML!")

if __name__ == '__main__':
    main()
