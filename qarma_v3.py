# QARMA Version 3 - "QARMA Thinks"
# sunana QARMA v3 - yanzu yana tunani kamar masanin kimiyya
# now QARMA thinks like a scientist
#
# sabon abu da na kara a v3 / new thing i added in v3:
#   - forgetting curve engine - yana san yaushe zaka manta
#   - forgetting curve engine - it knows when you will forget
#   - smart daily plan - yana gaya maka wane surahohi ka bita yau
#   - smart daily plan - tells you exactly which surahs to revise today
#   - multilanguage - Arabic, English, Hausa
#   - multilanguage - user picks their 2 preferred languages
#
# na koyi game da forgetting curve daga Hermann Ebbinghaus
# i learned about the forgetting curve from Hermann Ebbinghaus
# wani masanin kimiyya na Jamus wanda ya gano a 1885
# a German scientist who discovered it in 1885
#
# yadda yake aiki / how the forgetting curve works:
#   - idan ka haddace surah yau za ka manta da yawa cikin kwana 1
#   - if you memorize today you forget a lot within 1 day
#   - amma idan ka bita kafin ka manta - kwakwalwarka tana riƙe da tsawo
#   - but if you revise before forgetting - your brain holds it longer
#   - Kwana 1 → 3 → 7 → 21 → 60 → 180 → haddace har abada
#   - Day 1 → 3 → 7 → 21 → 60 → 180 → memorized forever

import json
import os
import random
from datetime import date, timedelta

# ina kokarin shigo da library din murya daga v2
# trying to import voice library from v2
try:
    import speech_recognition as sr
    VOICE_READY = True
except ImportError:
    VOICE_READY = False

MY_SAVE_FILE = "qarma_save.json"

# ----------------------------------------------------------
# zaɓin harshe - language selection
# mai amfani zai zaɓi harsunan 2 da yake son su
# user will pick 2 languages they want to use
# ----------------------------------------------------------
SUPPORTED_LANGUAGES = {
    "ar": "Arabic / العربية",
    "en": "English",
    "ha": "Hausa",
    "ff": "Fulfulde",
    "yo": "Yoruba",
    "ig": "Igbo",
    "kr": "Kanuri",
    "shu": "Shuwa Arab"
}

# ----------------------------------------------------------
# fassarar menu a harsuna daban daban
# menu translations in different languages
# zan kara karin fassarori daga baya inshallah
# i will add more translations later inshallah
# ----------------------------------------------------------
TRANSLATIONS = {
    "welcome": {
        "ar": "مرحباً بك في قارما",
        "en": "Welcome to QARMA",
        "ha": "Barka da zuwa QARMA",
        "ff": "Jaaraama e QARMA",
        "yo": "Kaabo si QARMA",
        "ig": "Nnọọ na QARMA",
        "kr": "Wurin zuwu QARMA",
        "shu": "مرحبا في قارما"
    },
    "start_revision": {
        "ar": "ابدأ المراجعة",
        "en": "Start Revision",
        "ha": "Fara Bita",
        "ff": "Fuɗɗit Taftaade",
        "yo": "Bẹrẹ Atunyẹwo",
        "ig": "Malite Ntugharia",
        "kr": "Fara Bita",
        "shu": "ابدأ المراجعة"
    },
    "mark_memorized": {
        "ar": "تسجيل المحفوظات",
        "en": "Mark Memorized",
        "ha": "Saka Surahohi",
        "ff": "Winndude Keɓɓiindi",
        "yo": "Samisi Ẹkọ",
        "ig": "Kọwaa Nke Ọ Mụtara",
        "kr": "Saka Surahohi",
        "shu": "تسجيل المحفوظات"
    },
    "view_progress": {
        "ar": "عرض التقدم",
        "en": "View Progress",
        "ha": "Duba Ci Gaba",
        "ff": "Yiy Laaɓital",
        "yo": "Wo Ilọsiwaju",
        "ig": "Hụ Ọganihu",
        "kr": "Duba Ci Gaba",
        "shu": "عرض التقدم"
    },
    "todays_plan": {
        "ar": "خطة اليوم",
        "en": "Today's Plan",
        "ha": "Shirin Yau",
        "ff": "Laawol Hannde",
        "yo": "Eto Oni",
        "ig": "Atụmatụ Taa",
        "kr": "Shirin Yau",
        "shu": "خطة اليوم"
    },
    "weak_surahs": {
        "ar": "السور الضعيفة",
        "en": "Weak Surahs",
        "ha": "Surahohi Rauni",
        "ff": "Suuwarɗe Raneeɗe",
        "yo": "Awọn Suratu Alailagbara",
        "ig": "Surahs Ndị Adịghị Ike",
        "kr": "Surahohi Rauni",
        "shu": "السور الضعيفة"
    },
    "quiz": {
        "ar": "اختبار",
        "en": "Quiz",
        "ha": "Wasan Tambaya",
        "ff": "Ñaawoore",
        "yo": "Idanwo",
        "ig": "Ule",
        "kr": "Wasan Tambaya",
        "shu": "اختبار"
    },
    "explanation": {
        "ar": "التفسير",
        "en": "Explanation",
        "ha": "Bayani",
        "ff": "Fassaraangal",
        "yo": "Alaye",
        "ig": "Nkọwa",
        "kr": "Bayani",
        "shu": "التفسير"
    },
    "voice_test": {
        "ar": "اختبار الصوت",
        "en": "Voice Test",
        "ha": "Gwajin Murya",
        "ff": "Ñaawoore Daande",
        "yo": "Idanwo Ohun",
        "ig": "Ule Olu",
        "kr": "Gwajin Murya",
        "shu": "اختبار الصوت"
    },
    "exit": {
        "ar": "خروج",
        "en": "Exit",
        "ha": "Fita",
        "ff": "Yaltude",
        "yo": "Jade",
        "ig": "Pụọ",
        "kr": "Fita",
        "shu": "خروج"
    },
    "correct": {
        "ar": "صحيح! أحسنت",
        "en": "Correct! MashaAllah",
        "ha": "Daidai! MashaAllah",
        "ff": "Tiindi! MashaAllah",
        "yo": "O tọ! MashaAllah",
        "ig": "Ọ dị mma! MashaAllah",
        "kr": "Daidai! MashaAllah",
        "shu": "صحيح! ماشاء الله"
    },
    "wrong": {
        "ar": "خطأ",
        "en": "Wrong",
        "ha": "Kuskure",
        "ff": "Faayre",
        "yo": "Aṣiṣe",
        "ig": "Nzuzu",
        "kr": "Kuskure",
        "shu": "خطأ"
    },
    "press_enter": {
        "ar": "اضغط Enter للمتابعة",
        "en": "Press Enter to continue",
        "ha": "Danna Enter don ci gaba",
        "ff": "Dif Enter ngam jokku",
        "yo": "Tẹ Enter lati tẹsiwaju",
        "ig": "Pịa Enter iji gaa n'ihu",
        "kr": "Danna Enter don ci gaba",
        "shu": "اضغط Enter للمتابعة"
    }
}

