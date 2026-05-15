# ╔══════════════════════════════════════════════════════════════════╗
# ║                         QARMA                                  ║
# ║         Qur'an AI Revision & Memorization Assistant            ║
# ║                    FINAL VERSION 4.0                           ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# Marubuci / Author: Muhammad Saleh Abdulhamid
# Wuri / Location: Nigeria
# Sigar / Version: 5.0 — Final Combined Edition
# Farawa / Started: 2026
# Harshe / Language: Python + Streamlit
# Yanayi / Status: Active Development
# GitHub: github.com/muhdsalehab01-cmd/QARMA-
#
# Bayani / Description:
# QARMA is an intelligent Quran memorization and revision
# assistant designed to help Huffaz strengthen long-term
# retention through adaptive revision, memorization tracking,
# and AI-assisted recitation analysis. Built specifically for
for Muslims worldwide with support for African languages,
#
# Abubuwan Da Shirin Yake Yi / Core Features:
# • Login & Registration system with password security
# • Surah memorization tracking (all 114 surahs)
# • Forgetting curve engine (Ebbinghaus 1885)
# • Adaptive stability scoring system
# • Tawbah/Recovery mode for missed revisions
# • Smart daily revision plan
# • QARMA Points & League system
# • Daily streak tracking
# • Bilingual interface (English + Hausa)
# • Hifz Passport shareable card
# • Quiz system
# • Progress analytics by Juz
# • Data persistence across sessions
#
# Buri Nan Gaba / Future Vision:
# To build the world's #1 AI-powered Quran learning companion
# serving 220 million African Muslims in their mother tongues.
#
# HOW TO DEPLOY (free, no PC needed):
# 1. Upload this file to your GitHub repository
# 2. Go to streamlit.io and sign in with GitHub
# 3. Click "New app" → select this file
# 4. Your app is live at qarma.streamlit.app
#
# Lasisi / License: MIT License (Open Source)
# ================================================================

import streamlit as st
import json
import os
import hashlib
import random
from datetime import date, timedelta

# ── PAGE CONFIG ─────────────────────────────────────────────────
st.set_page_config(
    page_title="QARMA — Quran Memorization Assistant",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── DATA PERSISTENCE & SECURITY ──────────────────────────────────
# na yi amfani da JSON don adana bayanai na duk masu amfani
# i used JSON to save data for all users permanently
USER_DATA_FILE = "qarma_users.json"

def save_all_users(users_dict):
    """Adana duk bayanai zuwa fayil / Save all user data to file"""
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users_dict, f, ensure_ascii=False, indent=2)

def load_all_users():
    """Loda bayanai daga fayil / Load user data from file"""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def make_hash(password):
    """Boye kalmar sirri / Securely hash password"""
    return hashlib.sha256(str.encode(password)).hexdigest()

def sync_data():
    """Adana bayanan mai amfani na yanzu / Save current user data"""
    if st.session_state.get("current_user"):
        users = load_all_users()
        users[st.session_state.current_user]["data"] = st.session_state.data
        save_all_users(users)

