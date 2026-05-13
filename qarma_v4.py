# ╔══════════════════════════════════════════════════════════════════╗
# ║                         QARMA                                  ║
# ║         Quran AI Revision & Memorization Assistant              ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# QARMA V4 - Qur'an AI Revision & Memorization Assistant
# Web App Version - Built with Streamlit
# ================================================================
# HOW TO DEPLOY (free, no PC needed):
# 1. Upload this file to your GitHub repository
# 2. Go to streamlit.io and sign in with GitHub
# 3. Click "New app" → select this file
# 4. Your app is live at qarma.streamlit.app
#
# Marubuci / Author: Muhammad Saleh Abdulhamid
# Wuri / Location: Nigeria
# Sigar / Version: 4.0.0
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
# • Forgetting curve engine (NEW in v3!)
# • Smart daily revision plan (NEW in v3!)
# • 8-language bilingual interface (NEW in v3!)
# • Hausa & English bilingual support
# • Progress analytics and revision history
# • Offline-friendly architecture
# • Voice recitation testing (v2)
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
# - Forgetting Curve Engine (Na Shirye / Ready - v3)
# - Smart Daily Planner (Na Shirye / Ready - v3)
# - Multilanguage System (Na Shirye / Ready - v3)
# - AI Mistake Detection (Mai Zuwa / Coming)
# - Mobile & Web Application (Mai Zuwa / Coming)
#
# Lasisi / License:
# MIT License (Planned Open Source Project)
#
# ----------------------------------------------------------
#
# sabon abu da na kara a v3 / new thing i added in v3:
#   - forgetting curve engine - yana san yaushe zaka manta
#   - forgetting curve engine - it knows when you will forget
#   - smart daily plan - yana gaya maka wane surahohi ka bita yau
#   - smart daily plan - tells you exactly which surahs to revise today
#   - multilanguage - Arabic, English, Hausa, Fulfulde, Yoruba, Igbo, Kanuri, Shuwa
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

import streamlit as st
import json
from datetime import date, timedelta
import random

# ── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(
    page_name="QARMA",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── BEAUTIFUL ISLAMIC CSS ────────────────────────────────────
