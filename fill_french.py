#!/usr/bin/env python3
"""Fill /fr/ HTML files with French content from book.md,
preserving the exact English HTML structure."""

import os, re, sys
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = os.path.dirname(os.path.abspath(__file__))

# ===================================================================
# 1. Parse book.md
# ===================================================================

def parse_book():
    with open(os.path.join(ROOT, 'book.md'), 'r', encoding='utf-8') as f:
        text = f.read()
    sections = {}
    header_re = re.compile(r'^## (.+)$', re.MULTILINE)
    anchor_re = re.compile(r'<a\s+id="([^"]+)"\s*>\s*</a>')
    headers = list(header_re.finditer(text))
    for i, m in enumerate(headers):
        title = m.group(1).strip()
        start = m.end()
        end_pos = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        content = text[start:end_pos].strip()
        content = re.sub(r'\n---\s*(\n<a .*)?$', '', content, flags=re.DOTALL).strip()
        content = re.sub(r'\n<a\s+id="[^"]+"\s*>\s*</a>\s*$', '', content).strip()
        paragraphs = [p.strip() for p in re.split(r'\n\n+', content) if p.strip()]
        before = text[:m.start()]
        am = re.search(r'<a\s+id="([^"]+)"\s*>\s*</a>\s*$', before.rstrip())
        anchor_id = am.group(1) if am else None
        entry = {'title': title, 'paragraphs': paragraphs, 'anchor': anchor_id}
        if anchor_id:
            sections[anchor_id] = entry
        sections['t:' + title] = entry
    return sections

# ===================================================================
# 2. Psalm lookup
# ===================================================================

def build_psalm_lookup(sections):
    psalms = {}
    for key, entry in sections.items():
        title = entry.get('title', '')
        m = re.match(r'Psaume (\d+)', title)
        if not m:
            continue
        num = int(m.group(1))
        if num in psalms:
            continue
        paras = []
        for p in entry['paragraphs']:
            if p.startswith('_') and p.endswith('_') and 'Allélouia' not in p:
                continue
            if p.startswith('> '):
                continue
            paras.append(p)
        psalms[num] = paras
    return psalms

def build_psalm118_stanzas(sections):
    """Split Psalm 118 into 22 stanzas by '> Gloire à Toi, Seigneur !' markers."""
    key = 'psalm118'
    if key not in sections:
        for k, v in sections.items():
            if v.get('title') == 'Psaume 118':
                key = k
                break
    if key not in sections:
        return {}
    paras = sections[key]['paragraphs']
    stanzas = {}
    current = []
    stanza_num = 1
    for p in paras:
        if p.startswith('_') and p.endswith('_') and 'Allélouia' not in p:
            continue
        if p.startswith('> '):
            if current:
                stanzas[stanza_num] = current
                current = []
                stanza_num += 1
            continue
        current.append(p)
    if current:
        stanzas[stanza_num] = current
    return stanzas

# ===================================================================
# 3. Tropaire / litany parser
# ===================================================================

def is_coptic(p):
    return bool(re.match(r'^[\u2C80-\u2CFF\u0300-\u036F]', p))

def is_bold(p):
    return p.startswith('**') and p.endswith('**')

def parse_tropaires(paragraphs):
    litanies = []
    dox_trans = []
    current = []
    for p in paragraphs:
        if is_coptic(p):
            if current:
                litanies.append(' '.join(current))
                current = []
            continue
        if is_bold(p):
            dox_trans.append(p.strip('*').strip())
            continue
        current.append(p)
    if current:
        litanies.append(' '.join(current))
    return litanies, dox_trans

# ===================================================================
# 4. Hard-coded common section French text
# ===================================================================

INTRO_FR = [
    "Au nom du Père et du Fils et du Saint-Esprit, Un Dieu Unique ! Amen.",
    "Seigneur aie pitié, Seigneur aie pitié, Seigneur, bénis ! Amen.",
    "Gloire au Père et au Fils et au Saint-Esprit, maintenant et toujours et pour les siècles des siècles ! Amen.",
]

LORDS_PRAYER_FR = [
    ("em", "Rends-nous dignes de dire en action de grâce :"),
    ("text", "Notre Père qui es aux cieux, que Ton Nom soit sanctifié, que Ton Règne vienne, que Ta Volonté soit faite, comme au ciel, aussi sur la terre. Notre pain de demain, donne-le-nous aujourd'hui,"),
    ("text", "et remets-nous nos dettes comme nous les remettons à nos débiteurs, et ne nous induis pas en tentation, mais délivre-nous du Mal. Par le Christ Jésus, notre Seigneur, car à Toi sont le Règne, la Puissance et la Gloire, pour les siècles. Amen !"),
]