# ── BEAUTIFUL ISLAMIC CSS ─────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Cinzel:wght@400;600;700&family=Raleway:wght@300;400;500;600;700&display=swap');

    :root {
        --dark-navy: #0A1628;
        --deep-green: #1B4332;
        --gold: #D4AF37;
        --light-gold: #F5E6B3;
        --accent-green: #2D6A4F;
        --text-light: #E8E8E8;
        --border-gold: rgba(212, 175, 55, 0.4);
    }

    .stApp {
        background: linear-gradient(135deg, #0A1628 0%, #1B4332 50%, #0A1628 100%);
        font-family: 'Raleway', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A1628 0%, #1B4332 100%);
        border-right: 1px solid var(--border-gold);
    }
    [data-testid="stSidebar"] * { color: var(--text-light) !important; }

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
        box-shadow: 0 8px 32px rgba(212, 175, 55, 0.15);
    }

    .qarma-header {
        text-align: center;
        padding: 30px 20px;
        background: linear-gradient(135deg, rgba(27,67,50,0.6), rgba(10,22,40,0.9));
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

    .stat-card {
        background: rgba(27, 67, 50, 0.5);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }
    .stat-number {
        font-family: 'Cinzel', serif;
        font-size: 2.2em;
        color: var(--gold);
        font-weight: 700;
        line-height: 1;
    }
    .stat-label {
        color: var(--light-gold);
        font-size: 0.8em;
        margin-top: 5px;
    }

    .surah-overdue {
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

    .stability-bar-bg {
        background: rgba(0,0,0,0.3);
        border-radius: 10px;
        height: 8px;
        margin: 6px 0;
        overflow: hidden;
    }
    .stability-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }

    .tawbah-card {
        background: linear-gradient(135deg, rgba(212,175,55,0.1), rgba(27,67,50,0.3));
        border: 1px solid rgba(212,175,55,0.5);
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
    }

    .hifz-passport {
        background: linear-gradient(135deg, #1B4332, #0A1628);
        border: 2px solid var(--gold);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
    }

    .league-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--deep-green), var(--accent-green));
        color: var(--gold) !important;
        border: 1px solid var(--gold) !important;
        border-radius: 10px;
        font-family: 'Raleway', sans-serif;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        box-shadow: 0 4px 20px rgba(212,175,55,0.3);
        transform: translateY(-1px);
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--gold) !important;
        font-family: 'Cinzel', serif !important;
    }
    p, div, span, label { color: var(--text-light); }

    .stSelectbox > div > div, .stTextInput > div > div > input {
        background: rgba(27,67,50,0.6) !important;
        border: 1px solid rgba(212,175,55,0.4) !important;
        color: var(--text-light) !important;
    }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--deep-green), var(--gold));
    }
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(27,67,50,0.4);
        border-radius: 10px;
        border: 1px solid rgba(212,175,55,0.3);
    }
    .stTabs [data-baseweb="tab"] { color: var(--light-gold); }
    .stTabs [aria-selected="true"] {
        background: rgba(212,175,55,0.2);
        color: var(--gold) !important;
    }
    hr { border-color: rgba(212,175,55,0.3); }

    .login-card {
        background: rgba(27,67,50,0.5);
        border: 1px solid rgba(212,175,55,0.4);
        border-radius: 20px;
        padding: 40px;
        max-width: 500px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# ── ALL 114 SURAHS ────────────────────────────────────────────────
# na rubuta duk surahohin Kur'ani 114 da bayanansu
# i wrote all 114 Quran surahs with their details
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

# ── TRANSLATIONS ──────────────────────────────────────────────────
# fassarar manhajar zuwa Hausa da Turanci
# translations of the app into Hausa and English
LANG = {
    "en": {
        "subtitle": "Qur'an AI Revision & Memorization Assistant",
        "dashboard": "Dashboard", "my_plan": "Today's Revision Plan",
        "stability": "Stability Scores", "mark_memorized": "Mark Memorized",
        "quiz": "Quiz", "progress": "My Progress", "passport": "Hifz Passport",
        "streak": "Day Streak", "memorized": "Memorized", "points": "QARMA Points",
        "overdue": "OVERDUE", "due_today": "DUE TODAY", "stable": "STABLE",
        "revise_now": "Revise Now", "rate_session": "Rate Your Revision",
        "forgot": "Forgot 😞", "hard": "Hard 😟", "okay": "Okay 😐",
        "good": "Good 😊", "perfect": "Perfect 🌟",
        "tawbah_title": "🤲 Tawbah Mode — Recovery Plan",
        "tawbah_msg": "You missed some revisions. Allah is Most Merciful. Let's recover together — one surah at a time.",
        "no_due": "MashaAllah! No revision due today! Rest well. 🌟",
        "select_surahs": "Select surahs you have memorized",
        "correct": "Correct! MashaAllah! 🌟", "wrong": "Wrong! Keep going 💪",
        "which_juz": "Which Juz is this surah in?",
        "login": "Sign In", "register": "Create Account",
        "username": "Username", "password": "Password",
        "logout": "Logout", "league": "League",
        "welcome_back": "Welcome back",
        "account_created": "Account created! Sign in now.",
        "invalid_creds": "Wrong username or password.",
        "user_exists": "Username already taken.",
        "name_short": "Username must be at least 3 characters.",
    },
    "ha": {
        "subtitle": "Mataimakin Kur'ani na AI",
        "dashboard": "Allon Sarrafa", "my_plan": "Shirin Bitar Yau",
        "stability": "Matakin Karfi", "mark_memorized": "Saka Surahohi",
        "quiz": "Tambayoyi", "progress": "Ci Gabana", "passport": "Takardun Hifz",
        "streak": "Kwanaki Jere", "memorized": "An Haddace", "points": "Maki na QARMA",
        "overdue": "YA WUCE LOKACI", "due_today": "YAU NE LOKACINSA", "stable": "LAFIYA",
        "revise_now": "Bita Yanzu", "rate_session": "Ba da Maki",
        "forgot": "Na Manta 😞", "hard": "Wahala 😟", "okay": "Tsakiya 😐",
        "good": "Kyau 😊", "perfect": "Cikakke 🌟",
        "tawbah_title": "🤲 Yanayin Tawba — Tsarin Murmurewa",
        "tawbah_msg": "Ka rasa wasu bita. Allah Mai Rahama ne. Bari mu murmure tare — surah guda guda.",
        "no_due": "MashaAllah! Babu bita yau! Ka huta. 🌟",
        "select_surahs": "Zaɓi surahohin da ka haddace",
        "correct": "Daidai! MashaAllah! 🌟", "wrong": "Kuskure! Ka ci gaba 💪",
        "which_juz": "Wane Juz ne wannan surah take ciki?",
        "login": "Shiga", "register": "Ƙirƙiri Asusun",
        "username": "Sunan Mai Amfani", "password": "Kalmar Sirri",
        "logout": "Fita", "league": "Matsayi",
        "welcome_back": "Barka da dawowa",
        "account_created": "An ƙirƙiri asusun! Ka shiga yanzu.",
        "invalid_creds": "Sunan mai amfani ko kalmar sirri ba daidai ba.",
        "user_exists": "An riga an yi wannan sunan.",
        "name_short": "Sunan dole ya zama haruffa 3 aƙalla.",
    }
}

# ── FORGETTING CURVE ENGINE ───────────────────────────────────────
# na koyi wannan daga Hermann Ebbinghaus wanda ya gano a 1885
# i learned this from Hermann Ebbinghaus who discovered it in 1885
# idan ka haddace surah amma ba ka bita ba — kwakwalwarka za ta manta
# if you memorize a surah but don't revise — your brain will forget
INTERVALS = [1, 3, 7, 14, 21, 60, 180, 365]

def calculate_stability(record):
    """
    Kirga karfin ƙwaƙwalwa bisa tsarin Ebbinghaus
    Calculate memory stability based on Ebbinghaus forgetting curve.
    Stability starts at 100% and decays based on days since last revision.
    More revisions = slower decay = stronger long-term memory.
    """
    if not record.get("last_date"):
        return 100.0
    last = date.fromisoformat(record["last_date"])
    days_since = (date.today() - last).days
    times = record.get("times_revised", 0)
    # adaptive decay — more revisions means slower forgetting
    # wannan shine zuciyar QARMA - this is the heart of QARMA
    if times == 0:
        decay_rate = 0.5      # never revised — forgets fast
    elif times < 3:
        decay_rate = 0.3      # revised a few times
    elif times < 6:
        decay_rate = 0.15     # well practiced
    elif times < 10:
        decay_rate = 0.08     # very strong
    else:
        decay_rate = 0.04     # deeply memorized — almost permanent
    stability = 100 * (0.5 ** (days_since * decay_rate))
    return max(0.0, min(100.0, stability))

def get_next_revision(record):
    """Gano ranar bita mai zuwa / Get next revision date"""
    times = record.get("times_revised", 0)
    days = INTERVALS[min(times, len(INTERVALS) - 1)]
    last = record.get("last_date")
    if not last:
        return str(date.today())
    return str(date.fromisoformat(last) + timedelta(days=days))

def is_due_today(record):
    """Duba idan surah tana bukatar bita yau / Check if surah is due today"""
    return date.fromisoformat(get_next_revision(record)) <= date.today()

def days_overdue(record):
    """Nawa kwanaki ya wuce lokaci / How many days past due date"""
    next_rev = get_next_revision(record)
    delta = (date.today() - date.fromisoformat(next_rev)).days
    return max(0, delta)

def get_stability_color(s):
    """Kalar matakin karfi / Color based on stability level"""
    if s >= 80: return "#51cf66"
    elif s >= 60: return "#D4AF37"
    elif s >= 40: return "#ff922b"
    else: return "#ff6b6b"

def get_league(points):
    """Matsayin mai amfani / User league based on points"""
    if points >= 50000: return "💎 Diamond Hafiz", "#b9f2ff"
    elif points >= 25000: return "🔵 Platinum Hafiz", "#a8d8ea"
    elif points >= 10000: return "🥇 Gold Hafiz", "#D4AF37"
    elif points >= 5000: return "🥈 Silver Hafiz", "#C0C0C0"
    elif points >= 1000: return "🥉 Bronze Hafiz", "#CD7F32"
    else: return "📖 Student", "#90EE90"

# ── SESSION STATE HELPERS ─────────────────────────────────────────
def fresh_user_data(name):
    """Sabon bayani don mai amfani sabon / Fresh data for new user"""
    return {
        "name": name,
        "lang": "en",
        "streak": 0,
        "last_session": None,
        "points": 0,
        "surahs": {},
        "start_date": str(date.today()),
        "total_sessions": 0,
    }

def init_state():
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "data" not in st.session_state:
        st.session_state.data = {}
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
    if "revising" not in st.session_state:
        st.session_state.revising = None
    if "quiz_q" not in st.session_state:
        st.session_state.quiz_q = None
    if "quiz_done" not in st.session_state:
        st.session_state.quiz_done = False

def get_surah_record(num):
    """Dawo da bayanan surah / Get surah record, create if missing"""
    key = str(num)
    if key not in st.session_state.data["surahs"]:
        st.session_state.data["surahs"][key] = {
            "memorized": False,
            "score": 0,
            "times_revised": 0,
            "last_date": None,
            "stability": 100.0,
        }
    return st.session_state.data["surahs"][key]

def update_revision(surah_num, rating):
    """
    Sabunta maki bayan bita / Update score after revision.
    Rating 1-5:
    1 = Na manta / forgot completely → lose points, reset interval
    2 = Wahala / hard → lose small points
    3 = Tsakiya / okay → keep same
    4 = Kyau / good → gain points, advance interval
    5 = Cikakke / perfect → gain most points, advance interval faster
    """
    rec = get_surah_record(surah_num)
    old_score = rec["score"]

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
    else:
        rec["score"] = min(5, old_score + 2)
        rec["times_revised"] += 1
        points_change = 50

    rec["last_date"] = str(date.today())
    rec["stability"] = calculate_stability(rec)

    # Maki ba zai fadi kasa da sifili ba / Points never go below zero
    st.session_state.data["points"] = max(
        0, st.session_state.data["points"] + points_change
    )

    # Sabunta silsila / Update streak
    today = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))
    last = st.session_state.data.get("last_session")
    if last != today:
        if last == yesterday:
            st.session_state.data["streak"] += 1
        else:
            st.session_state.data["streak"] = 1
        st.session_state.data["last_session"] = today
        st.session_state.data["total_sessions"] = \
            st.session_state.data.get("total_sessions", 0) + 1

    sync_data()
    return points_change

