# sunana QARMA - Quran AI Revision and Memorization Assistant
# my name is QARMA - Quran AI Revision and Memorization Assistant
#
# Marubuci / Author: Muhammad Saleh Abdulhamid
# Wuri / Location: Nigeria
# Sigar / Version: 4.0.0
# Farawa / Started: 2026
# Harshe / Language: Python
# Yanayi / Status: Active Development
#
# na yi wannan shirin don taimaka min wajen haddace Quran
# i made this program to help me memorize and revise the Quran
#
# yadda yake aiki / how it works:
#   - zan saka surorin da na haddace / i'd add the surahs i have memorized
#   - yana gaya mini wanne ne rauni / it tells me which ones are weak
#   - yana ba ni tambayoyi / it gives me revision questions
#   - yana adana bayanai / it saves my progress
#
# na fara wannan project a 2026
# i started this project in 2026
# har yanzu ina koyon python / i am still learning python so i kept it simple

import json
import os
import random
from datetime import date

# sunan fayil ɗin da zan adana bayanaina
# name of the file where i will save my data
MY_SAVE_FILE = "qarma_save.json"

# ----------------------------------------------------------
# duk surorin Quran 114 - All 114 surahs of the Quran
# na rubuta suna, larabci, da juz
# i wrote the name, arabic, and juz number
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

# bayani a Hausa da Turanci na wasu surahohi muhimmai
# explanation in Hausa and English for some important surahs
# zan kara karin surahohi nan gaba inshallah
# i will add more surahs later inshallah
SURAH_EXPLANATION = {
    1: {
        "hausa": "Al-Fatihah ita ce mabudin Kur'ani. Muna karanta ta a kowace salah. Ma'anarta ita ce muna rokon Allah ya shiryar da mu hanya madaidaiciya.",
        "english": "Al-Fatihah is the opening of the Quran. We read it in every prayer. It means we are asking Allah to guide us to the straight path."
    },
    2: {
        "hausa": "Al-Baqarah ita ce mafi tsawo daga cikin surahohin Kur'ani. A cikinta akwai Ayatul Kursi wanda ita ce mafi girman aya a Kur'ani. Tana kare gida daga shaiɗan.",
        "english": "Al-Baqarah is the longest surah in the Quran. It contains Ayatul Kursi which is the greatest verse in the Quran. It protects the home from Shaytan."
    },
    18: {
        "hausa": "Al-Kahf ana karanta ta kowace Jumma'a. Tana kare mai karanta ta daga fitinar Dajjal. Tana ɗauke da labarun da suka yi fice kamar Ashabul Kahf da Musa da Khidr.",
        "english": "Al-Kahf is read every Friday. It protects its reader from the trial of the Dajjal. It contains great stories like the People of the Cave and Moses with Khidr."
    },
    36: {
        "hausa": "Ya-Sin ana kiranta da zuciyar Ƙur'ani. Manzon Allah SAW ya ce duk wanda ya karanta ta Allah zai sassauta masa harkokin duniya da lahira.",
        "english": "Ya-Sin is called the heart of the Quran. The Prophet SAW said whoever reads it Allah will make his worldly and religious affairs easy."
    },
    55: {
        "hausa": "Ar-Rahman ana kiranta da aro jar Kur'ani. Allah yana lissafa ni'imomin da Ya yi wa bayin Sa kuma yana tambaya: Wanne daga ni'imamin Ubangijinku kuke musantawa?",
        "english": "Ar-Rahman is called the bride of the Quran. Allah lists His blessings upon His servants and asks: Which of the favors of your Lord will you deny?"
    },
    67: {
        "hausa": "Al-Mulk tana kare mai karanta ta daga azabar kabari. Muna karanta ta kowace dare kafin kwanciya.",
        "english": "Al-Mulk protects its reader from the punishment of the grave. We read it every night before sleeping."
    },
    78: {
        "hausa": "An-Naba tana magana ne akan ranar tashin kiyama da tambayar da mutane suke yi game da ita.",
        "english": "An-Naba talks about the Day of Resurrection and the question people were arguing about."
    },
    112: {
        "hausa": "Al-Ikhlas tana magana ne akan tauhidi - cewa Allah daya ne, babu abin bauta sai Shi. Tana daidai da kashi daya bisa uku na Kur'ani wajen lada.",
        "english": "Al-Ikhlas talks about Tawheed - that Allah is one, there is nothing worthy of worship except Him. It equals one third of the Quran in reward."
    },
    113: {
        "hausa": "Al-Falaq tana neman tsari daga sharrin duk wani abu, daga sharrin dare, daga sihiri, da daga sharrin masu kishi.",
        "english": "Al-Falaq seeks protection from the evil of all that Allah created, from the darkness of night, from magic, and from the envy of the envious."
    },
    114: {
        "hausa": "An-Nas tana neman tsari daga sharrin shaiɗan wanda yake zuga zukatan mutane da aljanu.",
        "english": "An-Nas seeks protection from the evil of the whisperer who whispers into the hearts of mankind and jinn."
    },
}


