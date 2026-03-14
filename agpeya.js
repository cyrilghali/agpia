// Agpeya JavaScript - Common functionality for all prayer hours
// This file contains all shared JavaScript to reduce file sizes

// ============================================================================
// ACCESS GUARD — redirect fr-unofficial to fr-lsg if variant not unlocked
// ============================================================================

(function guardFrUnofficial() {
    if (window.location.pathname.includes('/fr-unofficial/')) {
        try {
            if (localStorage.getItem('variantUnlocked') !== '1') {
                window.location.replace(
                    window.location.pathname.replace('/fr-unofficial/', '/fr-lsg/')
                );
            }
        } catch(e) {
            window.location.replace(
                window.location.pathname.replace('/fr-unofficial/', '/fr-lsg/')
            );
        }
    }
})();

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js');
    navigator.serviceWorker.addEventListener('controllerchange', () => {
        window.location.reload();
    });
}

// ============================================================================
// LANG MIGRATION — reset old French variants to fr-lsg
// ============================================================================

(function migrateLang() {
    try {
        var _l = localStorage.getItem('lang');
        if ((_l === 'fr' || _l === 'fr-unofficial') && localStorage.getItem('variantUnlocked') !== '1') localStorage.setItem('lang', 'fr-lsg');
    } catch(e) {}
})();

// ============================================================================
// STICKY SUBHEADER (injected via JS, like the footer)
// ============================================================================