def t(key, lang1, lang2):
    # na yi wannan function don nuna fassarar a harsuna biyu
    # i made this function to show translation in 2 languages
    # idan harshe baya nan sai na dawo da turanci
    # if language not found i return english
    text1 = TRANSLATIONS.get(key, {}).get(lang1, TRANSLATIONS.get(key, {}).get("en", key))
    text2 = TRANSLATIONS.get(key, {}).get(lang2, TRANSLATIONS.get(key, {}).get("en", key))
    if lang1 == lang2:
        return text1
    return f"{text1} / {text2}"

# ----------------------------------------------------------
# duk surahin Quran 114 - All 114 surahs
# ----------------------------------------------------------
ALL_SURAHS = {
    1:   {"name": "Al-Fatihah",     "arabic": "الفاتحة",    "juz": 1},
    2:   {"name": "Al-Baqarah",     "arabic": "البقرة",     "juz": 1},
    3:   {"name": "Aal-Imran",      "arabic": "آل عمران",   "juz": 3},
    4:   {"name": "An-Nisa",        "arabic": "النساء",     "juz": 4},
    5:   {"name": "Al-Maidah",      "arabic": "المائدة",    "juz": 6},
    6:   {"name": "Al-Anam",        "arabic": "الأنعام",    "juz": 7},
    7:   {"name": "Al-Araf",        "arabic": "الأعراف",    "juz": 8},
    8:   {"name": "Al-Anfal",       "arabic": "الأنفال",    "juz": 9},
    9:   {"name": "At-Tawbah",      "arabic": "التوبة",     "juz": 10},
    10:  {"name": "Yunus",          "arabic": "يونس",       "juz": 11},
    11:  {"name": "Hud",            "arabic": "هود",        "juz": 11},
    12:  {"name": "Yusuf",          "arabic": "يوسف",       "juz": 12},
    13:  {"name": "Ar-Rad",         "arabic": "الرعد",      "juz": 13},
    14:  {"name": "Ibrahim",        "arabic": "إبراهيم",    "juz": 13},
    15:  {"name": "Al-Hijr",        "arabic": "الحجر",      "juz": 14},
    16:  {"name": "An-Nahl",        "arabic": "النحل",      "juz": 14},
    17:  {"name": "Al-Isra",        "arabic": "الإسراء",    "juz": 15},
    18:  {"name": "Al-Kahf",        "arabic": "الكهف",      "juz": 15},
    19:  {"name": "Maryam",         "arabic": "مريم",       "juz": 16},
    20:  {"name": "Ta-Ha",          "arabic": "طه",         "juz": 16},
    21:  {"name": "Al-Anbiya",      "arabic": "الأنبياء",   "juz": 17},
    22:  {"name": "Al-Hajj",        "arabic": "الحج",       "juz": 17},
    23:  {"name": "Al-Muminun",     "arabic": "المؤمنون",   "juz": 18},
    24:  {"name": "An-Nur",         "arabic": "النور",      "juz": 18},
    25:  {"name": "Al-Furqan",      "arabic": "الفرقان",    "juz": 18},
    26:  {"name": "Ash-Shuara",     "arabic": "الشعراء",    "juz": 19},
    27:  {"name": "An-Naml",        "arabic": "النمل",      "juz": 19},
    28:  {"name": "Al-Qasas",       "arabic": "القصص",      "juz": 20},
    29:  {"name": "Al-Ankabut",     "arabic": "العنكبوت",   "juz": 20},
    30:  {"name": "Ar-Rum",         "arabic": "الروم",      "juz": 21},
    31:  {"name": "Luqman",         "arabic": "لقمان",      "juz": 21},
    32:  {"name": "As-Sajdah",      "arabic": "السجدة",     "juz": 21},
    33:  {"name": "Al-Ahzab",       "arabic": "الأحزاب",    "juz": 21},
    34:  {"name": "Saba",           "arabic": "سبأ",        "juz": 22},
    35:  {"name": "Fatir",          "arabic": "فاطر",       "juz": 22},
    36:  {"name": "Ya-Sin",         "arabic": "يس",         "juz": 22},
    37:  {"name": "As-Saffat",      "arabic": "الصافات",    "juz": 23},
    38:  {"name": "Sad",            "arabic": "ص",          "juz": 23},
    39:  {"name": "Az-Zumar",       "arabic": "الزمر",      "juz": 23},
    40:  {"name": "Ghafir",         "arabic": "غافر",       "juz": 24},
    41:  {"name": "Fussilat",       "arabic": "فصلت",       "juz": 24},
    42:  {"name": "Ash-Shura",      "arabic": "الشورى",     "juz": 25},
    43:  {"name": "Az-Zukhruf",     "arabic": "الزخرف",     "juz": 25},
    44:  {"name": "Ad-Dukhan",      "arabic": "الدخان",     "juz": 25},
    45:  {"name": "Al-Jathiyah",    "arabic": "الجاثية",    "juz": 25},
    46:  {"name": "Al-Ahqaf",       "arabic": "الأحقاف",    "juz": 26},
    47:  {"name": "Muhammad",       "arabic": "محمد",       "juz": 26},
    48:  {"name": "Al-Fath",        "arabic": "الفتح",      "juz": 26},
    49:  {"name": "Al-Hujurat",     "arabic": "الحجرات",    "juz": 26},
    50:  {"name": "Qaf",            "arabic": "ق",          "juz": 26},
    51:  {"name": "Adh-Dhariyat",   "arabic": "الذاريات",   "juz": 26},
    52:  {"name": "At-Tur",         "arabic": "الطور",      "juz": 27},
    53:  {"name": "An-Najm",        "arabic": "النجم",      "juz": 27},
    54:  {"name": "Al-Qamar",       "arabic": "القمر",      "juz": 27},
    55:  {"name": "Ar-Rahman",      "arabic": "الرحمن",     "juz": 27},
    56:  {"name": "Al-Waqiah",      "arabic": "الواقعة",    "juz": 27},
    57:  {"name": "Al-Hadid",       "arabic": "الحديد",     "juz": 27},
    58:  {"name": "Al-Mujadila",    "arabic": "المجادلة",   "juz": 28},
    59:  {"name": "Al-Hashr",       "arabic": "الحشر",      "juz": 28},
    60:  {"name": "Al-Mumtahanah",  "arabic": "الممتحنة",   "juz": 28},
    61:  {"name": "As-Saf",         "arabic": "الصف",       "juz": 28},
    62:  {"name": "Al-Jumuah",      "arabic": "الجمعة",     "juz": 28},
    63:  {"name": "Al-Munafiqun",   "arabic": "المنافقون",  "juz": 28},
    64:  {"name": "At-Taghabun",    "arabic": "التغابن",    "juz": 28},
    65:  {"name": "At-Talaq",       "arabic": "الطلاق",     "juz": 28},
    66:  {"name": "At-Tahrim",      "arabic": "التحريم",    "juz": 28},
    67:  {"name": "Al-Mulk",        "arabic": "الملك",      "juz": 29},
    68:  {"name": "Al-Qalam",       "arabic": "القلم",      "juz": 29},
    69:  {"name": "Al-Haqqah",      "arabic": "الحاقة",     "juz": 29},
    70:  {"name": "Al-Maarij",      "arabic": "المعارج",    "juz": 29},
    71:  {"name": "Nuh",            "arabic": "نوح",        "juz": 29},
    72:  {"name": "Al-Jinn",        "arabic": "الجن",       "juz": 29},
    73:  {"name": "Al-Muzzammil",   "arabic": "المزمل",     "juz": 29},
    74:  {"name": "Al-Muddaththir", "arabic": "المدثر",     "juz": 29},
    75:  {"name": "Al-Qiyamah",     "arabic": "القيامة",    "juz": 29},
    76:  {"name": "Al-Insan",       "arabic": "الإنسان",    "juz": 29},
    77:  {"name": "Al-Mursalat",    "arabic": "المرسلات",   "juz": 29},
    78:  {"name": "An-Naba",        "arabic": "النبأ",      "juz": 30},
    79:  {"name": "An-Naziat",      "arabic": "النازعات",   "juz": 30},
    80:  {"name": "Abasa",          "arabic": "عبس",        "juz": 30},
    81:  {"name": "At-Takwir",      "arabic": "التكوير",    "juz": 30},
    82:  {"name": "Al-Infitar",     "arabic": "الانفطار",   "juz": 30},
    83:  {"name": "Al-Mutaffifin",  "arabic": "المطففين",   "juz": 30},
    84:  {"name": "Al-Inshiqaq",    "arabic": "الانشقاق",   "juz": 30},
    85:  {"name": "Al-Buruj",       "arabic": "البروج",     "juz": 30},
    86:  {"name": "At-Tariq",       "arabic": "الطارق",     "juz": 30},
    87:  {"name": "Al-Ala",         "arabic": "الأعلى",     "juz": 30},
    88:  {"name": "Al-Ghashiyah",   "arabic": "الغاشية",    "juz": 30},
    89:  {"name": "Al-Fajr",        "arabic": "الفجر",      "juz": 30},
    90:  {"name": "Al-Balad",       "arabic": "البلد",      "juz": 30},
    91:  {"name": "Ash-Shams",      "arabic": "الشمس",      "juz": 30},
    92:  {"name": "Al-Layl",        "arabic": "الليل",      "juz": 30},
    93:  {"name": "Ad-Duha",        "arabic": "الضحى",      "juz": 30},
    94:  {"name": "Ash-Sharh",      "arabic": "الشرح",      "juz": 30},
    95:  {"name": "At-Tin",         "arabic": "التين",      "juz": 30},
    96:  {"name": "Al-Alaq",        "arabic": "العلق",      "juz": 30},
    97:  {"name": "Al-Qadr",        "arabic": "القدر",      "juz": 30},
    98:  {"name": "Al-Bayyinah",    "arabic": "البينة",     "juz": 30},
    99:  {"name": "Az-Zalzalah",    "arabic": "الزلزلة",    "juz": 30},
    100: {"name": "Al-Adiyat",      "arabic": "العاديات",   "juz": 30},
    101: {"name": "Al-Qariah",      "arabic": "القارعة",    "juz": 30},
    102: {"name": "At-Takathur",    "arabic": "التكاثر",    "juz": 30},
    103: {"name": "Al-Asr",         "arabic": "العصر",      "juz": 30},
    104: {"name": "Al-Humazah",     "arabic": "الهمزة",     "juz": 30},
    105: {"name": "Al-Fil",         "arabic": "الفيل",      "juz": 30},
    106: {"name": "Quraysh",        "arabic": "قريش",       "juz": 30},
    107: {"name": "Al-Maun",        "arabic": "الماعون",    "juz": 30},
    108: {"name": "Al-Kawthar",     "arabic": "الكوثر",     "juz": 30},
    109: {"name": "Al-Kafirun",     "arabic": "الكافرون",   "juz": 30},
    110: {"name": "An-Nasr",        "arabic": "النصر",      "juz": 30},
    111: {"name": "Al-Masad",       "arabic": "المسد",      "juz": 30},
    112: {"name": "Al-Ikhlas",      "arabic": "الإخلاص",    "juz": 30},
    113: {"name": "Al-Falaq",       "arabic": "الفلق",      "juz": 30},
    114: {"name": "An-Nas",         "arabic": "الناس",      "juz": 30},
}

