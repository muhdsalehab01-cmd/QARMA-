# ╔══════════════════════════════════════════════════════════════════╗
# ║                         QARMA                                  ║
# ║         Quran AI Revision & Memorization Assistant              ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# QARMA Version 2 - "QARMA Speaks"
# wannan sabon sigar QARMA ce wadda zata iya ji muryarka
# this is the new version of QARMA that can hear your voice
#
# Marubuci / Author: Muhammad Saleh Abdulhamid
# Wuri / Location: Nigeria
# Sigar / Version: 2.0
# Farawa / Started: 2026
# Harshe / Language: Python
# Yanayi / Status: Active Development
#
# Bayani / Description:
# QARMA is an intelligent Quran memorization and revision
# assistant designed to help Huffaz strengthen long-term
# retention through adaptive revision, memorization tracking,
# and future AI-assisted recitation analysis.
#
# Abubuwan Da Shirin Yake Yi / Core Features:
# • Surah memorization tracking
# • Adaptive revision scoring system
# • Weak-surah detection
# • Hausa & English bilingual support
# • Progress analytics and revision history
# • Offline-friendly architecture
# • Voice recitation testing (NEW in v2!)
# • AI recitation roadmap (future)
#
# Buri Nan Gaba / Future Vision:
# To build an AI-powered Quran learning companion for
# students of Hifz across Africa and the Muslim world.
#
# Sassan Da Ake Shirin Karawa / Modules Planned:
# - Revision Engine (Na Shirye / Ready)
# - Quran Database (Na Shirye / Ready)
# - Memorization Analytics (Na Shirye / Ready)
# - Voice Recognition System (Na Shirye / Ready - v2)
# - AI Mistake Detection (Mai Zuwa / Coming)
# - Mobile & Web Application (Mai Zuwa / Coming)
#
# Lasisi / License:
# MIT License (Planned Open Source Project)
#
# ----------------------------------------------------------
#
# abin da na kara a wannan version / what i added in this version:
#   - yana jin ka karanta surah da muryarka
#   - it listens to you recite a surah with your voice
#   - yana kwatanta abin da ka ce da rubutun daidai
#   - it compares what you said to the correct text
#   - yana gaya maka idan ka yi kuskure
#   - it tells you if you made a mistake
#
# libraries da nake bukata / libraries i need:
#   pip install SpeechRecognition
#   pip install pyaudio
#
# idan pyaudio ya ki aiki a windows / if pyaudio fails on windows:
#   pip install pipwin
#   pipwin install pyaudio

import json
import os
import random
from datetime import date

# ina kokarin shigo da library din muryar
# i am trying to import the voice library
try:
    import speech_recognition as sr
    VOICE_READY = True
except ImportError:
    VOICE_READY = False

MY_SAVE_FILE = "qarma_save.json"

# ----------------------------------------------------------
# duk surorin Ƙurani 114 - All 114 surahs
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

# ----------------------------------------------------------
# kalmomin farko na wasu surahohi don gwajin murya
# opening words of some surahs for voice recitation test
# na zabi juz 30 da sauran shahararrun surahohi don fara
# i picked juz 30 and famous surahs to start with
# zan kara sauran daga baya inshallah
# i will add more later inshallah
# ----------------------------------------------------------
SURAH_FIRST_WORDS = {
    1:   "بسم الله الرحمن الرحيم الحمد لله رب العالمين",
    36:  "يس والقرآن الحكيم",
    55:  "الرحمن علم القرآن",
    67:  "تبارك الذي بيده الملك",
    78:  "عم يتساءلون",
    79:  "والنازعات غرقا",
    80:  "عبس وتولى",
    81:  "إذا الشمس كورت",
    82:  "إذا السماء انفطرت",
    83:  "ويل للمطففين",
    84:  "إذا السماء انشقت",
    85:  "والسماء ذات البروج",
    86:  "والسماء والطارق",
    87:  "سبح اسم ربك الأعلى",
    88:  "هل أتاك حديث الغاشية",
    89:  "والفجر وليال عشر",
    90:  "لا أقسم بهذا البلد",
    91:  "والشمس وضحاها",
    92:  "والليل إذا يغشى",
    93:  "والضحى والليل إذا سجى",
    94:  "ألم نشرح لك صدرك",
    95:  "والتين والزيتون",
    96:  "اقرأ باسم ربك الذي خلق",
    97:  "إنا أنزلناه في ليلة القدر",
    98:  "لم يكن الذين كفروا",
    99:  "إذا زلزلت الأرض زلزالها",
    100: "والعاديات ضبحا",
    101: "القارعة ما القارعة",
    102: "ألهاكم التكاثر",
    103: "والعصر إن الإنسان لفي خسر",
    104: "ويل لكل همزة لمزة",
    105: "ألم تر كيف فعل ربك بأصحاب الفيل",
    106: "لإيلاف قريش",
    107: "أرأيت الذي يكذب بالدين",
    108: "إنا أعطيناك الكوثر",
    109: "قل يا أيها الكافرون",
    110: "إذا جاء نصر الله والفتح",
    111: "تبت يدا أبي لهب وتب",
    112: "قل هو الله أحد",
    113: "قل أعوذ برب الفلق",
    114: "قل أعوذ برب الناس",
}