(function injectSubheader() {
    var lang = document.documentElement.lang || 'en';
    var path = window.location.pathname;

    // Determine current folder
    var folders = ['fr-lsg', 'fr-unofficial', 'ar', 'cop'];
    var currentFolder = '';
    for (var i = 0; i < folders.length; i++) {
        if (path.indexOf('/' + folders[i] + '/') !== -1) { currentFolder = folders[i]; break; }
    }
    if (!currentFolder) return; // Not inside a language folder — skip injection (e.g. root index.html)

    var currentPage = path.split('/').pop() || 'index.html';

    // ---- Localized data ----
    var subheaderI18n = {
        'fr-lsg': {
            hours: [
                { value: 'index.html', long: 'Accueil', short: 'Accueil' },
                { value: 'prime.html', long: "Pri\u00e8re de l'aube", short: '1\u00e8re Heure' },
                { value: 'terce.html', long: 'Pri\u00e8re de la troisi\u00e8me heure', short: '3\u00e8me Heure' },
                { value: 'sext.html', long: 'Pri\u00e8re de la sixi\u00e8me heure', short: '6\u00e8me Heure' },
                { value: 'none.html', long: 'Pri\u00e8re de la neuvi\u00e8me heure', short: '9\u00e8me Heure' },
                { value: 'vespers.html', long: 'Pri\u00e8re de la onzi\u00e8me heure', short: '11\u00e8me Heure' },
                { value: 'compline.html', long: 'Pri\u00e8re de la douzi\u00e8me heure', short: '12\u00e8me Heure' },
                { value: 'midnight.html', long: 'Pri\u00e8re de minuit', short: 'Minuit' },
                { value: 'veil.html', long: 'Pri\u00e8re de la fermeture du voile', short: 'Voile' },
                { value: 'other.html', long: 'Pri\u00e8res diverses', short: 'Autres' },
                { value: 'about.html', long: '\u00c0 propos', short: '\u00c0 propos' }
            ],
            topLabel: 'Haut',
            themeLight: 'Clair',
            themeDark: 'Sombre',
            lineComfyTitle: 'Interligne confortable',
            lineDefaultTitle: 'Interligne standard',
            lineCondensedTitle: 'Interligne condens\u00e9'
        },
        'fr-unofficial': {
            hours: [
                { value: 'index.html', long: 'Accueil', short: 'Accueil' },
                { value: 'prime.html', long: '1\u00e8re Heure - Prime', short: '1\u00e8re Heure' },
                { value: 'terce.html', long: '3\u00e8me Heure - Tierce', short: '3\u00e8me Heure' },
                { value: 'sext.html', long: '6\u00e8me Heure - Sexte', short: '6\u00e8me Heure' },
                { value: 'none.html', long: '9\u00e8me Heure - None', short: '9\u00e8me Heure' },
                { value: 'vespers.html', long: '11\u00e8me Heure - V\u00eapres', short: '11\u00e8me Heure' },
                { value: 'compline.html', long: '12\u00e8me Heure - Complies', short: '12\u00e8me Heure' },
                { value: 'midnight.html', long: 'Minuit', short: 'Minuit' },
                { value: 'veil.html', long: 'Pri\u00e8re du Voile', short: 'Voile' },
                { value: 'other.html', long: 'Pri\u00e8res diverses', short: 'Autres' },
                { value: 'about.html', long: '\u00c0 propos', short: '\u00c0 propos' }
            ],
            topLabel: 'Haut',
            themeLight: 'Clair',
            themeDark: 'Sombre',
            lineComfyTitle: 'Interligne confortable',
            lineDefaultTitle: 'Interligne standard',
            lineCondensedTitle: 'Interligne condens\u00e9'
        },
        ar: {
            hours: [
                { value: 'index.html', long: '\u0627\u0644\u0631\u0626\u064a\u0633\u064a\u0629', short: '\u0627\u0644\u0631\u0626\u064a\u0633\u064a\u0629' },
                { value: 'prime.html', long: '\u0627\u0644\u0633\u0627\u0639\u0629 \u0627\u0644\u0623\u0648\u0644\u0649 - \u0628\u0627\u0643\u0631', short: '\u0627\u0644\u0633\u0627\u0639\u0629 \u0661' },
                { value: 'terce.html', long: '\u0627\u0644\u0633\u0627\u0639\u0629 \u0627\u0644\u062b\u0627\u0644\u062b\u0629', short: '\u0627\u0644\u0633\u0627\u0639\u0629 \u0663' },
                { value: 'sext.html', long: '\u0627\u0644\u0633\u0627\u0639\u0629 \u0627\u0644\u0633\u0627\u062f\u0633\u0629', short: '\u0627\u0644\u0633\u0627\u0639\u0629 \u0666' },
                { value: 'none.html', long: '\u0627\u0644\u0633\u0627\u0639\u0629 \u0627\u0644\u062a\u0627\u0633\u0639\u0629', short: '\u0627\u0644\u0633\u0627\u0639\u0629 \u0669' },
                { value: 'vespers.html', long: '\u0627\u0644\u0633\u0627\u0639\u0629 \u0627\u0644\u062d\u0627\u062f\u064a\u0629 \u0639\u0634\u0631 - \u0627\u0644\u063a\u0631\u0648\u0628', short: '\u0627\u0644\u0633\u0627\u0639\u0629 \u0661\u0661' },
                { value: 'compline.html', long: '\u0627\u0644\u0633\u0627\u0639\u0629 \u0627\u0644\u062b\u0627\u0646\u064a\u0629 \u0639\u0634\u0631 - \u0627\u0644\u0646\u0648\u0645', short: '\u0627\u0644\u0633\u0627\u0639\u0629 \u0661\u0662' },
                { value: 'midnight.html', long: '\u0646\u0635\u0641 \u0627\u0644\u0644\u064a\u0644', short: '\u0646\u0635\u0641 \u0627\u0644\u0644\u064a\u0644' },
                { value: 'veil.html', long: '\u0635\u0644\u0627\u0629 \u0627\u0644\u0633\u062a\u0627\u0631', short: '\u0627\u0644\u0633\u062a\u0627\u0631' },
                { value: 'other.html', long: '\u0635\u0644\u0648\u0627\u062a \u0623\u062e\u0631\u0649', short: '\u0623\u062e\u0631\u0649' },
                { value: 'about.html', long: '\u0639\u0646 \u0627\u0644\u0623\u062c\u0628\u064a\u0629', short: '\u0639\u0646' }
            ],
            topLabel: '\u0623\u0639\u0644\u0649',
            themeLight: '\u0641\u0627\u062a\u062d',
            themeDark: '\u062f\u0627\u0643\u0646',
            lineComfyTitle: 'Comfy line spacing',
            lineDefaultTitle: 'Default line spacing',
            lineCondensedTitle: 'Condensed line spacing'
        },
        cop: {
            hours: [
                { value: 'index.html', long: 'Home', short: 'Home' },
                { value: 'prime.html', long: '\u2C90\u2C91\u2C80\u2CA5\u2C89\u2CA9\u2CAD\u2C8F \u2C9B\u2CA7\u2C89 \u2CAF\u2C93\u2C81\u2CA9 \u2C9B\u2CB3\u2C99\u2CA1\u2C90', short: 'Prime' },
                { value: 'terce.html', long: '\u2C90\u2C91\u2C80\u2CA5\u2C89\u2CA9\u2CAD\u2C8F \u2C9B\u2CA7\u2C89 \u2CAF\u2C93\u2C81\u2CA9 \u2C9C\u2C9C\u2C81\u2CB1\u2CB3\u2C99\u2CA7', short: 'Terce' },
                { value: 'sext.html', long: '\u2C90\u2C91\u2C80\u2CA5\u2C89\u2CA9\u2CAD\u2C8F \u2C9B\u2CA7\u2C89 \u2CAF\u2C93\u2C81\u2CA9 \u2C9C\u2C9C\u2C81\u2CB1\u2CA5\u2C9F\u2C9F\u2CA9', short: 'Sext' },
                { value: 'none.html', long: '\u2C90\u2C91\u2C80\u2CA5\u2C89\u2CA9\u2CAD\u2C8F \u2C9B\u2CA7\u2C89 \u2CAF\u2C93\u2C81\u2CA9 \u2C9C\u2C9C\u2C81\u2CB1\u2CB0\u2C93\u2CA5', short: 'None' },
                { value: 'vespers.html', long: '\u2C90\u2C91\u2C80\u2CA5\u2C89\u2CA9\u2CAD\u2C8F \u2C9B\u2CA7\u2C89 \u2CAF\u2C93\u2C81\u2CA9 \u2C9B\u2CA1\u2C9F\u2CA9\u2CB1\u2C93', short: 'Vespers' },
                { value: 'compline.html', long: '\u2C90\u2C91\u2C80\u2CA5\u2C89\u2CA9\u2CAD\u2C8F \u2C9B\u2CA7\u2C89 \u2CAF\u2C93\u2C81\u2CA9 \u2C9B\u2C89\u2C9B\u2C95\u2C9F\u2CA7', short: 'Compline' },
                { value: 'midnight.html', long: '\u2C90\u2C91\u2C80\u2CA5\u2C89\u2CA9\u2CAD\u2C8F \u2C9B\u2CA7\u2C89 \u2CAF\u2C93\u2C81\u2CA9 \u2C9B\u2C89\u2CB4\u2CA3\u2CA1\u2CB1', short: 'Midnight' },
                { value: 'veil.html', long: '\u2C90\u2C91\u2C80\u2CA5\u2C89\u2CA9\u2CAD\u2C8F \u2C9B\u2CA7\u2C89 \u2C90\u2C93\u2C95\u2C81\u2CA7\u2C81\u2C90\u2C89\u2CA7\u2C81\u2CA5\u2C9C\u2C81', short: 'Veil' },
                { value: 'other.html', long: 'Other prayers', short: 'Other' },
                { value: 'about.html', long: 'About', short: 'About' }
            ],
            topLabel: 'Top',
            themeLight: 'Light',
            themeDark: 'Dark',
            lineComfyTitle: 'Comfy line spacing',
            lineDefaultTitle: 'Default line spacing',
            lineCondensedTitle: 'Condensed line spacing'
        }
    };

    var t = subheaderI18n[currentFolder] || subheaderI18n[lang] || subheaderI18n['fr-lsg'];

    // ---- Build hour options ----
    var hourOptionsHtml = '';
    for (var h = 0; h < t.hours.length; h++) {
        var hr = t.hours[h];
        var sel = (hr.value === currentPage) ? ' selected' : '';
        hourOptionsHtml += '<option data-long="' + hr.long + '" data-short="' + hr.short + '" value="' + hr.value + '"' + sel + '>' + hr.long + '</option>';
    }

    // ---- Build language selector links (relative paths) ----
    var relFrUnofficial = '../fr-unofficial/' + currentPage;
    var relFrLsg = '../fr-lsg/' + currentPage;
    var relAr = '../ar/' + currentPage;
    var relCop = '../cop/' + currentPage;

    // ---- Assemble full subheader HTML ----
    var html =
        '<div class="sticky-subheader">' +
        '<div class="dropdown-wrapper">' +
        '<select class="hour-dropdown" id="hourDropdown">' +
        hourOptionsHtml +
        '</select>' +
        '<select class="section-dropdown" id="sectionDropdown">' +
        '<option value="">' + t.topLabel + '</option>' +
        '</select>' +
        '</div>' +
        '<button class="settings-btn" id="settingsBtn"><img alt="Settings" src="../cog_wheel.png"/></button>' +
        '<div class="settings-menu" id="settingsMenu">' +
        '<!-- Font Size Row -->' +
        '<div class="settings-row">' +
        '<button class="settings-menu-btn settings-menu-btn-small" id="fontDownBtn">A-</button>' +
        '<button class="settings-menu-btn settings-menu-btn-small" id="fontResetBtn">100%</button>' +
        '<button class="settings-menu-btn settings-menu-btn-small" id="fontUpBtn">A+</button>' +
        '</div>' +
        '<!-- Line Height Row -->' +
        '<div class="settings-row">' +
        '<button class="settings-menu-btn settings-toggle" id="lineComfyBtn" title="' + t.lineComfyTitle + '">' +
        '<span class="line-height-icon comfy-icon">' +
        '<span class="line"></span>' +
        '<span class="line"></span>' +
        '</span>' +
        '</button>' +
        '<button class="settings-menu-btn settings-toggle active" id="lineDefaultBtn" title="' + t.lineDefaultTitle + '">' +
        '<span class="line-height-icon default-icon">' +
        '<span class="line"></span>' +
        '<span class="line"></span>' +
        '</span>' +
        '</button>' +
        '<button class="settings-menu-btn settings-toggle" id="lineCondensedBtn" title="' + t.lineCondensedTitle + '">' +
        '<span class="line-height-icon condensed-icon">' +
        '<span class="line"></span>' +
        '<span class="line"></span>' +
        '</span>' +
        '</button>' +
        '</div>' +
        '<!-- Theme Row -->' +
        '<div class="settings-row">' +
        '<button class="settings-menu-btn settings-toggle" id="lightModeBtn">' + t.themeLight + '</button>' +
        '<button class="settings-menu-btn settings-toggle active" id="darkModeBtn">' + t.themeDark + '</button>' +
        '</div>' +
        '<!-- Language Selector -->' +
        '<div class="settings-row lang-selector">' +
        '<a class="settings-menu-btn settings-toggle" data-lang="fr" href="' + relFrUnofficial + '">Fran\u00e7ais</a>' +
        '<a class="settings-menu-btn settings-toggle" data-lang="ar" href="' + relAr + '">\u0639\u0631\u0628\u064a</a>' +
        '<a class="settings-menu-btn settings-toggle" data-lang="cop" href="' + relCop + '">\u2C98\u2C89\u2C99\u2CA7</a>' +
        '</div>' +
        '<div class="settings-row lang-variant-selector">' +
        '<a class="settings-menu-btn settings-toggle" data-variant="fr-unofficial" href="' + relFrUnofficial + '">Traduit du copte</a>' +
        '<a class="settings-menu-btn settings-toggle" data-variant="fr-lsg" href="' + relFrLsg + '">Classique</a>' +
        '</div>' +
        '</div>' +
        '</div>';

    var wrapper = document.createElement('div');
    wrapper.innerHTML = html;
    var subheader = wrapper.firstElementChild;
    document.body.insertBefore(subheader, document.body.firstChild);
})();