# ── LOGIN PAGE ────────────────────────────────────────────────────
def render_login():
    # language selector before login
    lang = st.selectbox("🌍 Language", ["English", "Hausa"],
                        label_visibility="collapsed")
    L = LANG["en"] if lang == "English" else LANG["ha"]

    st.markdown(f"""
    <div style='text-align:center; padding:30px 0 20px 0;'>
        <div class='bismillah'>بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</div>
        <div class='qarma-title'>🕌 QARMA</div>
        <div class='qarma-subtitle'>{L["subtitle"]}</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs([f"🔑 {L['login']}", f"✨ {L['register']}"])
        users = load_all_users()

        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            u = st.text_input(L["username"], key="login_user",
                              placeholder="your_username")
            p = st.text_input(L["password"], type="password",
                              key="login_pass", placeholder="••••••••")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"🚀 {L['login']}", key="do_login"):
                if u in users and users[u]["password"] == make_hash(p):
                    st.session_state.current_user = u
                    st.session_state.data = users[u]["data"]
                    st.success(f"✅ {L['welcome_back']}, {u}!")
                    st.rerun()
                else:
                    st.error(f"❌ {L['invalid_creds']}")

        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            nu = st.text_input(L["username"], key="reg_user",
                               placeholder="choose_username")
            np = st.text_input(L["password"], type="password",
                               key="reg_pass", placeholder="••••••••")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"✨ {L['register']}", key="do_register"):
                if nu in users:
                    st.error(f"❌ {L['user_exists']}")
                elif len(nu) < 3:
                    st.error(f"❌ {L['name_short']}")
                elif len(np) < 4:
                    st.error("❌ Password must be at least 4 characters.")
                else:
                    users[nu] = {
                        "password": make_hash(np),
                        "data": fresh_user_data(nu)
                    }
                    save_all_users(users)
                    st.success(f"✅ {L['account_created']}")

    st.markdown("""
    <div style='text-align:center; color:#aaa; font-size:0.8em; margin-top:40px;'>
        Built for the Ummah 🌍 | github.com/muhdsalehab01-cmd/QARMA-
    </div>
    """, unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────
def render_sidebar():
    L = LANG[st.session_state.data.get("lang", "en")]
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding:15px 0;'>
            <div style='font-family:Cinzel,serif; font-size:1.8em;
                        color:#D4AF37; letter-spacing:3px;'>🕌 QARMA</div>
            <div style='font-family:Amiri,serif; font-size:0.85em;
                        color:#F5E6B3;'>بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</div>
        </div>
        """, unsafe_allow_html=True)
        st.divider()

        # Language
        lang_choice = st.selectbox(
            "🌍 Language / Harshe",
            ["English", "Hausa"],
            index=0 if st.session_state.data.get("lang", "en") == "en" else 1
        )
        new_lang = "en" if lang_choice == "English" else "ha"
        if new_lang != st.session_state.data.get("lang"):
            st.session_state.data["lang"] = new_lang
            sync_data()
        L = LANG[st.session_state.data["lang"]]

        # User stats
        name = st.session_state.data.get("name", "Hafiz")
        memorized = sum(1 for n in ALL_SURAHS if get_surah_record(n)["memorized"])
        streak = st.session_state.data.get("streak", 0)
        points = st.session_state.data.get("points", 0)
        league, league_color = get_league(points)

        st.markdown(f"""
        <div style='color:#D4AF37; font-weight:600; margin-bottom:10px;'>
            👤 {name}
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-number'>{memorized}</div>
                <div class='stat-label'>{L["memorized"]}</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-number'>{streak}🔥</div>
                <div class='stat-label'>{L["streak"]}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class='stat-card' style='margin-top:8px;'>
            <div class='stat-number' style='font-size:1.4em;'>⭐ {points:,}</div>
            <div class='stat-label'>{L["points"]}</div>
            <div style='margin-top:6px;'>
                <span class='league-badge'
                    style='background:rgba(212,175,55,0.15);
                           color:{league_color};'>{league}</span>
            </div>
        </div>""", unsafe_allow_html=True)

        st.divider()

        # Navigation
        pages = [
            ("🏠", L["dashboard"], "dashboard"),
            ("📖", L["mark_memorized"], "mark"),
            ("🎯", L["quiz"], "quiz"),
            ("📊", L["progress"], "progress"),
            ("🏆", L["passport"], "passport"),
        ]
        for icon, label, pg in pages:
            if st.button(f"{icon} {label}", key=f"nav_{pg}"):
                st.session_state.page = pg
                st.session_state.revising = None
                st.rerun()

        st.divider()
        if st.button(f"🚪 {L['logout']}", key="logout_btn"):
            sync_data()
            st.session_state.current_user = None
            st.session_state.data = {}
            st.session_state.page = "dashboard"
            st.rerun()

