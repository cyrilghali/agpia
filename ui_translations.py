"""UI translation dictionaries and functions for French Agpeya pages."""
import re
from bs4 import BeautifulSoup, NavigableString

TITLE_MAP = {
    'Introduction to Every Hour': 'Introduction de chaque heure',
    "The Lord's Prayer": 'Le Notre Père',
    'The Prayer of Thanksgiving': "Prière d'action de grâce",
    '41 Kyrie Eleison': '41 Kyrie Eleison',
    'Holy Holy Holy': 'Saint Saint Saint',
    'The Orthodox Creed': 'Acte de Foi',
    'Introduction to the Creed': "Introduction de l'Acte de Foi",
    'Conclusion of Every Hour': 'Conclusion de chaque heure',
    'First Absolution': "Première absolution de l'aube",
    'Second Absolution': "Seconde absolution de l'aube",
    'Hail to Saint Mary': 'Tropaires de la Vierge',
    'Hail to You': 'Tropaires de la Vierge',
    'The Trisagion': 'Le Trisagion',
    'The Gloria': 'Louange des anges',
    'Graciously Accord, O Lord': 'Daigne, Seigneur',
    'Let My Supplication': 'Que ma supplication',
    'Opening Prayer': 'Prière de minuit',
    'Come Let Us Kneel Down': "Prière de l'aube",
    'The Faith of the Church': "La foi de l'Église",
    'The First Watch': 'La Première Veille',
    'The Second Watch': 'La Deuxième Veille',
    'The Third Watch': 'La Troisième Veille',
    'The Holy Gospel According to Saint John (1:1-17)': "Évangile de l'aube",
    'The Holy Gospel (John 14:26-31 & 15:1-4)': 'Évangile de la troisième heure',
    'The Holy Gospel (Matthew 5:1-16)': 'Évangile de la sixième heure',
    'The Holy Gospel (Luke 9:10-17)': 'Évangile de la neuvième heure',
    'The Holy Gospel (Luke 4:38-41)': 'Évangile de la onzième heure',
    'The Holy Gospel (St. Luke 2:25-32)': 'Évangile de la douzième heure',
    'The Holy Gospel (Matthew 25:1-13)': 'Évangile du premier service',
    'The Holy Gospel (Luke 7:36-50)': 'Évangile du second service',
    'The Holy Gospel (Luke 12:32-46)': 'Évangile du troisième service',
    'The Holy Gospel (Luke 2:29-32)': 'Cantique de Siméon',
    'The Holy Gospel (John 6:15-23)': 'Évangile du voile',
    "The Pauline Epistle (Ephesians 4:1-5)": 'Epître de Paul',
    'Prayer Before Confession': 'Prière avant la confession',
    'Prayer After Confession': 'Prière après la confession',
    'Prayer Before Communion 1': 'Prière avant la communion',
    'Prayer Before Communion 2': 'Seconde prière avant la communion',
    'Prayer After Communion 1': 'Prière après la communion',
    'Prayer After Communion 2': 'Seconde prière après la communion',
    'Prayer Before Meals 1': 'Prière avant de manger',
    'Prayer Before Meals 2': 'Prière pour demander à Dieu de nous guider',
    'Prayer After Meals': 'Prière / Remerciements',
    'Prayer Before Studying': "Prière avant l'étude",
    'Prayer After Studying': "Prière après l'étude",
    'The Word Agpeya': 'Le mot Agpia',
    'The Book of the Agpeya': "Le Livre de l'Agpia",
    'Why Do We Use the Agpeya for Praying?': "Pourquoi utilisons-nous l'Agpia pour prier ?",
    'The Originality of the Agpeya': "L'originalité de l'Agpia",
    'The Agpeya and the Psalms': "L'Agpia et les Psaumes",
    'The Agpeya and Prayer': "L'Agpia et la Prière",
    'The Order of the Agpeya': "L'Ordre de l'Agpia",
    'Manner of Praying the Hours': 'Manière de prier les heures',
    'Themes of the Hours': 'Les thèmes des heures',
    'Advice on How to Use the Agpeya': "Conseils pour l'utilisation de l'Agpia",
}