st.markdown("""
<style>
    /* Import beautiful fonts */
    @import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Cinzel:wght@400;600;700&family=Raleway:wght@300;400;500;600;700&display=swap');

    /* Root variables */
    :root {
        --dark-navy: #0A1628;
        --deep-green: #1B4332;
        --gold: #D4AF37;
        --light-gold: #F5E6B3;
        --cream: #FFF8E7;
        --accent-green: #2D6A4F;
        --text-light: #E8E8E8;
        --card-bg: rgba(27, 67, 50, 0.3);
        --border-gold: rgba(212, 175, 55, 0.4);
    }

    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0A1628 0%, #1B4332 50%, #0A1628 100%);
        font-family: 'Raleway', sans-serif;
    }

    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A1628 0%, #1B4332 100%);
        border-right: 1px solid var(--border-gold);
    }

    [data-testid="stSidebar"] * {
        color: var(--text-light) !important;
    }

    /* Cards */
    .qarma-card {
        background: rgba(27, 67, 50, 0.4);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .qarma-card:hover {
        border-color: rgba(212, 175, 55, 0.7);
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(212, 175, 55, 0.2);
    }

    /* Header */
    .qarma-header {
        text-align: center;
        padding: 30px 20px;
        background: linear-gradient(135deg, rgba(27,67,50,0.6), rgba(10,22,40,0.8));
        border-radius: 20px;
        border: 1px solid rgba(212,175,55,0.4);
        margin-bottom: 20px;
    }

    .qarma-title {
        font-family: 'Cinzel', serif;
        font-size: 3em;
        font-weight: 700;
        color: var(--gold);
        text-shadow: 0 0 30px rgba(212,175,55,0.5);
        margin: 0;
        letter-spacing: 4px;
    }

    .qarma-subtitle {
        font-family: 'Amiri', serif;
        font-size: 1.3em;
        color: var(--light-gold);
        margin: 5px 0;
    }

    .bismillah {
        font-family: 'Amiri', serif;
        font-size: 1.8em;
        color: var(--gold);
        text-align: center;
        margin: 10px 0;
    }

    /* Stats cards */
    .stat-card {
        background: rgba(27, 67, 50, 0.5);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }

    .stat-number {
        font-family: 'Cinzel', serif;
        font-size: 2.5em;
        color: var(--gold);
        font-weight: 700;
        line-height: 1;
    }

    .stat-label {
        color: var(--light-gold);
        font-size: 0.85em;
        margin-top: 5px;
        font-family: 'Raleway', sans-serif;
    }

    /* Surah cards */
    .surah-due {
        background: rgba(180, 50, 50, 0.2);
        border: 1px solid rgba(255, 100, 100, 0.4);
        border-radius: 12px;
        padding: 12px 16px;
        margin: 6px 0;
    }

    .surah-today {
        background: rgba(27, 67, 50, 0.5);
        border: 1px solid rgba(212, 175, 55, 0.4);
        border-radius: 12px;
        padding: 12px 16px;
        margin: 6px 0;
    }

    .surah-good {
        background: rgba(20, 80, 40, 0.4);
        border: 1px solid rgba(50, 200, 100, 0.3);
        border-radius: 12px;
        padding: 12px 16px;
        margin: 6px 0;
    }

    /* Stability bar */
    .stability-bar-container {
        background: rgba(0,0,0,0.3);
        border-radius: 10px;
        height: 8px;
        margin: 8px 0;
        overflow: hidden;
    }

    .stability-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--deep-green), var(--accent-green));
        color: var(--gold);
        border: 1px solid var(--gold);
        border-radius: 10px;
        font-family: 'Raleway', sans-serif;
        font-weight: 600;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, var(--accent-green), var(--deep-green));
        box-shadow: 0 4px 20px rgba(212,175,55,0.4);
        transform: translateY(-1px);
    }

    /* Text colors */
    h1, h2, h3, h4, h5, h6 {
        color: var(--gold) !important;
        font-family: 'Cinzel', serif !important;
    }

    p, div, span, label {
        color: var(--text-light);
    }

    /* Selectbox and inputs */
    .stSelectbox > div > div {
        background: rgba(27,67,50,0.6);
        border: 1px solid rgba(212,175,55,0.4);
        color: var(--text-light);
    }

    .stTextInput > div > div > input {
        background: rgba(27,67,50,0.6);
        border: 1px solid rgba(212,175,55,0.4);
        color: var(--text-light);
    }

    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--deep-green), var(--gold));
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(27,67,50,0.4);
        border-radius: 10px;
        border: 1px solid rgba(212,175,55,0.3);
    }

    .stTabs [data-baseweb="tab"] {
        color: var(--light-gold);
        font-family: 'Raleway', sans-serif;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(212,175,55,0.2);
        color: var(--gold) !important;
    }

    /* Divider */
    hr {
        border-color: rgba(212,175,55,0.3);
    }

    /* Hifz passport card */
    .hifz-passport {
        background: linear-gradient(135deg, #1B4332, #0A1628);
        border: 2px solid var(--gold);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .hifz-passport::before {
        content: '🕌';
        position: absolute;
        font-size: 8em;
        opacity: 0.05;
        top: -20px;
        right: -20px;
    }

    /* Alert/Warning boxes */
    .overdue-alert {
        background: rgba(180,50,50,0.15);
        border-left: 4px solid #ff6b6b;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
    }

    .success-alert {
        background: rgba(50,180,100,0.15);
        border-left: 4px solid #51cf66;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
    }

    /* Tawbah mode */
    .tawbah-card {
        background: linear-gradient(135deg, rgba(212,175,55,0.1), rgba(27,67,50,0.3));
        border: 1px solid rgba(212,175,55,0.5);
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
    }

    /* League badge */
    .league-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: 600;
        font-family: 'Raleway', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# ── ALL 114 SURAHS ───────────────────────────────────────────
ALL_SURAHS = {
    1: {"name": "Al-Fatihah", "arabic": "الفاتحة", "juz": 1, "ayahs": 7},
    2: {"name": "Al-Baqarah", "arabic": "البقرة", "juz": 1, "ayahs": 286},
    3: {"name": "Aal-Imran", "arabic": "آل عمران", "juz": 3, "ayahs": 200},
    4: {"name": "An-Nisa", "arabic": "النساء", "juz": 4, "ayahs": 176},
    5: {"name": "Al-Maidah", "arabic": "المائدة", "juz": 6, "ayahs": 120},
    6: {"name": "Al-Anam", "arabic": "الأنعام", "juz": 7, "ayahs": 165},
    7: {"name": "Al-Araf", "arabic": "الأعراف", "juz": 8, "ayahs": 206},
    8: {"name": "Al-Anfal", "arabic": "الأنفال", "juz": 9, "ayahs": 75},
    9: {"name": "At-Tawbah", "arabic": "التوبة", "juz": 10, "ayahs": 129},
    10: {"name": "Yunus", "arabic": "يونس", "juz": 11, "ayahs": 109},
    11: {"name": "Hud", "arabic": "هود", "juz": 11, "ayahs": 123},
    12: {"name": "Yusuf", "arabic": "يوسف", "juz": 12, "ayahs": 111},
    13: {"name": "Ar-Rad", "arabic": "الرعد", "juz": 13, "ayahs": 43},
    14: {"name": "Ibrahim", "arabic": "إبراهيم", "juz": 13, "ayahs": 52},
    15: {"name": "Al-Hijr", "arabic": "الحجر", "juz": 14, "ayahs": 99},
    16: {"name": "An-Nahl", "arabic": "النحل", "juz": 14, "ayahs": 128},
    17: {"name": "Al-Isra", "arabic": "الإسراء", "juz": 15, "ayahs": 111},
    18: {"name": "Al-Kahf", "arabic": "الكهف", "juz": 15, "ayahs": 110},
    19: {"name": "Maryam", "arabic": "مريم", "juz": 16, "ayahs": 98},
    20: {"name": "Ta-Ha", "arabic": "طه", "juz": 16, "ayahs": 135},
    21: {"name": "Al-Anbiya", "arabic": "الأنبياء", "juz": 17, "ayahs": 112},
    22: {"name": "Al-Hajj", "arabic": "الحج", "juz": 17, "ayahs": 78},
    23: {"name": "Al-Muminun", "arabic": "المؤمنون", "juz": 18, "ayahs": 118},
    24: {"name": "An-Nur", "arabic": "النور", "juz": 18, "ayahs": 64},
    25: {"name": "Al-Furqan", "arabic": "الفرقان", "juz": 18, "ayahs": 77},
    26: {"name": "Ash-Shuara", "arabic": "الشعراء", "juz": 19, "ayahs": 227},
    27: {"name": "An-Naml", "arabic": "النمل", "juz": 19, "ayahs": 93},
    28: {"name": "Al-Qasas", "arabic": "القصص", "juz": 20, "ayahs": 88},
    29: {"name": "Al-Ankabut", "arabic": "العنكبوت", "juz": 20, "ayahs": 69},
    30: {"name": "Ar-Rum", "arabic": "الروم", "juz": 21, "ayahs": 60},
    31: {"name": "Luqman", "arabic": "لقمان", "juz": 21, "ayahs": 34},
    32: {"name": "As-Sajdah", "arabic": "السجدة", "juz": 21, "ayahs": 30},
    33: {"name": "Al-Ahzab", "arabic": "الأحزاب", "juz": 21, "ayahs": 73},
    34: {"name": "Saba", "arabic": "سبأ", "juz": 22, "ayahs": 54},
    35: {"name": "Fatir", "arabic": "فاطر", "juz": 22, "ayahs": 45},
    36: {"name": "Ya-Sin", "arabic": "يس", "juz": 22, "ayahs": 83},
    37: {"name": "As-Saffat", "arabic": "الصافات", "juz": 23, "ayahs": 182},
    38: {"name": "Sad", "arabic": "ص", "juz": 23, "ayahs": 88},
    39: {"name": "Az-Zumar", "arabic": "الزمر", "juz": 23, "ayahs": 75},
    40: {"name": "Ghafir", "arabic": "غافر", "juz": 24, "ayahs": 85},
    41: {"name": "Fussilat", "arabic": "فصلت", "juz": 24, "ayahs": 54},
    42: {"name": "Ash-Shura", "arabic": "الشورى", "juz": 25, "ayahs": 53},
    43: {"name": "Az-Zukhruf", "arabic": "الزخرف", "juz": 25, "ayahs": 89},
    44: {"name": "Ad-Dukhan", "arabic": "الدخان", "juz": 25, "ayahs": 59},
    45: {"name": "Al-Jathiyah", "arabic": "الجاثية", "juz": 25, "ayahs": 37},
    46: {"name": "Al-Ahqaf", "arabic": "الأحقاف", "juz": 26, "ayahs": 35},
    47: {"name": "Muhammad", "arabic": "محمد", "juz": 26, "ayahs": 38},
    48: {"name": "Al-Fath", "arabic": "الفتح", "juz": 26, "ayahs": 29},
    49: {"name": "Al-Hujurat", "arabic": "الحجرات", "juz": 26, "ayahs": 18},
    50: {"name": "Qaf", "arabic": "ق", "juz": 26, "ayahs": 45},
    51: {"name": "Adh-Dhariyat", "arabic": "الذاريات", "juz": 26, "ayahs": 60},
    52: {"name": "At-Tur", "arabic": "الطور", "juz": 27, "ayahs": 49},
    53: {"name": "An-Najm", "arabic": "النجم", "juz": 27, "ayahs": 62},
    54: {"name": "Al-Qamar", "arabic": "القمر", "juz": 27, "ayahs": 55},
    55: {"name": "Ar-Rahman", "arabic": "الرحمن", "juz": 27, "ayahs": 78},
    56: {"name": "Al-Waqiah", "arabic": "الواقعة", "juz": 27, "ayahs": 96},
    57: {"name": "Al-Hadid", "arabic": "الحديد", "juz": 27, "ayahs": 29},
    58: {"name": "Al-Mujadila", "arabic": "المجادلة", "juz": 28, "ayahs": 22},
    59: {"name": "Al-Hashr", "arabic": "الحشر", "juz": 28, "ayahs": 24},
    60: {"name": "Al-Mumtahanah", "arabic": "الممتحنة", "juz": 28, "ayahs": 13},
    61: {"name": "As-Saf", "arabic": "الصف", "juz": 28, "ayahs": 14},
    62: {"name": "Al-Jumuah", "arabic": "الجمعة", "juz": 28, "ayahs": 11},
    63: {"name": "Al-Munafiqun", "arabic": "المنافقون", "juz": 28, "ayahs": 11},
    64: {"name": "At-Taghabun", "arabic": "التغابن", "juz": 28, "ayahs": 18},
    65: {"name": "At-Talaq", "arabic": "الطلاق", "juz": 28, "ayahs": 12},
    66: {"name": "At-Tahrim", "arabic": "التحريم", "juz": 28, "ayahs": 12},
    67: {"name": "Al-Mulk", "arabic": "الملك", "juz": 29, "ayahs": 30},
    68: {"name": "Al-Qalam", "arabic": "القلم", "juz": 29, "ayahs": 52},
    69: {"name": "Al-Haqqah", "arabic": "الحاقة", "juz": 29, "ayahs": 52},
    70: {"name": "Al-Maarij", "arabic": "المعارج", "juz": 29, "ayahs": 44},
    71: {"name": "Nuh", "arabic": "نوح", "juz": 29, "ayahs": 28},
    72: {"name": "Al-Jinn", "arabic": "الجن", "juz": 29, "ayahs": 28},
    73: {"name": "Al-Muzzammil", "arabic": "المزمل", "juz": 29, "ayahs": 20},
    74: {"name": "Al-Muddaththir", "arabic": "المدثر", "juz": 29, "ayahs": 56},
    75: {"name": "Al-Qiyamah", "arabic": "القيامة", "juz": 29, "ayahs": 40},
    76: {"name": "Al-Insan", "arabic": "الإنسان", "juz": 29, "ayahs": 31},
    77: {"name": "Al-Mursalat", "arabic": "المرسلات", "juz": 29, "ayahs": 50},
    78: {"name": "An-Naba", "arabic": "النبأ", "juz": 30, "ayahs": 40},
    79: {"name": "An-Naziat", "arabic": "النازعات", "juz": 30, "ayahs": 46},
    80: {"name": "Abasa", "arabic": "عبس", "juz": 30, "ayahs": 42},
    81: {"name": "At-Takwir", "arabic": "التكوير", "juz": 30, "ayahs": 29},
    82: {"name": "Al-Infitar", "arabic": "الانفطار", "juz": 30, "ayahs": 19},
    83: {"name": "Al-Mutaffifin", "arabic": "المطففين", "juz": 30, "ayahs": 36},
    84: {"name": "Al-Inshiqaq", "arabic": "الانشقاق", "juz": 30, "ayahs": 25},
    85: {"name": "Al-Buruj", "arabic": "البروج", "juz": 30, "ayahs": 22},
    86: {"name": "At-Tariq", "arabic": "الطارق", "juz": 30, "ayahs": 17},
    87: {"name": "Al-Ala", "arabic": "الأعلى", "juz": 30, "ayahs": 19},
    88: {"name": "Al-Ghashiyah", "arabic": "الغاشية", "juz": 30, "ayahs": 26},
    89: {"name": "Al-Fajr", "arabic": "الفجر", "juz": 30, "ayahs": 30},
    90: {"name": "Al-Balad", "arabic": "البلد", "juz": 30, "ayahs": 20},
    91: {"name": "Ash-Shams", "arabic": "الشمس", "juz": 30, "ayahs": 15},
    92: {"name": "Al-Layl", "arabic": "الليل", "juz": 30, "ayahs": 21},
    93: {"name": "Ad-Duha", "arabic": "الضحى", "juz": 30, "ayahs": 11},
    94: {"name": "Ash-Sharh", "arabic": "الشرح", "juz": 30, "ayahs": 8},
    95: {"name": "At-Tin", "arabic": "التين", "juz": 30, "ayahs": 8},
    96: {"name": "Al-Alaq", "arabic": "العلق", "juz": 30, "ayahs": 19},
    97: {"name": "Al-Qadr", "arabic": "القدر", "juz": 30, "ayahs": 5},
    98: {"name": "Al-Bayyinah", "arabic": "البينة", "juz": 30, "ayahs": 8},
    99: {"name": "Az-Zalzalah", "arabic": "الزلزلة", "juz": 30, "ayahs": 8},
    100: {"name": "Al-Adiyat", "arabic": "العاديات", "juz": 30, "ayahs": 11},
    101: {"name": "Al-Qariah", "arabic": "القارعة", "juz": 30, "ayahs": 11},
    102: {"name": "At-Takathur", "arabic": "التكاثر", "juz": 30, "ayahs": 8},
    103: {"name": "Al-Asr", "arabic": "العصر", "juz": 30, "ayahs": 3},
    104: {"name": "Al-Humazah", "arabic": "الهمزة", "juz": 30, "ayahs": 9},
    105: {"name": "Al-Fil", "arabic": "الفيل", "juz": 30, "ayahs": 5},
    106: {"name": "Quraysh", "arabic": "قريش", "juz": 30, "ayahs": 4},
    107: {"name": "Al-Maun", "arabic": "الماعون", "juz": 30, "ayahs": 7},
    108: {"name": "Al-Kawthar", "arabic": "الكوثر", "juz": 30, "ayahs": 3},
    109: {"name": "Al-Kafirun", "arabic": "الكافرون", "juz": 30, "ayahs": 6},
    110: {"name": "An-Nasr", "arabic": "النصر", "juz": 30, "ayahs": 3},
    111: {"name": "Al-Masad", "arabic": "المسد", "juz": 30, "ayahs": 5},
    112: {"name": "Al-Ikhlas", "arabic": "الإخلاص", "juz": 30, "ayahs": 4},
    113: {"name": "Al-Falaq", "arabic": "الفلق", "juz": 30, "ayahs": 5},
    114: {"name": "An-Nas", "arabic": "الناس", "juz": 30, "ayahs": 6},
}

# ── TRANSLATIONS ─────────────────────────────────────────────
LANG = {
    "en": {
        "title": "QARMA",
        "subtitle": "Qur'an AI Revision & Memorization Assistant",
        "dashboard": "Dashboard",
        "my_plan": "Today's Revision Plan",
        "stability": "Stability Scores",
        "mark_memorized": "Mark Memorized",
        "quiz": "Quiz",
        "progress": "My Progress",
        "passport": "Hifz Passport",
        "streak": "Day Streak",
        "memorized": "Memorized",
        "points": "QARMA Points",
        "overdue": "OVERDUE",
        "due_today": "DUE TODAY",
        "stable": "STABLE",
        "revise_now": "Revise Now",
        "rate_session": "Rate Your Revision",
        "forgot": "Forgot 😞",
        "hard": "Hard 😟",
        "okay": "Okay 😐",
        "good": "Good 😊",
        "perfect": "Perfect 🌟",
        "tawbah_title": "Tawbah Mode — Recovery Plan",
        "tawbah_msg": "You missed some revisions. Allah is Most Merciful. Let's recover together — one surah at a time.",
        "no_due": "MashaAllah! No revision due today! 🌟",
        "select_surahs": "Select surahs you have memorized",
        "save": "Save",
        "correct": "Correct! MashaAllah! 🌟",
        "wrong": "Wrong! Keep trying 💪",
        "which_juz": "Which Juz is this surah in?",
        "league": "League",
    },
    "ha": {
        "title": "QARMA",
        "subtitle": "Mataimakin Kur'ani na AI",
        "dashboard": "Allon Sarrafa",
        "my_plan": "Shirin Bitar Yau",
        "stability": "Matakin Karfi",
        "mark_memorized": "Saka Surahohi",
        "quiz": "Tambayoyi",
        "progress": "Ci Gabana",
        "passport": "Takardun Hifz",
        "streak": "Kwanaki Jere",
        "memorized": "An Haddace",
        "points": "Maki na QARMA",
        "overdue": "YA WUCE LOKACI",
        "due_today": "YAU NE LOKACINSA",
        "stable": "LAFIYA",
        "revise_now": "Bita Yanzu",
        "rate_session": "Ba da Maki",
        "forgot": "Na Manta 😞",
        "hard": "Wahala 😟",
        "okay": "Tsakiya 😐",
        "good": "Kyau 😊",
        "perfect": "Cikakke 🌟",
        "tawbah_title": "Yanayin Tawba — Tsarin Murmurewa",
        "tawbah_msg": "Ka rasa wasu bita. Allah Mahaukaci ne. Bari mu murmure tare — surah guda guda.",
        "no_due": "MashaAllah! Babu bita yau! 🌟",
        "select_surahs": "Zaɓi surahohin da ka haddace",
        "save": "Adana",
        "correct": "Daidai! MashaAllah! 🌟",
        "wrong": "Kuskure! Ka ci gaba 💪",
        "which_juz": "Wane Juz ne wannan surah take ciki?",
        "league": "Matsayi",
    }
}

# ── FORGETTING CURVE ENGINE ──────────────────────────────────
INTERVALS = [1, 3, 7, 14, 21, 60, 180, 365]

def calculate_stability(record):
    """Calculate stability percentage based on forgetting curve"""
    if not record.get("last_date"):
        return 100.0
    last = date.fromisoformat(record["last_date"])
    days_since = (date.today() - last).days
    times_revised = record.get("times_revised", 0)
    if times_revised == 0:
        decay_rate = 0.5
    elif times_revised < 3:
        decay_rate = 0.3
    elif times_revised < 6:
        decay_rate = 0.15
    else:
        decay_rate = 0.05
    stability = 100 * (0.5 ** (days_since * decay_rate))
    return max(0.0, min(100.0, stability))

def get_next_revision(record):
    """Get next revision date"""
    times = record.get("times_revised", 0)
    if times < len(INTERVALS):
        days = INTERVALS[times]
    else:
        days = 365
    last = record.get("last_date")
    if not last:
        return str(date.today())
    return str(date.fromisoformat(last) + timedelta(days=days))

def is_due(record):
    """Check if surah is due for revision"""
    next_rev = get_next_revision(record)
    return date.fromisoformat(next_rev) <= date.today()

def days_overdue(record):
    """How many days overdue"""
    next_rev = get_next_revision(record)
    delta = (date.today() - date.fromisoformat(next_rev)).days
    return max(0, delta)

def get_league(points):
    """Get league based on points"""
    if points >= 50000:
        return "💎 Diamond Hafiz", "#b9f2ff"
    elif points >= 25000:
        return "🔵 Platinum Hafiz", "#a8d8ea"
    elif points >= 10000:
        return "🥇 Gold Hafiz", "#D4AF37"
    elif points >= 5000:
        return "🥈 Silver Hafiz", "#C0C0C0"
    elif points >= 1000:
        return "🥉 Bronze Hafiz", "#CD7F32"
    else:
        return "📖 Student", "#90EE90"

def get_stability_color(stability):
    """Get color based on stability"""
    if stability >= 80:
        return "#51cf66"
    elif stability >= 60:
        return "#D4AF37"
    elif stability >= 40:
        return "#ff922b"
    else:
        return "#ff6b6b"

# ── SESSION STATE ────────────────────────────────────────────
def init_state():
    if "data" not in st.session_state:
        st.session_state.data = {
            "name": "",
            "lang": "en",
            "streak": 0,
            "last_session": None,
            "points": 0,
            "surahs": {},
            "start_date": str(date.today()),
        }
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
    if "revising" not in st.session_state:
        st.session_state.revising = None

def get_surah(num):
    key = str(num)
    if key not in st.session_state.data["surahs"]:
        st.session_state.data["surahs"][key] = {
            "memorized": False,
            "score": 0,
            "times_revised": 0,
            "last_date": None,
            "stability": 100.0,
            "points_earned": 0,
        }
    return st.session_state.data["surahs"][key]

def update_revision(surah_num, rating):
    """Update surah after revision — rating 1-5"""
    rec = get_surah(surah_num)
    old_score = rec["score"]
    # update score
    if rating == 1:
        rec["score"] = max(0, old_score - 2)
        rec["times_revised"] = max(0, rec["times_revised"] - 1)
        points_change = -20
    elif rating == 2:
        rec["score"] = max(0, old_score - 1)
        points_change = -10
    elif rating == 3:
        rec["score"] = old_score
        points_change = 15
    elif rating == 4:
        rec["score"] = min(5, old_score + 1)
        rec["times_revised"] += 1
        points_change = 30
    else:  # 5
        rec["score"] = min(5, old_score + 2)
        rec["times_revised"] += 1
        points_change = 50
    rec["last_date"] = str(date.today())
    rec["stability"] = calculate_stability(rec)
    # update total points — never below 0
    st.session_state.data["points"] = max(
        0,
        st.session_state.data["points"] + points_change
    )
    # update streak
    today = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))
    last_session = st.session_state.data.get("last_session")
    if last_session != today:
        if last_session == yesterday:
            st.session_state.data["streak"] += 1
        elif last_session != today:
            st.session_state.data["streak"] = 1
        st.session_state.data["last_session"] = today
    return points_change

# ── SIDEBAR ──────────────────────────────────────────────────
def render_sidebar():
    L = LANG[st.session_state.data.get("lang", "en")]
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style='text-align:center; padding: 20px 0;'>
            <div style='font-family: Cinzel, serif; font-size: 2em; color: #D4AF37; letter-spacing: 3px;'>🕌 QARMA</div>
            <div style='font-family: Amiri, serif; font-size: 0.9em; color: #F5E6B3;'>بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</div>
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        # User info
        name = st.session_state.data.get("name", "")
        if not name:
            name = st.text_input("Your name / Sunanka", placeholder="Enter your name...")
            if name:
                st.session_state.data["name"] = name
                st.rerun()
        else:
            st.markdown(f"<div style='color:#D4AF37; font-weight:600;'>👤 {name}</div>", unsafe_allow_html=True)
        # Language toggle
        lang_choice = st.selectbox(
            "🌍 Language / Harshe",
            ["English", "Hausa"],
            index=0 if st.session_state.data.get("lang", "en") == "en" else 1
        )
        st.session_state.data["lang"] = "en" if lang_choice == "English" else "ha"
        L = LANG[st.session_state.data["lang"]]
        st.divider()
        # Stats
        memorized = sum(1 for n in ALL_SURAHS if get_surah(n)["memorized"])
        streak = st.session_state.data.get("streak", 0)
        points = st.session_state.data.get("points", 0)
        league, league_color = get_league(points)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-number'>{memorized}</div>
                <div class='stat-label'>{L["memorized"]}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-number'>{streak}🔥</div>
                <div class='stat-label'>{L["streak"]}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class='stat-card' style='margin-top:10px;'>
            <div class='stat-number' style='font-size:1.5em;'>⭐ {points:,}</div>
            <div class='stat-label'>{L["points"]}</div>
            <div style='margin-top:5px;'>
                <span class='league-badge' style='background:rgba(212,175,55,0.2); color:{league_color};'>{league}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        # Navigation
        pages = [
            ("🏠", L["dashboard"], "dashboard"),
            ("📖", L["mark_memorized"], "mark"),
            ("🎯", L["quiz"], "quiz"),
            ("📊", L["progress"], "progress"),
            ("🏆", L["passport"], "passport"),
        ]
        for icon, label, page_key in pages:
            if st.button(f"{icon} {label}", key=f"nav_{page_key}"):
                st.session_state.page = page_key
                st.session_state.revising = None
                st.rerun()

# ── DASHBOARD PAGE ───────────────────────────────────────────
def render_dashboard():
    L = LANG[st.session_state.data.get("lang", "en")]
    name = st.session_state.data.get("name", "Student")
    # Header
    st.markdown(f"""
    <div class='qarma-header'>
        <div class='bismillah'>بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</div>
        <div class='qarma-title'>QARMA</div>
        <div class='qarma-subtitle'>{L["subtitle"]}</div>
        <div style='color:#F5E6B3; margin-top:10px; font-size:0.9em;'>
            Assalamu Alaykum, <strong style='color:#D4AF37;'>{name}</strong> 🌙 — {date.today().strftime("%A, %d %B %Y")}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Get memorized surahs
    memorized = [n for n in ALL_SURAHS if get_surah(n)["memorized"]]

    if not memorized:
        st.markdown(f"""
        <div class='qarma-card' style='text-align:center; padding:40px;'>
            <div style='font-size:3em;'>🕌</div>
            <div style='color:#D4AF37; font-size:1.2em; font-family:Cinzel,serif; margin:10px 0;'>
                Welcome to QARMA
            </div>
            <div style='color:#F5E6B3;'>
                Start by marking your memorized surahs.<br>
                Go to <strong>"{L["mark_memorized"]}"</strong> in the sidebar.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Categorize surahs
    overdue_list = []
    due_today_list = []
    stable_list = []

    for n in memorized:
        rec = get_surah(n)
        rec["stability"] = calculate_stability(rec)
        od = days_overdue(rec)
        if od > 0:
            overdue_list.append((n, od))
        elif is_due(rec):
            due_today_list.append(n)
        else:
            stable_list.append(n)

    overdue_list.sort(key=lambda x: x[1], reverse=True)

    # Tawbah mode if many overdue
    if len(overdue_list) >= 5:
        st.markdown(f"""
        <div class='tawbah-card'>
            <div style='color:#D4AF37; font-family:Cinzel,serif; font-size:1.1em; margin-bottom:8px;'>
                🤲 {L["tawbah_title"]}
            </div>
            <div style='color:#F5E6B3; font-size:0.9em;'>{L["tawbah_msg"]}</div>
            <div style='color:#D4AF37; margin-top:8px; font-weight:600;'>
                Revision Debt: {len(overdue_list)} surahs — Recovering {min(3, len(overdue_list))} today
            </div>
        </div>
        """, unsafe_allow_html=True)
        # limit overdue to 3 for recovery mode
        overdue_list = overdue_list[:3]

    # Today's plan
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown(f"### 📅 {L['my_plan']}")

        if not overdue_list and not due_today_list:
            st.markdown(f"""
            <div class='success-alert'>
                <span style='font-size:1.3em;'>✅</span>
                <strong style='color:#51cf66;'> {L["no_due"]}</strong>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Show overdue
            for n, od in overdue_list:
                s = ALL_SURAHS[n]
                rec = get_surah(n)
                stability = rec.get("stability", 0)
                color = get_stability_color(stability)
                st.markdown(f"""
                <div class='surah-due'>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <div>
                            <span style='color:#ff6b6b; font-weight:700; font-size:0.75em;'>🔴 {L["overdue"]} — {od} days</span><br>
                            <span style='color:#E8E8E8; font-weight:600;'>{s["name"]}</span>
                            <span style='color:#F5E6B3; font-size:0.85em;'> — {s["arabic"]}</span>
                            <span style='color:#aaa; font-size:0.8em;'> | Juz {s["juz"]}</span>
                        </div>
                        <div style='text-align:right;'>
                            <div style='color:{color}; font-weight:700;'>{stability:.0f}%</div>
                            <div style='font-size:0.75em; color:#aaa;'>stability</div>
                        </div>
                    </div>
                    <div class='stability-bar-container'>
                        <div class='stability-bar-fill' style='width:{stability}%; background:{color};'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"📖 {L['revise_now']} — {s['name']}", key=f"revise_od_{n}"):
                    st.session_state.revising = n
                    st.rerun()

            # Show due today
            for n in due_today_list:
                s = ALL_SURAHS[n]
                rec = get_surah(n)
                stability = rec.get("stability", 50)
                color = get_stability_color(stability)
                st.markdown(f"""
                <div class='surah-today'>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <div>
                            <span style='color:#D4AF37; font-weight:700; font-size:0.75em;'>⭐ {L["due_today"]}</span><br>
                            <span style='color:#E8E8E8; font-weight:600;'>{s["name"]}</span>
                            <span style='color:#F5E6B3; font-size:0.85em;'> — {s["arabic"]}</span>
                            <span style='color:#aaa; font-size:0.8em;'> | Juz {s["juz"]}</span>
                        </div>
                        <div style='text-align:right;'>
                            <div style='color:{color}; font-weight:700;'>{stability:.0f}%</div>
                            <div style='font-size:0.75em; color:#aaa;'>stability</div>
                        </div>
                    </div>
                    <div class='stability-bar-container'>
                        <div class='stability-bar-fill' style='width:{stability}%; background:{color};'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"📖 {L['revise_now']} — {s['name']}", key=f"revise_dt_{n}"):
                    st.session_state.revising = n
                    st.rerun()

    with col2:
        st.markdown(f"### 📊 {L['stability']}")
        # Show stability for all memorized surahs
        for n in memorized[:8]:
            s = ALL_SURAHS[n]
            rec = get_surah(n)
            stability = calculate_stability(rec)
            color = get_stability_color(stability)
            st.markdown(f"""
            <div style='margin:6px 0;'>
                <div style='display:flex; justify-content:space-between;'>
                    <span style='color:#E8E8E8; font-size:0.85em;'>{s["name"]}</span>
                    <span style='color:{color}; font-weight:700; font-size:0.85em;'>{stability:.0f}%</span>
                </div>
                <div class='stability-bar-container'>
                    <div class='stability-bar-fill' style='width:{stability}%; background:linear-gradient(90deg, {color}, {color}88);'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Revision session
    if st.session_state.revising:
        render_revision_session()

# ── REVISION SESSION ─────────────────────────────────────────
def render_revision_session():
    L = LANG[st.session_state.data.get("lang", "en")]
    n = st.session_state.revising
    s = ALL_SURAHS[n]
    rec = get_surah(n)
    stability = calculate_stability(rec)
    color = get_stability_color(stability)
    next_intervals = INTERVALS[min(rec.get("times_revised", 0), len(INTERVALS)-1)]

    st.divider()
    st.markdown(f"""
    <div class='qarma-card' style='border-color: rgba(212,175,55,0.6);'>
        <div style='text-align:center;'>
            <div style='font-family:Amiri,serif; font-size:2em; color:#D4AF37;'>{s["arabic"]}</div>
            <div style='font-family:Cinzel,serif; font-size:1.3em; color:#E8E8E8; margin:5px 0;'>Surah {n}: {s["name"]}</div>
            <div style='color:#aaa; font-size:0.9em;'>Juz {s["juz"]} | {s["ayahs"]} Ayahs</div>
            <div style='color:{color}; font-weight:700; margin:8px 0;'>Current Stability: {stability:.0f}%</div>
            <div style='color:#F5E6B3; font-size:0.85em;'>
                After revision → next review in <strong style='color:#D4AF37;'>{next_intervals} days</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"#### {L['rate_session']}")
    cols = st.columns(5)
    ratings = [
        (1, L["forgot"], "#ff6b6b"),
        (2, L["hard"], "#ff922b"),
        (3, L["okay"], "#D4AF37"),
        (4, L["good"], "#69db7c"),
        (5, L["perfect"], "#51cf66"),
    ]
    for i, (rating, label, color) in enumerate(ratings):
        with cols[i]:
            if st.button(label, key=f"rate_{rating}"):
                points_change = update_revision(n, rating)
                emoji = ["", "😞", "😟", "😐", "😊", "🌟"][rating]
                if rating >= 4:
                    st.success(f"{emoji} +{points_change} QP! {L['correct'] if rating == 5 else 'Well done!'}")
                else:
                    st.warning(f"{emoji} {points_change} QP. {L['wrong']}")
                st.session_state.revising = None
                st.rerun()

    if st.button("✕ Cancel", key="cancel_revision"):
        st.session_state.revising = None
        st.rerun()

# ── MARK MEMORIZED PAGE ──────────────────────────────────────
def render_mark_memorized():
    L = LANG[st.session_state.data.get("lang", "en")]
    st.markdown(f"## 📖 {L['mark_memorized']}")
    st.markdown(f"<p style='color:#F5E6B3;'>{L['select_surahs']}</p>", unsafe_allow_html=True)

    # Quick mark Juz 30
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⚡ Mark All Juz 30 (78-114)"):
            for n in range(78, 115):
                rec = get_surah(n)
                rec["memorized"] = True
                if not rec["last_date"]:
                    rec["last_date"] = str(date.today())
            st.success("MashaAllah! Juz 30 marked! ✅")
            st.rerun()
    with col2:
        if st.button("⚡ Mark Surah 1 (Al-Fatihah)"):
            rec = get_surah(1)
            rec["memorized"] = True
            if not rec["last_date"]:
                rec["last_date"] = str(date.today())
            st.success("Al-Fatihah marked! ✅")
    with col3:
        if st.button("🗑️ Clear All"):
            st.session_state.data["surahs"] = {}
            st.warning("All cleared.")
            st.rerun()

    st.divider()

    # Group by Juz
    juz_groups = {}
    for n, s in ALL_SURAHS.items():
        j = s["juz"]
        if j not in juz_groups:
            juz_groups[j] = []
        juz_groups[j].append(n)

    for juz_num in sorted(juz_groups.keys()):
        with st.expander(f"📚 Juz {juz_num}", expanded=(juz_num == 30)):
            cols = st.columns(3)
            for i, n in enumerate(juz_groups[juz_num]):
                s = ALL_SURAHS[n]
                rec = get_surah(n)
                with cols[i % 3]:
                    checked = st.checkbox(
                        f"{n}. {s['name']} ({s['arabic']})",
                        value=rec["memorized"],
                        key=f"mem_{n}"
                    )
                    if checked != rec["memorized"]:
                        rec["memorized"] = checked
                        if checked and not rec["last_date"]:
                            rec["last_date"] = str(date.today())
                            st.session_state.data["points"] += 75
                        st.rerun()

# ── QUIZ PAGE ────────────────────────────────────────────────
def render_quiz():
    L = LANG[st.session_state.data.get("lang", "en")]
    st.markdown(f"## 🎯 {L['quiz']}")

    memorized = [n for n in ALL_SURAHS if get_surah(n)["memorized"]]
    if len(memorized) < 4:
        st.warning("You need at least 4 memorized surahs for the quiz!")
        return

    if "quiz_question" not in st.session_state:
        st.session_state.quiz_question = None
        st.session_state.quiz_answered = False

    if st.session_state.quiz_question is None or st.session_state.quiz_answered:
        if st.button("🎲 New Question", key="new_quiz"):
            correct_num = random.choice(memorized)
            correct = ALL_SURAHS[correct_num]
            wrong_juz = [j for j in range(1, 31) if j != correct["juz"]]
            options = [correct["juz"]] + random.sample(wrong_juz, 3)
            random.shuffle(options)
            st.session_state.quiz_question = {
                "surah_num": correct_num,
                "options": options,
                "correct_juz": correct["juz"]
            }
            st.session_state.quiz_answered = False
            st.rerun()

    if st.session_state.quiz_question and not st.session_state.quiz_answered:
        q = st.session_state.quiz_question
        s = ALL_SURAHS[q["surah_num"]]
        st.markdown(f"""
        <div class='qarma-card' style='text-align:center;'>
            <div style='font-family:Amiri,serif; font-size:2.5em; color:#D4AF37;'>{s["arabic"]}</div>
            <div style='color:#E8E8E8; font-size:1.1em; margin:8px 0;'>Surah {q["surah_num"]}: {s["name"]}</div>
            <div style='color:#F5E6B3; font-size:0.9em;'>{L["which_juz"]}</div>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(2)
        for i, opt in enumerate(q["options"]):
            with cols[i % 2]:
                if st.button(f"Juz {opt}", key=f"quiz_opt_{i}"):
                    if opt == q["correct_juz"]:
                        st.success(f"✅ {L['correct']}")
                        update_revision(q["surah_num"], 5)
                    else:
                        st.error(f"❌ {L['wrong']} — Correct: Juz {q['correct_juz']}")
                        update_revision(q["surah_num"], 1)
                    st.session_state.quiz_answered = True
                    st.rerun()

# ── PROGRESS PAGE ────────────────────────────────────────────
def render_progress():
    L = LANG[st.session_state.data.get("lang", "en")]
    st.markdown(f"## 📊 {L['progress']}")

    memorized = [n for n in ALL_SURAHS if get_surah(n)["memorized"]]
    total = len(memorized)
    percent = (total / 114) * 100

    # Overall progress
    st.markdown(f"""
    <div class='qarma-card'>
        <div style='display:flex; justify-content:space-between; margin-bottom:8px;'>
            <span style='color:#D4AF37; font-family:Cinzel,serif;'>Quran Progress</span>
            <span style='color:#D4AF37; font-weight:700;'>{total}/114 Surahs ({percent:.1f}%)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(percent / 100)

    # Stats row
    mastered = sum(1 for n in memorized if get_surah(n)["score"] >= 5)
    due_count = sum(1 for n in memorized if is_due(get_surah(n)))
    overdue_count = sum(1 for n in memorized if days_overdue(get_surah(n)) > 0)

    c1, c2, c3, c4 = st.columns(4)
    for col, label, value, color in [
        (c1, "Memorized", total, "#D4AF37"),
        (c2, "Mastered ⭐", mastered, "#51cf66"),
        (c3, "Due Today", due_count, "#ff922b"),
        (c4, "Overdue 🔴", overdue_count, "#ff6b6b"),
    ]:
        with col:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-number' style='color:{color};'>{value}</div>
                <div class='stat-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # By Juz
    st.markdown("### Progress by Juz")
    juz_mem = {}
    for n in memorized:
        j = ALL_SURAHS[n]["juz"]
        juz_mem.setdefault(j, []).append(n)

    if juz_mem:
        for j in sorted(juz_mem.keys()):
            surahs_in_juz = [n for n, s in ALL_SURAHS.items() if s["juz"] == j]
            done = len(juz_mem[j])
            total_in_juz = len(surahs_in_juz)
            names = ", ".join(ALL_SURAHS[n]["name"] for n in sorted(juz_mem[j]))
            pct = done / total_in_juz
            st.markdown(f"""
            <div style='margin:6px 0;'>
                <div style='display:flex; justify-content:space-between;'>
                    <span style='color:#D4AF37;'>Juz {j}</span>
                    <span style='color:#F5E6B3; font-size:0.85em;'>{done}/{total_in_juz}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(pct)
    else:
        st.info("No surahs memorized yet. Start marking them!")

# ── HIFZ PASSPORT ────────────────────────────────────────────
def render_passport():
    L = LANG[st.session_state.data.get("lang", "en")]
    name = st.session_state.data.get("name", "Hafiz")
    memorized = [n for n in ALL_SURAHS if get_surah(n)["memorized"]]
    total = len(memorized)
    streak = st.session_state.data.get("streak", 0)
    points = st.session_state.data.get("points", 0)
    league, league_color = get_league(points)
    avg_stability = sum(calculate_stability(get_surah(n)) for n in memorized) / max(1, total)

    st.markdown(f"## 🏆 {L['passport']}")

    st.markdown(f"""
    <div class='hifz-passport'>
        <div style='font-family:Amiri,serif; font-size:1.5em; color:#D4AF37;'>بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</div>
        <div style='font-family:Cinzel,serif; font-size:2em; color:#D4AF37; margin:10px 0; letter-spacing:3px;'>🕌 QARMA</div>
        <div style='font-family:Cinzel,serif; font-size:1.3em; color:#E8E8E8;'>HIFZ PASSPORT</div>
        <div style='color:#F5E6B3; font-size:0.9em; margin:5px 0;'>Issued: {date.today().strftime("%d %B %Y")}</div>
        <hr style='border-color:rgba(212,175,55,0.4); margin:15px 0;'/>
        <div style='font-family:Cinzel,serif; font-size:1.5em; color:#D4AF37;'>{name}</div>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:15px; margin:15px 0;'>
            <div style='background:rgba(27,67,50,0.6); border-radius:10px; padding:12px;'>
                <div style='font-size:1.8em; color:#D4AF37; font-weight:700;'>{total}/114</div>
                <div style='color:#F5E6B3; font-size:0.8em;'>Surahs Memorized</div>
            </div>
            <div style='background:rgba(27,67,50,0.6); border-radius:10px; padding:12px;'>
                <div style='font-size:1.8em; color:#D4AF37; font-weight:700;'>{streak}🔥</div>
                <div style='color:#F5E6B3; font-size:0.8em;'>Day Streak</div>
            </div>
            <div style='background:rgba(27,67,50,0.6); border-radius:10px; padding:12px;'>
                <div style='font-size:1.8em; color:#D4AF37; font-weight:700;'>{avg_stability:.0f}%</div>
                <div style='color:#F5E6B3; font-size:0.8em;'>Avg Stability</div>
            </div>
            <div style='background:rgba(27,67,50,0.6); border-radius:10px; padding:12px;'>
                <div style='font-size:1.8em; font-weight:700;' style='color:{league_color};'>{league}</div>
                <div style='color:#F5E6B3; font-size:0.8em;'>League</div>
            </div>
        </div>
        <div style='color:#D4AF37; font-style:italic; font-family:Amiri,serif;'>
            "وَرَتِّلِ الْقُرْآنَ تَرْتِيلًا"
        </div>
        <div style='color:#F5E6B3; font-size:0.8em; margin-top:5px;'>
            "And recite the Qur'an with measured recitation" — Al-Muzzammil 73:4
        </div>
        <div style='color:#aaa; font-size:0.75em; margin-top:15px;'>
            github.com/muhdsalehab01-cmd/QARMA- | Built for the Ummah 🌍
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📤 Share Your Progress")
    share_text = f"""🕌 QARMA Hifz Report
━━━━━━━━━━━━━━━━━━━━
👤 {name}
📖 Memorized: {total}/114 Surahs
🔥 Streak: {streak} days
⭐ Points: {points:,} QP
🏆 League: {league}
📊 Avg Stability: {avg_stability:.0f}%
━━━━━━━━━━━━━━━━━━━━
QARMA — AI Quran Memorization
For African Muslims 🌍
#QARMA #Quran #Hifz"""

    st.code(share_text, language=None)
    st.info("📱 Copy the text above and share on WhatsApp!")

# ── MAIN APP ─────────────────────────────────────────────────
def main():
    init_state()
    render_sidebar()

    page = st.session_state.page

    if page == "dashboard":
        render_dashboard()
    elif page == "mark":
        render_mark_memorized()
    elif page == "quiz":
        render_quiz()
    elif page == "progress":
        render_progress()
    elif page == "passport":
        render_passport()

if __name__ == "__main__":
    main()