# ── DASHBOARD ─────────────────────────────────────────────────────
def render_dashboard():
    L = LANG[st.session_state.data.get("lang", "en")]
    name = st.session_state.data.get("name", "Student")

    st.markdown(f"""
    <div class='qarma-header'>
        <div class='bismillah'>بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</div>
        <div class='qarma-title'>QARMA</div>
        <div class='qarma-subtitle'>{L["subtitle"]}</div>
        <div style='color:#F5E6B3; margin-top:8px; font-size:0.9em;'>
            Assalamu Alaykum,
            <strong style='color:#D4AF37;'>{name}</strong> 🌙 —
            {date.today().strftime("%A, %d %B %Y")}
        </div>
    </div>
    """, unsafe_allow_html=True)

    memorized = [n for n in ALL_SURAHS if get_surah_record(n)["memorized"]]

    if not memorized:
        st.markdown(f"""
        <div class='qarma-card' style='text-align:center; padding:40px;'>
            <div style='font-size:3em;'>🕌</div>
            <div style='color:#D4AF37; font-family:Cinzel,serif;
                        font-size:1.2em; margin:10px 0;'>Welcome to QARMA</div>
            <div style='color:#F5E6B3;'>
                Start by marking your memorized surahs.<br>
                Go to <strong>"{L["mark_memorized"]}"</strong> in the sidebar.
            </div>
        </div>""", unsafe_allow_html=True)
        return

    # Categorize surahs
    overdue_list, due_today_list = [], []
    for n in memorized:
        rec = get_surah_record(n)
        rec["stability"] = calculate_stability(rec)
        od = days_overdue(rec)
        if od > 0:
            overdue_list.append((n, od))
        elif is_due_today(rec):
            due_today_list.append(n)
    overdue_list.sort(key=lambda x: x[1], reverse=True)

    # Tawbah mode
    if len(overdue_list) >= 5:
        st.markdown(f"""
        <div class='tawbah-card'>
            <div style='color:#D4AF37; font-family:Cinzel,serif;
                        font-size:1.05em; margin-bottom:6px;'>
                {L["tawbah_title"]}
            </div>
            <div style='color:#F5E6B3; font-size:0.9em;'>
                {L["tawbah_msg"]}
            </div>
            <div style='color:#D4AF37; margin-top:8px; font-weight:600;'>
                Revision Debt: {len(overdue_list)} surahs —
                Recovering {min(3, len(overdue_list))} today 💪
            </div>
        </div>""", unsafe_allow_html=True)
        overdue_list = overdue_list[:3]

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown(f"### 📅 {L['my_plan']}")

        if not overdue_list and not due_today_list:
            st.markdown(f"""
            <div style='background:rgba(50,180,100,0.15);
                        border-left:4px solid #51cf66;
                        border-radius:8px; padding:15px; margin:8px 0;'>
                ✅ <strong style='color:#51cf66;'>{L["no_due"]}</strong>
            </div>""", unsafe_allow_html=True)

        def surah_card(n, badge_color, badge_text, is_overdue_days=0):
            s = ALL_SURAHS[n]
            rec = get_surah_record(n)
            stab = rec.get("stability", calculate_stability(rec))
            col = get_stability_color(stab)
            cls = "surah-overdue" if is_overdue_days > 0 else "surah-today"
            tag = f"{badge_text} — {is_overdue_days} days" \
                  if is_overdue_days > 0 else badge_text
            st.markdown(f"""
            <div class='{cls}'>
                <div style='display:flex; justify-content:space-between;
                            align-items:center;'>
                    <div>
                        <span style='color:{badge_color}; font-weight:700;
                                     font-size:0.75em;'>{tag}</span><br>
                        <span style='color:#E8E8E8; font-weight:600;'>
                            {s["name"]}</span>
                        <span style='color:#F5E6B3; font-size:0.85em;'>
                            — {s["arabic"]}</span>
                        <span style='color:#aaa; font-size:0.78em;'>
                            | Juz {s["juz"]} | {s["ayahs"]} ayahs</span>
                    </div>
                    <div style='text-align:right;'>
                        <div style='color:{col}; font-weight:700;'>
                            {stab:.0f}%</div>
                        <div style='font-size:0.72em; color:#aaa;'>
                            stability</div>
                    </div>
                </div>
                <div class='stability-bar-bg'>
                    <div class='stability-bar'
                         style='width:{stab}%; background:{col};'></div>
                </div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"📖 {L['revise_now']} — {s['name']}",
                         key=f"rev_{n}"):
                st.session_state.revising = n
                st.rerun()

        for n, od in overdue_list:
            surah_card(n, "#ff6b6b", f"🔴 {L['overdue']}", od)
        for n in due_today_list:
            surah_card(n, "#D4AF37", f"⭐ {L['due_today']}")

    with col2:
        st.markdown(f"### 📊 {L['stability']}")
        for n in memorized[:10]:
            s = ALL_SURAHS[n]
            rec = get_surah_record(n)
            stab = calculate_stability(rec)
            col = get_stability_color(stab)
            st.markdown(f"""
            <div style='margin:5px 0;'>
                <div style='display:flex; justify-content:space-between;'>
                    <span style='color:#E8E8E8; font-size:0.83em;'>
                        {s["name"]}</span>
                    <span style='color:{col}; font-weight:700;
                                 font-size:0.83em;'>{stab:.0f}%</span>
                </div>
                <div class='stability-bar-bg'>
                    <div class='stability-bar'
                         style='width:{stab}%; background:{col};'></div>
                </div>
            </div>""", unsafe_allow_html=True)

    if st.session_state.revising:
        render_revision_session()

# ── REVISION SESSION ──────────────────────────────────────────────
def render_revision_session():
    L = LANG[st.session_state.data.get("lang", "en")]
    n = st.session_state.revising
    s = ALL_SURAHS[n]
    rec = get_surah_record(n)
    stab = calculate_stability(rec)
    col = get_stability_color(stab)
    nxt = INTERVALS[min(rec.get("times_revised", 0), len(INTERVALS) - 1)]

    st.divider()
    st.markdown(f"""
    <div class='qarma-card' style='border-color:rgba(212,175,55,0.7);'>
        <div style='text-align:center;'>
            <div style='font-family:Amiri,serif; font-size:2.2em;
                        color:#D4AF37;'>{s["arabic"]}</div>
            <div style='font-family:Cinzel,serif; font-size:1.2em;
                        color:#E8E8E8; margin:6px 0;'>
                Surah {n}: {s["name"]}</div>
            <div style='color:#aaa; font-size:0.88em;'>
                Juz {s["juz"]} | {s["ayahs"]} Ayahs</div>
            <div style='color:{col}; font-weight:700; margin:8px 0;'>
                Stability: {stab:.0f}%</div>
            <div style='color:#F5E6B3; font-size:0.85em;'>
                After revision → next review in
                <strong style='color:#D4AF37;'>{nxt} days</strong>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"#### {L['rate_session']}")
    ratings = [
        (1, L["forgot"], "#ff6b6b"),
        (2, L["hard"], "#ff922b"),
        (3, L["okay"], "#D4AF37"),
        (4, L["good"], "#69db7c"),
        (5, L["perfect"], "#51cf66"),
    ]
    cols = st.columns(5)
    for i, (rating, label, _) in enumerate(ratings):
        with cols[i]:
            if st.button(label, key=f"rate_{rating}_{n}"):
                pts = update_revision(n, rating)
                emoji = ["", "😞", "😟", "😐", "😊", "🌟"][rating]
                if rating >= 4:
                    st.success(f"{emoji} +{pts} QP! "
                               f"{L['correct'] if rating==5 else 'Well done!'}")
                elif rating == 3:
                    st.info(f"😐 +{pts} QP. Keep going!")
                else:
                    st.warning(f"{emoji} {pts} QP. {L['wrong']}")
                st.session_state.revising = None
                st.rerun()

    if st.button("✕ Cancel Revision", key="cancel_rev"):
        st.session_state.revising = None
        st.rerun()