// ============================================================================
// UNOFFICIAL TRANSLATION NOTICE (fr-unofficial only)
// ============================================================================

(function injectUnofficialNotice() {
    if (!window.location.pathname.includes('/fr-unofficial/')) return;
    const notice = document.createElement('div');
    notice.className = 'unofficial-notice';
    notice.textContent = 'Traduction en cours d\'élaboration — ces textes sont provisoires et n\'ont pas encore reçu de validation officielle.';
    document.body.insertBefore(notice, document.body.firstChild);
})();

// ============================================================================
// SITE FOOTER
// ============================================================================

(function injectFooter() {
    const lang = document.documentElement.lang || 'en';
    const footerText = {
        fr: {
            attribution: 'Ce site est basé sur le travail de <a href="https://agpeya.org" target="_blank" rel="noopener">agpeya.org</a>.',
            credit: 'Tout le mérite du contenu des prières revient à son auteur — que ce travail lui soit rendu en hommage.',
            contact: 'Contact',
            source: 'Code source'
        },
        ar: {
            attribution: 'هذا الموقع مبني على عمل <a href="https://agpeya.org" target="_blank" rel="noopener">agpeya.org</a>.',
            credit: 'كل الفضل في محتوى الصلوات يعود لصاحب العمل الأصلي — تقديراً لجهده.',
            contact: 'تواصل',
            source: 'الكود المصدري'
        },
        cop: {
            attribution: 'This site is based on the work of <a href="https://agpeya.org" target="_blank" rel="noopener">agpeya.org</a>.',
            credit: 'All credit for the prayer content belongs to its original author, Marian-Apollos Balastre.',
            contact: 'Contact',
            source: 'Source code'
        }
    };
    const t = footerText[lang] || {
        attribution: 'This site is based on the work of <a href="https://agpeya.org" target="_blank" rel="noopener">agpeya.org</a>.',
        credit: 'All credit for the prayer content belongs to its original author — this is offered in tribute to their work.',
        contact: 'Contact',
        source: 'Source code'
    };

    const footer = document.createElement('footer');
    footer.className = 'site-footer';
    footer.innerHTML =
        '<div>' + t.attribution + '</div>' +
        '<div class="footer-credit">' + t.credit + '</div>' +
        '<div class="footer-links">' +
            '<a href="https://github.com/cyrilghali/agpia/issues" target="_blank" rel="noopener">' + t.contact + '</a>' +
            '<a href="https://github.com/cyrilghali/agpia" target="_blank" rel="noopener">' + t.source + '</a>' +
        '</div>';

    document.body.appendChild(footer);
})();

