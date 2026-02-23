# AGPIA — Digital Coptic Agpeya

A web app for the Coptic Book of Hours (Agpeya), supporting multiple languages. Static HTML pages with a shared JS/CSS layer.

Live at: [agpia.app](https://agpia.app) (or equivalent deployment)

---

## Project structure

```
agpia/
├── ar/                   # Arabic locale
├── fr-lsg/               # French — Louis Segond (LSG) Bible (default French)
├── fr-unofficial/        # French — unofficial translation (locked behind flag)
├── agpeya.js             # Shared JavaScript for all HTML pages
├── agpeya-style.css      # Shared CSS
├── build.sh              # Build script — copies locales + assets into dist/
├── sw.js                 # Service worker (PWA offline support)
├── manifest.json         # Web app manifest
└── index.html            # Root redirect / landing
```

---

## Locale structure

Each locale directory (`ar/`, `fr-lsg/`, `fr-unofficial/`) contains the same set of HTML files:

| File           | Hour / content                          |
|----------------|-----------------------------------------|
| `prime.html`   | Prime (first hour, ~6 AM)               |
| `terce.html`   | Terce (third hour, ~9 AM)               |
| `sext.html`    | Sext (sixth hour, noon)                 |
| `none.html`    | None (ninth hour, ~3 PM)                |
| `vespers.html` | Vespers (eleventh hour, sunset)         |
| `compline.html`| Compline (twelfth hour, ~9 PM)          |
| `veil.html`    | Veil (before midnight)                  |
| `midnight.html`| Midnight hour (three watches)           |
| `index.html`   | Locale home — hour selection grid       |
| `about.html`   | About / info page                       |
| `other.html`   | Other prayers                           |

---

## Locale notes

- **`fr-lsg/`** is the canonical French locale (Louis Segond Bible, 1910). This is what users see by default.
- **`fr-unofficial/`** is an alternative French translation (not yet validated). It is hidden behind a `localStorage` flag (`variantUnlocked = '1'`). `agpeya.js` redirects users from `fr-unofficial/` to `fr-lsg/` if the flag is not set.

---

## HTML conventions

### Alleluia

All alleluia responses use a styled span — never italic `<em>`:

```html
<!-- Standalone response (between psalm verses) -->
<div class="prayer-text"><span class="alleluia">ALLELUIA.</span></div>

<!-- End of psalm text (inline) -->
...last line of psalm text. <span class="alleluia">ALLELUIA.</span>
```

CSS (`.alleluia` in `agpeya-style.css` ~line 761):
```css
.alleluia { color: var(--burgundy); font-weight: 700; }
```

### Gospel goto button

Each psalm section that ends before the gospel adds a jump button:

```html
<div class="psalm-verse">
    ...psalm text... <span class="alleluia">ALLELUIA.</span>
</div>
<a class="jump-gospel-btn" href="#gospel">Aller à l'évangile ↓</a>
</section>
```

The gospel section itself is marked with:
```html
<section class="section" id="gospel">
```

- **Standard hours**: button `href="#gospel"`, handled by `initJumpToGospel()` in `agpeya.js`
- **Midnight hour**: button `href="#gospel"` is dynamically rewritten by `initMidnightJumpToGospel()` to `#gospel-watch1/2/3` based on which watch the user is in

### Standalone alleluia vs. psalm-ending alleluia

| Type | Gets gospel button? |
|------|-------------------|
| Standalone (between psalms, own `<div class="prayer-text">`) | No |
| Psalm-ending (inline at end of `<div class="psalm-verse">`) | Yes |

---

## Shared assets

### `agpeya.js` — section map

| Section | Description |
|---|---|
| ACCESS GUARD | Redirects `fr-unofficial/` → `fr-lsg/` if variant not unlocked |
| LANG MIGRATION | Resets old `fr`/`fr-unofficial` localStorage lang to `fr-lsg` |
| UNOFFICIAL NOTICE | Injects a warning banner in `fr-unofficial/` pages |
| SITE FOOTER | Injects footer with credits and contact link |
| COMMON PRAYER SECTIONS | Loads shared prayer blocks (Lord's Prayer, Creed, etc.) |
| THEME AND FONT MANAGEMENT | Dark/light mode, font size, line height |
| SETTINGS MENU | Settings panel toggle, font/theme/line-height controls |
| LANGUAGE SELECTOR | Folder-based locale switching (rewrites URL path) |
| LOGO EASTER EGG | 3 clicks on logo → unlock `fr-unofficial/` |
| HOUR DROPDOWN | Short/long name toggling in hour navigation |
| SECTION DROPDOWN & SCROLL | Sticky subheader section dropdown, scroll tracking |
| `initJumpToGospel()` | Gospel button logic for standard hours |
| `initMidnightJumpToGospel()` | Gospel button logic for midnight (watch-aware) |

### `agpeya-style.css` — key classes

| Class | Purpose |
|---|---|
| `.alleluia` | Burgundy bold text for ALLELUIA responses |
| `.jump-gospel-btn` | Styled anchor button to jump to gospel section |
| `.section` | Card wrapper for each prayer block |
| `.section-title` | H2 heading inside a section (e.g., psalm name) |
| `.psalm-verse` | Individual psalm verse block |
| `.prayer-text` | Generic prose prayer text |
| `.sticky-subheader` | Sticky top bar with hour name and section dropdown |
| `.hour-header` | Page title area with crosses and hour info |
| `.doxology-coptic` | Coptic-font doxology text |

CSS custom properties (`:root`): `--bg`, `--bg-card`, `--text`, `--text-light`, `--gold`, `--burgundy`, etc. Dark theme overrides these via `[data-theme="dark"]`.

---

## Build

```bash
bash build.sh
```

Copies all locale directories and shared assets into `dist/`. No compilation step — HTML files are hand-maintained.

---

## Git hooks

Hooks live in `.githooks/` (tracked). To activate on a fresh clone:

```bash
git config core.hooksPath .githooks
```

### `pre-commit`

Automatically busts the service worker cache whenever cached assets (HTML, CSS, JS, fonts, images) are staged. Updates `sw.js` with a new random 8-char hex and adds it to the commit:

```
CACHE_NAME = 'agpeya-<random-8-char-hex>'
```

Only fires when relevant assets change — committing only markdown or other non-cached files leaves `sw.js` untouched.

---

## PWA

The app is a Progressive Web App:
- `manifest.json` defines name, icons, theme colors
- `sw.js` registers a service worker for offline caching
- `capacitor.config.json` suggests potential native app wrapping (Capacitor)