THANKSGIVING_FR = [
    "Rendons grâce au Bienfaiteur et Miséricordieux, Dieu le Père de notre Seigneur, notre Dieu et notre Sauveur Jésus-Christ parce qu'Il nous a protégés, secourus, préservés, reçus auprès de Lui, pris en pitié, aidés et amenés jusqu'à cette heure. Supplions-Le encore de nous garder en ce saint jour et tous les jours de notre vie en toute paix, Lui le Tout-Puissant, le Seigneur notre Dieu.",
    "Ô Maître, Seigneur, Dieu Tout-Puissant, Père de notre Seigneur, Dieu et Sauveur Jésus-Christ, Nous Te rendons grâce, de toute chose, pour toute chose et en toute chose, parce que c'est Toi qui nous as protégés, secourus, préservés, reçus auprès de Toi, pris en pitié, aidés et amenés jusqu'à cette heure.",
    "C'est pourquoi nous supplions et implorons Ta bonté, ô Ami du genre humain, donne-nous de parfaire ce saint jour et tous les jours de notre vie en toute paix dans Ta crainte. Toute envie, toute tentation, toute œuvre de Satan, tout conseil des hommes mauvais, tout assaut des ennemis cachés et manifestes : enlève-les de nous et de tout ton peuple et de cette église et de ce lieu saint qui est à Toi.",
    "Les choses bonnes et profitables, fournis-les-nous, car c'est Toi qui nous as donné l'autorité pour fouler aux pieds les serpents, les scorpions et toute la puissance de l'ennemi.",
    "Et ne nous induis pas en tentation, mais délivre-nous du Mal, Par la grâce, la miséricorde et l'amour du genre humain de Ton Fils Unique-Engendré notre Seigneur, Dieu et Sauveur Jésus-Christ, par Qui la gloire, l'honneur, la souveraineté et l'adoration Te sont dus avec Lui et le Saint Esprit vivifiant et de même essence que Toi, Maintenant et toujours et dans les siècles des siècles. Amen !",
]

KYRIE_FR = [
    ("em", "Que le fidèle prie :"),
    ("text", "Seigneur, entends-nous et aie pitié de nous, et pardonne-nous nos péchés. Amen."),
    ("em", "(Seigneur aie pitié) 41 fois"),
]

HOLY_HOLY_FR = [
    "Tu es Saint, Saint, Saint, Seigneur Sabaoth, le ciel et la terre sont remplis de Ta gloire et de Ton honneur ! Aie pitié de nous ô Dieu le Père Tout-Puissant. Ô Trinité Sainte, aie pitié de nous ! Ô Seigneur Dieu des puissances, sois avec nous, car nous n'avons d'aide que de Toi dans nos tribulations et nos angoisses.",
    "Ô Dieu absous, pardonne et remets nos péchés, que nous les ayons commis volontairement ou involontairement, en connaissance ou par ignorance, secrètement ou ouvertement. Ô Seigneur tu nous les pardonneras à cause de Ton saint Nom qui a été invoqué sur nous.",
    "Selon Ta miséricorde Seigneur et non selon nos péchés !",
]

CONCLUSION_FR = [
    "Ô Dieu, aie pitié de nous, Toi qui es adoré et glorifié, en tout temps et à toute heure, dans le ciel et sur la terre. Ô Christ notre Dieu bon, longanime, plein de miséricorde et abondant en compassion, Toi qui aimes les justes et qui fais miséricorde aux pécheurs (dont je suis le premier), toi qui ne veux pas la mort du pécheur mais qu'il se repente et vive. Tu appelles tout un chacun au Salut à cause de la promesse des bienfaits attendus.",
    "Ô Seigneur, reçois nos supplications en cette heure, dirige nos vies pour que nous accomplissions Tes commandements. Sanctifie nos esprits, purifie nos corps, rectifie nos pensées, purifie nos consciences, et délivre-nous de toute douleur et de toute peine. Entoure-nous de Tes saints anges, afin qu'ils nous préservent et nous guident comme par une escorte armée. Ainsi nous atteindrons l'Unité de la Foi et la connaissance de Ta Gloire intouchable (et incommensurable), car Tu es béni éternellement. Amen !",
]

CREED_FR = [
    "En vérité, nous croyons en un Dieu Unique : le Père Tout-Puissant qui a créé le ciel et la terre, les choses visibles et invisibles.",
    "Nous croyons en un Seigneur unique : Jésus-Christ le Fils de Dieu, Unique-engendré, né du Père avant tous les siècles. Lumière de Lumière, vrai Dieu né du Vrai Dieu, engendré, non pas créé, de même essence que le Père, et par qui tout est advenu.",
    "Lui qui pour nous, les humains, et pour notre Salut est descendu du ciel. Il s'est incarné par l'Esprit Saint et par la Vierge Marie et s'est fait homme. Puis il a été crucifié pour nous sous Ponce Pilate, a souffert et a été enseveli. Et il est ressuscité des morts le troisième jour conformément aux Écritures. Il est monté aux cieux et s'est assis à la droite de son Père.",
    "Et Il reviendra dans Sa gloire pour juger les vivants et les morts, et son Règne n'aura pas de fin. Oui, nous croyons en l'Esprit Saint qui est Seigneur et qui donne la vie. Il procède du Père. Avec le Père et le Fils il est adoré et glorifié. Il a parlé par les prophètes.",
    "Et en l'Église, Une, Sainte, Catholique et Apostolique. Nous professons un seul baptême pour la rémission des péchés. Nous attendons la Résurrection des morts, et la vie du siècle à venir. Amen.",
]