// ============================================================================
// COMMON PRAYER SECTIONS
// ============================================================================

const commonPrayers = {
    'introduction': `
        <section class="section">
            <h2 class="section-title">Introduction to Every Hour</h2>
            <div class="prayer-text">
                In the name of the Father, and the Son, and the Holy Spirit, one God. Amen.
            </div>
            <div class="prayer-text">
                Kyrie eleison. Lord have mercy, Lord have mercy, Lord bless us. Amen.
            </div>
            <div class="prayer-text">
                Glory to the Father, and to the Son, and to the Holy Spirit, now and forever and unto the ages of all ages. Amen.
            </div>
        </section>
    `,
    
    'lords-prayer': `
        <section class="section">
            <h2 class="section-title">The Lord's Prayer</h2>
            <div class="prayer-text">
                <em>Make us worthy to pray thankfully:</em>
            </div>
            <div class="prayer-text">
                Our Father Who art in heaven; hallowed be Thy name. Thy kingdom come. Thy will be done on earth as it is in heaven. Give us this day our daily bread.
            </div>
            <div class="prayer-text">
                And forgive us our trespasses, as we forgive those who trespass against us. And lead us not into temptation, but deliver us from evil, in Christ Jesus our Lord. For Thine is the kingdom, the power and the glory, forever. Amen.
            </div>
        </section>
    `,
    
    'thanksgiving': `
        <section class="section">
            <h2 class="section-title">The Prayer of Thanksgiving</h2>
            <div class="prayer-text">
                Let us give thanks to the beneficent and merciful God, the Father of our Lord, God and Savior, Jesus Christ, for He has covered us, helped us, guarded us, accepted us unto Him, spared us, supported us, and brought us to this hour. Let us also ask Him, the Lord our God, the Pantocrator, to guard us in all peace this holy day and all the days of our life.
            </div>
            <div class="prayer-text">
                O Master, Lord, God the Pantocrator, the Father of our Lord, God and Savior, Jesus Christ, we thank You for every condition, concerning every condition, and in every condition, for You have covered us, helped us, guarded us, accepted us unto You, spared us, supported us, and brought us to this hour.
            </div>
            <div class="prayer-text">
                Therefore, we ask and entreat Your goodness, O Lover of mankind, to grant us to complete this holy day, and all the days of our life, in all peace with Your fear. All envy, all temptation, all the work of Satan, the counsel of wicked men, and the rising up of enemies, hidden and manifest, take them away from us, and from all Your people, and from this holy place that is Yours.
            </div>
            <div class="prayer-text">
                But those things which are good and profitable do provide for us; for it is You Who have given us the authority to tread on serpents and scorpions, and upon all the power of the enemy.
            </div>
            <div class="prayer-text">
                And lead us not into temptation, but deliver us from evil, by the grace, compassion and love of mankind, of Your Only-Begotten Son, our Lord, God and Savior, Jesus Christ, through Whom the glory, the honor, the dominion, and the adoration are due unto You, with Him, and the Holy Spirit, the Life-Giver, Who is of one essence with You, now and at all times, and unto the ages of all ages. Amen.
            </div>
        </section>
    `,
    
    'psalm-50': `
        <section class="section">
            <h2 class="section-title">Psalm 50</h2>
            <div class="psalm-verse drop-cap">
                Have mercy upon me, O God, according to Your great mercy; and according to the multitude of Your compassions blot out my iniquity. Wash me thoroughly from my iniquity, and cleanse me from my sin. For I am conscious of my iniquity; and my sin is at all times before me.
            </div>
            <div class="psalm-verse">
                Against You only I have sinned, and done evil before You: that You might be just in Your sayings, and might overcome when You are judged. For, behold, I was conceived in iniquities, and in sins my mother conceived me.
            </div>
            <div class="psalm-verse">
                For, behold, You have loved the truth: You have manifested to me the hidden and unrevealed things of Your wisdom. You shall sprinkle me with Your hyssop, and I shall be purified: You shall wash me, and I shall be made whiter than snow. You shall make me to hear gladness and joy: the humbled bones shall rejoice.
            </div>
            <div class="psalm-verse">
                Turn away Your face from my sins, and blot out all my iniquities. Create in me a clean heart, O God; and renew a right spirit in my inward parts. Do not cast me away from Your face; and do not remove Your Holy Spirit from me. Give me the joy of Your salvation: and uphold me with a directing spirit. Then I shall teach the transgressors Your ways; and the ungodly men shall turn to You.
            </div>
            <div class="psalm-verse">
                Deliver me from blood, O God, the God of my salvation: and my tongue shall rejoice in Your righteousness. O Lord, You shall open my lips; and my mouth shall declare Your praise. For if You desired sacrifice, I would have given it: You do not take pleasure in burnt offerings. The sacrifice of God is a broken spirit: a broken and humbled heart God shall not despise.
            </div>
            <div class="psalm-verse">
                Do good, O Lord, in Your good pleasure to Zion; and let the walls of Jerusalem be built. Then You shall be pleased with sacrifices of righteousness, offering, and burnt sacrifices: then they shall offer calves upon Your altar. <span class="alleluia">ALLELUIA.</span>
            </div>
        </section>
    `,
    
    'conclusion': `
        <section class="section">
            <h2 class="section-title">Conclusion of Every Hour</h2>
            <div class="prayer-text">
                Have mercy on us, O God, and have mercy on us, who, at all times and in every hour, in heaven and on earth, is worshipped and glorified, Christ our God, the good, the long suffering, the abundant in mercy, and the great in compassion, who loves the righteous and has mercy on the sinners of whom I am chief.
            </div>
            <div class="prayer-text">
                Lord receive from us our prayers in this hour and in every hour. Ease our life and guide us to fulfill Your commandments. Sanctify our spirits. Cleanse our bodies. Conduct our thoughts. Purify our intentions. Heal our diseases. Forgive our sins.
            </div>
            <div class="prayer-text">
                Deliver us from every evil grief and distress of heart. Surround us by Your holy angels, that, by their camp, we may be guarded and guided, and attain the unity of faith, and the knowledge of Your imperceptible and infinite glory. For You are blessed forever. Amen.
            </div>
        </section>
    `
};