# bayani a Hausa da Turanci - explanation in Hausa and English
SURAH_EXPLANATION = {
    1:   {"hausa": "Al-Fatihah ita ce mabudin Kur'ani. Muna karanta ta a kowace salah. Ma'anarta ita ce muna rokon Allah ya shiryar da mu hanya madaidaiciya.", "english": "Al-Fatihah is the opening of the Quran. We read it in every prayer. It means we are asking Allah to guide us to the straight path."},
    2:   {"hausa": "Al-Baqarah ita ce mafi tsawo daga cikin surahohin Kur'ani. A cikinta akwai Ayatul Kursi. Tana kare gida daga shaiɗan.", "english": "Al-Baqarah is the longest surah in the Quran. It contains Ayatul Kursi. It protects the home from Shaytan."},
    18:  {"hausa": "Al-Kahf ana karanta ta kowace Jumma'a. Tana kare mai karanta ta daga fitinar Dajjal.", "english": "Al-Kahf is read every Friday. It protects its reader from the trial of the Dajjal."},
    36:  {"hausa": "Ya-Sin ana kiranta da zuciyar Kur'ani. Duk wanda ya karanta ta Allah zai sassauta masa harkokinsa.", "english": "Ya-Sin is called the heart of the Quran. Whoever reads it Allah will make his affairs easy."},
    55:  {"hausa": "Ar-Rahman ana kiranta da aro jar Kur'ani. Allah yana lissafa ni'imomin da Ya yi wa bayin Sa.", "english": "Ar-Rahman is called the bride of the Quran. Allah lists His blessings upon His servants."},
    67:  {"hausa": "Al-Mulk tana kare mai karanta ta daga azabar kabari. Muna karanta ta kowace dare.", "english": "Al-Mulk protects its reader from the punishment of the grave. We read it every night."},
    112: {"hausa": "Al-Ikhlas tana magana ne akan tauhidi. Tana daidai da kashi daya bisa uku na Kur'ani wajen lada.", "english": "Al-Ikhlas talks about Tawheed. It equals one third of the Quran in reward."},
    113: {"hausa": "Al-Falaq tana neman tsari daga sharrin duk wani abu, daga sihiri, da daga masu kishi.", "english": "Al-Falaq seeks protection from the evil of all creation, magic, and the envious."},
    114: {"hausa": "An-Nas tana neman tsari daga sharrin shaiɗan wanda yake zuga zukatan mutane da aljanu.", "english": "An-Nas seeks protection from the evil of the whisperer who whispers into the hearts of mankind and jinn."},
}


# ----------------------------------------------------------
# loda da adana bayanai - load and save data
# ----------------------------------------------------------
def load_my_data():
    if os.path.exists(MY_SAVE_FILE):
        with open(MY_SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"my_name": "", "start_date": str(date.today()), "surahs": {}}

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
            "voice_attempts": 0,    # sabon abu - new thing i added for v2
            "voice_passed": 0,      # nawa ya wuce gwajin murya - how many times passed voice test
            "last_date": None,
            "my_note": ""
        }
    return my_data["surahs"][key]