LITANIES_BY_HOUR = {
    'prime': "Tropaires de l'aube",
    'terce': 'Tropaires de la troisième heure',
    'sext': 'Tropaires de la sixième heure',
    'none': 'Tropaires de la neuvième heure',
    'vespers': 'Tropaires de la onzième heure',
    'compline': 'Tropaires de la douzième heure',
    'veil': 'Tropaires du voile',
}

ABSOLUTION_BY_HOUR = {
    'terce': 'Absolution de la troisième heure',
    'sext': 'Absolution de la sixième heure',
    'none': 'Absolution de la neuvième heure',
    'vespers': 'Absolution de la onzième heure',
    'compline': 'Absolution de la douzième heure',
    'veil': 'Absolution du voile',
    'midnight': 'Absolution de minuit',
}

MIDNIGHT_LITANIES_BY_WATCH = {
    1: 'Tropaires du premier service',
    2: 'Tropaires du second service',
    3: 'Tropaires du troisième service',
}

PAGE_TITLES = {
    'Prime | Agpeya': 'Prime | Agpia',
    'Terce | Agpeya': 'Tierce | Agpia',
    'Sext | Agpeya': 'Sexte | Agpia',
    'None | Agpeya': 'None | Agpia',
    'Vespers | Agpeya': 'V\u00eapres | Agpia',
    'Compline | Agpeya': 'Complies | Agpia',
    'Midnight Prayer | Agpeya': 'Pri\u00e8re de Minuit | Agpia',
    'Prayer of the Veil | Agpeya': 'Pri\u00e8re du Voile | Agpia',
    'Other Prayers | Agpeya': 'Autres Pri\u00e8res | Agpia',
    'About | Agpeya': '\u00c0 propos | Agpia',
    'Agpeya - The Coptic Book of Hours': 'Agpia - Le Livre des Heures Copte',
}

H1_MAP = {
    'Prime': 'Prime', 'Terce': 'Tierce', 'Sext': 'Sexte', 'None': 'None',
    'Vespers': 'V\u00eapres', 'Compline': 'Complies',
    'Midnight Prayer': 'Pri\u00e8re de Minuit',
    'Prayer of the Veil': 'Pri\u00e8re du Voile',
    'Other Prayers': 'Autres Pri\u00e8res',
    'About the Agpeya': "\u00c0 propos de l'Agpia",
}

HOUR_TIME_MAP = {
    'The First Hour \u00b7 6:00 AM': 'La Premi\u00e8re Heure \u00b7 6h00',
    'The Third Hour \u00b7 9:00 AM': 'La Troisi\u00e8me Heure \u00b7 9h00',
    'The Sixth Hour \u00b7 12:00 PM': 'La Sixi\u00e8me Heure \u00b7 12h00',
    'The Ninth Hour \u00b7 3:00 PM': 'La Neuvi\u00e8me Heure \u00b7 15h00',
    'The Eleventh Hour \u00b7 6:00 PM': 'La Onzi\u00e8me Heure \u00b7 18h00',
    'The Twelfth Hour \u00b7 9:00 PM': 'La Douzi\u00e8me Heure \u00b7 21h00',
    'Midnight \u00b7 12:00 AM': 'Minuit \u00b7 0h00',
    'Selected Psalms from All Hours': 'Psaumes choisis de toutes les heures',
}