# bayani a harsuna 3 - explanation in 3 languages
# Arabic, English, Hausa
# zan kara harsuna bayan an tabbatar da fassarar
# i will add more languages after translations are verified
SURAH_EXPLANATION = {
    1:   {"ar": "الفاتحة هي مفتاح القرآن. نقرأها في كل صلاة. معناها أننا نسأل الله أن يهدينا الصراط المستقيم.", "en": "Al-Fatihah is the opening of the Quran. We read it in every prayer. It means we ask Allah to guide us to the straight path.", "ha": "Al-Fatihah ita ce mabudin Kur'ani. Muna karanta ta a kowace salah. Ma'anarta ita ce muna rokon Allah ya shiryar da mu hanya madaidaiciya."},
    18:  {"ar": "الكهف تُقرأ كل جمعة. تحمي قارئها من فتنة الدجال. تحتوي على قصص عظيمة.", "en": "Al-Kahf is read every Friday. It protects from the trial of Dajjal. It contains great stories.", "ha": "Al-Kahf ana karanta ta kowace Jumma'a. Tana kare mai karanta ta daga fitinar Dajjal."},
    36:  {"ar": "يس تُسمى قلب القرآن. من قرأها يسّر الله أمره.", "en": "Ya-Sin is called the heart of the Quran. Whoever reads it Allah makes his affairs easy.", "ha": "Ya-Sin ana kiranta da zuciyar Kur'ani. Duk wanda ya karanta ta Allah zai sassauta masa harkokinsa."},
    55:  {"ar": "الرحمن تُسمى عروس القرآن. الله يعدد نعمه على عباده.", "en": "Ar-Rahman is called the bride of the Quran. Allah lists His blessings upon His servants.", "ha": "Ar-Rahman ana kiranta da aro jar Kur'ani. Allah yana lissafa ni'imomin da Ya yi wa bayin Sa."},
    67:  {"ar": "الملك تحمي قارئها من عذاب القبر. نقرأها كل ليلة.", "en": "Al-Mulk protects from punishment of the grave. We read it every night.", "ha": "Al-Mulk tana kare mai karanta ta daga azabar kabari. Muna karanta ta kowace dare."},
    112: {"ar": "الإخلاص تتحدث عن التوحيد. ثوابها يعادل ثلث القرآن.", "en": "Al-Ikhlas is about Tawheed. Its reward equals one third of the Quran.", "ha": "Al-Ikhlas tana magana ne akan tauhidi. Tana daidai da kashi daya bisa uku na Kur'ani wajen lada."},
    113: {"ar": "الفلق تطلب الحماية من شر كل شيء ومن السحر والحسد.", "en": "Al-Falaq seeks protection from evil of all creation, magic and envy.", "ha": "Al-Falaq tana neman tsari daga sharrin duk wani abu, daga sihiri, da daga masu kishi."},
    114: {"ar": "الناس تطلب الحماية من وسواس الشيطان في صدور الناس والجن.", "en": "An-Nas seeks protection from the whisperer who whispers into hearts of mankind and jinn.", "ha": "An-Nas tana neman tsari daga sharrin shaiɗan wanda yake zuga zukatan mutane da aljanu."},
}