def update_my_score(surah_record, rating):
    old_score = surah_record["score"]
    if rating == 1:
        surah_record["score"] = max(0, old_score - 2)
    elif rating == 2:
        surah_record["score"] = max(0, old_score - 1)
    elif rating == 3:
        surah_record["score"] = old_score
    elif rating == 4:
        surah_record["score"] = min(5, old_score + 1)
    elif rating == 5:
        surah_record["score"] = min(5, old_score + 2)
    surah_record["times_revised"] += 1
    surah_record["last_date"] = str(date.today())

def show_strength(score):
    bars = "█" * score + "░" * (5 - score)
    labels = ["Rauni sosai/Very Weak", "Rauni/Weak", "Tsakiya/Fair",
              "Kyau/Good", "Karfi/Strong", "Haddace/Mastered ⭐"]
    return f"[{bars}] {labels[score]}"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_title():
    print("=" * 60)
    print("  🕌  QARMA v2 - Quran Revision & Memorization Assistant")
    print("           بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ")
    print("=" * 60)


# ----------------------------------------------------------
# wannan shine sabon abu na version 2 - THE NEW THING IN V2
# tsarin ji da kwatanta murya - voice listening and comparing
#
# yadda yake aiki / how it works:
#   1. yana amfani da microphone don ji muryarka
#      it uses your microphone to hear your voice
#   2. yana aika sauti zuwa google don fassara
#      it sends audio to google to translate to text
#   3. yana kwatanta kalmomin da ka ce da kalmomin daidai
#      it compares the words you said to the correct words
#   4. yana gaya maka nawa daga cikin kalmomi ka yi daidai
#      it tells you how many words out of total you got right
# ----------------------------------------------------------
def listen_to_recitation():
    # idan library bata nan sai mu dawo da None
    # if library is not installed return None
    if not VOICE_READY:
        return None

    # kirkiro mai ji - create the listener
    my_listener = sr.Recognizer()

    # yi amfani da microphone - use the microphone
    with sr.Microphone() as mic_source:
        print("\n  🎙️  Yana jira muryarka / Listening for your voice...")
        print("  Ka karanta surah da murya a hankali")
        print("  Recite the surah clearly and slowly\n")

        # daidaita ga amo na bango - adjust for background noise
        my_listener.adjust_for_ambient_noise(mic_source, duration=1)

        try:
            # ji har zuwa dakika 15 - listen for up to 15 seconds
            audio_data = my_listener.listen(mic_source, timeout=15, phrase_time_limit=15)
            print("  ⏳ Ana nazari / Processing your recitation...")

            # aika zuwa google don gane kalmomin larabci
            # send to google to recognize the arabic words
            # na zaɓi arabic ne don mun karanta larabci
            # i chose arabic because we are reciting arabic
            what_i_heard = my_listener.recognize_google(audio_data, language="ar-SA")
            return what_i_heard

        except sr.WaitTimeoutError:
            # ya yi tsawo ba tare da murya ba - waited too long without voice
            print("  ⚠️  Ban ji murya ba / I did not hear any voice")
            return None
        except sr.UnknownValueError:
            # bai fahimci murya ba - could not understand the voice
            print("  ⚠️  Ban fahimci abin da ka ce ba / Could not understand what you said")
            return None
        except sr.RequestError:
            # matsalar intanet - internet problem
            print("  ⚠️  Matsalar intanet / Internet connection problem")
            return None