# ── MARK MEMORIZED ────────────────────────────────────────────────
def render_mark_memorized():
    L = LANG[st.session_state.data.get("lang", "en")]
    st.markdown(f"## 📖 {L['mark_memorized']}")
    st.markdown(f"<p style='color:#F5E6B3;'>"
                f"{L['select_surahs']}</p>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("⚡ All Juz 30 (78–114)"):
            for n in range(78, 115):
                rec = get_surah_record(n)
                if not rec["memorized"]:
                    rec["memorized"] = True
                    rec["last_date"] = str(date.today())
                    st.session_state.data["points"] += 75
            sync_data()
            st.success("MashaAllah! Juz 30 marked! ✅")
            st.rerun()
    with c2:
        if st.button("⚡ Al-Fatihah (1)"):
            rec = get_surah_record(1)
            if not rec["memorized"]:
                rec["memorized"] = True
                rec["last_date"] = str(date.today())
                st.session_state.data["points"] += 75
            sync_data()
            st.success("Al-Fatihah marked! ✅")
    with c3:
        if st.button("⚡ All Juz 29 (67–77)"):
            for n in range(67, 78):
                rec = get_surah_record(n)
                if not rec["memorized"]:
                    rec["memorized"] = True
                    rec["last_date"] = str(date.today())
                    st.session_state.data["points"] += 75
            sync_data()
            st.success("MashaAllah! Juz 29 marked! ✅")
            st.rerun()
    with c4:
        if st.button("🗑️ Clear All"):
            st.session_state.data["surahs"] = {}
            sync_data()
            st.warning("All cleared.")
            st.rerun()

    st.divider()

    # Group by Juz
    juz_groups = {}
    for n, s in ALL_SURAHS.items():
        juz_groups.setdefault(s["juz"], []).append(n)

    for juz_num in sorted(juz_groups.keys()):
        mem_in_juz = sum(1 for n in juz_groups[juz_num]
                         if get_surah_record(n)["memorized"])
        total_in_juz = len(juz_groups[juz_num])
        label = f"📚 Juz {juz_num}   ({mem_in_juz}/{total_in_juz} memorized)"
        with st.expander(label, expanded=(juz_num == 30)):
            cols = st.columns(3)
            for i, n in enumerate(juz_groups[juz_num]):
                s = ALL_SURAHS[n]
                rec = get_surah_record(n)
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
                        sync_data()
                        st.rerun()

# ── QUIZ ──────────────────────────────────────────────────────────
def render_quiz():
    L = LANG[st.session_state.data.get("lang", "en")]
    st.markdown(f"## 🎯 {L['quiz']}")

    memorized = [n for n in ALL_SURAHS if get_surah_record(n)["memorized"]]
    if len(memorized) < 4:
        st.warning("You need at least 4 memorized surahs for the quiz! "
                   "Go mark some first.")
        return

    if st.session_state.quiz_q is None or st.session_state.quiz_done:
        if st.button("🎲 New Question / Sabuwar Tambaya", key="new_q"):
            correct_num = random.choice(memorized)
            correct = ALL_SURAHS[correct_num]
            q_type = random.choice(["juz", "number", "arabic"])
            wrong_nums = random.sample(
                [n for n in memorized if n != correct_num],
                min(3, len(memorized) - 1)
            )
            wrong_juz = random.sample(
                [j for j in range(1, 31) if j != correct["juz"]], 3
            )
            st.session_state.quiz_q = {
                "type": q_type,
                "correct_num": correct_num,
                "wrong_nums": wrong_nums,
                "juz_options": [correct["juz"]] + wrong_juz,
                "num_options": [correct_num] + wrong_nums,
            }
            random.shuffle(st.session_state.quiz_q["juz_options"])
            random.shuffle(st.session_state.quiz_q["num_options"])
            st.session_state.quiz_done = False
            st.rerun()

    if st.session_state.quiz_q and not st.session_state.quiz_done:
        q = st.session_state.quiz_q
        correct_num = q["correct_num"]
        s = ALL_SURAHS[correct_num]

        if q["type"] == "juz":
            question = f"{L['which_juz']}"
            st.markdown(f"""
            <div class='qarma-card' style='text-align:center;'>
                <div style='font-family:Amiri,serif; font-size:2.2em;
                            color:#D4AF37;'>{s["arabic"]}</div>
                <div style='color:#E8E8E8; font-size:1.05em; margin:8px 0;'>
                    Surah {correct_num}: {s["name"]}</div>
                <div style='color:#F5E6B3;'>{question}</div>
            </div>""", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, opt in enumerate(q["juz_options"]):
                with cols[i % 2]:
                    if st.button(f"Juz {opt}", key=f"qopt_{i}"):
                        if opt == s["juz"]:
                            st.success(f"✅ {L['correct']}")
                            update_revision(correct_num, 5)
                        else:
                            st.error(f"❌ {L['wrong']} — Juz {s['juz']}")
                            update_revision(correct_num, 1)
                        st.session_state.quiz_done = True
                        st.rerun()

        elif q["type"] == "number":
            st.markdown(f"""
            <div class='qarma-card' style='text-align:center;'>
                <div style='color:#F5E6B3; font-size:0.9em;'>
                    What is the name of</div>
                <div style='font-family:Cinzel,serif; font-size:2em;
                            color:#D4AF37;'>Surah {correct_num}?</div>
            </div>""", unsafe_allow_html=True)
            options = q["num_options"]
            cols = st.columns(2)
            for i, n in enumerate(options):
                with cols[i % 2]:
                    ss = ALL_SURAHS[n]
                    if st.button(f"{ss['name']} ({ss['arabic']})",
                                 key=f"qopt_{i}"):
                        if n == correct_num:
                            st.success(f"✅ {L['correct']}")
                            update_revision(correct_num, 5)
                        else:
                            st.error(f"❌ {L['wrong']} — {s['name']}")
                            update_revision(correct_num, 1)
                        st.session_state.quiz_done = True
                        st.rerun()

        else:  # arabic
            st.markdown(f"""
            <div class='qarma-card' style='text-align:center;'>
                <div style='color:#F5E6B3; font-size:0.9em;'>
                    Which surah is this? / Wace surah ce wannan?</div>
                <div style='font-family:Amiri,serif; font-size:3em;
                            color:#D4AF37; margin:10px 0;'>{s["arabic"]}</div>
            </div>""", unsafe_allow_html=True)
            options = q["num_options"]
            cols = st.columns(2)
            for i, n in enumerate(options):
                with cols[i % 2]:
                    ss = ALL_SURAHS[n]
                    if st.button(f"{ss['name']}", key=f"qopt_{i}"):
                        if n == correct_num:
                            st.success(f"✅ {L['correct']}")
                            update_revision(correct_num, 5)
                        else:
                            st.error(f"❌ {L['wrong']} — {s['name']}")
                            update_revision(correct_num, 1)
                        st.session_state.quiz_done = True
                        st.rerun()

# ── PROGRESS ──────────────────────────────────────────────────────
def render_progress():
    L = LANG[st.session_state.data.get("lang", "en")]
    st.markdown(f"## 📊 {L['progress']}")

    memorized = [n for n in ALL_SURAHS if get_surah_record(n)["memorized"]]
    total = len(memorized)
    percent = (total / 114) * 100

    st.markdown(f"""
    <div class='qarma-card'>
        <div style='display:flex; justify-content:space-between;
                    margin-bottom:8px;'>
            <span style='color:#D4AF37; font-family:Cinzel,serif;'>
                Quran Progress</span>
            <span style='color:#D4AF37; font-weight:700;'>
                {total}/114 ({percent:.1f}%)</span>
        </div>
    </div>""", unsafe_allow_html=True)
    st.progress(percent / 100)

    mastered = sum(1 for n in memorized if get_surah_record(n)["score"] >= 5)
    due_c = sum(1 for n in memorized if is_due_today(get_surah_record(n)))
    overdue_c = sum(1 for n in memorized if days_overdue(get_surah_record(n)) > 0)
    sessions = st.session_state.data.get("total_sessions", 0)

    c1, c2, c3, c4, c5 = st.columns(5)
    for col, label, val, color in [
        (c1, L["memorized"], total, "#D4AF37"),
        (c2, "Mastered ⭐", mastered, "#51cf66"),
        (c3, "Due Today", due_c, "#ff922b"),
        (c4, "Overdue 🔴", overdue_c, "#ff6b6b"),
        (c5, "Sessions", sessions, "#a8d8ea"),
    ]:
        with col:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-number' style='color:{color};'>{val}</div>
                <div class='stat-label'>{label}</div>
            </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("### Progress by Juz")

    juz_mem = {}
    for n in memorized:
        j = ALL_SURAHS[n]["juz"]
        juz_mem.setdefault(j, []).append(n)

    juz_groups = {}
    for n, s in ALL_SURAHS.items():
        juz_groups.setdefault(s["juz"], []).append(n)

    if juz_mem:
        for j in sorted(juz_mem.keys()):
            done = len(juz_mem[j])
            total_j = len(juz_groups[j])
            pct = done / total_j
            names = ", ".join(ALL_SURAHS[n]["name"]
                              for n in sorted(juz_mem[j]))
            st.markdown(f"""
            <div style='margin:6px 0;'>
                <div style='display:flex; justify-content:space-between;'>
                    <span style='color:#D4AF37;'>Juz {j}</span>
                    <span style='color:#F5E6B3; font-size:0.85em;'>
                        {done}/{total_j} — {names}</span>
                </div>
            </div>""", unsafe_allow_html=True)
            st.progress(pct)
    else:
        st.info("No surahs memorized yet. Use Mark Memorized to start!")

# ── HIFZ PASSPORT ─────────────────────────────────────────────────
def render_passport():
    L = LANG[st.session_state.data.get("lang", "en")]
    name = st.session_state.data.get("name", "Hafiz")
    memorized = [n for n in ALL_SURAHS if get_surah_record(n)["memorized"]]
    total = len(memorized)
    streak = st.session_state.data.get("streak", 0)
    points = st.session_state.data.get("points", 0)
    sessions = st.session_state.data.get("total_sessions", 0)
    start = st.session_state.data.get("start_date", str(date.today()))
    league, league_color = get_league(points)
    avg_stab = (sum(calculate_stability(get_surah_record(n)) for n in memorized)
                / max(1, total))
    mastered = sum(1 for n in memorized if get_surah_record(n)["score"] >= 5)

    st.markdown(f"## 🏆 {L['passport']}")

    st.markdown(f"""
    <div class='hifz-passport'>
        <div style='font-family:Amiri,serif; font-size:1.6em;
                    color:#D4AF37;'>بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</div>
        <div style='font-family:Cinzel,serif; font-size:2.2em; color:#D4AF37;
                    margin:10px 0; letter-spacing:4px;'>🕌 QARMA</div>
        <div style='font-family:Cinzel,serif; font-size:1.2em;
                    color:#E8E8E8; letter-spacing:2px;'>HIFZ PASSPORT</div>
        <div style='color:#aaa; font-size:0.85em; margin:5px 0;'>
            Member since {start} | Issued: {date.today().strftime("%d %B %Y")}
        </div>
        <hr style='border-color:rgba(212,175,55,0.4); margin:15px 0;'/>
        <div style='font-family:Cinzel,serif; font-size:1.6em;
                    color:#D4AF37; margin-bottom:15px;'>{name}</div>
        <div style='display:grid; grid-template-columns:1fr 1fr 1fr;
                    gap:12px; margin:15px 0;'>
            <div style='background:rgba(27,67,50,0.6); border-radius:10px;
                        padding:12px;'>
                <div style='font-size:1.8em; color:#D4AF37;
                            font-weight:700;'>{total}/114</div>
                <div style='color:#F5E6B3; font-size:0.78em;'>
                    Surahs Memorized</div>
            </div>
            <div style='background:rgba(27,67,50,0.6); border-radius:10px;
                        padding:12px;'>
                <div style='font-size:1.8em; color:#D4AF37;
                            font-weight:700;'>{streak}🔥</div>
                <div style='color:#F5E6B3; font-size:0.78em;'>Day Streak</div>
            </div>
            <div style='background:rgba(27,67,50,0.6); border-radius:10px;
                        padding:12px;'>
                <div style='font-size:1.8em; color:#51cf66;
                            font-weight:700;'>{mastered}</div>
                <div style='color:#F5E6B3; font-size:0.78em;'>Mastered ⭐</div>
            </div>
            <div style='background:rgba(27,67,50,0.6); border-radius:10px;
                        padding:12px;'>
                <div style='font-size:1.8em; color:#D4AF37;
                            font-weight:700;'>{avg_stab:.0f}%</div>
                <div style='color:#F5E6B3; font-size:0.78em;'>
                    Avg Stability</div>
            </div>
            <div style='background:rgba(27,67,50,0.6); border-radius:10px;
                        padding:12px;'>
                <div style='font-size:1.8em; color:#D4AF37;
                            font-weight:700;'>⭐{points:,}</div>
                <div style='color:#F5E6B3; font-size:0.78em;'>
                    QARMA Points</div>
            </div>
            <div style='background:rgba(27,67,50,0.6); border-radius:10px;
                        padding:12px;'>
                <div style='font-size:1em; font-weight:700;
                            color:{league_color}; margin-top:5px;'>
                    {league}</div>
                <div style='color:#F5E6B3; font-size:0.78em;'>League</div>
            </div>
        </div>
        <div style='color:#D4AF37; font-family:Amiri,serif;
                    font-size:1.1em; font-style:italic;'>
            "وَرَتِّلِ الْقُرْآنَ تَرْتِيلًا"
        </div>
        <div style='color:#F5E6B3; font-size:0.82em; margin-top:4px;'>
            "And recite the Qur'an with measured recitation"
            — Al-Muzzammil 73:4
        </div>
        <div style='color:#666; font-size:0.75em; margin-top:15px;'>
            github.com/muhdsalehab01-cmd/QARMA- |
            Built for the Ummah 🌍 | Sessions: {sessions}
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("### 📤 Share Your Progress")
    share_text = (
        f"🕌 QARMA Hifz Report\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 {name}\n"
        f"📖 Memorized: {total}/114 Surahs\n"
        f"⭐ Mastered: {mastered} Surahs\n"
        f"🔥 Streak: {streak} days\n"
        f"⭐ Points: {points:,} QP\n"
        f"🏆 League: {league}\n"
        f"📊 Avg Stability: {avg_stab:.0f}%\n"
        f"📅 Sessions: {sessions}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"QARMA — AI Quran Memorization\n"
        f"For African Muslims 🌍\n"
        f"#QARMA #Quran #Hifz #Africa"
    )
    st.code(share_text, language=None)
    st.info("📱 Copy the text above and share on WhatsApp, Twitter or Instagram!")

# ── MAIN ──────────────────────────────────────────────────────────
def main():
    init_state()

    # idan ba a shiga ba - if not logged in
    if not st.session_state.current_user:
        render_login()
        return

    # nuna sidebar da shafin da aka zaba
    # show sidebar and selected page
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