CREED_INTRO_FR = [
    "Nous t'exaltons ô Mère de la vraie Lumière, et nous te glorifions ô sainte Mère de Dieu, car tu as enfanté pour nous le Sauveur du monde entier. Il est venu et a sauvé nos âmes.",
    "Gloire à Toi ô notre Maître et notre Roi, le Christ : fierté des apôtres, couronne des martyrs, allégresse des justes, affermissement des Églises et rémission des péchés.",
    "Nous proclamons la Trinité sainte qui est en une Divinité unique, nous l'adorons et nous la glorifions.",
    "Seigneur fais miséricorde ! Seigneur fais miséricorde ! Seigneur bénis ! Amen !",
]

VIRGIN_FR = [
    "Salut à toi, nous te supplions, ô toi la Sainte, pleine de gloire, toujours vierge, Mère de Dieu, Mère du Christ :",
    "Fais monter notre prière vers Ton Fils bien-aimé pour qu'Il nous pardonne nos péchés.",
    "Salut à toi, qui as enfanté pour nous la Lumière véritable, le Christ, notre Dieu, ô Vierge sainte !",
    "Supplie le Seigneur pour nous afin qu'il nous fasse miséricorde à nos âmes et nous pardonne nos péchés.",
    "Ô Vierge Marie, sainte Theotokos, Protectrice, fidèle au genre humain,",
    "Intercède pour nous devant le Christ que tu as enfanté afin qu'Il nous gratifie de la rémission de nos péchés.",
    "Salut à toi, ô Vierge, Reine véritable. Salut à toi, fierté de notre race ! Tu as enfanté pour nous Emmanuel.",
    "Nous te supplions, souviens-toi de nous, ô Médiatrice fidèle, devant notre Seigneur Jésus Christ, afin qu'Il nous pardonne nos péchés.",
]

GRACIOUSLY_ACCORD_FR = [
    "Daigne, Seigneur, nous garder cette nuit sans péché. Tu es béni, Seigneur, Dieu de nos pères, et excessivement béni et glorifié est Ton Nom à jamais. Amen.",
    "Que Ta miséricorde, Seigneur, soit sur nous, selon notre espérance en Toi ; car les yeux de tous sont tournés vers Toi, et Tu leur donnes leur nourriture en temps opportun. Exauce-nous, ô Dieu, notre Sauveur, espérance de toutes les régions de la terre. Et Toi, Seigneur, garde-nous de cette génération et pour toujours. Amen.",
    "Tu es béni, Seigneur, enseigne-moi Tes ordonnances. Tu es béni, Seigneur, fais-moi comprendre Tes commandements. Tu es béni, Seigneur, éclaire-moi de Ta justice. Ta miséricorde, Seigneur, dure à jamais. Ne dédaigne pas, Seigneur, les œuvres de Tes mains. Tu as été mon refuge de génération en génération.",
    "J'ai dit : Seigneur, aie pitié de moi, guéris mon âme, car j'ai péché contre Toi. Seigneur, je me suis réfugié en Toi, sauve-moi et enseigne-moi à faire Ta volonté, car Tu es mon Dieu, et auprès de Toi est la source de la vie. Dans Ta lumière nous verrons la lumière.",
    "Que Ta miséricorde s'étende sur ceux qui Te connaissent, et Ta justice sur les cœurs droits. À Toi la bénédiction. À Toi la louange. À Toi la gloire, ô Père, Fils et Saint-Esprit, de tout temps, maintenant et pour les siècles des siècles. Amen.",
    "Il est bon de confesser le Seigneur et de chanter des louanges à Ton Nom, ô Très-Haut ; de proclamer Ta miséricorde chaque matin et Ta fidélité chaque nuit.",
]

GOSPEL_DOX_FR = "Nous t'adorons ô Christ avec ton Père qui est bon et le Saint-Esprit, car tu es venu et tu nous as sauvés. Fais-nous miséricorde !"

PSALMS_INTRO_FR = "Psaume de David le Prophète, que sa sainte bénédiction soit avec nous, Amen."