# ----------------------------------------------------------
# ajiye da loda bayanai - save and load data
# ina amfani da json don adana bayanaina cikin fayil
# i am using json to save my data inside a file
# ----------------------------------------------------------
def load_my_data():
    # idan fayil yana nan sai na loda shi
    # if the file exists load it
    if os.path.exists(MY_SAVE_FILE):
        with open(MY_SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # idan baya nan sai na fara sabon bayanai
    # if it does not exist start fresh data
    return {
        "my_name": "",
        "start_date": str(date.today()),
        "surahs": {}
    }

def save_my_data(my_data):
    # adana zuwa fayil - save to file
    with open(MY_SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(my_data, f, ensure_ascii=False, indent=2)


# ----------------------------------------------------------
# dawo da bayanan surah daya - get one surah record
# idan surah bata nan cikin bayanaina sai na kirkiro ta
# if surah not in my data i create it fresh
# ----------------------------------------------------------
def get_surah_info(my_data, surah_num):
    key = str(surah_num)
    if key not in my_data["surahs"]:
        my_data["surahs"][key] = {
            "memorized": False,
            "score": 0,        # 0 rauni sosai, 5 na haddace sosai / 0 very weak 5 very strong
            "times_revised": 0,
            "last_date": None,
            "my_note": ""
        }
    return my_data["surahs"][key]


# ----------------------------------------------------------
# bayan mai amfani ya bita surah sai ya ba da maki
# after user revises a surah they give a rating
# idan ya manta sai na rage maki, idan ya yi kyau sai na kara
# if they forgot i reduce score if they did well i increase
# ----------------------------------------------------------
def update_my_score(surah_record, rating):
    # rating: 1=na manta, 2=wahala, 3=tsakiya, 4=kyau, 5=cikakke
    # rating: 1=forgot, 2=hard, 3=okay, 4=good, 5=perfect
    old_score = surah_record["score"]

    if rating == 1:
        # na manta gaba daya - i forgot completely
        surah_record["score"] = max(0, old_score - 2)
    elif rating == 2:
        # akwai kurakurai da yawa - many mistakes
        surah_record["score"] = max(0, old_score - 1)
    elif rating == 3:
        # tsakiya - okay keep same score
        surah_record["score"] = old_score
    elif rating == 4:
        # na yi kyau - i did well
        surah_record["score"] = min(5, old_score + 1)
    elif rating == 5:
        # cikakke - perfect
        surah_record["score"] = min(5, old_score + 2)

    surah_record["times_revised"] += 1
    surah_record["last_date"] = str(date.today())


# ----------------------------------------------------------
# nuna yadda ake bayyana karfi - show strength visually
# ----------------------------------------------------------
def show_strength(score):
    # na yi wannan don ya zama a iya gani a fili
    # i made this so it shows clearly on screen
    bars = "█" * score + "░" * (5 - score)
    if score == 0:
        label = "Rauni sosai / Very Weak"
    elif score == 1:
        label = "Rauni / Weak"
    elif score == 2:
        label = "Tsakiya / Fair"
    elif score == 3:
        label = "Kyau / Good"
    elif score == 4:
        label = "Karfi / Strong"
    else:
        label = "Haddace sosai / Mastered ⭐"
    return f"[{bars}] {label}"


# ----------------------------------------------------------
# share allo - clear the screen
# ----------------------------------------------------------
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# ----------------------------------------------------------
# nuna taken shirin - show the program title
# ----------------------------------------------------------
def show_title():
    print("=" * 58)
    print("   🕌  QARMA - Quran Revision & Memorization Assistant")
    print("          بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ")
    print("=" * 58)


# ----------------------------------------------------------
# shigar da sunayen mai amfani lokacin farko
# get user name on first run
# ----------------------------------------------------------
def first_time_setup(my_data):
    clear_screen()
    show_title()
    print("\n  Barka da zuwa QARMA! / Welcome to QARMA!\n")
    name = input("  Shigar da sunanka / Enter your name: ").strip()
    if name == "":
        name = "Dan Kur'ani"
    my_data["my_name"] = name
    save_my_data(my_data)
    print(f"\n  Assalamu Alaykum {name}! Bari mu fara. / Let us begin.")
    input("\n  Danna Enter don ci gaba / Press Enter to continue...")


# ----------------------------------------------------------
# saka wane surahohin da na haddace
# mark which surahs i have memorized
# ----------------------------------------------------------
def mark_memorized(my_data):
    clear_screen()
    show_title()
    print("\n  📖 SAKA SURAHODI DA NA HADDACE / MARK MEMORIZED SURAHS\n")
    print("  Rubuta lambobin surahodi da koma da koma")
    print("  Type surah numbers separated by commas")
    print("  Misali / Example: 1,112,113,114\n")
    print("  Ko rubuta 'juz30' don sanya duk surahohin Juz 30 (78-114)")
    print("  Or type 'juz30' to mark all Juz 30 surahs (78-114)\n")

    user_input = input("  > ").strip()

    nums_to_mark = []

    if user_input.lower() == "juz30":
        # surahohin juz 30 sune 78 zuwa 114
        # juz 30 surahs are 78 to 114
        nums_to_mark = list(range(78, 115))
    else:
        # raba da koma - split by comma
        parts = user_input.split(",")
        for part in parts:
            part = part.strip()
            if part.isdigit():
                n = int(part)
                if 1 <= n <= 114:
                    nums_to_mark.append(n)

    count = 0
    for n in nums_to_mark:
        record = get_surah_info(my_data, n)
        record["memorized"] = True
        count += 1

    save_my_data(my_data)
    print(f"\n  ✅ Na saka {count} surah(s). / Marked {count} surah(s) as memorized.")
    input("\n  Danna Enter / Press Enter to continue...")


# ----------------------------------------------------------
# duba ci gabana - view my progress
# ----------------------------------------------------------
def view_my_progress(my_data):
    clear_screen()
    show_title()
    print("\n  📊 CI GABANA / MY PROGRESS\n")

    # lissafa wanene na haddace - count how many i memorized
    memorized_list = []
    for n in ALL_SURAHS:
        record = get_surah_info(my_data, n)
        if record["memorized"]:
            memorized_list.append(n)

    total_memorized = len(memorized_list)

    # nuna bar din ci gaba - show progress bar
    bar_size = 30
    filled = int((total_memorized / 114) * bar_size)
    bar = "█" * filled + "░" * (bar_size - filled)
    percent = round((total_memorized / 114) * 100, 1)

    print(f"  Surahohi da na haddace / Surahs memorized: {total_memorized} / 114")
    print(f"  [{bar}] {percent}%\n")

    if total_memorized == 0:
        print("  Har yanzu ba ka saka kowane surah ba.")
        print("  You have not marked any surah yet. Use option 2.\n")
    else:
        # nuna su a juz - group by juz number
        print(f"  {'Juz':<6} {'Surahohi / Surahs'}")
        print(f"  {'-' * 50}")

        juz_groups = {}
        for n in memorized_list:
            j = ALL_SURAHS[n]["juz"]
            if j not in juz_groups:
                juz_groups[j] = []
            juz_groups[j].append(n)

        for j in sorted(juz_groups.keys()):
            names = ", ".join(ALL_SURAHS[n]["name"] for n in sorted(juz_groups[j]))
            print(f"  Juz {j:<3}: {names}")

    input("\n  Danna Enter / Press Enter to continue...")


# ----------------------------------------------------------
# lokacin bita - revision session
# zan nuna maka wane surahohi sun fi rauni don ka bita su
# i will show which surahs are weakest so you revise them
# yadda na zabi waɗanne - how i pick which ones to show:
#   mafi ƙarancin maki suna farko - lowest score comes first
# ----------------------------------------------------------
def start_revision(my_data):
    clear_screen()
    show_title()

    # zabi surahohin da na haddace kawai
    # only pick surahs i have memorized
    memorized_list = [n for n in ALL_SURAHS if get_surah_info(my_data, n)["memorized"]]

    if len(memorized_list) == 0:
        print("\n  ⚠️  Ba ka saka kowane surah ba tukuna!")
        print("  You have not marked any surah yet! Go to option 2 first.\n")
        input("  Danna Enter / Press Enter to continue...")
        return

    # tsara su daga mafi rauni zuwa mafi karfi
    # sort from weakest score to strongest score
    memorized_list.sort(key=lambda n: get_surah_info(my_data, n)["score"])

    # dauki 5 na mafi rauni - take top 5 weakest ones
    revision_queue = memorized_list[:5]

    print("\n  🔁 LOKACIN BITA / REVISION SESSION\n")
    print(f"  Yau za ka bita waɗannan surahohi {len(revision_queue)}:")
    print(f"  Today you will revise these {len(revision_queue)} surahs:\n")

    for n in revision_queue:
        record = get_surah_info(my_data, n)
        s = ALL_SURAHS[n]
        print(f"  • Surah {n}: {s['name']} ({s['arabic']}) - Juz {s['juz']}")
        print(f"    Karfi / Strength: {show_strength(record['score'])}\n")

    input("  Danna Enter don fara / Press Enter to start...")

    # fara bita kowane surah daya bayan daya
    # revise each surah one by one
    for n in revision_queue:
        clear_screen()
        show_title()
        record = get_surah_info(my_data, n)
        s = ALL_SURAHS[n]

        print(f"\n  📖 Yanzu ka bita / Now revise:")
        print(f"  Surah {n}: {s['name']}")
        print(f"  Larabci / Arabic: {s['arabic']}")
        print(f"  Juz: {s['juz']}")
        print(f"  Karfi yanzu / Current strength: {show_strength(record['score'])}")

        # idan akwai bayani sai mu nuna shi
        # if there is explanation for this surah show it
        if n in SURAH_EXPLANATION:
            print(f"\n  📝 Bayani (Hausa):\n  {SURAH_EXPLANATION[n]['hausa']}")
            print(f"\n  📝 Explanation (English):\n  {SURAH_EXPLANATION[n]['english']}")

        print("\n  ─────────────────────────────────────────────")
        print("  Ka karanta surah din a zuciyarka ko da baki")
        print("  Recite the surah in your mind or out loud")
        print("  Bayan ka gama, ba da maki / After finishing rate yourself:")
        print("  ─────────────────────────────────────────────")
        print("  1 = Na manta gaba daya / Forgot completely 😞")
        print("  2 = Akwai kurakurai da yawa / Many mistakes 😟")
        print("  3 = Tsakiya kadan kurakurai / Okay few mistakes 😐")
        print("  4 = Na yi kyau / Did well 😊")
        print("  5 = Cikakke babu kuskure / Perfect no mistakes 🌟")

        # jira mai amfani ya ba da maki - wait for user rating
        while True:
            try:
                rating = int(input("\n  Maki / Rating [1-5]: "))
                if 1 <= rating <= 5:
                    break
                else:
                    print("  Rubuta lamba daga 1 zuwa 5 / Enter number from 1 to 5")
            except:
                print("  Rubuta lamba daga 1 zuwa 5 / Enter number from 1 to 5")

        update_my_score(record, rating)
        save_my_data(my_data)

        emojis = {1: "😞", 2: "😟", 3: "😐", 4: "😊", 5: "🌟"}
        print(f"\n  {emojis[rating]} An adana! / Saved!")
        print(f"  Karfi sabon / New strength: {show_strength(record['score'])}")
        input("\n  Danna Enter don ci gaba / Press Enter for next...")

    clear_screen()
    show_title()
    print(f"\n  ✅ Kammala bitar yau! / Today's revision complete!")
    print(f"  Ka bita surahohi {len(revision_queue)}. Baarakallahu Feek! 🌙")
    input("\n  Danna Enter / Press Enter to continue...")


# ----------------------------------------------------------
# nuna surahohin da suka fi rauni - show weakest surahs
# ----------------------------------------------------------
def show_weak_surahs(my_data):
    clear_screen()
    show_title()
    print("\n  ⚠️  SURAHOHIN DA SUKA FI RAUNI / WEAKEST SURAHS\n")

    memorized_list = [n for n in ALL_SURAHS if get_surah_info(my_data, n)["memorized"]]

    if len(memorized_list) == 0:
        print("  Ba ka saka kowane surah ba tukuna.")
        print("  You have not marked any surah yet.\n")
        input("  Danna Enter / Press Enter to continue...")
        return

    # tsara daga mafi rauni - sort weakest first
    memorized_list.sort(key=lambda n: get_surah_info(my_data, n)["score"])
    weak_ones = memorized_list[:10]

    print(f"  {'#':<5} {'Surah':<20} {'Larabci':<16} {'Karfi / Strength'}")
    print(f"  {'-' * 62}")

    for n in weak_ones:
        record = get_surah_info(my_data, n)
        s = ALL_SURAHS[n]
        print(f"  {n:<5} {s['name']:<20} {s['arabic']:<16} {show_strength(record['score'])}")

    input("\n  Danna Enter / Press Enter to continue...")


# ----------------------------------------------------------
# wasan tambaya - simple quiz
# zan tambaye ka wanne surah yake a wace juz ko sunansa
# i will ask you which surah is in which juz or its name
# ----------------------------------------------------------
def quiz_me(my_data):
    clear_screen()
    show_title()

    memorized_list = [n for n in ALL_SURAHS if get_surah_info(my_data, n)["memorized"]]

    if len(memorized_list) < 4:
        print("\n  ⚠️  Kana bukatar akalla surahohi 4 don wasan tambaya!")
        print("  You need at least 4 memorized surahs for the quiz!\n")
        input("  Danna Enter / Press Enter to continue...")
        return

    print("\n  🎯 WASAN TAMBAYA / QUIZ TIME!\n")

    # zabi surah guda don tambaya - pick one surah for question
    correct_num = random.choice(memorized_list)
    correct_surah = ALL_SURAHS[correct_num]

    # zabi irin tambayar - randomly pick type of question
    question_type = random.choice(["juz", "arabic", "number"])

    answered_correct = False

    if question_type == "juz":
        print(f"  Tambaya / Question:")
        print(f"  Surah {correct_surah['name']} tana cikin wane Juz?")
        print(f"  Surah {correct_surah['name']} is in which Juz?\n")

        # zabi 3 amsar karya - pick 3 wrong juz numbers
        all_juz = list(range(1, 31))
        wrong_juz = [j for j in all_juz if j != correct_surah["juz"]]
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
            print(f"  Ee! {correct_surah['name']} tana cikin Juz {correct_surah['juz']}")
            print(f"  Yes! {correct_surah['name']} is in Juz {correct_surah['juz']}")
        else:
            print(f"\n  ❌ Kuskure! / Wrong!")
            print(f"  Amsar daidai / Correct answer: Juz {correct_surah['juz']}")

    elif question_type == "arabic":
        print(f"  Tambaya / Question:")
        print(f"  Wannan rubutun larabci na wace surah ne?")
        print(f"  Which surah does this Arabic belong to?\n")
        print(f"  ➤  {correct_surah['arabic']}\n")

        wrong_nums = random.sample([n for n in memorized_list if n != correct_num], min(3, len(memorized_list) - 1))
        options = [correct_num] + wrong_nums
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

        if options[ans - 1] == correct_num:
            answered_correct = True
            print(f"\n  ✅ Daidai! / Correct! MashaAllah! 🌟")
        else:
            print(f"\n  ❌ Kuskure! / Wrong!")
            print(f"  Amsar daidai / Correct answer: {correct_surah['name']}")

    else:
        print(f"  Tambaya / Question:")
        print(f"  Surah mai lamba {correct_num} sunainta mene ne?")
        print(f"  What is the name of Surah number {correct_num}?\n")

        wrong_nums = random.sample([n for n in memorized_list if n != correct_num], min(3, len(memorized_list) - 1))
        options = [correct_num] + wrong_nums
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

        if options[ans - 1] == correct_num:
            answered_correct = True
            print(f"\n  ✅ Daidai! / Correct! MashaAllah! 🌟")
        else:
            print(f"\n  ❌ Kuskure! / Wrong!")
            print(f"  Amsar daidai / Correct answer: {correct_surah['name']}")

    # sabunta maki bisa amsar - update score based on answer
    record = get_surah_info(my_data, correct_num)
    if answered_correct:
        update_my_score(record, 5)
    else:
        update_my_score(record, 1)
    save_my_data(my_data)

    input("\n  Danna Enter / Press Enter to continue...")


# ----------------------------------------------------------
# karanta bayani na surah - read explanation of a surah
# ina da bayani a Hausa da Turanci
# i have explanation in Hausa and English
# ----------------------------------------------------------
def read_explanation(my_data):
    clear_screen()
    show_title()
    print("\n  📚 KARANTA BAYANI / READ SURAH EXPLANATION\n")
    print("  Waɗannan surahohi suna da bayani a yanzu:")
    print("  These surahs have explanation available now:\n")

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
        print(f"\n  ═══════════════════════════════════════════════")
        print(f"  Surah {n}: {s['name']}  {s['arabic']}  - Juz {s['juz']}")
        print(f"  ═══════════════════════════════════════════════")
        print(f"\n  🟢 HAUSA:\n  {SURAH_EXPLANATION[n]['hausa']}")
        print(f"\n  🔵 ENGLISH:\n  {SURAH_EXPLANATION[n]['english']}")
    else:
        print("\n  Babu bayani ga wannan surah tukuna. Zan kara nan gaba inshallah.")
        print("  No explanation for this surah yet. I will add more later inshallah!")

    input("\n  Danna Enter / Press Enter to continue...")


# ----------------------------------------------------------
# babban menu - main menu
# anan ne farkon shirin duk lokacin da aka bude shi
# this is where the program starts every time you open it
# ----------------------------------------------------------
def main():
    # loda bayanai - load saved data
    my_data = load_my_data()

    # idan farkon amfani - if using for the first time
    if my_data["my_name"] == "":
        first_time_setup(my_data)

    # dawafi menu - keep showing menu until user exits
    while True:
        clear_screen()
        show_title()

        name = my_data["my_name"]
        today = str(date.today())

        # kirga nawa na haddace - count how many i memorized
        memorized_count = sum(1 for n in ALL_SURAHS if get_surah_info(my_data, n)["memorized"])

        print(f"\n  👤 {name}  |  📅 {today}  |  📖 {memorized_count}/114 Surahs")
        print()
        print("  ┌────────────────────────────────────────────┐")
        print("  │             BABBAN MENU / MAIN MENU        │")
        print("  ├────────────────────────────────────────────┤")
        print("  │  1. 🔁  Fara Bita        / Start Revision  │")
        print("  │  2. 📖  Saka Surahohi    / Mark Memorized  │")
        print("  │  3. 📊  Duba Ci Gaba     / View Progress   │")
        print("  │  4. ⚠️   Surahohi Rauni   / Weak Surahs    │")
        print("  │  5. 🎯  Wasan Tambaya    / Quiz            │")
        print("  │  6. 📚  Karanta Bayani   / Explanation     │")
        print("  │  7. 🚪  Fita             / Exit            │")
        print("  └────────────────────────────────────────────┘")

        choice = input("\n  Zabin ka / Your choice [1-7]: ").strip()

        if choice == "1":
            start_revision(my_data)
        elif choice == "2":
            mark_memorized(my_data)
        elif choice == "3":
            view_my_progress(my_data)
        elif choice == "4":
            show_weak_surahs(my_data)
        elif choice == "5":
            quiz_me(my_data)
        elif choice == "6":
            read_explanation(my_data)
        elif choice == "7":
            clear_screen()
            print("\n  Ma'assalama! Goodbye! 🌙")
            print("  Allah Ya karbi aikinmu. Ameen.\n")
            break
        else:
            print("\n  Zaɓi daga 1 zuwa 7 / Choose from 1 to 7")
            input("  Danna Enter / Press Enter to continue...")


# fara shirin - start the program
if __name__ == "__main__":
    main()