HOUR_DESC_FR = {
    'prime': "La Pri\u00e8re du Matin est con\u00e7ue pour \u00eatre pri\u00e9e t\u00f4t, \u00e0 l'aube, en r\u00e9f\u00e9rence \u00e0 la venue de la vraie Lumi\u00e8re, le Seigneur J\u00e9sus-Christ. Prime est principalement associ\u00e9e \u00e0 l'\u00e9ternit\u00e9 de Dieu, Son incarnation et Sa r\u00e9surrection d'entre les morts. Elle est destin\u00e9e \u00e0 Lui offrir des remerciements pour nous avoir relev\u00e9s du sommeil, Le suppliant de briller sur nous, d'\u00e9clairer nos vies et de nous accorder la puissance de Sa r\u00e9surrection.",
    'terce': "La Troisi\u00e8me Heure comm\u00e9more trois \u00e9v\u00e9nements significatifs : le proc\u00e8s du Christ devant Pilate, Son ascension au ciel et la descente du Saint-Esprit sur les disciples. Nous prions pour que la gr\u00e2ce du Saint-Esprit purifie nos c\u0153urs et renouvelle nos vies.",
    'sext': "La Sixi\u00e8me Heure nous rappelle la crucifixion et la passion du Christ. Nous prions pour que, par Sa passion vivifiante, Il d\u00e9livre nos esprits des convoitises, tourne nos pens\u00e9es vers le souvenir de Ses commandements, et fasse de nous une lumi\u00e8re du monde et le sel de la terre.",
    'none': "La Neuvi\u00e8me Heure comm\u00e9more la mort r\u00e9demptrice du Christ en la chair sur la croix, et Son acceptation de la repentance du Larron. Nous prions pour que le Sauveur mortifie nos convoitises charnelles, nous fasse participants de Sa gr\u00e2ce, et accepte notre repentance lorsque nous crions avec le Larron : \u00ab Souviens-toi de nous, Seigneur, quand Tu viendras dans Ton Royaume \u00bb (Luc 23:42).",
    'vespers': "Les V\u00eapres (Coucher du soleil) : la Onzi\u00e8me Heure est associ\u00e9e \u00e0 l'acte de descendre le corps du Christ de la croix. \u00c0 la fin du jour, nous rendons gr\u00e2ce pour la protection de Dieu, et confessons nos p\u00e9ch\u00e9s avec le Fils Prodigue (Luc 15:11-31) afin d'\u00eatre compt\u00e9s parmi les ouvriers appel\u00e9s \u00e0 la onzi\u00e8me heure du jour (Matt. 20:1-16).",
    'compline': "Les Complies (Coucher) : la Douzi\u00e8me Heure comm\u00e9more l'ensevelissement du Christ. Nous nous souvenons du monde qui passe et du jugement dernier. Conscients de notre comparution imminente devant Dieu, nous demandons le pardon de nos p\u00e9ch\u00e9s et la protection durant la nuit.",
    'midnight': "L'Heure de Minuit comm\u00e9more le second av\u00e8nement du Seigneur. L'office se compose de trois veilles, correspondant aux trois \u00e9tapes de la pri\u00e8re du Christ au jardin de Geths\u00e9mani (Matt. 25:1-13).",
    'veil': "Le Voile : cette pri\u00e8re est destin\u00e9e \u00e0 \u00eatre lue par les \u00e9v\u00eaques et les pr\u00eatres comme un moyen d'examiner leur c\u0153ur. C'est aussi une pri\u00e8re qui concerne les moines.",
    'other': "La pri\u00e8re est une relation vivante avec Dieu. Cette collection rassemble les pri\u00e8res essentielles de la liturgie copte, sacramentelles et spirituelles quotidiennes tir\u00e9es de l'Agpia et de la tradition \u00e9vang\u00e9lique. Elle guide les croyants \u00e0 travers la confession, la communion, les repas, l'\u00e9tude et les supplications personnelles, formant un rythme structur\u00e9 de culte, de repentance, de gratitude et de d\u00e9votion disciplin\u00e9e pour une vie quotidienne fid\u00e8le.",
}

HOUR_DROPDOWN_FR = [
    {'short': 'Accueil', 'long': 'Accueil', 'text': 'Accueil'},
    {'short': '1\u00e8re Heure', 'long': '1\u00e8re Heure - Prime', 'text': '1\u00e8re Heure - Prime'},
    {'short': '3\u00e8me Heure', 'long': '3\u00e8me Heure - Tierce', 'text': '3\u00e8me Heure - Tierce'},
    {'short': '6\u00e8me Heure', 'long': '6\u00e8me Heure - Sexte', 'text': '6\u00e8me Heure - Sexte'},
    {'short': '9\u00e8me Heure', 'long': '9\u00e8me Heure - None', 'text': '9\u00e8me Heure - None'},
    {'short': '11\u00e8me Heure', 'long': '11\u00e8me Heure - V\u00eapres', 'text': '11\u00e8me Heure - V\u00eapres'},
    {'short': '12\u00e8me Heure', 'long': '12\u00e8me Heure - Complies', 'text': '12\u00e8me Heure - Complies'},
    {'short': 'Minuit', 'long': 'Minuit', 'text': 'Minuit'},
    {'short': 'Voile', 'long': 'Pri\u00e8re du Voile', 'text': 'Pri\u00e8re du Voile'},
    {'short': 'Autres', 'long': 'Autres Pri\u00e8res', 'text': 'Autres Pri\u00e8res'},
    {'short': '\u00c0 propos', 'long': '\u00c0 propos', 'text': '\u00c0 propos'},
]