def compare_recitation(what_i_said, correct_text):
    # na kwatanta kalmomin biyu don gane nawa ya yi daidai
    # i compare the two texts to find how many words matched
    #
    # yadda nake kwatanta / how i compare:
    #   - na raba kowane jumla zuwa kalmomi
    #   - i split each sentence into individual words
    #   - na duba kowace kalma idan tana cikin dayan
    #   - i check each word if it exists in the other

    # cire haruffan da ba kalmomi ba - remove non-word characters
    def clean_text(text):
        cleaned = ""
        for char in text:
            # ci gaba da haruffa da sarari kawai
            # keep only letters and spaces
            if char.isalpha() or char == " ":
                cleaned += char
        return cleaned.strip()

    my_words = clean_text(what_i_said).split()
    correct_words = clean_text(correct_text).split()

    if len(correct_words) == 0:
        return 0, 0, []

    # duba wane kalmomi sun yi daidai - check which words matched
    matched = []
    missed = []

    for word in correct_words:
        if word in my_words:
            matched.append(word)
        else:
            missed.append(word)

    match_count = len(matched)
    total_count = len(correct_words)

    return match_count, total_count, missed


# ----------------------------------------------------------
# gwajin murya - voice recitation test
# wannan shine babban sabon abu na version 2
# this is the main new feature of version 2
# ----------------------------------------------------------
def voice_recitation_test(my_data):
    clear_screen()
    show_title()

    # duba idan library yana nan - check if library is installed
    if not VOICE_READY:
        print("\n  ⚠️  MATSALA / PROBLEM:\n")
        print("  Library din murya bata nan a kwamfutarka")
        print("  The voice library is not installed on your computer\n")
        print("  Don gyara wannan, bude terminal ka rubuta:")
        print("  To fix this, open terminal and type:\n")
        print("  pip install SpeechRecognition")
        print("  pip install pyaudio\n")
        print("  Idan pyaudio ya ki aiki a Windows:")
        print("  If pyaudio fails on Windows:\n")
        print("  pip install pipwin")
        print("  pipwin install pyaudio\n")
        input("  Danna Enter / Press Enter to go back...")
        return

    # surahohin da akwai farkon kalmomin su
    # surahs that have their opening words available
    available = [n for n in ALL_SURAHS
                 if get_surah_info(my_data, n)["memorized"]
                 and n in SURAH_FIRST_WORDS]

    if len(available) == 0:
        print("\n  ⚠️  Babu wani surah da ya dace don gwajin murya tukuna.")
        print("  No memorized surah is available for voice test yet.")
        print("  Saka surahohi da ke cikin Juz 30 ko shahararrun surahohi.")
        print("  Mark surahs from Juz 30 or the famous surahs.\n")
        input("  Danna Enter / Press Enter to go back...")
        return

    print("\n  🎙️  GWAJIN MURYA / VOICE RECITATION TEST\n")
    print("  Zaɓi surah don gwaji / Choose a surah to test:\n")

    # nuna surahohin da ake iya gwajin su
    # show surahs available for voice test
    for i, n in enumerate(available, 1):
        s = ALL_SURAHS[n]
        rec = get_surah_info(my_data, n)
        attempts = rec["voice_attempts"]
        passed = rec["voice_passed"]
        print(f"  {i}. Surah {n}: {s['name']} ({s['arabic']}) - "
              f"Gwaji: {attempts} | Ya wuce: {passed}")

    print(f"\n  0. Koma / Go back")

    while True:
        try:
            choice = int(input("\n  Zabin ka / Your choice: "))
            if choice == 0:
                return
            if 1 <= choice <= len(available):
                break
        except:
            pass

    # surah da aka zaba - the chosen surah
    chosen_num = available[choice - 1]
    chosen_surah = ALL_SURAHS[chosen_num]
    correct_opening = SURAH_FIRST_WORDS[chosen_num]
    record = get_surah_info(my_data, chosen_num)

    clear_screen()
    show_title()
    print(f"\n  📖 Surah da aka zaɓa / Chosen Surah:")
    print(f"  Surah {chosen_num}: {chosen_surah['name']} ({chosen_surah['arabic']})")
    print(f"  Juz: {chosen_surah['juz']}\n")
    print(f"  ─────────────────────────────────────────────────")
    print(f"  Ka karanta farkon wannan surah da murya a hankali")
    print(f"  Recite the opening of this surah clearly and slowly")
    print(f"  ─────────────────────────────────────────────────\n")

    input("  Danna Enter idan ka shirya / Press Enter when ready...")

    # ji muryar mai amfani - listen to the user's voice
    what_i_heard = listen_to_recitation()

    if what_i_heard is None:
        print("\n  Ban iya ji muryarka ba. Gwada karo guda.")
        print("  Could not hear your voice. Please try again.")
        record["voice_attempts"] += 1
        save_my_data(my_data)
        input("\n  Danna Enter / Press Enter to continue...")
        return

    print(f"\n  👂 Abin da na ji / What I heard:")
    print(f"  {what_i_heard}\n")

    # kwatanta da rubutun daidai - compare to correct text
    matched, total, missed_words = compare_recitation(what_i_heard, correct_opening)

    # lissafa kashi dari - calculate percentage
    if total > 0:
        percentage = round((matched / total) * 100)
    else:
        percentage = 0

    print(f"  📊 Sakamakon / Result:")
    print(f"  Kalmomi daidai / Words correct: {matched} / {total}")
    print(f"  Kashi / Percentage: {percentage}%\n")

    # yanke hukunci - give feedback based on score
    if percentage >= 80:
        print("  ✅ MashaAllah! Ka yi kyau sosai! / Excellent recitation! 🌟")
        print("  Ka wuce gwajin murya! / You passed the voice test!")
        update_my_score(record, 5)
        record["voice_passed"] += 1
    elif percentage >= 60:
        print("  🟡 Kyau amma kana iya inganta / Good but you can improve")
        print("  Ka ci gaba da bita / Keep practicing")
        update_my_score(record, 3)
    elif percentage >= 40:
        print("  🟠 Kana bukatar karin bita / You need more practice")
        update_my_score(record, 2)
    else:
        print("  🔴 Ka sake bita wannan surah / Revise this surah again")
        update_my_score(record, 1)

    # nuna kalmomin da ya rasa - show missed words
    if missed_words:
        print(f"\n  Kalmomin da ka rasa / Words you missed:")
        print(f"  {' | '.join(missed_words[:8])}")
        if len(missed_words) > 8:
            print(f"  ... da wasu {len(missed_words) - 8} / ...and {len(missed_words) - 8} more")

    print(f"\n  Rubutun daidai / Correct text was:")
    print(f"  {correct_opening}")

    record["voice_attempts"] += 1
    save_my_data(my_data)

    input("\n  Danna Enter / Press Enter to continue...")


