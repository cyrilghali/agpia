---
title: "feat: Add Coptic language from PDF extraction"
type: feat
status: active
date: 2026-03-14
---

# feat: Add Coptic language from PDF extraction

## Enhancement Summary

**Deepened on:** 2026-03-14
**Research agents used:** pattern-recognition-specialist, architecture-strategist, performance-oracle, best-practices-researcher, spec-flow-analyzer

### Key Improvements
1. **Complete CS Coptic font mapping table** reverse-engineered from PDF analysis (not guesswork)
2. **Architecture: Extract sticky subheader into JS** before adding Coptic (prevents touching 44+ files)
3. **Use pdfplumber** instead of PyPDF2 for superior two-column layout handling
4. **Font fix:** Convert TTF to WOFF2 and add missing `font-display: swap`
5. **Separate extraction from generation** into two scripts with JSON checkpoint

### New Considerations Discovered
- The ASCII text is NOT a transliteration system -- it's **CS Coptic legacy font encoding** (ASCII positions mapped to Coptic glyphs)
- Greek liturgical phrases (Kyrie eleison, Doxa Patri, etc.) must be detected and preserved as-is
- `=` signs in PDF mark nomina sacra abbreviations (e.g., `pi=p=na =e=;u` = Ⲡⲓⲡⲛⲉⲩⲙⲁ ⲉⲑⲟⲩⲁⲃ)
- `@` is used as a verse/period separator in the ASCII encoding
- The `<` character also maps to ⲭ (khi) alongside `,` in some PDF sections

---

## Overview

Extract Coptic prayer text from `agpia.pdf` (138 pages) and add Coptic (`cop/`) as a new language to the Agpia website. The PDF contains Coptic text in two formats: **Unicode Coptic** (U+2C80-2CFF, used in 88 pages for Psalms) and **CS Coptic legacy font encoding** (ASCII positions mapped to Coptic glyphs via the font, used in 58 pages for prayers/tropaires). The site already bundles the `Avva Shenouda` Coptic font and CSS classes for Coptic text.

## Problem Statement / Motivation

The Agpia website currently supports French and Arabic but lacks the original Coptic language -- the liturgical source language of the prayers. The PDF contains a complete Coptic Agpia with French translation, created by Marian-Apollos Balastre, certified in Coptic language from the Institut Catholique de Paris.

## Proposed Solution

### Phase 0: Prerequisite Refactors (Critical)

Before adding Coptic content, fix two architectural issues that would otherwise multiply work:

#### 0a. Extract sticky subheader into JS injection

**Why:** The sticky subheader (~63 lines of HTML) is duplicated in every single HTML file (~33 files). Adding Coptic means adding a language link to all of them, then maintaining ~44 files going forward. The footer is already JS-injected (agpeya.js lines 58-92) -- apply the same pattern to the subheader.

**How:**
1. Create `injectSubheader()` function in `agpeya.js` that builds the subheader HTML
2. Derive the current page from `window.location.pathname`
3. Construct language links by swapping the folder segment in the URL
4. Store hour dropdown labels in a language-keyed data structure
5. Remove the raw HTML subheader from all ~33 existing files
6. Replace with a minimal `<div id="subheader-mount"></div>` placeholder

**Benefit:** Adding Coptic (or any future language) becomes a config-only change in `agpeya.js`. No need to touch existing HTML files.

#### 0b. Font optimization

- Convert `Avva_Shenouda.ttf` (37KB) to WOFF2 (~22KB), move to `fonts/avva-shenouda.woff2`
- Add missing `font-display: swap` to the `@font-face` rule (currently defaults to `auto`/`block`, causing 3 seconds of invisible text on first load)
- This is a real bug today -- Coptic text on existing doxology sections is invisible until font loads

#### 0c. Clean up phantom `en/` references