# ----------------------------------------------------------
# BABBAN SABON ABU NA V3 - THE BIG NEW THING IN V3
# forgetting curve engine
#
# na yi amfani da algorithm mai suna SM2
# i used an algorithm called SM2
# wannan shine algorithm din da Anki ke amfani da shi
# this is the same algorithm that Anki uses
#
# intervals - kwannakin da ake jira kafin bita
# intervals - the days to wait before next revision:
#   Bita na 1: kwana 1  / Revision 1: day 1
#   Bita na 2: kwana 3  / Revision 2: day 3
#   Bita na 3: kwana 7  / Revision 3: day 7
#   Bita na 4: kwana 21 / Revision 4: day 21
#   Bita na 5: kwana 60 / Revision 5: day 60
#   Bita na 6: kwana 180/ Revision 6: day 180
# ----------------------------------------------------------

# jadawalin kwannakin bita - the revision interval schedule
INTERVALS = [1, 3, 7, 21, 60, 180]

def calculate_next_revision(record):
    # yanke hukunci akan ranar bita mai zuwa
    # decide the next revision date
    times = record.get("times_revised", 0)
    if times < len(INTERVALS):
        days = INTERVALS[times]
    else:
        # bayan kammala duk matakun - after completing all stages
        # ya haddace sosai - fully memorized
        days = 365
    last = record.get("last_date")
    if last is None:
        # idan bai taba bita ba - if never revised
        return str(date.today())
    last_date = date.fromisoformat(last)
    next_date = last_date + timedelta(days=days)
    return str(next_date)

def is_due_today(record):
    # duba idan surah tana bukatar bita yau
    # check if surah needs revision today
    next_revision = calculate_next_revision(record)
    next_date = date.fromisoformat(next_revision)
    return next_date <= date.today()

def days_until_revision(record):
    # nawa kwanaki har bita mai zuwa
    # how many days until next revision
    next_revision = calculate_next_revision(record)
    next_date = date.fromisoformat(next_revision)
    delta = (next_date - date.today()).days
    return max(0, delta)

