#!/usr/bin/env python3
"""
Clean French text contamination from cop/ HTML files.

The PDF has a two-column layout (Coptic left, French right) and the extraction
didn't separate them properly. This script:
1. Removes ALL <div class="prayer-text"> blocks (those WITHOUT coptic-text class)
   -- these are entirely French contamination from the right column.
2. Removes coptic-text divs that contain ONLY French (no Coptic at all).
3. Removes French trailing fragments from coptic-text lines.
"""
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COP_DIR = os.path.join(BASE, 'cop')

FRENCH_ACCENTED = set('éèêëàâäùûüôîïçœæÉÈÊËÀÂÄÙÛÜÔÎÏÇŒÆ')


def has_coptic_unicode(text):
    for ch in text:
        cp = ord(ch)
        if 0x2C80 <= cp <= 0x2CFF:
            return True
    return False


def has_cs_coptic(text):
    """Check if text contains CS Coptic encoding markers."""
    if '`' in text:
        return True
    if '@' in text:
        return True
    # Semicolon in CS Coptic represents the letter theta (;)
    # Words containing ; are almost certainly CS Coptic
    if ';' in text and re.search(r'[a-zA-Z];|;[a-zA-Z]', text):
        return True
    # Square brackets used in CS Coptic for special chars
    if '[' in text and re.search(r'[a-zA-Z]\[|\\[a-zA-Z]', text):
        return True
    # ] used as prefix in CS Coptic
    if ']' in text and re.search(r'][a-zA-Z]|[a-zA-Z]]', text):
        return True
    cs_words = [
        r'\bVnou', r'\bViwt', r'\bPi,', r'\bP\[', r'\bPen\[',
        r'\bIycouc\b', r'\bOuoh\b', r'\bouoh\b', r'\bAmyn\b', r'\bamyn\b',
        r'\bqen\b', r'\bhijen\b', r'\bniben\b', r'\bmaref\b',
        r'\bmaren\b', r'\btwbh\b', r'\bebol\b', r'\bswpi\b',
        r'\bneman\b', r'\bpirefernobi\b', r'\bKurie\b', r'\bDoxa\b',
        r'\bPatri\b', r'\bUiw\b', r'\bPneumati\b', r'\beulogycon\b',
        r'\bIwannyn\b', r'\bLoukan\b', r'\bagiou\b', r'\beuaggeliou\b',
        r'\banagnwcma\b', r'\banagnw\b', r'\bnitwou\b',
        r'\bnai\b', r'\bnyi\b', r'\bnyeteron\b',
        r'\bpenwik\b', r'\btekmetouro\b', r'\bpekran\b',
        r'\bpiwou\b', r'\bmatoujon\b', r'\bnan\b',
        r'\bnem\b', r'\bnekmetsenhyt\b', r'\bnijom\b',
        r'\bPicrayl\b', r'\bpekcaji\b', r'\bpjincouwn\b',
        r'\bharwten\b', r'\btyrou\b', r'\beumeh\b',
        r'\btera\b', r'\btena\b',
    ]
    for pat in cs_words:
        if re.search(pat, text):
            return True
    return False


def has_coptic(text):
    """Check if text contains any form of Coptic."""
    clean = re.sub(r'<[^>]+>', ' ', text).strip()
    return has_coptic_unicode(clean) or has_cs_coptic(clean)