- Remove `/en/*.html` entries from `sw.js` PRECACHE_URLS (the directory doesn't exist)
- Remove `en` from `build.sh` cp command

### Phase 1: PDF Text Extraction & Conversion

Build two Python scripts with a JSON checkpoint between them:

#### `scripts/extract_coptic.py` -- Extraction + Conversion

Uses **pdfplumber** (not PyPDF2) for superior layout analysis with two-column PDFs.

**Step 1: Extract text with layout awareness**

pdfplumber provides character-level x-coordinates, enabling proper column separation. The PDF has Coptic on the left and French on the right. Use x-position thresholds to split columns.

**Step 2: Identify text encoding type per text run**

Each text run is either:
- **Unicode Coptic** (characters in U+2C80-2CFF or U+03E2-03EF range) -- pass through as-is
- **CS Coptic legacy encoding** (ASCII characters from legacy font) -- convert using mapping table
- **French text** -- discard (already on the site)
- **Greek liturgical phrases** -- detect and preserve (Kyrie eleison, Doxa Patri, etc.)

**Step 3: Convert CS Coptic to Unicode**

Complete mapping table (reverse-engineered from PDF analysis of dual-encoding pages):

| ASCII | Unicode | Coptic Name | Example |
|---|---|---|---|
| `a` | ⲁ (U+2C81) | alpha | `amyn` → ⲁⲙⲏⲛ |
| `b` | ⲃ (U+2C83) | vida | `ebol` → ⲉⲃⲟⲗ |
| `g` | ⲅ (U+2C85) | gamma | `agiw` → ⲁⲅⲓⲱ |
| `d` | ⲇ (U+2C87) | dalda | |
| `e` | ⲉ (U+2C89) | ei | |
| `z` | ⲍ (U+2C91) | zeta | |
| `y` | ⲏ (U+2C8F) | hita/eta | `amyn` → ⲁⲙⲏⲛ |
| `;` | ⲑ (U+2C91) | thida/theta | `e;ouab` → ⲉⲑⲟⲩⲁⲃ |
| `i` | ⲓ (U+2C93) | yota/iota | |
| `k` | ⲕ (U+2C95) | kappa | |
| `l` | ⲗ (U+2C97) | laula | |
| `m` | ⲙ (U+2C99) | mi | |
| `n` | ⲛ (U+2C9B) | ni | |
| `x` | ⲝ (U+2C9D) | eksi | |
| `o` | ⲟ (U+2C9F) | o | |
| `p` | ⲡ (U+2CA1) | pi | |
| `r` | ⲣ (U+2CA3) | ro | |
| `c` | ⲥ (U+2CA5) | sima | `P[oic` → Ⲡϭⲟⲓⲥ |
| `t` | ⲧ (U+2CA7) | tav | |
| `u` | ⲩ (U+2CA9) | he/epsilon | |
| `v` | ⲫ (U+2CAB) | fi/phi | `Vnou]` → Ⲫⲛⲟⲩϯ |
| `,` | ⲭ (U+2CAD) | khi | `Pi,rictoc` → Ⲡⲓⲭⲣⲓⲥⲧⲟⲥ |
| `<` | ⲭ (U+2CAD) | khi (alt) | `Pi<rictoc` → Ⲡⲓⲭⲣⲓⲥⲧⲟⲥ |
| `w` | ⲱ (U+2CB1) | oou/omega | |
| `s` | ϣ (U+03E3) | shai | `Psyri` → Ⲡϣⲏⲣⲓ |
| `f` | ϥ (U+03E5) | fai | `afmou` → ⲁϥⲙⲟⲩ |
| `h` | ϩ (U+2CB5) | hori | `hwb` → ϩⲱⲃ |
| `q` | ϧ (U+2CB7) | khai | `qen` → ϧⲉⲛ |
| `j` | ϫ (U+2CBC) | jandja | `njoc` → ⲛϫⲟⲥ |
| `[` | ϭ (U+03E9) | tchima | `P[oic` → Ⲡϭⲟⲓⲥ |
| `]` | ϯ (U+03EF) | ti | `Pennou]` → ⲡⲉⲛⲛⲟⲩϯ |

**Special characters:**
| ASCII | Meaning | Handling |
|---|---|---|
| `` ` `` (backtick) | Supralinear stroke / jinkim | Convert to combining overline (U+0305) over following char |
| `=` | Nomina sacra abbreviation | Convert to combining overline over following char |
| `@` | Verse/period separator | Convert to Coptic full stop or period |
| `:` | Standard punctuation | Preserve |

**Uppercase mapping:** Same letters but uppercase Coptic (e.g., `A`→Ⲁ, `V`→Ⲫ, `P`→Ⲡ, `Q`→Ϧ, `J`→Ϫ)

**Greek phrase detection:** Lines containing `Kuri`, `Doxa`, `Patri`, `Pneumati`, `agiou`, `euaggeliou` etc. are Greek liturgical text and should NOT be converted through the Coptic mapping. Preserve them with a Greek class marker.

**Step 4: Output structured JSON**

```json
{
  "prime": {
    "sections": [
      {
        "title": "ϯⲡⲣⲟⲥⲉⲩⲭⲏ ⲛⲧⲉ ϯⲛⲁⲩ ⲛϣⲱⲣⲡ",
        "type": "header",
        "content": ""
      },
      {
        "title": "Ⲯⲁⲗⲙⲟⲥ ⲁ̅",
        "type": "psalm",
        "verses": ["Ⲟⲩⲙⲁⲕⲁⲣⲓⲟⲥ ⲡⲉ ⲡⲓⲣⲱⲙⲓ...", "..."]
      },
      {
        "title": "ⲡⲓⲉⲩⲁⲅⲅⲉⲗⲓⲟⲛ",
        "type": "gospel",
        "content": "..."
      }
    ]
  }
}
```

### Phase 2: HTML Page Generation

#### `scripts/generate_coptic_html.py` -- JSON to HTML

Consumes the JSON from Phase 1, applies the HTML template patterns from existing pages.

**Required HTML structure per page** (from pattern analysis):

```html
<!DOCTYPE html>
<html lang="cop">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0, viewport-fit=cover" name="viewport"/>
  <title>PAGE_TITLE | Agpia</title>
  <link href="../agpeya-style.css" rel="stylesheet"/>
  <!-- OG tags, PWA meta, analytics -->
</head>
<body>
  <div id="subheader-mount"></div> <!-- JS-injected after Phase 0a -->
  <main class="container">
    <div class="hour-header">
      <div class="header-crosses">
        <img alt="Coptic Cross" src="../coptic-cross.png"/>
      </div>
      <h1 class="hour-title">COPTIC_HOUR_NAME</h1>
      <p class="hour-time">HOUR_TIME</p>
    </div>
    <div class="prayer-content">
      <div class="ornament"><!-- 3x coptic-cross.png --></div>

      <section class="section">
        <h2 class="section-title">SECTION_TITLE</h2>
        <div class="prayer-text coptic-text">PRAYER_TEXT</div>
      </section>

      <!-- Psalms use psalm-verse class with drop-cap on first -->
      <section class="section">
        <h2 class="section-title">PSALM_TITLE</h2>
        <div class="psalm-verse drop-cap coptic-text">FIRST_VERSE</div>
        <div class="psalm-verse coptic-text">NEXT_VERSE</div>
      </section>

      <!-- Gospel gets id="gospel" -->
      <section class="section" id="gospel">
        <h2 class="section-title">GOSPEL_REF</h2>
        <div class="prayer-text coptic-text">GOSPEL_TEXT</div>
      </section>

      <div class="ornament"><!-- 3x coptic-cross.png --></div>
    </div>
    <nav class="nav-hours"><!-- hour links --></nav>
  </main>
  <script src="../agpeya.js"></script>
  <script>initJumpToGospel();</script>
</body>
</html>
```

**CSS class usage:**
- `coptic-text` on all Coptic content divs (triggers Avva Shenouda font)
- `psalm-verse` for psalm content (not `prayer-text`)
- `drop-cap` on first psalm verse div only
- `alleluia` span at end of each psalm section
- `section-title` on `<h2>` elements (drives section dropdown)

**Page-to-PDF mapping:**

| File | PDF Pages | Shared Sections |
|---|---|---|
| `prime.html` | 6-32 | Introduction (p6) + Thanksgiving (p7) + Psalm 50 (p8) + Prime proper (p9-32) |
| `terce.html` | 33-46 | |
| `sext.html` | 47-59 | |
| `none.html` | 60-71 | |
| `vespers.html` | 72-82 | |
| `compline.html` | 83-95 | |
| `midnight.html` | 99-123 | 3 services with separate gospels and tropaires |
| `veil.html` | 96-98 | |
| `other.html` | 124-137 | Annexes, additional prayers |
| `index.html` | — | Hour selection grid with Coptic labels |
| `about.html` | — | About page |

### Phase 3: Site-Wide Integration

After Phase 0a (subheader extraction), this becomes minimal:

#### `agpeya.js` modifications:
- Add `'cop'` to `folders` array (line ~421)
- Add `cop` branch to `activeLang` logic (lines ~429-430, currently only handles `fr`/`ar`)
- Add Coptic footer text to `footerText` dictionary (key: `'cop'`)
- Add Coptic hour labels to subheader data structure (new after Phase 0a)
- Add Coptic strings to PWA install `i18n` object (lines ~700-769)

#### `index.html` (root):
- Add `'cop'` to `validLangs` array (line ~41)

#### `sw.js`:
- Add `/cop/*.html` entries to `PRECACHE_URLS`

#### `build.sh`:
- Add `cop` directory to the copy command

### Phase 4: CSS & Font Adjustments

- Add `font-display: swap` to Avva Shenouda `@font-face` (bug fix -- currently missing)
- Add `unicode-range: U+2C80-2CFF, U+03E2-03EF, U+0300-036F` to scope font loading
- Add body-text CSS for `[lang="cop"]`:
  ```css
  [lang="cop"] .prayer-text,
  [lang="cop"] .psalm-verse {
      font-family: 'Avva Shenouda', serif;
      font-size: 1.15rem;
      line-height: 1.8;
  }
  ```
- Test drop-cap rendering with Coptic `::first-letter` (LTR, same as French)

## Technical Considerations

### CS Coptic Legacy Font Encoding (Critical Insight)

The ASCII text in the PDF is **NOT a transliteration system**. It is the underlying character codes from a CS Coptic legacy font. When the PDF was created, the font mapped ASCII positions to Coptic glyphs. When text extraction tools read the PDF, they get the raw ASCII codes rather than Unicode Coptic. This is a well-known problem with pre-Unicode Coptic fonts.

The CopticChurch.net font converter tool handles this conversion for several legacy fonts (CS, Avva Shenouda, Athanasius, Pishoi, Copt, Coptic1, Coptonew, Koptos). The mapping table above was reverse-engineered by comparing pages in the PDF that contain both Unicode Coptic (Psalms) and CS encoding (prayers) for the same or adjacent text.

### Two-Column PDF Layout

**Use pdfplumber** instead of PyPDF2. pdfplumber (built on pdfminer.six) provides character-level x,y coordinates, enabling:
1. Cluster characters by x-position to identify left (Coptic) vs right (French) columns
2. A midpoint threshold (typically around x=300 for a standard A4 page) separates the columns
3. Within each column, reconstruct lines by y-position

PyPDF2 only extracts raw text without positional data, making column separation unreliable.

### Greek Liturgical Phrases

The PDF contains Greek liturgical phrases in the same CS encoding:
- `Kuri'e 'ele'ycon` = Κύριε ἐλέησον (Lord have mercy)
- `Doxa Patri ke Uiw` = Δόξα Πατρί καί Υἱῷ (Glory to the Father and Son)
- `agiou euaggeliou` = ἁγίου εὐαγγελίου (holy gospel)

These must be detected and handled separately -- either preserved in Greek Unicode or wrapped in a `<span class="greek-text">` element.

### Pages with Both Encodings

20+ pages contain both Unicode Coptic and CS encoding. These serve as validation checkpoints. The extraction script should:
1. Detect which encoding each text run uses
2. Pass Unicode through unchanged
3. Convert CS encoding using the mapping table
4. Compare output against known correct Unicode text on the same page

### Performance (No Concerns)

- Adding 11 Coptic pages increases service worker precache by ~800KB (current total ~2.3MB). Acceptable.
- Coptic Unicode (U+2C80-2CFF) is simple LTR script with no complex shaping. Renders identically to Latin in performance.
- Avva Shenouda font is only 37KB (22KB as WOFF2). No download concern.
- `ar/midnight.html` is already 440KB, confirming long prayer pages work fine.
- `backdrop-filter: blur(10px)` on sticky header may cause scroll jank on budget phones with very long Coptic pages -- monitor but don't preemptively fix.

## Acceptance Criteria

- [ ] Phase 0: Sticky subheader extracted into JS injection (all ~33 files simplified)
- [ ] Phase 0: `font-display: swap` added, TTF converted to WOFF2
- [ ] Phase 0: Phantom `en/` references cleaned up
- [ ] Phase 1: Extraction script handles both Unicode Coptic and CS legacy encoding
- [ ] Phase 1: CS-to-Unicode conversion validated against dual-encoding pages
- [ ] Phase 1: Greek liturgical phrases detected and preserved
- [ ] Phase 1: JSON output covers all prayer hours (introduction through midnight + annexes)
- [ ] Phase 2: `cop/` directory created with all 11 HTML files
- [ ] Phase 2: HTML follows exact pattern (section classes, psalm-verse, drop-cap, gospel id, ornaments)
- [ ] Phase 2: Coptic text renders correctly with Avva Shenouda font
- [ ] Phase 3: Language switching works bidirectionally (Coptic/French/Arabic)
- [ ] Phase 3: Footer, section dropdown, hour dropdown work on Coptic pages
- [ ] Phase 3: PWA caching includes Coptic pages
- [ ] Phase 4: Coptic body text CSS is readable (font-size, line-height tuned)

## Dependencies & Risks

| Risk | Impact | Mitigation |
|---|---|---|
| CS font mapping errors | Incorrect Coptic text | Validate against 20+ dual-encoding pages; use CopticChurch.net converter as reference |
| PDF column extraction fails | Mixed Coptic/French text | pdfplumber provides x-coordinates for column splitting; fallback: manual threshold tuning |
| Greek phrases wrongly converted | Garbled text | Whitelist Greek liturgical vocabulary; detect by pattern matching |
| Missing text from PDF | Incomplete prayers | Compare section count per hour against PDF table of contents |
| Subheader extraction breaks existing pages | Regression | Test all existing pages in all languages before proceeding to Coptic |
| Font rendering edge cases | Visual glitches | Test combining marks (overline/jinkim), nomina sacra; fallback to Noto Sans Coptic |

## Implementation Order

1. **Phase 0a:** Extract sticky subheader into JS (prep PR, pure refactor)
2. **Phase 0b:** Font optimization (WOFF2 + font-display: swap)
3. **Phase 0c:** Clean up phantom en/ references
4. **Phase 1:** Build CS-to-Unicode mapping table, validate against dual-encoding pages
5. **Phase 1:** Write extraction script with pdfplumber
6. **Phase 1:** Extract and validate JSON output
7. **Phase 2:** Write HTML generation script
8. **Phase 2:** Generate all 11 cop/ HTML files
9. **Phase 3:** Update agpeya.js, root index.html, sw.js, build.sh
10. **Phase 4:** CSS tuning for Coptic body text
11. **Manual review** of extracted Coptic against PDF

## Sources

- PDF source: `agpia.pdf` -- 138 pages, bilingual Coptic-French
- Author: Marian-Apollos Balastre, certified Coptic language (Institut Catholique de Paris)
- Unicode Coptic block: U+2C80-2CFF (88 pages), Greek-Coptic supplement: U+03E2-03EF
- CS Coptic legacy encoding: 58 pages use this
- Dual-encoding pages (for validation): 10, 31, 33, 43, 47, 58-60, 70, 72, 79, 81, 83, 99, 112, 121, 123, 126, 129-131
- CopticChurch.net font converter: https://www.copticchurch.net/coptic_language/fonts/convert
- pdfplumber documentation: https://github.com/jsvine/pdfplumber
- Unicode Coptic chart: https://www.unicode.org/charts/PDF/U2C80.pdf