// Load common prayer sections on page load
function loadCommonSections() {
    document.querySelectorAll('[data-common-section]').forEach(element => {
        const sectionName = element.getAttribute('data-common-section');
        if (commonPrayers[sectionName]) {
            element.outerHTML = commonPrayers[sectionName];
        }
    });
}

// Call immediately when script loads
loadCommonSections();

// ============================================================================
// THEME AND FONT MANAGEMENT
// ============================================================================

// Load and apply saved theme
const theme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', theme);

// Load and apply saved font size
const fontSize = localStorage.getItem('fontSize') || '1.3';
document.documentElement.style.setProperty('--font-scale', fontSize);

// Update theme icon based on current theme
const updateThemeIcon = () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const themeBtn = document.getElementById('themeToggleBtn');
    if (themeBtn) {
        themeBtn.textContent = currentTheme === 'dark' ? 'â˜€ï¸' : 'ðŸŒ™';
    }
};
updateThemeIcon();

// ============================================================================
// SETTINGS MENU
// ============================================================================

const settingsBtn = document.getElementById('settingsBtn');
const settingsMenu = document.getElementById('settingsMenu');

if (settingsBtn && settingsMenu) {
    settingsBtn.onclick = (e) => {
        e.stopPropagation();
        settingsMenu.classList.toggle('active');
    };
    
    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!settingsMenu.contains(e.target) && !settingsBtn.contains(e.target)) {
            settingsMenu.classList.remove('active');
        }
    });
}

// Font controls - ALL buttons keep menu open
const fontDownBtn = document.getElementById('fontDownBtn');
const fontResetBtn = document.getElementById('fontResetBtn');
const fontUpBtn = document.getElementById('fontUpBtn');

// Function to update font button display
function updateFontDisplay() {
    const current = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--font-scale')) || 1.3;
    const percentage = Math.round((current / 1.3) * 100);
    
    if (fontResetBtn) {
        fontResetBtn.textContent = percentage + '%';
        
        // Add active state when at 100%
        if (percentage === 100) {
            fontResetBtn.classList.add('active');
        } else {
            fontResetBtn.classList.remove('active');
        }
    }
}

// Initialize font display
updateFontDisplay();

if (fontDownBtn) {
    fontDownBtn.onclick = (e) => {
        e.stopPropagation();
        const current = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--font-scale')) || 1.3;
        const newSize = Math.max(1.0, current - 0.1);
        document.documentElement.style.setProperty('--font-scale', newSize);
        localStorage.setItem('fontSize', newSize.toFixed(1));
        updateFontDisplay();
    };
}

if (fontResetBtn) {
    fontResetBtn.onclick = (e) => {
        e.stopPropagation();
        document.documentElement.style.setProperty('--font-scale', '1.3');
        localStorage.setItem('fontSize', '1.3');
        updateFontDisplay();
    };
}

