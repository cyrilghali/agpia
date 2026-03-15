#!/usr/bin/env python3
"""
Fix subheaders:
1. Add sticky-subheader HTML to cop/ pages (except index.html)
2. Add Coptic language link to all existing pages in fr-lsg/, fr-unofficial/, ar/
"""
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Coptic hour dropdown options
COP_HOURS = [
    ('index.html', 'Home', 'Home'),
    ('prime.html', 'Prime', 'Prime'),
    ('terce.html', 'Terce', 'Terce'),
    ('sext.html', 'Sext', 'Sext'),
    ('none.html', 'None', 'None'),
    ('vespers.html', 'Vespers', 'Vespers'),
    ('compline.html', 'Compline', 'Compline'),
    ('midnight.html', 'Midnight', 'Midnight'),
    ('veil.html', 'Veil', 'Veil'),
    ('other.html', 'Other prayers', 'Other'),
    ('about.html', 'About', 'About'),
]

def make_cop_subheader(page_name):
    """Generate the full sticky-subheader HTML for a cop/ page."""
    options = []
    for value, long_name, short_name in COP_HOURS:
        options.append(f'<option data-long="{long_name}" data-short="{short_name}" value="{value}">{long_name}</option>')
    options_html = '\n'.join(options)

    return f'''<div class="sticky-subheader">
<div class="dropdown-wrapper">
<select class="hour-dropdown" id="hourDropdown">
{options_html}
</select>
<select class="section-dropdown" id="sectionDropdown">
<option value="">Top</option>
</select>
</div>
<button class="settings-btn" id="settingsBtn"><img alt="Settings" src="../cog_wheel.png"/></button>
<div class="settings-menu" id="settingsMenu">
<!-- Font Size Row -->
<div class="settings-row">
<button class="settings-menu-btn settings-menu-btn-small" id="fontDownBtn">A-</button>
<button class="settings-menu-btn settings-menu-btn-small" id="fontResetBtn">100%</button>
<button class="settings-menu-btn settings-menu-btn-small" id="fontUpBtn">A+</button>
</div>
<!-- Line Height Row -->
<div class="settings-row">
<button class="settings-menu-btn settings-toggle" id="lineComfyBtn" title="Comfy line spacing">
<span class="line-height-icon comfy-icon">
<span class="line"></span>
<span class="line"></span>
</span>
</button>
<button class="settings-menu-btn settings-toggle active" id="lineDefaultBtn" title="Default line spacing">
<span class="line-height-icon default-icon">
<span class="line"></span>
<span class="line"></span>
</span>
</button>
<button class="settings-menu-btn settings-toggle" id="lineCondensedBtn" title="Condensed line spacing">
<span class="line-height-icon condensed-icon">
<span class="line"></span>
<span class="line"></span>
</span>
</button>
</div>
<!-- Theme Row -->
<div class="settings-row">
<button class="settings-menu-btn settings-toggle" id="autoModeBtn">Auto</button>
<button class="settings-menu-btn settings-toggle" id="lightModeBtn">Light</button>
<button class="settings-menu-btn settings-toggle active" id="darkModeBtn">Dark</button>
</div>
<!-- Language Selector -->
<div class="settings-row lang-selector">
<a class="settings-menu-btn settings-toggle" data-lang="fr" href="../fr-unofficial/{page_name}">Fran\u00e7ais</a>
<a class="settings-menu-btn settings-toggle" data-lang="ar" href="../ar/{page_name}">\u0639\u0631\u0628\u064a</a>
<a class="settings-menu-btn settings-toggle" data-lang="cop" href="../cop/{page_name}">\u2C98\u2C89\u2C99\u2CA7</a>
</div>
<div class="settings-row lang-variant-selector">
<a class="settings-menu-btn settings-toggle" data-variant="fr-unofficial" href="../fr-unofficial/{page_name}">Traduit du copte</a>
<a class="settings-menu-btn settings-toggle" data-variant="fr-lsg" href="../fr-lsg/{page_name}">Classique</a>
</div>
</div>
</div>'''


def add_subheader_to_cop_pages():
    """Add subheader HTML to cop/ pages (except index.html)."""
    cop_dir = os.path.join(BASE, 'cop')
    for fname in os.listdir(cop_dir):
        if not fname.endswith('.html') or fname == 'index.html':
            continue
        fpath = os.path.join(cop_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Skip if already has a subheader
        if 'sticky-subheader' in content:
            print(f"  SKIP cop/{fname} (already has subheader)")
            continue

        subheader = make_cop_subheader(fname)
        # Insert right after <body> (or <body class="...">)
        content = re.sub(r'(<body[^>]*>)\n', r'\1\n' + subheader + '\n', content, count=1)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ADD subheader to cop/{fname}")


def add_coptic_link_to_existing_pages():
    """Add Coptic language link to fr-lsg/, fr-unofficial/, ar/ pages."""
    coptic_link_template = '<a class="settings-menu-btn settings-toggle" data-lang="cop" href="../cop/{page}">\u2C98\u2C89\u2C99\u2CA7</a>'

    for folder in ['fr-lsg', 'fr-unofficial', 'ar']:
        folder_dir = os.path.join(BASE, folder)
        for fname in os.listdir(folder_dir):
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(folder_dir, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Skip if already has cop link
            if 'data-lang="cop"' in content:
                print(f"  SKIP {folder}/{fname} (already has Coptic link)")
                continue

            # Find the lang-selector div and add the Coptic link after the Arabic link
            cop_link = coptic_link_template.format(page=fname)
            # Insert before the closing </div> of the lang-selector section
            # The pattern: last link in lang-selector is the Arabic link, add after it
            pattern = r'(<div class="settings-row lang-selector">.*?)(</div>)'
            def add_cop_link(m):
                return m.group(1) + '\n' + cop_link + '\n' + m.group(2)
            new_content = re.sub(pattern, add_cop_link, content, count=1, flags=re.DOTALL)

            if new_content != content:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  ADD Coptic link to {folder}/{fname}")
            else:
                print(f"  WARN no lang-selector found in {folder}/{fname}")


if __name__ == '__main__':
    print("Adding subheaders to cop/ pages...")
    add_subheader_to_cop_pages()
    print("\nAdding Coptic language link to existing pages...")
    add_coptic_link_to_existing_pages()
    print("\nDone!")