HOUR_INTRO_FR = {
    'prime':    "Hymne de l'aube du jour béni, je l'offre au Christ mon Roi et mon Dieu, j'espérerai en Lui afin qu'il me remette mes péchés.",
    'terce':    "Hymne de la troisième heure du jour béni, je l'offre au Christ mon Roi et mon Dieu, j'espérerai en Lui afin qu'il me remette mes péchés.",
    'sext':     "Hymne de la sixième heure du jour béni, je l'offre au Christ mon Roi et mon Dieu, j'espérerai en Lui afin qu'il me remette mes péchés.",
    'none':     "Hymne de la neuvième heure du jour béni, je l'offre au Christ mon Roi et mon Dieu, j'espérerai en Lui afin qu'il me remette mes péchés.",
    'vespers':  "Hymne des Vêpres du jour béni, je l'offre au Christ mon Roi et mon Dieu, j'espérerai en Lui afin qu'il me remette mes péchés.",
    'compline': "Hymne des Complies du jour béni, je l'offre au Christ mon Roi et mon Dieu, j'espérerai en Lui afin qu'il me remette mes péchés.",
    'veil':     "Hymne de la fermeture du Voile du jour béni, je l'offre au Christ mon Roi et mon Dieu, j'espérerai en Lui afin qu'il me remette mes péchés.",
    'midnight-1': "Hymne du premier service béni, je l'offre au Christ mon Roi et mon Dieu, j'espérerai en Lui afin qu'il me remette mes péchés.",
    'midnight-2': "Hymne du deuxième service béni, je l'offre au Christ mon Roi et mon Dieu, j'espérerai en Lui afin qu'il me remette mes péchés.",
    'midnight-3': "Hymne du troisième service béni, je l'offre au Christ mon Roi et mon Dieu, j'espérerai en Lui afin qu'il me remette mes péchés.",
}

LET_MY_SUPPLICATION_FR = [
    "Que ma supplication arrive devant Toi, Seigneur ; donne-moi l'intelligence selon Ta parole. Que ma requête arrive devant Toi ; vivifie-moi selon Ta parole. Que mes lèvres profèrent Ta louange, car Tu m'as enseigné Tes ordonnances. Que ma langue proclame Tes paroles, car tous Tes commandements sont justes. Que Ta main soit mon salut, car j'ai désiré Tes commandements. J'ai désiré ardemment Ton salut, Seigneur, et Ta loi est ma méditation. Mon âme vivra et Te louera, et Tes jugements m'aideront. J'ai erré comme une brebis perdue ; cherche Ton serviteur, car je n'ai point oublié Tes commandements.",
    "Gloire au Père et au Fils et au Saint-Esprit, maintenant et toujours et pour les siècles des siècles ! Amen.",
    "Gloire au Père et au Fils et au Saint-Esprit, maintenant et toujours et pour les siècles des siècles ! Amen.",
    "Gloire à Toi ô Toi le bon et l'ami du genre humain ! Salut à Ta mère la Vierge et à tous Tes saints. Gloire à Toi, Sainte Trinité, aie pitié de nous !",
    "Que Dieu se lève et que Ses ennemis soient dispersés ; et que tous ceux qui haïssent Son saint Nom fuient devant Sa Face. Mais que Ton peuple soit dans la bénédiction, des milliers de milliers et des myriades de myriades, faisant Ta volonté. Seigneur, Tu ouvriras mes lèvres, et ma bouche proclamera Ta louange. Amen !",
]

# ===================================================================
# 5. HTML replacement helpers
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
    """Combine many paragraphs into exactly n groups, joined by spaces."""
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

def split_text(text, n):
    """Split a single long text into n parts at sentence boundaries."""
    if n <= 1:
        return [text]
    sentences = re.split(r'(?<=[.!?»"])\s+', text)
    if len(sentences) <= n:
        return sentences + [''] * (n - len(sentences))
    return distribute(sentences, n)

def replace_psalm(section_el, fr_paras):
    divs = section_el.find_all('div', class_='psalm-verse')
    if not divs or not fr_paras:
        return
    paras = [re.sub(r'\s*_?Allélouia\s*!?\s*_?\s*$', '', p).strip() for p in fr_paras]
    paras = [p for p in paras if p]
    if len(paras) > len(divs):
        paras = distribute(paras, len(divs))
    for i, div in enumerate(divs):
        if i >= len(paras):
            break
        fp = paras[i]
        has_alleluia = div.find('span', class_='alleluia')
        is_last = (i == len(divs) - 1)
        div.clear()
        div.append(NavigableString(SP + fp + ' '))
        if has_alleluia or is_last:
            al = Tag(name='span')
            al['class'] = ['alleluia']
            al.string = 'ALLELUIA.'
            div.append(al)
        div.append(NavigableString(SP_END))