if (fontUpBtn) {
    fontUpBtn.onclick = (e) => {
        e.stopPropagation();
        const current = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--font-scale')) || 1.3;
        const newSize = Math.min(2.0, current + 0.1);
        document.documentElement.style.setProperty('--font-scale', newSize);
        localStorage.setItem('fontSize', newSize.toFixed(1));
        updateFontDisplay();
    };
}

// Line height controls
const lineComfyBtn = document.getElementById('lineComfyBtn');
const lineDefaultBtn = document.getElementById('lineDefaultBtn');
const lineCondensedBtn = document.getElementById('lineCondensedBtn');

// Initialize line height from localStorage (default is 'default')
const savedLineHeight = localStorage.getItem('lineHeight') || 'default';
document.documentElement.setAttribute('data-line-height', savedLineHeight);

// Function to find the currently visible section
function getCurrentVisibleSection() {
    const sections = document.querySelectorAll('.section');
    let closestSection = null;
    let closestDistance = Infinity;
    
    // Find the section closest to the top of the viewport
    sections.forEach(section => {
        const rect = section.getBoundingClientRect();
        const distanceFromTop = Math.abs(rect.top);
        
        // If this section is in viewport and closer to top than previous
        if (rect.top < window.innerHeight && rect.bottom > 0 && distanceFromTop < closestDistance) {
            closestDistance = distanceFromTop;
            closestSection = section;
        }
    });
    
    return closestSection;
}

// Function to change line height and preserve position
function changeLineHeight(newHeight) {
    // Get current visible section before changing line height
    const currentSection = getCurrentVisibleSection();
    
    // Change line height
    document.documentElement.setAttribute('data-line-height', newHeight);
    localStorage.setItem('lineHeight', newHeight);
    updateLineHeightButtons();
    
    // Scroll back to the same section after layout recalculates
    // Use double requestAnimationFrame to ensure layout is complete
    if (currentSection) {
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                currentSection.scrollIntoView({ behavior: 'auto', block: 'start' });
            });
        });
    }
}

function updateLineHeightButtons() {
    const currentLineHeight = document.documentElement.getAttribute('data-line-height') || 'default';
    if (lineComfyBtn && lineDefaultBtn && lineCondensedBtn) {
        lineComfyBtn.classList.toggle('active', currentLineHeight === 'comfy');
        lineDefaultBtn.classList.toggle('active', currentLineHeight === 'default');
        lineCondensedBtn.classList.toggle('active', currentLineHeight === 'condensed');
    }
}
updateLineHeightButtons();

if (lineComfyBtn) {
    lineComfyBtn.onclick = (e) => {
        e.stopPropagation();
        changeLineHeight('comfy');
    };
}

if (lineDefaultBtn) {
    lineDefaultBtn.onclick = (e) => {
        e.stopPropagation();
        changeLineHeight('default');
    };
}

if (lineCondensedBtn) {
    lineCondensedBtn.onclick = (e) => {
        e.stopPropagation();
        changeLineHeight('condensed');
    };
}

// Theme controls - separate light/dark buttons
const lightModeBtn = document.getElementById('lightModeBtn');
const darkModeBtn = document.getElementById('darkModeBtn');

function updateThemeButtons() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    if (lightModeBtn && darkModeBtn) {
        lightModeBtn.classList.toggle('active', currentTheme === 'light');
        darkModeBtn.classList.toggle('active', currentTheme === 'dark');
    }
}
updateThemeButtons();

if (lightModeBtn) {
    lightModeBtn.onclick = (e) => {
        e.stopPropagation();
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
        updateThemeButtons();
    };
}

if (darkModeBtn) {
    darkModeBtn.onclick = (e) => {
        e.stopPropagation();
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        updateThemeButtons();
    };
}

// ============================================================================
// LANGUAGE SELECTOR (folder-based)
// ============================================================================

(function initLangSelector() {
    const path = window.location.pathname;
    const folders = ['fr-lsg', 'fr-unofficial', 'ar', 'cop'];
    let currentFolder = 'fr-lsg';
    for (const f of folders) {
        if (path.includes('/' + f + '/')) { currentFolder = f; break; }
    }

    localStorage.setItem('lang', currentFolder);

    const isFrench = currentFolder === 'fr-unofficial' || currentFolder === 'fr-lsg';
    const activeLang = isFrench ? 'fr' : currentFolder === 'cop' ? 'cop' : 'ar';

    document.querySelectorAll('.lang-selector a').forEach(link => {
        link.classList.toggle('active', link.getAttribute('data-lang') === activeLang);
    });

    const variantUnlocked = localStorage.getItem('variantUnlocked') === '1';
    document.querySelectorAll('.lang-variant-selector').forEach(el => {
        el.style.display = (isFrench && variantUnlocked) ? 'flex' : 'none';
    });

    document.querySelectorAll('.lang-variant-selector a').forEach(link => {
        link.classList.toggle('active', link.getAttribute('data-variant') === currentFolder);
    });
})();


// ============================================================================
// LOGO EASTER EGG — 4 clicks opens confirmation modal
// ============================================================================