def is_french(text):
    """Check if text is French (contains French words/chars, but no Coptic)."""
    clean = re.sub(r'<[^>]+>', ' ', text).strip()
    if not clean:
        return False
    if has_coptic(clean):
        return False
    if has_french_accented(clean):
        return True

    # Known French contamination words (no accents) found in the PDF extraction
    french_contam = {
        # Common words
        'le', 'la', 'les', 'de', 'du', 'des', 'un', 'une', 'et', 'est',
        'en', 'qui', 'que', 'nous', 'dans', 'pour', 'par', 'sur', 'son',
        'ses', 'sa', 'aussi', 'avec', 'mais', 'tous', 'toute', 'tout',
        'mon', 'ma', 'mes', 'ton', 'ta', 'tes', 'il', 'elle', 'au', 'aux',
        'ce', 'cette', 'ou', 'ne', 'pas', 'se', 'si', 'car', 'je', 'tu',
        'notre', 'nos', 'vie',
        # Words specific to contamination found in cop/ pages
        'esprit', 'parole', 'paroles', 'sauveur', 'marie', 'bon',
        'connaissance', 'divine', 'chair', 'chaque', 'nuit',
        'commandements', 'directrice', 'enfantement', 'ineffable',
        'enseveli', 'existence', 'vaine', 'faveur', 'hommes',
        'honneur', 'honte', 'humain', 'immortels', 'jour',
        'jugement', 'jugements', 'justes', 'mort', 'ordonnances',
        'ouvertement', 'peuple', 'peuples', 'puissance', 'adverse',
        'puissant', 'selon', 'souillure', 'tentation',
        'toujours', 'vierge', 'vivifiante', 'vivifiant',
        'attendus', 'symbole', 'credo', 'trisagion',
        'sainte', 'saint', 'sans', 'sois', 'petit', 'troupeau',
        'votre', 'pere', 'alors', 'point', 'honteux', 'comprendrai',
        'gardant', 'garder', 'garderai', 'oublierai',
        'montagne', 'droite', 'soutient', 'remplira',
        'bienheureux', 'entendu', 'vaines', 'psalmodiez',
        'intelligence', 'anges', 'disant', 'commis',
        'volontairement', 'trouble', 'peine', 'fatigue',
        'suspendu', 'harpes', 'court', 'vite', 'main',
        'exulteront', 'incessantes', 'exaltent',
        'parvienne', 'devant', 'donne', 'talon', 'contre',
        'secourront', 'recherche', 'serviteur', 'perdue',
    }

    words = re.findall(r"[a-zA-Z']+", clean.lower())
    if not words:
        return False
    # Strip punctuation for matching
    stripped = [w.rstrip("'.,!?;:") for w in words]
    fr_count = sum(1 for w in stripped if w in french_contam)
    total = len(words)
    if total == 0:
        return False
    # If any word matches known contamination, and it's a short fragment
    if fr_count > 0 and (fr_count / total > 0.3 or total <= 3):
        return True
    return False


def has_french_accented(text):
    return bool(FRENCH_ACCENTED & set(text))


def is_french_fragment(text):
    """Detect short French fragments that may not have accents or common words.
    E.g., 'sauve-moi !', 'ennemis.', 'crainte.', 'Esprit.'"""
    clean = re.sub(r'<[^>]+>', ' ', text).strip()
    if not clean:
        return False
    if has_coptic(clean):
        return False
    # Known French single-word or short fragments
    french_singles = {
        'sauve', 'moi', 'esprit', 'parole', 'paroles', 'sauveur',
        'chair', 'mort', 'honte', 'jour', 'nuit', 'vie',
        'jugement', 'jugements', 'justes', 'faveur',
        'peuple', 'peuples', 'tentation', 'honneur',
        'crainte', 'ennemi', 'ennemis', 'louange',
        'hommes', 'terre', 'immortels', 'puissant',
        'ordonnances', 'commandements', 'souillure',
        'enseveli', 'ouvertement', 'directrice',
        'vivifiante', 'vivifiant', 'humain',
        'attendus', 'rend', 'bouche', 'proclamera',
        'perdue', 'serviteur', 'recherche',
        'vaine', 'vaines', 'adverse', 'dignement',
        'fond', 'noble', 'prolonge',
    }
    words = re.findall(r"[a-zA-Z]+", clean.lower())
    if not words:
        return False
    matches = sum(1 for w in words if w.rstrip("s") in french_singles or w in french_singles)
    # If any word is a known French fragment word
    if matches > 0:
        return True
    return False