def replace_prayer(section_el, fr_paras, skip_doxology=True):
    divs = []
    for d in section_el.find_all('div', class_='prayer-text'):
        if skip_doxology and 'doxology' in d.get('class', []):
            continue
        divs.append(d)
    plain = [p for p in fr_paras if not isinstance(p, tuple)]
    if not any(isinstance(p, tuple) for p in fr_paras):
        if len(plain) > len(divs):
            fr_paras = distribute(fr_paras, len(divs))
        elif len(plain) < len(divs) and len(plain) == 1:
            fr_paras = split_text(plain[0], len(divs))
    for i, div in enumerate(divs):
        if i >= len(fr_paras):
            break
        fp = fr_paras[i]
        if isinstance(fp, tuple):
            kind, txt = fp
            if kind == 'em':
                set_em(div, txt)
            else:
                set_text(div, txt)
        else:
            em_child = div.find('em')
            if em_child and len(list(div.children)) <= 2:
                set_em(div, fp.strip('_').strip())
            else:
                set_text(div, fp)

def replace_litanies(section_el, lits_fr, dox_fr):
    lit_idx = 0
    dox_idx = 0
    for div in section_el.find_all('div', class_='prayer-text'):
        classes = div.get('class', [])
        if 'doxology' in classes:
            eng = div.find('span', class_='doxology-english')
            if eng and dox_idx < len(dox_fr):
                eng.string = dox_fr[dox_idx]
                dox_idx += 1
        else:
            num = div.find('span', class_='litany-number')
            if num and lit_idx < len(lits_fr):
                num_html = str(num)
                div.clear()
                div.append(BeautifulSoup(num_html, 'html.parser'))
                div.append(NavigableString(' ' + lits_fr[lit_idx]))
                lit_idx += 1

def replace_gospel(section_el, fr_paras):
    intro_text = None
    body = []
    outro_text = "Gloire à toi Seigneur !"
    for p in fr_paras:
        if p.startswith('_') and p.endswith('_'):
            stripped = p.strip('_').strip()
            if not intro_text and not body:
                intro_text = stripped
            elif 'Gloire à toi' in stripped and len(stripped) < 80:
                outro_text = stripped
        else:
            body.append(p)

    verse_divs = section_el.find_all('div', class_='psalm-verse')
    if body and len(body) < len(verse_divs):
        body = split_text(' '.join(body), len(verse_divs))

    divs = list(section_el.find_all('div'))
    body_idx = 0
    for div in divs:
        classes = div.get('class', [])
        if 'doxology' in classes:
            eng = div.find('span', class_='doxology-english')
            if eng:
                eng.string = GOSPEL_DOX_FR
            continue
        em_child = div.find('em')
        if em_child and 'psalm-verse' not in classes:
            txt = div.get_text(strip=True)
            if intro_text and ('Glory' in txt or 'Holy' in txt or 'reading' in txt.lower()):
                set_em(div, intro_text)
            elif 'Glory to God forever' in txt or 'glory' in txt.lower()[:20]:
                set_text(div, outro_text)
            continue
        if 'psalm-verse' in classes:
            if body_idx < len(body):
                div.clear()
                div.append(NavigableString(SP + body[body_idx] + SP_END))
                body_idx += 1
            continue
        txt = div.get_text(strip=True)
        if 'Glory to God forever' in txt:
            set_text(div, outro_text)

# ===================================================================
# 6. Main section dispatcher
# ===================================================================