NAV_LINKS_FR = {
    'Prime': 'Prime', 'Terce': 'Tierce', 'Sext': 'Sexte', 'None': 'None',
    'Vespers': 'V\u00eapres', 'Compline': 'Complies', 'Midnight': 'Minuit',
    'Veil': 'Voile', 'Other Prayers': 'Autres Pri\u00e8res', 'About': '\u00c0 propos',
}

SETTINGS_TOOLTIPS_FR = {
    'Comfy line spacing': 'Interligne confortable',
    'Default line spacing': 'Interligne standard',
    'Condensed line spacing': 'Interligne condens\u00e9',
}

HOME_CARDS_FR = {
    'Prime - 1st Hour': 'Prime - 1\u00e8re Heure',
    'Terce - 3rd Hour': 'Tierce - 3\u00e8me Heure',
    'Sext - 6th Hour': 'Sexte - 6\u00e8me Heure',
    'None - 9th Hour': 'None - 9\u00e8me Heure',
    'Vespers - 11th Hour': 'V\u00eapres - 11\u00e8me Heure',
    'Compline - 12th Hour': 'Complies - 12\u00e8me Heure',
    'Midnight': 'Minuit',
    'Prayer of the Veil': 'Pri\u00e8re du Voile',
    'Other Prayers': 'Autres Pri\u00e8res',
    'About the Agpeya': "\u00c0 propos de l'Agpia",
}

HOME_TIMES_FR = {
    '6:00 AM': '6h00', '9:00 AM': '9h00', '12:00 PM': '12h00',
    '3:00 PM': '15h00', '6:00 PM': '18h00', '9:00 PM': '21h00',
    '12:00 AM': '0h00', 'Special Prayer': 'Pri\u00e8re Sp\u00e9ciale',
    'Various Occasions': 'Diverses Occasions', 'Foreword': 'Avant-propos',
}