def days_overdue(record):
    # nawa kwanaki da ya wuce lokacin bita
    # how many days past the revision date
    next_revision = calculate_next_revision(record)
    next_date = date.fromisoformat(next_revision)
    delta = (date.today() - next_date).days
    return max(0, delta)


# ----------------------------------------------------------
# loda da adana bayanai - load and save
# ----------------------------------------------------------
def load_my_data():
    if os.path.exists(MY_SAVE_FILE):
        with open(MY_SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "my_name": "",
        "lang1": "en",
        "lang2": "ha",
        "start_date": str(date.today()),
        "streak": 0,
        "last_session_date": None,
        "surahs": {}
    }

def save_my_data(my_data):
    with open(MY_SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(my_data, f, ensure_ascii=False, indent=2)

def get_surah_info(my_data, surah_num):
    key = str(surah_num)
    if key not in my_data["surahs"]:
        my_data["surahs"][key] = {
            "memorized": False,
            "score": 0,
            "times_revised": 0,
            "voice_attempts": 0,
            "voice_passed": 0,
            "last_date": None,
            "next_revision": None,
            "my_note": ""
        }
    return my_data["surahs"][key]

def update_my_score(surah_record, rating):
    old_score = surah_record["score"]
    if rating == 1:
        surah_record["score"] = max(0, old_score - 2)
        # idan ya manta - reset interval
        # if forgot - reset the interval back
        surah_record["times_revised"] = max(0, surah_record["times_revised"] - 2)
    elif rating == 2:
        surah_record["score"] = max(0, old_score - 1)
        surah_record["times_revised"] = max(0, surah_record["times_revised"] - 1)
    elif rating == 3:
        surah_record["score"] = old_score
    elif rating == 4:
        surah_record["score"] = min(5, old_score + 1)
        surah_record["times_revised"] += 1
    elif rating == 5:
        surah_record["score"] = min(5, old_score + 2)
        surah_record["times_revised"] += 1
    surah_record["last_date"] = str(date.today())
    surah_record["next_revision"] = calculate_next_revision(surah_record)

def show_strength(score):
    bars = "█" * score + "░" * (5 - score)
    labels = ["Very Weak🔴", "Weak🟠", "Fair🟡", "Good🟢", "Strong🔵", "Mastered⭐"]
    return f"[{bars}] {labels[score]}"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_title(my_data):
    l1 = my_data.get("lang1", "en")
    l2 = my_data.get("lang2", "ha")
    print("=" * 62)
    print("  🕌  QARMA v3 - Quran Revision & Memorization Assistant")
    print("           بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ")
    print(f"  🌐 {SUPPORTED_LANGUAGES.get(l1,'English')} + {SUPPORTED_LANGUAGES.get(l2,'Hausa')}")
    print("=" * 62)

def update_streak(my_data):
    # sabunta silsila - update the daily streak
    today = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))
    last = my_data.get("last_session_date")
    if last == today:
        pass  # an riga an kidaya yau - already counted today
    elif last == yesterday:
        my_data["streak"] = my_data.get("streak", 0) + 1
    else:
        my_data["streak"] = 1  # sake farawa - restart streak
    my_data["last_session_date"] = today


# ----------------------------------------------------------
# zaɓin harshe - language selection setup
# ----------------------------------------------------------
def setup_language(my_data):
    clear_screen()
    show_title(my_data)
    print("\n  🌐 ZAƁI HARSUNANKA 2 / CHOOSE YOUR 2 LANGUAGES\n")
    langs = list(SUPPORTED_LANGUAGES.items())
    for i, (code, name) in enumerate(langs, 1):
        print(f"  {i}. {name}")

    print("\n  Harshe na farko / First language:")
    while True:
        try:
            c1 = int(input("  > "))
            if 1 <= c1 <= len(langs):
                break
        except:
            pass
    lang1_code = langs[c1-1][0]

    print("\n  Harshe na biyu / Second language:")
    while True:
        try:
            c2 = int(input("  > "))
            if 1 <= c2 <= len(langs):
                break
        except:
            pass
    lang2_code = langs[c2-1][0]

    my_data["lang1"] = lang1_code
    my_data["lang2"] = lang2_code
    save_my_data(my_data)
    print(f"\n  ✅ {SUPPORTED_LANGUAGES[lang1_code]} + {SUPPORTED_LANGUAGES[lang2_code]}")
    input(f"\n  {t('press_enter', lang1_code, lang2_code)}...")