# ----------------------------------------------------------
# duk ayyukan version 1 - all version 1 functions kept here
# na kiyaye dukkan abubuwan da na yi a v1
# i kept everything from v1 and just added new things
# ----------------------------------------------------------

def first_time_setup(my_data):
    clear_screen()
    show_title()
    print("\n  Barka da zuwa QARMA v2! / Welcome to QARMA v2!\n")
    name = input("  Shigar da sunanka / Enter your name: ").strip()
    if name == "":
        name = "Dan Kur'ani"
    my_data["my_name"] = name
    save_my_data(my_data)
    print(f"\n  Assalamu Alaykum {name}! Bari mu fara. / Let us begin.")
    input("\n  Danna Enter / Press Enter to continue...")

def mark_memorized(my_data):
    clear_screen()
    show_title()
    print("\n  📖 SAKA SURAHODI DA NA HADDACE / MARK MEMORIZED SURAHS\n")
    print("  Rubuta lambobin surahodi da koma / Type surah numbers with commas")
    print("  Misali / Example: 1,112,113,114")
    print("  Ko / Or: 'juz30' don sanya Juz 30 duka / to mark all of Juz 30\n")
    user_input = input("  > ").strip()
    nums_to_mark = []
    if user_input.lower() == "juz30":
        nums_to_mark = list(range(78, 115))
    else:
        for part in user_input.split(","):
            part = part.strip()
            if part.isdigit():
                n = int(part)
                if 1 <= n <= 114:
                    nums_to_mark.append(n)
    count = 0
    for n in nums_to_mark:
        get_surah_info(my_data, n)["memorized"] = True
        count += 1
    save_my_data(my_data)
    print(f"\n  ✅ Na saka {count} surah(s). / Marked {count} surah(s).")
    input("\n  Danna Enter / Press Enter to continue...")