ABOUT_CONTENT = {
    'The Word Agpeya': [
        'Le mot <em>Agpia</em> (<span class="coptic-text">5agpia</span>) est dérivé du copte <em>Ti agp</em> (<span class="coptic-text">5agp</span>) qui signifie : l\u2019heure ; ainsi le copte <em>Ti agpeya</em> (<span class="coptic-text">5agpia</span>) signifie : le Livre des Heures.',
    ],
    'The Book of the Agpeya': [
        'Le livre contient les offices des sept heures canoniques utilisées par l\u2019Église copte orthodoxe. Il contient des Psaumes, des lectures évangéliques et des prières à dire à des heures spécifiques du jour et de la nuit, disposées conformément aux événements analogues de la vie du Seigneur Jésus-Christ. David le Prophète dit : \u00ab Sept fois par jour je Te loue à cause de Tes justes jugements \u00bb (Ps. 119:164) ; et le Seigneur ordonne : \u00ab Il faut toujours prier et ne point se lasser \u00bb (Luc 18:1).',
    ],
    'Why Do We Use the Agpeya for Praying?': [
        '<strong>S.S. le Pape Chenouda III écrit :</strong>',
        '\u2720 <em>Nous utilisons l\u2019Agpia pour prier en raison de la spiritualité et de l\u2019idéalisme de son contenu.</em>',
        '\u2720 <em>Avec l\u2019aide de l\u2019Agpia, nous apprenons comment formuler nos prières et la manière appropriée de parler à Dieu.</em>',
        '\u2720 <em>L\u2019Agpia nous enseigne à prier et à tout examiner avec soin. Une telle méthode nous permet d\u2019impliquer Dieu dans les détails de toute notre vie, car nous n\u2019omettons rien dans notre dialogue avec Lui.</em>',
        '\u2720 <em>Un fidèle qui a constamment accès à l\u2019Agpia pendant son temps de prière découvre de nombreux passages bibliques qui l\u2019assistent dans sa vie quotidienne et qui exercent une profonde influence sur ses sentiments et son comportement.</em>',
    ],
    'The Originality of the Agpeya': [
        "L\u2019incorporation de Psaumes, d\u2019Évangiles et de prières choisis dans le culte chrétien a été adoptée en premier par l\u2019Église copte d\u2019Alexandrie. Grâce à la paix relative dont elle a joui pendant les premier et deuxième siècles, l\u2019Église égyptienne, bien avant toute autre Église, a pu établir le schéma de ces heures canoniques. La structure et le contenu de l\u2019Agpia copte sont les descendants directs des heures canoniques originales qui étaient utilisées par les monastères cénobitiques (communautaires) qui ont vu le jour en Égypte au premier quart du quatrième siècle.",
    ],
    'The Agpeya and the Psalms': [
        "L\u2019élément principal dans la structure de l\u2019Agpia est une sélection de Psaumes spécialement arrangés pour correspondre au thème fondamental de l\u2019heure en question. Le <em>Livre des Psaumes</em> est considéré par l\u2019Église copte comme une source de trésors divins et un fleuve d\u2019édification et d\u2019enseignement spirituels qui couvre tous les aspects de la relation entre Dieu et l\u2019homme. C\u2019est pourquoi l\u2019Église a utilisé les Psaumes comme remède pour la vie des croyants et comme moyen d\u2019enflammer leurs c\u0153urs du feu de l\u2019amour divin.",
    ],
    'The Agpeya and Prayer': [
        "Les heures de l\u2019Agpia sont utilisées dans toutes sortes de prières : individuelles, familiales et congrégationnelles. Dans le service eucharistique, la prière de Minuit est récitée avant la louange de Minuit, laquelle est suivie de la prière du Matin. Puis, après le service d\u2019offrande d\u2019encens du Matin, les heures de Tierce, Sexte et, les jours de jeûne, de None sont incorporées. Les jours de Jonas et pendant le Carême, les Vêpres et Complies sont ajoutées, puis suit la Divine Liturgie. None, Vêpres et Complies précèdent l\u2019offrande d\u2019encens du Soir, tandis que les jours de jeûne, None n\u2019est pas récitée, car elle l\u2019est le matin.",
    ],
    'The Order of the Agpeya': [
        "Conformément à la pratique courante au temps du Christ (Jean 11:9), le jour est compté du lever au coucher du soleil ; ainsi, la première heure correspond à 6h, la troisième heure à 9h, la sixième heure à midi, la neuvième heure à 15h, et ainsi de suite (voir aussi Actes 2:15 ; 3:1 ; 10:3 ; 16:25). Le système des Psaumes des heures canoniques coptes est encore celui mentionné par saint Jean Cassien (c. 360 \u2013 435 apr. J.-C.) dans son <em>De Institutis</em> 2:4 ; à savoir, douze psaumes pour chaque heure. Cependant, sept psaumes supplémentaires sont ajoutés aux douze de l\u2019office de la prière du Matin, tandis que l\u2019office de la prière de Minuit est composé de trois nocturnes (veilles).",
    ],
    'Manner of Praying the Hours': [
        "Chacune des heures canoniques commence par le Notre Père, la prière d\u2019action de grâce et le Psaume 50. Suivent ensuite les Psaumes appropriés, la lecture de l\u2019Évangile et les litanies. Celles-ci sont suivies de <em>Kyrie eleison</em> 41 fois (représentant les trente-neuf coups de fouet (2 Cor. 11:24) du Seigneur, la lance et la couronne d\u2019épines), la pétition, \u00ab Saint, Saint, Saint, Seigneur Sabaoth\u2026 \u00bb, le Notre Père, l\u2019absolution, et en conclusion la supplication : \u00ab Aie pitié de nous, ô Dieu, et aie pitié de nous\u2026 \u00bb",
    ],
    'Themes of the Hours': [
        "1 \u2013 <strong>Prime :</strong> La prière du Matin est destinée à être priée tôt le matin, en référence à la venue de la vraie Lumière, le Seigneur Jésus-Christ. La Prime est principalement associée à l\u2019éternité de Dieu, Son incarnation et Sa résurrection d\u2019entre les morts. Elle vise à Lui rendre grâce de nous avoir relevés du sommeil, Le suppliant de briller sur nous, d\u2019illuminer nos vies et de nous accorder la puissance de Sa résurrection.",
        "2 \u2013 <strong>Tierce :</strong> La troisième heure commémore trois événements significatifs : le procès du Christ devant Pilate, Son ascension aux cieux et la descente du Saint-Esprit sur les disciples. Nous prions pour que la grâce du Saint-Esprit purifie nos c\u0153urs et renouvelle nos vies.",
        "3 \u2013 <strong>Sexte :</strong> La sixième heure nous rappelle la crucifixion et la passion du Christ. Nous prions pour que, par Sa passion vivifiante, Il délivre nos esprits des convoitises, tourne nos pensées vers le souvenir de Ses commandements, et fasse de nous la lumière du monde et le sel de la terre.",
        "4 \u2013 <strong>None :</strong> La neuvième heure commémore la mort rédemptrice du Christ dans la chair sur la croix et Son acceptation du repentir du Larron. Nous prions pour que le Sauveur mortifie nos convoitises charnelles, nous rende participants de Sa grâce et accepte notre repentir quand nous crions avec le Larron : \u00ab Souviens-toi de nous, Seigneur, quand Tu viendras dans Ton Royaume \u00bb (Luc 23:42).",
        "5 \u2013 <strong>Vêpres :</strong> La onzième heure est associée à la descente du corps du Christ de la croix. À la fin du jour, nous rendons grâce pour la protection de Dieu et confessons nos péchés avec le Fils Prodigue (Luc 15:11-31) afin d\u2019être comptés parmi les ouvriers appelés à la onzième heure du jour (Matt. 20:1-16).",
        "6 \u2013 <strong>Complies :</strong> La douzième heure commémore la sépulture du Christ. Nous nous souvenons du monde qui passe et du jugement dernier. Conscients de notre comparution imminente devant Dieu, nous demandons le pardon de nos péchés et la protection durant la nuit.",
        "7 \u2013 <strong>Minuit :</strong> Commémore le second avènement du Seigneur. L\u2019office consiste en trois nocturnes (veilles), correspondant aux trois étapes de la prière du Christ au jardin de Gethsémani (Matt. 25:1-13).",
        "8 \u2013 <strong>Le Voile :</strong> En plus de ces heures, il existe une autre prière appelée l\u2019office du Voile. La Didascalie prescrit qu\u2019elle soit lue par les évêques et les prêtres comme moyen d\u2019examiner le c\u0153ur avant le sommeil. Selon l\u2019Agpia, elle est destinée aux moines.",
    ],
    'Advice on How to Use the Agpeya': [
        "1. L\u2019Agpia est un livre de prière ; qu\u2019il soit le premier à être ouvert le matin. Cela orientera toute la journée vers Dieu et nous encouragera à utiliser le livre plusieurs fois par jour.",
        "2. Prier les heures est un moyen d\u2019examiner le c\u0153ur et de corriger ses défauts. C\u2019est pourquoi, en suivant l\u2019ordre de l\u2019Agpia, nous devons constamment purifier nos c\u0153urs par le repentir et l\u2019humilité, demeurer dans la vérité et aimer tous les hommes. Ainsi, notre ordre de prière sera efficace et fructueux.",
        "3. Les quelques minutes pendant lesquelles nous nous préparons à la prière par l\u2019examen du c\u0153ur, le repentir, la prostration et la contemplation ont une influence importante pour obtenir l\u2019esprit de prière.",
        "4. Les Psaumes sont une riche nourriture de l\u2019esprit ; aimons-les et prenons plaisir à les réciter fréquemment.",
        "5. La qualité du temps consacré à la prière importe plus que la quantité de psaumes récités. Vous pouvez consulter votre père spirituel : il est utile de comprendre le sens de la prière et d\u2019y réfléchir dans votre esprit.",
        "6. Les paroles des psaumes doivent être appliquées à vous-même, et être dites comme si elles étaient vos propres paroles, et non comme les dires d\u2019autrui.",
        "7. Ne passez pas d\u2019un mot à l\u2019autre et d\u2019un psaume à l\u2019autre sans saisir le sentiment et la vérité qu\u2019il porte. Essayez de comprendre le but de chaque mot et touchez-le avec votre c\u0153ur, afin d\u2019en expérimenter le sens caché et réel.",
        "8. À chaque mot qui vise l\u2019adoration, agenouillez-vous ou au moins inclinez la tête en révérence.",
        "9. Consacrez un temps pour vos propres prières exprimées par vous-même, dans lesquelles vous exprimez votre désir et votre amour brûlant envers Dieu. Lorsque vous priez Dieu avec vos propres mots ou des versets des psaumes, vous expérimenterez que joie et bonheur domineront votre vie.",
    ],
    '__psalm_note__': [
        '<strong>N.B.</strong> La numérotation des Psaumes dans ce <em>Livre des Heures Copte</em> (Agpia) suit la version copte de la Bible. Elle est en retard d\u2019un numéro par rapport aux autres versions publiées de la Bible. Par exemple, le Psaume 50 dans cet Agpia est le Psaume 51 dans les autres versions.',
    ],
}