# ----------------------------------------------------------
# shirin yau - TODAY'S SMART PLAN
# wannan shine zuciyar v3 - this is the heart of v3
# yana gaya maka daidai wane surahohi ka bita yau
# it tells you exactly which surahs to revise today
# bisa ga forgetting curve - based on the forgetting curve
# ----------------------------------------------------------
def todays_plan(my_data):
    clear_screen()
    l1 = my_data.get("lang1", "en")
    l2 = my_data.get("lang2", "ha")
    show_title(my_data)

    memorized = [n for n in ALL_SURAHS if get_surah_info(my_data, n)["memorized"]]

    if not memorized:
        print("\n  ⚠️  Ba ka saka kowane surah ba tukuna!")
        print("  No surahs marked yet! Use option 2 first.\n")
        input(f"  {t('press_enter', l1, l2)}...")
        return

    # raba surahohi zuwa rukunoni 3
    # divide surahs into 3 groups

    # rukuni 1 - sun wuce lokaci - overdue
    overdue = []
    # rukuni 2 - yau ne lokacin su - due today
    due_today = []
    # rukuni 3 - har yanzu ba lokacin su - not yet due
    upcoming = []

    for n in memorized:
        rec = get_surah_info(my_data, n)
        overdue_days = days_overdue(rec)
        if overdue_days > 0:
            overdue.append((n, overdue_days))
        elif is_due_today(rec):
            due_today.append(n)
        else:
            upcoming.append((n, days_until_revision(rec)))

    # tsara mafi wuce lokaci ya zo farko
    # sort most overdue comes first
    overdue.sort(key=lambda x: x[1], reverse=True)
    upcoming.sort(key=lambda x: x[1])

    print(f"\n  📅 {t('todays_plan', l1, l2).upper()} — {date.today()}\n")

    # nuna silsila - show streak
    streak = my_data.get("streak", 0)
    if streak > 0:
        fire = "🔥" * min(streak, 10)
        print(f"  Silsila / Streak: {fire} {streak} days!\n")

    # nuna surahohin da suka wuce lokaci
    # show overdue surahs
    if overdue:
        print(f"  🚨 SUN WUCE LOKACI / OVERDUE ({len(overdue)} surahs):")
        for n, days in overdue[:5]:
            s = ALL_SURAHS[n]
            print(f"  ⚠️  Surah {n}: {s['name']} ({s['arabic']}) — {days} days overdue!")
        print()

    # nuna surahohin yau - show today's surahs
    if due_today:
        print(f"  ✅ YAU / DUE TODAY ({len(due_today)} surahs):")
        for n in due_today:
            s = ALL_SURAHS[n]
            rec = get_surah_info(my_data, n)
            print(f"  📖 Surah {n}: {s['name']} ({s['arabic']}) — {show_strength(rec['score'])}")
        print()

    # nuna masu zuwa - show upcoming
    if upcoming:
        print(f"  🔮 MAI ZUWA / UPCOMING (next 7 days):")
        for n, days in upcoming[:5]:
            if days <= 7:
                s = ALL_SURAHS[n]
                print(f"  📅 Surah {n}: {s['name']} — in {days} day(s)")
        print()

    if not overdue and not due_today:
        print("  🌟 Babu bita yau! / No revision due today!")
        print("  Ka huta! Ka yi aiki sosai! / Rest! You worked hard!")
        print()

    # nuna jimlar surahohi - show summary numbers
    total_mem = len(memorized)
    total_mastered = sum(1 for n in memorized if get_surah_info(my_data, n)["score"] >= 5)
    print(f"  📊 Jimla / Summary: {total_mem} memorized | {total_mastered} mastered | {len(overdue)+len(due_today)} due")

    input(f"\n  {t('press_enter', l1, l2)}...")


# ----------------------------------------------------------
# lokacin bita - revision session
# yanzu yana bita surahohin da suka wuce lokaci da na yau
# now revises overdue and today's due surahs first
# ----------------------------------------------------------
def start_revision(my_data):
    clear_screen()
    l1 = my_data.get("lang1", "en")
    l2 = my_data.get("lang2", "ha")
    show_title(my_data)

    memorized = [n for n in ALL_SURAHS if get_surah_info(my_data, n)["memorized"]]
    if not memorized:
        print(f"\n  ⚠️  {t('mark_memorized', l1, l2)} first!\n")
        input(f"  {t('press_enter', l1, l2)}...")
        return

    # zabi surahohin da suka fi bukatar bita
    # pick surahs that need revision most urgently
    due = []
    for n in memorized:
        rec = get_surah_info(my_data, n)
        if is_due_today(rec):
            overdue = days_overdue(rec)
            due.append((n, overdue))

    # idan babu surahohin yau sai a dauki mafi rauni
    # if no surahs due today take the weakest ones
    if not due:
        memorized.sort(key=lambda n: get_surah_info(my_data, n)["score"])
        queue = memorized[:3]
        print(f"\n  ✅ Babu bita yau! Amma za mu bita mafi rauni 3.")
        print(f"  No revision due! But let us revise the 3 weakest.\n")
    else:
        due.sort(key=lambda x: x[1], reverse=True)
        queue = [n for n, _ in due[:5]]
        print(f"\n  🔁 {t('start_revision', l1, l2).upper()}\n")
        print(f"  Surahohi {len(queue)} suna bukatar bita yau!")
        print(f"  {len(queue)} surahs need revision today!\n")

    for n in queue:
        s = ALL_SURAHS[n]
        rec = get_surah_info(my_data, n)
        print(f"  • Surah {n}: {s['name']} ({s['arabic']}) — {show_strength(rec['score'])}")

    input(f"\n  {t('press_enter', l1, l2)} to start...")

    for n in queue:
        clear_screen()
        show_title(my_data)
        rec = get_surah_info(my_data, n)
        s = ALL_SURAHS[n]
        overdue = days_overdue(rec)
        days_left = days_until_revision(rec)

        print(f"\n  📖 Surah {n}: {s['name']} ({s['arabic']}) — Juz {s['juz']}")
        print(f"  Karfi / Strength: {show_strength(rec['score'])}")
        if overdue > 0:
            print(f"  ⚠️  Ya wuce kwanaki {overdue} / {overdue} days overdue!")
        else:
            print(f"  ✅ An shirya yau / Due today")

        # nuna bita mai zuwa bayan wannan
        # show when next revision will be after this one
        next_interval = INTERVALS[min(rec['times_revised'], len(INTERVALS)-1)]
        next_date = date.today() + timedelta(days=next_interval)
        print(f"  🔮 Bita mai zuwa / Next revision: {next_date} (in {next_interval} days)")

        # nuna bayani - show explanation
        if n in SURAH_EXPLANATION:
            exp = SURAH_EXPLANATION[n]
            text1 = exp.get(l1, exp.get("en", ""))
            text2 = exp.get(l2, exp.get("ha", ""))
            if text1:
                print(f"\n  [{SUPPORTED_LANGUAGES.get(l1,'').split('/')[0].strip()}]:")
                print(f"  {text1}")
            if text2 and l2 != l1:
                print(f"\n  [{SUPPORTED_LANGUAGES.get(l2,'').split('/')[0].strip()}]:")
                print(f"  {text2}")

        print(f"\n  ─────────────────────────────────────────────────")
        print(f"  Ka karanta surah / Recite the surah now")
        print(f"  1=Manta/Forgot  2=Wahala/Hard  3=Ok  4=Kyau/Good  5=Cikakke/Perfect")

        while True:
            try:
                rating = int(input(f"\n  Maki/Rating [1-5]: "))
                if 1 <= rating <= 5:
                    break
            except:
                pass

        update_my_score(rec, rating)
        save_my_data(my_data)

        emojis = {1: "😞", 2: "😟", 3: "😐", 4: "😊", 5: "🌟"}
        new_next = calculate_next_revision(rec)
        print(f"\n  {emojis[rating]} {show_strength(rec['score'])}")
        print(f"  🔮 Bita mai zuwa / Next revision: {new_next}")
        input(f"\n  {t('press_enter', l1, l2)}...")

    update_streak(my_data)
    save_my_data(my_data)
    clear_screen()
    show_title(my_data)
    streak = my_data.get("streak", 0)
    print(f"\n  ✅ Kammala! / Done! Ka bita {len(queue)} surahs.")
    print(f"  🔥 Silsila / Streak: {streak} days! Baarakallahu Feek! 🌙")
    input(f"\n  {t('press_enter', l1, l2)}...")