def process_section(section_el, title, sections, psalms, p118_stanzas, hour_config, watch_state=None):
    pm = re.match(r'Psalm (\d+)(?:\s*\(([IVXLC]+)\))?', title)
    if pm:
        num = int(pm.group(1))
        roman = pm.group(2)
        if num == 118 and roman:
            rom_map = {'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8,'IX':9,'X':10,
                       'XI':11,'XII':12,'XIII':13,'XIV':14,'XV':15,'XVI':16,'XVII':17,'XVIII':18,
                       'XIX':19,'XX':20,'XXI':21,'XXII':22}
            sn = rom_map.get(roman, 0)
            if sn in p118_stanzas:
                replace_psalm(section_el, p118_stanzas[sn])
        elif num in psalms:
            replace_psalm(section_el, psalms[num])
        return

    # Common sections
    if title == 'Introduction to Every Hour':
        replace_prayer(section_el, INTRO_FR)
        return
    if title == "The Lord's Prayer":
        replace_prayer(section_el, LORDS_PRAYER_FR)
        return
    if title == 'The Prayer of Thanksgiving':
        replace_prayer(section_el, THANKSGIVING_FR)
        return
    if title == '41 Kyrie Eleison':
        replace_prayer(section_el, KYRIE_FR)
        return
    if title == 'Holy Holy Holy':
        replace_prayer(section_el, HOLY_HOLY_FR)
        return
    if title == 'Conclusion of Every Hour':
        replace_prayer(section_el, CONCLUSION_FR)
        return
    if title == 'The Orthodox Creed':
        replace_prayer(section_el, CREED_FR)
        return
    if title == 'Introduction to the Creed':
        replace_prayer(section_el, CREED_INTRO_FR)
        return
    if title in ('Hail to Saint Mary', 'Hail to You'):
        replace_prayer(section_el, VIRGIN_FR)
        return
    if title == 'Graciously Accord, O Lord':
        replace_prayer(section_el, GRACIOUSLY_ACCORD_FR)
        return
    if title == 'The Faith of the Church':
        key = 'dawn-faith'
        if key not in sections:
            for k, v in sections.items():
                if 'foi' in v.get('title', '').lower():
                    key = k
                    break
        if key in sections:
            replace_prayer(section_el, sections[key]['paragraphs'])
        return
    if title == 'Let My Supplication':
        replace_prayer(section_el, LET_MY_SUPPLICATION_FR)
        return
    if title in ('The First Watch', 'The Second Watch', 'The Third Watch'):
        return

    # Hour-specific via config
    cfg = hour_config.get(title)
    if not cfg and title.startswith('The Holy Gospel'):
        for k, v in hour_config.items():
            if k.startswith('The Holy Gospel'):
                cfg = v
                break
    if not cfg and title == 'Litanies' and watch_state:
        cfg = watch_state.get('litany')
    if not cfg and title == 'Litanies':
        cfg = hour_config.get('Litanies')

    if cfg:
        kind = cfg.get('type', 'prayer')
        sec_key = cfg['key']
        if sec_key == '__hardcoded__':
            replace_prayer(section_el, cfg['text'])
            return
        sec_data = sections.get(sec_key)
        if not sec_data:
            print(f"    WARN: key '{sec_key}' not found for '{title}'")
            return
        paras = sec_data['paragraphs']
        if kind == 'gospel':
            replace_gospel(section_el, paras)
        elif kind == 'litany':
            lits, doxs = parse_tropaires(paras)
            replace_litanies(section_el, lits, doxs)
        else:
            replace_prayer(section_el, paras)
        return

# ===================================================================
# 7. Per-hour configs
# ===================================================================

CONFIGS = {
    'prime': {
        'Come Let Us Kneel Down': {'key': 'dawn', 'type': 'prayer'},
        'The Pauline Epistle (Ephesians 4:1-5)': {'key': 'dawn-epistle', 'type': 'prayer'},
        'The Faith of the Church': {'key': 'dawn-faith', 'type': 'prayer'},
        'The Holy Gospel According to Saint John (1:1-17)': {'key': 'dawn-gospel', 'type': 'gospel'},
        'Litanies': {'key': 'dawn-oraisons', 'type': 'litany'},
        'The Gloria': {'key': 'dawn-angels-praise', 'type': 'prayer'},
        'The Trisagion': {'key': 'dawn-trisagion', 'type': 'prayer'},
        'First Absolution': {'key': 'dawn-absolution', 'type': 'prayer'},
        'Second Absolution': {'key': 'dawn-absolution-2', 'type': 'prayer'},
    },
    'terce': {
        'The Holy Gospel (John 14:26-31 & 15:1-4)': {'key': 'third-hour-gospel', 'type': 'gospel'},
        'Litanies': {'key': 'third-hour-oraisons', 'type': 'litany'},
        'Absolution': {'key': 'third-hour-absolution', 'type': 'prayer'},
    },
    'sext': {
        'The Holy Gospel (Matthew 5:1-16)': {'key': 'sixth-hour-gospel', 'type': 'gospel'},
        'Litanies': {'key': 'sixth-hour-oraisons', 'type': 'litany'},
        'Absolution': {'key': 'sixth-hour-absolution', 'type': 'prayer'},
    },
    'none': {
        'The Holy Gospel (Luke 9:10-17)': {'key': 'ninth-hour-gospel', 'type': 'gospel'},
        'Litanies': {'key': 'ninth-hour-oraisons', 'type': 'litany'},
        'Absolution': {'key': 'ninth-hour-absolution', 'type': 'prayer'},
    },
    'vespers': {
        'The Holy Gospel (Luke 4:38-41)': {'key': 'eleventh-hour-gospel', 'type': 'gospel'},
        'Litanies': {'key': 'eleventh-hour-oraisons', 'type': 'litany'},
        'Absolution': {'key': 'eleventh-hour-absolution', 'type': 'prayer'},
    },
    'compline': {
        'The Holy Gospel (St. Luke 2:25-32)': {'key': 'twelfth-hour-gospel', 'type': 'gospel'},
        'Litanies': {'key': 'twelfth-hour-oraisons', 'type': 'litany'},
        'The Trisagion': {'key': 'dawn-trisagion', 'type': 'prayer'},
        'Absolution': {'key': 'twelfth-hour-absolution', 'type': 'prayer'},
    },
    'veil': {
        'The Holy Gospel (John 6:15-23)': {'key': 'veil', 'type': 'gospel'},
        'Litanies': {'key': 'veil-oraisons', 'type': 'litany'},
        'The Trisagion': {'key': 'dawn-trisagion', 'type': 'prayer'},
        'Absolution': {'key': 'veil-absolution', 'type': 'prayer'},
    },
}