def _translate_h2(h2, title, hour_name):
    """Translate a single h2 section title."""
    if title == 'Litanies' and hour_name in LITANIES_BY_HOUR:
        h2.string = LITANIES_BY_HOUR[hour_name]
    elif title == 'Absolution' and hour_name in ABSOLUTION_BY_HOUR:
        h2.string = ABSOLUTION_BY_HOUR[hour_name]
    elif title in TITLE_MAP:
        h2.string = TITLE_MAP[title]
    else:
        m = re.match(r'Psalm (\d+(?:\s*\([IVXLC]+\))?)', title)
        if m:
            h2.string = 'Psaume ' + m.group(1)


def translate_ui(soup, hour_name=None):
    """Translate all visible UI elements from English to French."""
    if hour_name == 'midnight':
        watch = 0
        for h2 in soup.find_all('h2', class_='section-title'):
            title = h2.get_text(strip=True)
            if title in ('The First Watch', 'The Second Watch', 'The Third Watch'):
                watch = {'The First Watch': 1, 'The Second Watch': 2,
                         'The Third Watch': 3}[title]
            if title == 'Litanies' and watch in MIDNIGHT_LITANIES_BY_WATCH:
                h2.string = MIDNIGHT_LITANIES_BY_WATCH[watch]
            else:
                _translate_h2(h2, title, hour_name)
    else:
        for h2 in soup.find_all('h2', class_='section-title'):
            title = h2.get_text(strip=True)
            _translate_h2(h2, title, hour_name)

    h1 = soup.find('h1', class_='hour-title')
    if h1:
        txt = h1.get_text(strip=True)
        if txt in H1_MAP:
            h1.string = H1_MAP[txt]

    title_tag = soup.find('title')
    if title_tag:
        txt = title_tag.get_text(strip=True)
        if txt in PAGE_TITLES:
            title_tag.string = PAGE_TITLES[txt]

    p_time = soup.find('p', class_='hour-time')
    if p_time:
        txt = p_time.get_text(strip=True)
        if txt in HOUR_TIME_MAP:
            p_time.string = HOUR_TIME_MAP[txt]

    if hour_name and hour_name in HOUR_DESC_FR:
        p_desc = soup.find('p', class_='hour-desc')
        if p_desc:
            p_desc.string = HOUR_DESC_FR[hour_name]

    dropdown = soup.find('select', id='hourDropdown')
    if dropdown:
        options = dropdown.find_all('option')
        for opt, fr_data in zip(options, HOUR_DROPDOWN_FR):
            opt['data-short'] = fr_data['short']
            opt['data-long'] = fr_data['long']
            opt.string = fr_data['text']

    for a in soup.find_all('a', class_='nav-hour'):
        div = a.find('div')
        if div:
            txt = div.get_text(strip=True)
            if txt in NAV_LINKS_FR:
                div.string = NAV_LINKS_FR[txt]

    light_btn = soup.find('button', id='lightModeBtn')
    if light_btn and light_btn.get_text(strip=True) == 'Light':
        light_btn.string = 'Clair'
    dark_btn = soup.find('button', id='darkModeBtn')
    if dark_btn and dark_btn.get_text(strip=True) == 'Dark':
        dark_btn.string = 'Sombre'

    for btn_id, eng_title in [('lineComfyBtn', 'Comfy line spacing'),
                               ('lineDefaultBtn', 'Default line spacing'),
                               ('lineCondensedBtn', 'Condensed line spacing')]:
        btn = soup.find('button', id=btn_id)
        if btn and btn.get('title') == eng_title:
            btn['title'] = SETTINGS_TOOLTIPS_FR[eng_title]

    sec_dropdown = soup.find('select', id='sectionDropdown')
    if sec_dropdown:
        top_opt = sec_dropdown.find('option', value='')
        if top_opt and top_opt.get_text(strip=True) == 'Top':
            top_opt.string = 'Haut'

    footer = soup.find('footer')
    if footer:
        for child in footer.descendants:
            if isinstance(child, NavigableString) and 'Coptic Book of Hours' in child:
                child.replace_with(child.replace('Coptic Book of Hours', 'Livre des Heures Copte'))