def view_my_progress(my_data):
    clear_screen()
    show_title()
    print("\n  📊 CI GABANA / MY PROGRESS\n")
    memorized_list = [n for n in ALL_SURAHS if get_surah_info(my_data, n)["memorized"]]
    total = len(memorized_list)
    filled = int((total / 114) * 30)
    bar = "█" * filled + "░" * (30 - filled)
    print(f"  {total}/114  [{bar}]  {round((total/114)*100, 1)}%\n")

    # sabon abu - also show voice test stats
    # new thing - also show how many voice tests passed
    total_voice = sum(get_surah_info(my_data, n)["voice_attempts"] for n in memorized_list)
    total_passed = sum(get_surah_info(my_data, n)["voice_passed"] for n in memorized_list)
    print(f"  🎙️  Gwajin murya / Voice tests: {total_voice} attempts | {total_passed} passed\n")

    if total == 0:
        print("  Ba ka saka kowane surah ba. / No surahs marked yet. Use option 2.\n")
    else:
        juz_groups = {}
        for n in memorized_list:
            j = ALL_SURAHS[n]["juz"]
            juz_groups.setdefault(j, []).append(n)
        print(f"  {'Juz':<6} {'Surahohi / Surahs'}")
        print(f"  {'-' * 50}")
        for j in sorted(juz_groups.keys()):
            names = ", ".join(ALL_SURAHS[n]["name"] for n in sorted(juz_groups[j]))
            print(f"  Juz {j:<3}: {names}")
    input("\n  Danna Enter / Press Enter to continue...")

def start_revision(my_data):
    clear_screen()
    show_title()
    memorized_list = [n for n in ALL_SURAHS if get_surah_info(my_data, n)["memorized"]]
    if len(memorized_list) == 0:
        print("\n  ⚠️  Ba ka saka kowane surah ba! / No surahs marked yet! Use option 2.\n")
        input("  Danna Enter / Press Enter to continue...")
        return
    memorized_list.sort(key=lambda n: get_surah_info(my_data, n)["score"])
    revision_queue = memorized_list[:5]
    print("\n  🔁 LOKACIN BITA / REVISION SESSION\n")
    for n in revision_queue:
        s = ALL_SURAHS[n]
        rec = get_surah_info(my_data, n)
        print(f"  • Surah {n}: {s['name']} ({s['arabic']}) - {show_strength(rec['score'])}\n")
    input("  Danna Enter don fara / Press Enter to start...")
    for n in revision_queue:
        clear_screen()
        show_title()
        rec = get_surah_info(my_data, n)
        s = ALL_SURAHS[n]
        print(f"\n  📖 Surah {n}: {s['name']} ({s['arabic']}) - Juz {s['juz']}")
        print(f"  Karfi / Strength: {show_strength(rec['score'])}")
        if n in SURAH_EXPLANATION:
            print(f"\n  🟢 Hausa: {SURAH_EXPLANATION[n]['hausa']}")
            print(f"\n  🔵 English: {SURAH_EXPLANATION[n]['english']}")
        print("\n  1=Manta 2=Wahala 3=Tsakiya 4=Kyau 5=Cikakke")
        print("  1=Forgot  2=Hard   3=Okay   4=Good  5=Perfect")
        while True:
            try:
                rating = int(input("\n  Maki / Rating [1-5]: "))
                if 1 <= rating <= 5:
                    break
            except:
                pass
        update_my_score(rec, rating)
        save_my_data(my_data)
        print(f"\n  Karfi sabon / New strength: {show_strength(rec['score'])}")
        input("  Danna Enter / Press Enter for next...")
    clear_screen()
    show_title()
    print(f"\n  ✅ Kammala! / Done! Ka bita {len(revision_queue)} surahs. Baarakallahu Feek! 🌙")
    input("\n  Danna Enter / Press Enter to continue...")