(function injectVariantModal() {
    const overlay = document.createElement('div');
    overlay.id = 'variant-unlock-modal';
    overlay.className = 'variant-modal-overlay';
    overlay.innerHTML =
        '<div class="variant-modal">' +
            '<h2 class="variant-modal-title">Traduction non officielle</h2>' +
            '<p class="variant-modal-body">' +
                'Vous êtes sur le point de débloquer la version <em>Traduit du copte</em>.<br><br>' +
                'Ces textes sont en cours d\'élaboration, provisoires, et n\'ont pas encore reçu de validation officielle. Ils peuvent contenir des erreurs.' +
            '</p>' +
            '<div class="variant-modal-actions">' +
                '<button class="variant-modal-btn variant-modal-cancel">Annuler</button>' +
                '<button class="variant-modal-btn variant-modal-confirm">Débloquer</button>' +
            '</div>' +
        '</div>';
    document.body.appendChild(overlay);

    overlay.querySelector('.variant-modal-cancel').addEventListener('click', function () {
        overlay.classList.remove('visible');
    });

    overlay.querySelector('.variant-modal-confirm').addEventListener('click', function () {
        try { localStorage.setItem('variantUnlocked', '1'); } catch(e) {}
        document.querySelectorAll('.lang-variant-selector').forEach(el => {
            el.style.display = 'flex';
        });
        overlay.classList.remove('visible');
        const cross = document.querySelector('.header-crosses') || document.querySelector('.hero-cross');
        if (cross) {
            cross.classList.add('easter-egg-unlock');
            setTimeout(() => cross.classList.remove('easter-egg-unlock'), 600);
        }
    });

    overlay.addEventListener('click', function (e) {
        if (e.target === overlay) overlay.classList.remove('visible');
    });
})();

(function initLogoEasterEgg() {
    const cross = document.querySelector('.header-crosses') || document.querySelector('.hero-cross');
    if (!cross) return;
    let clicks = 0, timer = null;
    cross.addEventListener('click', function () {
        clicks++;
        clearTimeout(timer);
        if (clicks >= 3) {
            clicks = 0;
            const modal = document.getElementById('variant-unlock-modal');
            if (modal) modal.classList.add('visible');
        } else {
            timer = setTimeout(() => { clicks = 0; }, 1000);
        }
    });
})();

// ============================================================================
// HOUR DROPDOWN - SHORT/LONG NAME SWITCHING
// ============================================================================

const hourDropdown = document.getElementById('hourDropdown');
const currentPage = window.location.pathname.split('/').pop();

// Function to update all options to show long names
const showLongNames = () => {
    Array.from(hourDropdown.options).forEach(option => {
        const longName = option.getAttribute('data-long');
        if (longName) {
            option.textContent = longName;
        }
    });
};

// Function to update selected option to show short name
const showShortName = () => {
    const selectedOption = hourDropdown.options[hourDropdown.selectedIndex];
    const shortName = selectedOption.getAttribute('data-short');
    if (shortName) {
        selectedOption.textContent = shortName;
    }
};

if (hourDropdown) {
    hourDropdown.value = currentPage;
    
    // Initialize with short name
    showShortName();
    
    // Show long names when dropdown is opened
    hourDropdown.addEventListener('focus', showLongNames);
    hourDropdown.addEventListener('mousedown', showLongNames);
    
    // Show short name when dropdown is closed
    hourDropdown.addEventListener('blur', showShortName);
    
    hourDropdown.addEventListener('change', (e) => {
        if (e.target.value) {
            window.location.href = e.target.value;
        }
    });
}

// ============================================================================
// SECTION DROPDOWN AND SCROLL TRACKING
// ============================================================================

const sections = document.querySelectorAll(".section");
const sectionDropdown = document.getElementById("sectionDropdown");
let isUserScrolling = true;

// Populate section dropdown
sections.forEach((section, index) => {
    const sectionTitle = section.querySelector(".section-title");
    if (sectionTitle) {
        const option = document.createElement("option");
        option.value = index;
        option.textContent = sectionTitle.textContent;
        sectionDropdown.appendChild(option);
    }
});

// Section dropdown change handler
sectionDropdown.addEventListener('change', (e) => {
    // Check if "Top" is selected FIRST (value is empty string)
    if (e.target.value === '') {
        isUserScrolling = false;
        window.scrollTo({ top: 0, behavior: 'smooth' });
        setTimeout(() => {
            isUserScrolling = true;
        }, 1000);
        return;
    }
    
    // Normal section navigation
    const index = parseInt(e.target.value);
    if (!isNaN(index) && sections[index]) {
        isUserScrolling = false;
        sections[index].scrollIntoView({ behavior: 'smooth', block: 'start' });
        setTimeout(() => {
            isUserScrolling = true;
        }, 1000);
    }
});

// Intersection Observer for scroll tracking
const observerOptions = {
    root: null,
    rootMargin: "-85px 0px -50% 0px",
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    if (!isUserScrolling) return;
    
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const sectionTitle = entry.target.querySelector(".section-title");
            if (sectionTitle) {
                const options = sectionDropdown.options;
                for (let i = 0; i < options.length; i++) {
                    if (options[i].textContent === sectionTitle.textContent) {
                        sectionDropdown.selectedIndex = i;
                        break;
                    }
                }
            }
        }
    });
}, observerOptions);

sections.forEach(section => observer.observe(section));

// ============================================================================
// JUMP TO GOSPEL BUTTONS
// ============================================================================