def clean_file(filepath):
    """Clean French contamination from a cop/ HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Step 1: Remove ALL non-coptic prayer-text divs.
    # These are French column contamination.
    content = re.sub(
        r'\s*<div class="prayer-text">.*?</div>\s*',
        '\n',
        content,
        flags=re.DOTALL
    )

    # Step 2: Remove coptic-text divs that have NO Coptic content at all
    def remove_french_coptic_divs(m):
        inner = m.group(1)
        if not has_coptic(inner):
            return ''
        return m.group(0)

    content = re.sub(
        r'<div class="prayer-text coptic-text">\s*(.*?)\s*</div>',
        remove_french_coptic_divs,
        content,
        flags=re.DOTALL
    )

    # Step 3: Clean French trailing fragments from within coptic-text lines
    def clean_coptic_div(m):
        opening = '<div class="prayer-text coptic-text">'
        inner = m.group(1)

        # Process each line (split by <br>)
        parts = re.split(r'(<br\s*/?>)', inner)
        cleaned = []
        modified = False

        for part in parts:
            if re.match(r'<br\s*/?>', part):
                cleaned.append(part)
                continue

            clean_text = re.sub(r'<[^>]+>', ' ', part).strip()
            if not clean_text:
                cleaned.append(part)
                continue

            # If entire segment is French (no Coptic), remove it
            if not has_coptic(part) and (is_french(part) or is_french_fragment(part)):
                modified = True
                if cleaned and re.match(r'<br\s*/?>', cleaned[-1]):
                    cleaned.pop()
                continue

            # Check for trailing French after Coptic
            result = part

            # Pattern 1: Coptic char/punctuation followed by French text
            trail = re.search(
                r'([\u03E2-\u03EF\u2C80-\u2CFF@`.:;\]\)\*])\s*[\*\s]*([A-Za-zéèêëàâäùûüôîïçœæÉÈÊËÀÂÄÙÛÜÔÎÏÇŒÆ][A-Za-zéèêëàâäùûüôîïçœæÉÈÊËÀÂÄÙÛÜÔÎÏÇŒÆ\s\'\u2018\u2019!?,;:.\-\*]{1,})$',
                result
            )
            if trail:
                candidate = trail.group(2).strip()
                if is_french(candidate) or has_french_accented(candidate) or is_french_fragment(candidate):
                    result = result[:trail.start(2)].rstrip(' *')
                    modified = True

            # Pattern 2: French text after guillemets « or quotes
            trail2 = re.search(
                r'\s*[«»"\u00AB\u00BB]\s*([A-Za-zéèêëàâäùûüôîïçœæÉÈÊËÀÂÄÙÛÜÔÎÏÇŒÆ][A-Za-zéèêëàâäùûüôîïçœæÉÈÊËÀÂÄÙÛÜÔÎÏÇŒÆ\s\'\u2018\u2019,!?.;:\-«»\u00AB\u00BB]{3,})$',
                result
            )
            if trail2:
                candidate = trail2.group(1).strip()
                if (is_french(candidate) or has_french_accented(candidate) or is_french_fragment(candidate)) and has_coptic(result[:trail2.start()]):
                    result = result[:trail2.start()].rstrip()
                    modified = True

            # Pattern 3: For CS Coptic lines, detect French at end after any word boundary
            # Only applies when the line already has CS Coptic markers
            if has_coptic(result):
                trail3 = re.search(
                    r'\s+([A-Za-zéèêëàâäùûüôîïçœæÉÈÊËÀÂÄÙÛÜÔÎÏÇŒÆ][A-Za-zéèêëàâäùûüôîïçœæÉÈÊËÀÂÄÙÛÜÔÎÏÇŒÆ\s\'\u2018\u2019!?,;:.\-\*]{1,})$',
                    result
                )
                if trail3:
                    candidate = trail3.group(1).strip()
                    if (is_french(candidate) or has_french_accented(candidate) or is_french_fragment(candidate)):
                        # Verify the part before is actually Coptic
                        before = result[:trail3.start()].strip()
                        if has_coptic(before):
                            result = before
                            modified = True

            cleaned.append(result)

        if modified:
            inner = ''.join(cleaned)
            # Remove trailing <br>
            inner = re.sub(r'\s*<br\s*/?>\s*$', '', inner)
            return opening + '\n' + inner + '\n</div>'
        return m.group(0)

    content = re.sub(
        r'<div class="prayer-text coptic-text">\s*(.*?)\s*</div>',
        clean_coptic_div,
        content,
        flags=re.DOTALL
    )

    # Step 3b: Remove standalone numbers and reference markers from coptic-text divs
    # These are page/footnote numbers from the PDF
    def clean_noise_lines(m):
        # (removed nonlocal changes)
        opening = '<div class="prayer-text coptic-text">'
        inner = m.group(1)
        parts = re.split(r'(<br\s*/?>)', inner)
        cleaned = []
        modified = False
        for part in parts:
            if re.match(r'<br\s*/?>', part):
                cleaned.append(part)
                continue
            clean_text = re.sub(r'<[^>]+>', ' ', part).strip()
            if not clean_text:
                cleaned.append(part)
                continue
            # Remove standalone numbers (page/footnote refs)
            if re.match(r'^\d+\.?\s*$', clean_text):
                modified = True
                if cleaned and re.match(r'<br\s*/?>', cleaned[-1]):
                    cleaned.pop()
                continue
            # Remove psalm/reference markers like "(Ps 133)"
            if re.match(r'^\(Ps\.?\s+\d+\)$', clean_text):
                modified = True
                if cleaned and re.match(r'<br\s*/?>', cleaned[-1]):
                    cleaned.pop()
                continue
            # Remove "l'ennemi" type French (with apostrophe, no accents)
            if re.match(r"^l'[a-z]+\.?$", clean_text, re.IGNORECASE):
                if not has_coptic(clean_text):
                    modified = True
                    if cleaned and re.match(r'<br\s*/?>', cleaned[-1]):
                        cleaned.pop()
                    continue
            cleaned.append(part)
        if modified:
            pass  # changed
            inner = ''.join(cleaned)
            inner = re.sub(r'\s*<br\s*/?>\s*$', '', inner)
            return opening + '\n' + inner + '\n</div>'
        return m.group(0)

    content = re.sub(
        r'<div class="prayer-text coptic-text">\s*(.*?)\s*</div>',
        clean_noise_lines,
        content, flags=re.DOTALL
    )

    # Step 4: Clean up multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def verify(filepath):
    """Check for remaining French contamination."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    issues = []
    # Check non-coptic divs
    for m in re.finditer(r'<div class="prayer-text">\s*(.*?)\s*</div>', content, re.DOTALL):
        txt = re.sub(r'<[^>]+>', ' ', m.group(1)).strip()
        if txt:
            issues.append(f"[non-coptic div] {txt[:100]}")
    # Check for French in coptic-text divs
    for m in re.finditer(r'<div class="prayer-text coptic-text">\s*(.*?)\s*</div>', content, re.DOTALL):
        for line in re.split(r'<br\s*/?>', m.group(1)):
            clean = re.sub(r'<[^>]+>', ' ', line).strip()
            if clean and has_french_accented(clean) and not has_coptic(clean):
                issues.append(f"[fr in coptic] {clean[:100]}")
    return issues


if __name__ == '__main__':
    print("Cleaning French from cop/ pages...\n")
    for fname in sorted(os.listdir(COP_DIR)):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(COP_DIR, fname)
        changed = clean_file(fpath)
        print(f"  {fname}: {'cleaned' if changed else 'no changes'}")

    print("\n--- Verification ---")
    all_ok = True
    for fname in sorted(os.listdir(COP_DIR)):
        if not fname.endswith('.html'):
            continue
        issues = verify(os.path.join(COP_DIR, fname))
        if issues:
            all_ok = False
            print(f"\n  {fname}:")
            for iss in issues[:15]:
                print(f"    - {iss}")
    if all_ok:
        print("  All clean!")
