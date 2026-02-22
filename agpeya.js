// Agpeya JavaScript - Common functionality for all prayer hours
// This file contains all shared JavaScript to reduce file sizes

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js');
}

// ============================================================================
// LANG MIGRATION — reset old French variants to fr-lsg
// ============================================================================

(function migrateLang() {
    try {
        var _l = localStorage.getItem('lang');
        if (_l === 'fr' || _l === 'fr-unofficial') localStorage.setItem('lang', 'fr-lsg');
    } catch(e) {}
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
            derived: 'Ce site est dérivé de',
            contact: 'Contact',
            source: 'Code source'
        },
        ar: {
            derived: 'هذا الموقع مشتق من',
            contact: 'تواصل',
            source: 'الكود المصدري'
        }
    };
    const t = footerText[lang] || {
        derived: 'This site is derived from',
        contact: 'Contact',
        source: 'Source code'
    };

    const footer = document.createElement('footer');
    footer.className = 'site-footer';
    footer.innerHTML =
        '<div>' + t.derived + ' <a href="https://agpeya.org" target="_blank" rel="noopener">agpeya.org</a></div>' +
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
    const folders = ['fr-lsg', 'fr-unofficial', 'ar'];
    let currentFolder = 'fr-lsg';
    for (const f of folders) {
        if (path.includes('/' + f + '/')) { currentFolder = f; break; }
    }

    localStorage.setItem('lang', currentFolder);

    const isFrench = currentFolder === 'fr-unofficial' || currentFolder === 'fr-lsg';
    const activeLang = isFrench ? 'fr' : 'ar';

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
// LOGO EASTER EGG — 4 clicks unlocks French variant selector
// ============================================================================

(function initLogoEasterEgg() {
    const cross = document.querySelector('.header-crosses');
    if (!cross) return;
    let clicks = 0, timer = null;
    cross.addEventListener('click', function () {
        clicks++;
        clearTimeout(timer);
        if (clicks >= 4) {
            clicks = 0;
            try { localStorage.setItem('variantUnlocked', '1'); } catch(e) {}
            document.querySelectorAll('.lang-variant-selector').forEach(el => {
                el.style.display = 'flex';
            });
            cross.classList.add('easter-egg-unlock');
            setTimeout(() => cross.classList.remove('easter-egg-unlock'), 600);
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
    const selectedText = e.target.options[e.target.selectedIndex].textContent;
    if (selectedText === 'Top') {
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