// Standard jump to gospel functionality (for most hours)
function initJumpToGospel() {
    const jumpGospelBtns = document.querySelectorAll('.jump-gospel-btn');
    jumpGospelBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            
            const gospelSection = document.getElementById('gospel');
            if (gospelSection) {
                isUserScrolling = false;
                gospelSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                
                // Update section dropdown to match
                const gospelTitle = gospelSection.querySelector('.section-title');
                if (gospelTitle && sectionDropdown) {
                    const options = sectionDropdown.options;
                    for (let i = 0; i < options.length; i++) {
                        if (options[i].textContent === gospelTitle.textContent) {
                            sectionDropdown.selectedIndex = i;
                            break;
                        }
                    }
                }
                
                setTimeout(() => {
                    isUserScrolling = true;
                }, 1000);
            }
        });
    });
}

// Midnight hour special jump to gospel (watch-aware)
function initMidnightJumpToGospel() {
    const jumpGospelBtns = document.querySelectorAll('.jump-gospel-btn');
    jumpGospelBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();

            // Get the target from href (e.g., "gospel-watch1", "gospel-watch2", etc.)
            const targetId = btn.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);

            if (targetSection) {
                isUserScrolling = false;
                targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

                // Update section dropdown to match
                const gospelTitle = targetSection.querySelector('.section-title');
                if (gospelTitle && sectionDropdown) {
                    const options = sectionDropdown.options;
                    for (let i = 0; i < options.length; i++) {
                        if (options[i].textContent === gospelTitle.textContent) {
                            sectionDropdown.selectedIndex = i;
                            break;
                        }
                    }
                }

                setTimeout(() => {
                    isUserScrolling = true;
                }, 1000);
            }
        });
    });
}

// ============================================================================
// PWA INSTALL PROMPT
// ============================================================================

(function initPwaInstallBanner() {
    // Don't show if already installed (standalone mode)
    if (window.matchMedia('(display-mode: standalone)').matches) return;
    if (window.navigator.standalone === true) return;

    // Don't show if user dismissed it before
    try {
        if (localStorage.getItem('pwaInstallDismissed') === '1') return;
    } catch(e) {}

    const lang = document.documentElement.lang || 'en';

    const i18n = {
        fr: { title: 'Installer Agpia', subtitle: 'Accédez rapidement depuis votre écran d\u2019accueil', install: 'Installer', iosSubtitle: 'Appuyez sur «\u00A0Partager\u00A0» puis «\u00A0Sur l\u2019écran d\u2019accueil\u00A0»' },
        ar: { title: '\u062A\u062B\u0628\u064A\u062A \u0627\u0644\u0623\u062C\u0628\u064A\u0629', subtitle: '\u0627\u0641\u062A\u062D\u0647\u0627 \u0628\u0633\u0631\u0639\u0629 \u0645\u0646 \u0634\u0627\u0634\u062A\u0643 \u0627\u0644\u0631\u0626\u064A\u0633\u064A\u0629', install: '\u062A\u062B\u0628\u064A\u062A', iosSubtitle: '\u0627\u0636\u063A\u0637 \u0639\u0644\u0649 \u00AB\u0645\u0634\u0627\u0631\u0643\u0629\u00BB \u062B\u0645 \u00AB\u0625\u0636\u0627\u0641\u0629 \u0625\u0644\u0649 \u0627\u0644\u0634\u0627\u0634\u0629 \u0627\u0644\u0631\u0626\u064A\u0633\u064A\u0629\u00BB' },
        cop: { title: 'Install Agpia', subtitle: 'Quick access from your home screen', install: 'Install', iosSubtitle: 'Tap "Share" then "Add to Home Screen"' }
    };
    const t = i18n[lang] || { title: 'Install Agpia', subtitle: 'Quick access from your home screen', install: 'Install', iosSubtitle: 'Tap "Share" then "Add to Home Screen"' };

    // Create banner element
    var banner = document.createElement('div');
    banner.className = 'pwa-install-banner';
    banner.innerHTML =
        '<img class="pwa-install-banner-icon" src="/icons/icon-192.png" alt="Agpia">' +
        '<div class="pwa-install-banner-text">' +
            '<div class="pwa-install-banner-title">' + t.title + '</div>' +
            '<div class="pwa-install-banner-subtitle">' + t.subtitle + '</div>' +
        '</div>' +
        '<button class="pwa-install-btn" id="pwaInstallBtn">' + t.install + '</button>' +
        '<button class="pwa-install-close" id="pwaInstallClose">\u00D7</button>';
    document.body.appendChild(banner);

    var deferredPrompt = null;

    // Close button handler
    document.getElementById('pwaInstallClose').addEventListener('click', function() {
        banner.classList.remove('visible');
        try { localStorage.setItem('pwaInstallDismissed', '1'); } catch(e) {}
    });

    // Android/Chrome: listen for beforeinstallprompt
    window.addEventListener('beforeinstallprompt', function(e) {
        e.preventDefault();
        deferredPrompt = e;
        banner.classList.add('visible');
    });

    document.getElementById('pwaInstallBtn').addEventListener('click', function() {
        if (deferredPrompt) {
            deferredPrompt.prompt();
            deferredPrompt.userChoice.then(function() {
                deferredPrompt = null;
                banner.classList.remove('visible');
            });
        }
    });

    // iOS Safari: show instructions banner
    var isIos = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
    var isSafari = /Safari/.test(navigator.userAgent) && !/CriOS|FxiOS|OPiOS|EdgiOS/.test(navigator.userAgent);
    if (isIos && isSafari) {
        banner.querySelector('.pwa-install-banner-subtitle').textContent = t.iosSubtitle;
        banner.querySelector('#pwaInstallBtn').style.display = 'none';
        banner.classList.add('visible');
    }

    // Hide banner if app gets installed
    window.addEventListener('appinstalled', function() {
        banner.classList.remove('visible');
    });
})();