def show_weak_surahs(my_data):
    clear_screen()
    show_title()
    print("\n  ⚠️  SURAHOHIN RAUNI / WEAKEST SURAHS\n")
    memorized_list = [n for n in ALL_SURAHS if get_surah_info(my_data, n)["memorized"]]
    if not memorized_list:
        print("  Ba ka saka kowane surah ba. / No surahs marked yet.\n")
        input("  Danna Enter / Press Enter to continue...")
        return
    memorized_list.sort(key=lambda n: get_surah_info(my_data, n)["score"])
    print(f"  {'#':<5} {'Surah':<20} {'Arabic':<16} {'Karfi / Strength'}")
    print(f"  {'-' * 62}")
    for n in memorized_list[:10]:
        rec = get_surah_info(my_data, n)
        s = ALL_SURAHS[n]
        print(f"  {n:<5} {s['name']:<20} {s['arabic']:<16} {show_strength(rec['score'])}")
    input("\n  Danna Enter / Press Enter to continue...")

def quiz_me(my_data):
    clear_screen()
    show_title()
    memorized_list = [n for n in ALL_SURAHS if get_surah_info(my_data, n)["memorized"]]
    if len(memorized_list) < 4:
        print("\n  ⚠️  Kana bukatar akalla surahohi 4! / Need at least 4 surahs!\n")
        input("  Danna Enter / Press Enter to continue...")
        return
    print("\n  🎯 WASAN TAMBAYA / QUIZ TIME!\n")
    correct_num = random.choice(memorized_list)
    correct_surah = ALL_SURAHS[correct_num]
    question_type = random.choice(["juz", "arabic", "number"])
    answered_correct = False
    if question_type == "juz":
        print(f"  Surah {correct_surah['name']} tana cikin wane Juz?")
        print(f"  Surah {correct_surah['name']} is in which Juz?\n")
        wrong_juz = [j for j in range(1, 31) if j != correct_surah["juz"]]
        options = [correct_surah["juz"]] + random.sample(wrong_juz, 3)
        random.shuffle(options)
        for i, opt in enumerate(options, 1):
            print(f"  {i}. Juz {opt}")
        while True:
            try:
                ans = int(input("\n  Zabin ka / Your choice [1-4]: "))
                if 1 <= ans <= 4:
                    break
            except:
                pass
        if options[ans - 1] == correct_surah["juz"]:
            answered_correct = True
            print(f"\n  ✅ Daidai! / Correct! MashaAllah! 🌟")
        else:
            print(f"\n  ❌ Kuskure! Amsar: Juz {correct_surah['juz']} / Wrong! Answer: Juz {correct_surah['juz']}")
    elif question_type == "arabic":
        print(f"  Wannan larabcin na wace surah?  {correct_surah['arabic']}")
        print(f"  Which surah is this Arabic?  {correct_surah['arabic']}\n")
        wrong = random.sample([n for n in memorized_list if n != correct_num], min(3, len(memorized_list)-1))
        options = [correct_num] + wrong
        random.shuffle(options)
        for i, n in enumerate(options, 1):
            print(f"  {i}. {ALL_SURAHS[n]['name']}")
        while True:
            try:
                ans = int(input("\n  Zabin ka / Your choice [1-4]: "))
                if 1 <= ans <= len(options):
                    break
            except:
                pass
        if options[ans-1] == correct_num:
            answered_correct = True
            print(f"\n  ✅ Daidai! / Correct! MashaAllah! 🌟")
        else:
            print(f"\n  ❌ Kuskure! Amsar: {correct_surah['name']} / Wrong! Answer: {correct_surah['name']}")
    else:
        print(f"  Surah mai lamba {correct_num} sunainta? / Name of Surah {correct_num}?\n")
        wrong = random.sample([n for n in memorized_list if n != correct_num], min(3, len(memorized_list)-1))
        options = [correct_num] + wrong
        random.shuffle(options)
        for i, n in enumerate(options, 1):
            print(f"  {i}. {ALL_SURAHS[n]['name']} ({ALL_SURAHS[n]['arabic']})")
        while True:
            try:
                ans = int(input("\n  Zabin ka / Your choice [1-4]: "))
                if 1 <= ans <= len(options):
                    break
            except:
                pass
        if options[ans-1] == correct_num:
            answered_correct = True
            print(f"\n  ✅ Daidai! / Correct! MashaAllah! 🌟")
        else:
            print(f"\n  ❌ Kuskure! Amsar: {correct_surah['name']} / Wrong! Answer: {correct_surah['name']}")
    rec = get_surah_info(my_data, correct_num)
    update_my_score(rec, 5 if answered_correct else 1)
    save_my_data(my_data)
    input("\n  Danna Enter / Press Enter to continue...")