def translate_home(soup):
    """Translate index.html home page content."""
    hero_en = soup.find('div', class_='hero-title-en')
    if hero_en and 'The Agpeya' in hero_en.get_text():
        hero_en.string = "L'Agpia"

    h1 = soup.find('h1')
    if h1 and 'The Coptic Book of Hours' in h1.get_text():
        h1.string = 'Le Livre des Heures Copte'

    cta = soup.find('a', class_='cta')
    if cta and 'Begin Prayer' in cta.get_text():
        cta.string = 'Commencer la Pri\u00e8re \u2192'

    for card in soup.find_all('a', class_='hour-card'):
        name = card.find('h3', class_='hour-name')
        if name:
            txt = name.get_text(strip=True)
            if txt in HOME_CARDS_FR:
                name.string = HOME_CARDS_FR[txt]
        time_div = card.find('div', class_='hour-time')
        if time_div:
            txt = time_div.get_text(strip=True)
            if txt in HOME_TIMES_FR:
                time_div.string = HOME_TIMES_FR[txt]

    for script in soup.find_all('script'):
        if script.string and 'updateBeginPrayerButton' in script.string:
            js = script.string
            js = js.replace("label: '1st Hour'", "label: '1\u00e8re Heure'")
            js = js.replace("label: '3rd Hour'", "label: '3\u00e8me Heure'")
            js = js.replace("label: '6th Hour'", "label: '6\u00e8me Heure'")
            js = js.replace("label: '9th Hour'", "label: '9\u00e8me Heure'")
            js = js.replace("label: '11th Hour'", "label: '11\u00e8me Heure'")
            js = js.replace("label: '12th Hour'", "label: '12\u00e8me Heure'")
            js = js.replace("label: 'Midnight Hour'", "label: 'Minuit'")
            js = js.replace("'en-US'", "'fr-FR'")
            js = js.replace("hour12: true", "hour12: false")
            js = js.replace("`It's ${timeString} ${timezone}`",
                            "`Il est ${timeString} ${timezone}`")
            js = js.replace("`Pray ${closestHour.label} \u2192`",
                            "`Prier ${closestHour.label} \u2192`")
            script.string = js


def translate_about(soup):
    """Translate about.html content."""
    for section in soup.find_all('section', class_='section'):
        h2 = section.find('h2', class_='section-title')
        if h2:
            key = h2.get_text(strip=True)
        else:
            first_div = section.find('div', class_='prayer-text')
            if first_div and 'N.B.' in first_div.get_text():
                key = '__psalm_note__'
            else:
                continue

        if key not in ABOUT_CONTENT:
            continue

        fr_content = ABOUT_CONTENT[key]
        divs = section.find_all('div', class_='prayer-text')
        for i, div in enumerate(divs):
            if i < len(fr_content):
                div.clear()
                div.append(BeautifulSoup(fr_content[i], 'html.parser'))