# ----------------------------------------------------------
# sauran ayyuka - other functions (same as v1/v2)
# ----------------------------------------------------------
def first_time_setup(my_data):
    clear_screen()
    show_title(my_data)
    print(f"\n  {t('welcome', 'en', 'ha')} v3!\n")
    name = input("  Sunanka / Your name: ").strip() or "Dan Kur'ani"
    my_data["my_name"] = name
    save_my_data(my_data)
    setup_language(my_data)

def mark_memorized(my_data):
    l1 = my_data.get("lang1", "en")
    l2 = my_data.get("lang2", "ha")
    clear_screen()
    show_title(my_data)
    print(f"\n  📖 {t('mark_memorized', l1, l2).upper()}\n")
    print("  Misali/Example: 1,112,113,114  or  juz30\n")
    user_input = input("  > ").strip()
    nums = []
    if user_input.lower() == "juz30":
        nums = list(range(78, 115))
    else:
        for p in user_input.split(","):
            p = p.strip()
            if p.isdigit() and 1 <= int(p) <= 114:
                nums.append(int(p))
    count = 0
    for n in nums:
        rec = get_surah_info(my_data, n)
        rec["memorized"] = True
        if rec["last_date"] is None:
            rec["last_date"] = str(date.today())
            rec["next_revision"] = calculate_next_revision(rec)
        count += 1
    save_my_data(my_data)
    print(f"\n  ✅ {count} surahs marked!")
    input(f"\n  {t('press_enter', l1, l2)}...")

def view_progress(my_data):
    l1 = my_data.get("lang1", "en")
    l2 = my_data.get("lang2", "ha")
    clear_screen()
    show_title(my_data)
    print(f"\n  📊 {t('view_progress', l1, l2).upper()}\n")
    memorized = [n for n in ALL_SURAHS if get_surah_info(my_data, n)["memorized"]]
    total = len(memorized)
    mastered = sum(1 for n in memorized if get_surah_info(my_data, n)["score"] >= 5)
    due = sum(1 for n in memorized if is_due_today(get_surah_info(my_data, n)))
    bar = "█" * int((total/114)*30) + "░" * (30 - int((total/114)*30))
    print(f"  [{bar}] {total}/114 ({round(total/114*100,1)}%)")
    print(f"\n  ⭐ Mastered: {mastered} | 📖 Due today: {due} | 🔥 Streak: {my_data.get('streak',0)} days")
    if memorized:
        juz_groups = {}
        for n in memorized:
            j = ALL_SURAHS[n]["juz"]
            juz_groups.setdefault(j, []).append(n)
        print(f"\n  {'Juz':<6} Surahs")
        print(f"  {'-'*50}")
        for j in sorted(juz_groups):
            names = ", ".join(ALL_SURAHS[n]["name"] for n in sorted(juz_groups[j]))
            print(f"  Juz {j:<3}: {names}")
    input(f"\n  {t('press_enter', l1, l2)}...")

def show_weak_surahs(my_data):
    l1 = my_data.get("lang1", "en")
    l2 = my_data.get("lang2", "ha")
    clear_screen()
    show_title(my_data)
    print(f"\n  ⚠️  {t('weak_surahs', l1, l2).upper()}\n")
    memorized = [n for n in ALL_SURAHS if get_surah_info(my_data, n)["memorized"]]
    if not memorized:
        print("  No surahs yet.\n")
        input(f"  {t('press_enter', l1, l2)}...")
        return
    memorized.sort(key=lambda n: get_surah_info(my_data, n)["score"])
    print(f"  {'#':<5} {'Surah':<20} {'Arabic':<16} {'Strength'}")
    print(f"  {'-'*60}")
    for n in memorized[:10]:
        rec = get_surah_info(my_data, n)
        s = ALL_SURAHS[n]
        print(f"  {n:<5} {s['name']:<20} {s['arabic']:<16} {show_strength(rec['score'])}")
    input(f"\n  {t('press_enter', l1, l2)}...")