def read_explanation(my_data):
    clear_screen()
    show_title()
    print("\n  📚 KARANTA BAYANI / READ EXPLANATION\n")
    for n in sorted(SURAH_EXPLANATION.keys()):
        s = ALL_SURAHS[n]
        print(f"  {n}. {s['name']} ({s['arabic']})")
    print()
    try:
        n = int(input("  Shigar da lamba / Enter surah number: "))
    except:
        n = 0
    if n in SURAH_EXPLANATION:
        s = ALL_SURAHS[n]
        print(f"\n  ══════════════════════════════════════════════")
        print(f"  Surah {n}: {s['name']}  {s['arabic']}  Juz {s['juz']}")
        print(f"  ══════════════════════════════════════════════")
        print(f"\n  🟢 HAUSA:\n  {SURAH_EXPLANATION[n]['hausa']}")
        print(f"\n  🔵 ENGLISH:\n  {SURAH_EXPLANATION[n]['english']}")
    else:
        print("\n  Babu bayani tukuna / No explanation yet. Coming soon inshallah!")
    input("\n  Danna Enter / Press Enter to continue...")


# ----------------------------------------------------------
# babban menu v2 - main menu version 2
# na kara option 3 don gwajin murya
# i added option 3 for the new voice test
# ----------------------------------------------------------
def main():
    my_data = load_my_data()
    if my_data["my_name"] == "":
        first_time_setup(my_data)

    while True:
        clear_screen()
        show_title()
        name = my_data["my_name"]
        memorized_count = sum(1 for n in ALL_SURAHS if get_surah_info(my_data, n)["memorized"])
        voice_status = "✅ READY" if VOICE_READY else "❌ Install library"

        print(f"\n  👤 {name}  |  📅 {date.today()}  |  📖 {memorized_count}/114")
        print(f"  🎙️  Voice: {voice_status}\n")
        print("  ┌──────────────────────────────────────────────┐")
        print("  │           BABBAN MENU / MAIN MENU  v2        │")
        print("  ├──────────────────────────────────────────────┤")
        print("  │  1. 🔁  Fara Bita         / Start Revision   │")
        print("  │  2. 📖  Saka Surahohi     / Mark Memorized   │")
        print("  │  3. 🎙️   Gwajin Murya  ★  / Voice Test NEW!  │")
        print("  │  4. 📊  Duba Ci Gaba      / View Progress    │")
        print("  │  5. ⚠️   Surahohi Rauni    / Weak Surahs     │")
        print("  │  6. 🎯  Wasan Tambaya     / Quiz             │")
        print("  │  7. 📚  Karanta Bayani    / Explanation      │")
        print("  │  8. 🚪  Fita              / Exit             │")
        print("  └──────────────────────────────────────────────┘")

        choice = input("\n  Zabin ka / Your choice [1-8]: ").strip()

        if choice == "1":
            start_revision(my_data)
        elif choice == "2":
            mark_memorized(my_data)
        elif choice == "3":
            voice_recitation_test(my_data)
        elif choice == "4":
            view_my_progress(my_data)
        elif choice == "5":
            show_weak_surahs(my_data)
        elif choice == "6":
            quiz_me(my_data)
        elif choice == "7":
            read_explanation(my_data)
        elif choice == "8":
            clear_screen()
            print("\n  Ma'assalama! Goodbye! 🌙")
            print("  Allah Ya karbi aikinmu. Ameen.\n")
            break
        else:
            print("\n  Zaɓi daga 1 zuwa 8 / Choose from 1 to 8")
            input("  Danna Enter / Press Enter to continue...")


# fara shirin - start the program
if __name__ == "__main__":
    main()