# ===================================================================
# 8. Process a standard hour file
# ===================================================================

GLOBAL_EM_REPLACEMENTS = {
    'The worshipper says:': 'Le fidèle dit :',
    'The following psalms are selected from the 1st hour:': 'Les psaumes suivants sont extraits de la 1ère heure :',
    'The following psalms are selected from the 3rd hour:': 'Les psaumes suivants sont extraits de la 3ème heure :',
    'The following psalms are selected from the 6th hour:': 'Les psaumes suivants sont extraits de la 6ème heure :',
    'The following psalms are selected from the 9th hour:': 'Les psaumes suivants sont extraits de la 9ème heure :',
    'The following psalms are selected from Vespers:': 'Les psaumes suivants sont extraits des Vêpres :',
    'The following psalms are selected from Compline:': 'Les psaumes suivants sont extraits des Complies :',
    'The following psalms are selected from Midnight:': 'Les psaumes suivants sont extraits de Minuit :',
}

GLOBAL_TEXT_REPLACEMENTS = {
    'Glory be to God forever. Amen.': 'Gloire à Dieu pour les siècles des siècles. Amen.',
    'Glory to God forever. Amen.': 'Gloire à Dieu pour les siècles des siècles. Amen.',
}

GLOBAL_DOX_REPLACEMENTS = {
    'Glory to You, the Lover of mankind.': 'Gloire à Toi, ami du genre humain !',
}

def global_replacements(soup):
    for div in soup.find_all('div', class_='prayer-text'):
        txt = div.get_text(strip=True)
        for eng, fra in GLOBAL_EM_REPLACEMENTS.items():
            if eng in txt:
                set_em(div, fra)
                break
        for eng, fra in GLOBAL_TEXT_REPLACEMENTS.items():
            if txt.strip() == eng:
                set_text(div, fra)
                break
        eng_span = div.find('span', class_='doxology-english')
        if eng_span:
            span_txt = eng_span.get_text(strip=True)
            for eng, fra in GLOBAL_DOX_REPLACEMENTS.items():
                if eng in span_txt:
                    eng_span.string = fra
                    break

def replace_hour_intros(soup, hour_name):
    """Replace the 'beseeching Him to forgive' and 'From the Psalms' sections."""
    hymn = HOUR_INTRO_FR.get(hour_name)
    if not hymn:
        return
    for sec in soup.find_all('section', class_='section'):
        for div in sec.find_all('div', class_='prayer-text'):
            txt = div.get_text(strip=True)
            if 'beseeching Him to forgive' in txt or 'beseeching him to forgive' in txt.lower():
                set_em(div, hymn)
            elif 'From the Psalms of our father David' in txt:
                set_em(div, PSALMS_INTRO_FR)