def quiz_me(my_data):
    l1 = my_data.get("lang1", "en")
    l2 = my_data.get("lang2", "ha")
    clear_screen()
    show_title(my_data)
    memorized = [n for n in ALL_SURAHS if get_surah_info(my_data, n)["memorized"]]
    if len(memorized) < 4:
        print(f"\n  ⚠️  Need at least 4 surahs!\n")
        input(f"  {t('press_enter', l1, l2)}...")
        return
    print(f"\n  🎯 {t('quiz', l1, l2).upper()}\n")
    correct_num = random.choice(memorized)
    correct = ALL_SURAHS[correct_num]
    q_type = random.choice(["juz", "arabic", "number"])
    answered_correct = False
    if q_type == "juz":
        print(f"  Surah {correct['name']} — wane Juz? / which Juz?\n")
        wrong = random.sample([j for j in range(1,31) if j != correct["juz"]], 3)
        options = [correct["juz"]] + wrong
        random.shuffle(options)
        for i, o in enumerate(options, 1):
            print(f"  {i}. Juz {o}")
        while True:
            try:
                ans = int(input("\n  > "))
                if 1 <= ans <= 4:
                    break
            except:
                pass
        if options[ans-1] == correct["juz"]:
            answered_correct = True
    elif q_type == "arabic":
        print(f"  Wannan larabcin na wace surah? / Which surah?  {correct['arabic']}\n")
        wrong = random.sample([n for n in memorized if n != correct_num], min(3, len(memorized)-1))
        options = [correct_num] + wrong
        random.shuffle(options)
        for i, n in enumerate(options, 1):
            print(f"  {i}. {ALL_SURAHS[n]['name']}")
        while True:
            try:
                ans = int(input("\n  > "))
                if 1 <= ans <= len(options):
                    break
            except:
                pass
        if options[ans-1] == correct_num:
            answered_correct = True
    else:
        print(f"  Surah mai lamba {correct_num} — sunainta? / Name of Surah {correct_num}?\n")
        wrong = random.sample([n for n in memorized if n != correct_num], min(3, len(memorized)-1))
        options = [correct_num] + wrong
        random.shuffle(options)
        for i, n in enumerate(options, 1):
            print(f"  {i}. {ALL_SURAHS[n]['name']} ({ALL_SURAHS[n]['arabic']})")
        while True:
            try:
                ans = int(input("\n  > "))
                if 1 <= ans <= len(options):
                    break
            except:
                pass
        if options[ans-1] == correct_num:
            answered_correct = True
    if answered_correct:
        print(f"\n  ✅ {t('correct', l1, l2)}! 🌟")
        update_my_score(get_surah_info(my_data, correct_num), 5)
    else:
        print(f"\n  ❌ {t('wrong', l1, l2)}! Answer: {correct['name']}")
        update_my_score(get_surah_info(my_data, correct_num), 1)
    save_my_data(my_data)
    input(f"\n  {t('press_enter', l1, l2)}...")

def read_explanation(my_data):
    l1 = my_data.get("lang1", "en")
    l2 = my_data.get("lang2", "ha")
    clear_screen()
    show_title(my_data)
    print(f"\n  📚 {t('explanation', l1, l2).upper()}\n")
    for n in sorted(SURAH_EXPLANATION.keys()):
        print(f"  {n}. {ALL_SURAHS[n]['name']} ({ALL_SURAHS[n]['arabic']})")
    print()
    try:
        n = int(input("  Surah number: "))
    except:
        n = 0
    if n in SURAH_EXPLANATION:
        exp = SURAH_EXPLANATION[n]
        s = ALL_SURAHS[n]
        print(f"\n  {'='*50}")
        print(f"  Surah {n}: {s['name']} {s['arabic']} — Juz {s['juz']}")
        print(f"  {'='*50}")
        for lang_code in [l1, l2]:
            text = exp.get(lang_code, "")
            if text:
                lang_name = SUPPORTED_LANGUAGES.get(lang_code, "").split("/")[0].strip()
                print(f"\n  [{lang_name}]:\n  {text}")
    else:
        print("\n  No explanation yet. Coming soon inshallah!")
    input(f"\n  {t('press_enter', l1, l2)}...")


# ----------------------------------------------------------
# babban menu v3 - main menu
# ----------------------------------------------------------
def main():
    my_data = load_my_data()
    if my_data["my_name"] == "":
        first_time_setup(my_data)
    l1 = my_data.get("lang1", "en")
    l2 = my_data.get("lang2", "ha")

    while True:
        clear_screen()
        show_title(my_data)
        l1 = my_data.get("lang1", "en")
        l2 = my_data.get("lang2", "ha")
        name = my_data["my_name"]
        memorized = sum(1 for n in ALL_SURAHS if get_surah_info(my_data, n)["memorized"])
        due = sum(1 for n in ALL_SURAHS
                  if get_surah_info(my_data, n)["memorized"]
                  and is_due_today(get_surah_info(my_data, n)))
        streak = my_data.get("streak", 0)

        print(f"\n  👤 {name}  |  📖 {memorized}/114  |  🔥 {streak} days  |  📅 {due} due today")
        print()
        print("  ┌────────────────────────────────────────────────┐")
        print(f"  │  1. 🔁  {t('start_revision', l1, l2):<38}│")
        print(f"  │  2. 📖  {t('mark_memorized', l1, l2):<38}│")
        print(f"  │  3. 📅  {t('todays_plan', l1, l2):<38}│")
        print(f"  │  4. 📊  {t('view_progress', l1, l2):<38}│")
        print(f"  │  5. ⚠️   {t('weak_surahs', l1, l2):<38}│")
        print(f"  │  6. 🎯  {t('quiz', l1, l2):<38}│")
        print(f"  │  7. 📚  {t('explanation', l1, l2):<38}│")
        print(f"  │  8. 🌐  Change Languages                       │")
        print(f"  │  9. 🚪  {t('exit', l1, l2):<38}│")
        print("  └────────────────────────────────────────────────┘")

        choice = input("\n  > ").strip()

        if choice == "1":
            start_revision(my_data)
        elif choice == "2":
            mark_memorized(my_data)
        elif choice == "3":
            todays_plan(my_data)
        elif choice == "4":
            view_progress(my_data)
        elif choice == "5":
            show_weak_surahs(my_data)
        elif choice == "6":
            quiz_me(my_data)
        elif choice == "7":
            read_explanation(my_data)
        elif choice == "8":
            setup_language(my_data)
            l1 = my_data.get("lang1", "en")
            l2 = my_data.get("lang2", "ha")
        elif choice == "9":
            clear_screen()
            print("\n  Ma'assalama! Goodbye! 🌙")
            print("  Allah Ya karbi aikinmu. Ameen.\n")
            break


if __name__ == "__main__":
    main()