def process_hour(en_path, fr_path, sections, psalms, p118, hour_config, hour_name=None):
    with open(en_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = 'fr'
    for sec in soup.find_all('section', class_='section'):
        h2 = sec.find('h2', class_='section-title')
        if not h2:
            continue
        title = h2.get_text(strip=True)
        process_section(sec, title, sections, psalms, p118, hour_config)
    if hour_name:
        replace_hour_intros(soup, hour_name)
    global_replacements(soup)
    with open(fr_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"  Wrote {os.path.basename(fr_path)}")

# ===================================================================
# 9. Process midnight (special: 3 watches with repeated titles)
# ===================================================================

MIDNIGHT_WATCH_GOSPELS = {
    1: 'midnight-first-gospel',
    2: 'midnight-second-gospel',
    3: 'midnight-third-gospel',
}
MIDNIGHT_WATCH_LITANIES = {
    1: 'midnight-first-oraisons',
    2: 'midnight-second-oraisons',
    3: 'midnight-third-oraisons',
}

def process_midnight(en_path, fr_path, sections, psalms, p118):
    with open(en_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = 'fr'

    config = {
        'Opening Prayer': {'key': 'midnight', 'type': 'prayer'},
    }
    watch = 0
    canticle_done = False

    for sec in soup.find_all('section', class_='section'):
        h2 = sec.find('h2', class_='section-title')
        if not h2:
            continue
        title = h2.get_text(strip=True)

        if title == 'The First Watch':
            watch = 1
            continue
        if title == 'The Second Watch':
            watch = 2
            continue
        if title == 'The Third Watch':
            watch = 3
            continue

        ws = None
        if watch > 0:
            if title.startswith('The Holy Gospel'):
                if watch == 3 and 'Luke 2:29' in title:
                    ws = None
                    process_section(sec, title, sections, psalms, p118, {
                        title: {'key': 'midnight-canticle-simeon', 'type': 'gospel'}
                    })
                    canticle_done = True
                    continue
                else:
                    gk = MIDNIGHT_WATCH_GOSPELS.get(watch)
                    if gk:
                        process_section(sec, title, sections, psalms, p118, {
                            title: {'key': gk, 'type': 'gospel'}
                        })
                        continue
            if title == 'Litanies':
                lk = MIDNIGHT_WATCH_LITANIES.get(watch)
                if lk:
                    ws = {'litany': {'key': lk, 'type': 'litany'}}
            if title == 'Absolution':
                process_section(sec, title, sections, psalms, p118, {
                    'Absolution': {'key': 'midnight-absolution', 'type': 'prayer'}
                })
                continue

        process_section(sec, title, sections, psalms, p118, config, ws)

    for sec in soup.find_all('section', class_='section'):
        for div in sec.find_all('div', class_='prayer-text'):
            txt = div.get_text(strip=True)
            if 'beseeching Him to forgive' in txt or 'beseeching him to forgive' in txt.lower():
                if 'first watch' in txt.lower():
                    set_em(div, HOUR_INTRO_FR['midnight-1'])
                elif 'second watch' in txt.lower():
                    set_em(div, HOUR_INTRO_FR['midnight-2'])
                elif 'third watch' in txt.lower():
                    set_em(div, HOUR_INTRO_FR['midnight-3'])
            elif 'From the Psalms of our father David' in txt:
                set_em(div, PSALMS_INTRO_FR)

    global_replacements(soup)
    with open(fr_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"  Wrote midnight.html")

# ===================================================================
# 10. Process other.html
# ===================================================================

OTHER_MAP = {
    'Prayer Before Confession': 'prayer-before-confession',
    'Prayer After Confession': 'prayer-after-confession',
    'Prayer Before Communion 1': 'prayer-before-communion',
    'Prayer Before Communion 2': 'prayer-before-communion-2',
    'Prayer After Communion 1': 'prayer-after-communion',
    'Prayer After Communion 2': 'prayer-after-communion-2',
    'Prayer Before Meals 1': 'prayer-before-meal',
    'Prayer Before Meals 2': 'prayer-guidance',
    'Prayer After Meals': 'prayer-closing',
    'Prayer Before Studying': 'prayer-before-studying',
    'Prayer After Studying': 'prayer-after-studying',
}

def process_other(en_path, fr_path, sections):
    with open(en_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = 'fr'
    for sec in soup.find_all('section', class_='section'):
        h2 = sec.find('h2', class_='section-title')
        if not h2:
            continue
        title = h2.get_text(strip=True)
        key = OTHER_MAP.get(title)
        if key and key in sections:
            replace_prayer(sec, sections[key]['paragraphs'])
    global_replacements(soup)
    with open(fr_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"  Wrote other.html")

# ===================================================================
# 11. Main
# ===================================================================

def main():
    print("Parsing book.md...")
    sections = parse_book()
    psalms = build_psalm_lookup(sections)
    p118 = build_psalm118_stanzas(sections)
    print(f"  {len(sections)} sections, {len(psalms)} psalms, {len(p118)} Psalm-118 stanzas")

    os.makedirs(os.path.join(ROOT, 'fr'), exist_ok=True)

    for hour in ['prime', 'terce', 'sext', 'none', 'vespers', 'compline', 'veil']:
        en = os.path.join(ROOT, 'en', f'{hour}.html')
        fr = os.path.join(ROOT, 'fr', f'{hour}.html')
        if not os.path.exists(en):
            print(f"  SKIP {hour}")
            continue
        print(f"Processing {hour}...")
        process_hour(en, fr, sections, psalms, p118, CONFIGS.get(hour, {}), hour_name=hour)

    mn_en = os.path.join(ROOT, 'en', 'midnight.html')
    mn_fr = os.path.join(ROOT, 'fr', 'midnight.html')
    if os.path.exists(mn_en):
        print("Processing midnight...")
        process_midnight(mn_en, mn_fr, sections, psalms, p118)

    ot_en = os.path.join(ROOT, 'en', 'other.html')
    ot_fr = os.path.join(ROOT, 'fr', 'other.html')
    if os.path.exists(ot_en):
        print("Processing other...")
        process_other(ot_en, ot_fr, sections)

    for name in ['index.html', 'about.html']:
        src = os.path.join(ROOT, 'en', name)
        dst = os.path.join(ROOT, 'fr', name)
        if os.path.exists(src):
            with open(src, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            ht = soup.find('html')
            if ht:
                ht['lang'] = 'fr'
            with open(dst, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"  Wrote {name}")

    print("\nDone!")

if __name__ == '__main__':
    main()
