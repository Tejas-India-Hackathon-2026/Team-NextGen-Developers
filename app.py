import streamlit as st
import os
import json
import base64
import hashlib
from datetime import datetime

# ==================================================
# 🎨 PAGE CONFIGURATION & METADATA
# ==================================================
st.set_page_config(
    page_title="CampusHub - Student Resource Sharing Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# 🗄️ DIRECTORIES & DATA STORAGE
# ==================================================
MATERIAL_FOLDER = "materials"
ANNOUNCEMENTS_FILE = "announcements.json"
METADATA_FILE = "materials_meta.json"
REQUESTS_FILE = "material_requests.json"
USERS_FILE = "users.json"
ATTENDANCE_FILE = "attendance.json"
TIMETABLE_FILE = "timetable.json"
EXAM_SCHEDULE_FILE = "exam_schedule.json"

os.makedirs(MATERIAL_FOLDER, exist_ok=True)

# ==================================================
# 💎 ULTRA-PREMIUM MODERN LIGHT THEME DESIGN SYSTEM (CSS)
# ==================================================
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

    :root {
        --primary-indigo: #4F46E5;
        --primary-violet: #7C3AED;
        --accent-cyan: #0284C7;
        --accent-emerald: #059669;
        --accent-rose: #E11D48;
        --accent-amber: #D97706;
        --bg-main: #F8FAFC;
        --bg-card: #FFFFFF;
        --border-card: #E2E8F0;
        --text-primary: #0F172A;
        --text-secondary: #334155;
        --text-muted: #64748B;
    }

    /* Light Theme Global Canvas */
    .stApp {
        background: #F8FAFC !important;
        color: #1E293B !important;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1E293B;
        font-size: 15px;
    }

    /* Increased Typography Hierarchy */
    h1 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        font-size: 34px !important;
        letter-spacing: -0.03em !important;
        color: #0F172A !important;
        margin-bottom: 8px !important;
    }

    h2 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        font-size: 28px !important;
        letter-spacing: -0.025em !important;
        color: #0F172A !important;
        margin-top: 14px !important;
        margin-bottom: 8px !important;
    }

    h3 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 22px !important;
        letter-spacing: -0.02em !important;
        color: #0F172A !important;
    }

    h4 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        color: #0F172A !important;
    }

    p, span, label, div {
        color: #334155;
    }

    strong, b {
        color: #0F172A;
        font-weight: 700;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
        background: #F1F5F9 !important;
        color: #4338CA !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 6px !important;
    }

    /* Sleek Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #F1F5F9;
    }
    ::-webkit-scrollbar-thumb {
        background: #CBD5E1;
        border-radius: 9999px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94A3B8;
    }

    /* Keyframe Animations */
    @keyframes pulseGlow {
        0%, 100% { transform: scale(1); opacity: 1; box-shadow: 0 0 10px rgba(16, 185, 129, 0.6); }
        50% { transform: scale(1.15); opacity: 0.85; box-shadow: 0 0 16px rgba(16, 185, 129, 0.8); }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }

    /* Live Status Indicator */
    .live-pulse {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10B981;
        animation: pulseGlow 2.4s infinite ease-in-out;
        margin-right: 6px;
        vertical-align: middle;
    }

    /* Clean Sidebar Styling with Enlarged Nav Menu */
    section[data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.03) !important;
    }

    /* Enlarged Navigation Radio Buttons in Sidebar */
    section[data-testid="stSidebar"] .stRadio > div {
        gap: 6px !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        font-size: 15px !important;
        font-weight: 600 !important;
        font-family: 'Outfit', sans-serif !important;
        color: #334155 !important;
        padding: 10px 14px !important;
        border-radius: 12px !important;
        background: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-bottom: 4px !important;
        display: flex !important;
        align-items: center !important;
        cursor: pointer !important;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background: #EEF2FF !important;
        border-color: #C7D2FE !important;
        color: #4338CA !important;
        transform: translateX(3px) !important;
    }
    section[data-testid="stSidebar"] .stRadio label[data-checked="true"],
    section[data-testid="stSidebar"] .stRadio div[aria-checked="true"] {
        background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
        color: #FFFFFF !important;
        border-color: #4F46E5 !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
    }

    /* Sidebar Profile Card (Light) */
    .profile-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    /* Ultra-Modern Hero Banner (Light Contrast Gradient) */
    .hero-container {
        background: linear-gradient(135deg, #312E81 0%, #4338CA 30%, #6366F1 70%, #7C3AED 100%);
        border-radius: 20px;
        padding: 36px 40px;
        color: white !important;
        margin-bottom: 24px;
        box-shadow: 0 16px 36px -10px rgba(79, 70, 229, 0.35);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .hero-container h1, .hero-container p, .hero-container span {
        color: white !important;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -60%;
        right: -15%;
        width: 420px;
        height: 420px;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }

    /* Premium Light Cards */
    .glass-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 18px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05), 0 2px 6px -1px rgba(0, 0, 0, 0.02);
        transition: all 0.26s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 30px -4px rgba(0, 0, 0, 0.1), 0 0 15px rgba(99, 102, 241, 0.12);
        border-color: #C7D2FE;
    }

    /* Quick Revision Specific Cards (Light) */
    .revision-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 6px solid #4F46E5;
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 18px;
        box-shadow: 0 4px 16px -2px rgba(0, 0, 0, 0.04);
    }

    /* Enlarged Metric KPI Box */
    .metric-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 22px 20px;
        display: flex;
        align-items: center;
        gap: 18px;
        box-shadow: 0 4px 18px -2px rgba(0, 0, 0, 0.05);
        transition: all 0.24s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .metric-box:hover {
        transform: translateY(-3px);
        border-color: #C7D2FE;
        box-shadow: 0 10px 25px -4px rgba(79, 70, 229, 0.15);
    }
    .metric-icon {
        font-size: 30px;
        width: 58px;
        height: 58px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .metric-val {
        font-size: 32px;
        font-weight: 800;
        font-family: 'Outfit', sans-serif;
        color: #0F172A;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }
    .metric-label {
        font-size: 13px;
        color: #64748B;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 3px;
    }

    /* Vibrant Badges & Pills */
    .badge-urgent {
        background: #FEE2E2;
        color: #DC2626;
        border: 1px solid #FECACA;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        display: inline-block;
    }
    .badge-important {
        background: #FEF3C7;
        color: #D97706;
        border: 1px solid #FDE68A;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        display: inline-block;
    }
    .badge-general {
        background: #DBEAFE;
        color: #1D4ED8;
        border: 1px solid #BFDBFE;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        display: inline-block;
    }
    .badge-open {
        background: #D1FAE5;
        color: #059669;
        border: 1px solid #A7F3D0;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        display: inline-block;
    }
    .badge-fulfilled {
        background: #EDE9FE;
        color: #6D28D9;
        border: 1px solid #DDD6FE;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        display: inline-block;
    }
    .tag-chip {
        display: inline-flex;
        align-items: center;
        background: #EEF2FF;
        color: #4338CA;
        border: 1px solid #C7D2FE;
        border-radius: 8px;
        padding: 4px 12px;
        font-size: 13px;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 4px;
    }
    .tag-new {
        display: inline-flex;
        align-items: center;
        background: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
        border-radius: 8px;
        padding: 4px 12px;
        font-size: 13px;
        font-weight: 700;
        margin-right: 6px;
        margin-bottom: 4px;
    }

    /* Home Dashboard Quick Action Launchpad */
    .quick-action-tile {
        background: #FFFFFF;
        border: 1.5px solid #E2E8F0;
        border-radius: 16px;
        padding: 16px 18px;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    .quick-action-tile:hover {
        transform: translateY(-3px);
        border-color: #818CF8;
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.12);
        background: #F8FAFC;
    }
    .quick-action-icon {
        width: 46px;
        height: 46px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        flex-shrink: 0;
    }

    /* Square Portal Tile (Horizontal Grid) */
    .square-portal-tile {
        background: #FFFFFF;
        border: 1.5px solid #E2E8F0;
        border-radius: 18px;
        padding: 20px 16px;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 145px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
        transition: all 0.24s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .square-portal-tile:hover {
        transform: translateY(-4px);
        border-color: #4F46E5;
        box-shadow: 0 12px 24px -4px rgba(79, 70, 229, 0.18);
    }
    .square-logo-box {
        width: 52px;
        height: 52px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .square-portal-title {
        font-size: 15px;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 4px;
        line-height: 1.2;
    }
    .square-portal-sub {
        font-size: 12px;
        color: #64748B;
        font-weight: 500;
    }

    /* Square Subject Cards (Horizontal Layout) */
    .square-subject-tile {
        background: #FFFFFF;
        border: 1.5px solid #E2E8F0;
        border-radius: 18px;
        padding: 18px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 160px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
        transition: all 0.24s ease;
    }
    .square-subject-tile:hover {
        transform: translateY(-3px);
        border-color: #818CF8;
        box-shadow: 0 10px 22px rgba(79, 70, 229, 0.12);
    }

    /* Concept of the Day Spotlight */
    .concept-card {
        background: linear-gradient(135deg, #EEF2FF 0%, #FAF5FF 100%);
        border: 1.5px solid #C7D2FE;
        border-radius: 18px;
        padding: 22px 26px;
        margin-bottom: 22px;
        box-shadow: 0 4px 16px rgba(79, 70, 229, 0.06);
    }

    /* Interactive Academic Milestone Card */
    .task-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 10px;
        transition: all 0.2s ease;
    }
    .task-box:hover {
        background: #FFFFFF;
        border-color: #CBD5E1;
    }

    /* Streamlit Global Widget Polish */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        font-family: 'Outfit', sans-serif !important;
        padding: 10px 22px !important;
        border: 1px solid #4F46E5 !important;
        background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
        color: white !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.45) !important;
        background: linear-gradient(135deg, #4338CA 0%, #4F46E5 100%) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    .stDownloadButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        font-family: 'Outfit', sans-serif !important;
        padding: 10px 22px !important;
        border: 1px solid #059669 !important;
        background: linear-gradient(135deg, #059669 0%, #10B981 100%) !important;
        color: white !important;
        box-shadow: 0 4px 14px rgba(5, 150, 105, 0.25) !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(5, 150, 105, 0.4) !important;
    }

    .stLinkButton > a {
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        font-family: 'Outfit', sans-serif !important;
        border: 1px solid #CBD5E1 !important;
        background: #FFFFFF !important;
        color: #4F46E5 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.2s ease !important;
    }
    .stLinkButton > a:hover {
        background: #EEF2FF !important;
        border-color: #818CF8 !important;
        transform: translateY(-2px) !important;
    }

    /* Enlarged Tabs Styling (Light) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #F1F5F9;
        padding: 6px;
        border-radius: 14px;
        border: 1px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 700;
        font-size: 15px;
        font-family: 'Outfit', sans-serif;
        color: #64748B;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: #4F46E5 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.35);
    }

    /* Inputs Polish (Light Theme) */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 12px !important;
        color: #0F172A !important;
        font-size: 15px !important;
        padding: 10px 14px !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
        border-color: #4F46E5 !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.18) !important;
    }
    .stSelectbox > div > div {
        background: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 12px !important;
        font-size: 15px !important;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 50%, #059669 100%) !important;
        border-radius: 9999px !important;
    }

    /* Tables in Cheatsheets & Revision (Light) */
    table {
        border-collapse: collapse;
        width: 100%;
        background: #FFFFFF;
        border-radius: 10px;
        overflow: hidden;
    }
    table th {
        background: #F1F5F9;
        color: #0F172A;
        font-weight: 700;
        padding: 10px 14px;
        border-bottom: 2px solid #E2E8F0;
        text-align: left;
    }
    table td {
        padding: 10px 14px;
        border-bottom: 1px solid #F1F5F9;
        color: #334155;
    }

    /* ============================================
       LOGIN PAGE LIGHT THEME STYLES
       ============================================ */
    .login-container-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 24px;
        padding: 38px 44px;
        box-shadow: 0 20px 45px -10px rgba(0, 0, 0, 0.08), 0 0 25px rgba(79, 70, 229, 0.06);
        position: relative;
        margin-top: 10px;
    }
    .login-crest {
        font-size: 58px;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
        filter: drop-shadow(0 8px 16px rgba(79, 70, 229, 0.25));
    }
    .login-title-text {
        font-family: 'Outfit', sans-serif;
        font-size: 38px;
        font-weight: 900;
        background: linear-gradient(135deg, #3730A3 0%, #4F46E5 50%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }
    .login-feature-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 9999px;
        padding: 6px 14px;
        font-size: 13px;
        color: #475569;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ==================================================
# 🔐 AUTHENTICATION SYSTEM
# ==================================================

def _hash_password(password: str) -> str:
    """SHA-256 hash of the password."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users() -> dict:
    """Load registered users from JSON file."""
    if not os.path.exists(USERS_FILE):
        # Seed with a demo admin account
        default_users = {
            "admin": {
                "name": "Admin User",
                "password": _hash_password("admin123"),
                "branch": "Computer Science & Engg",
                "semester": "3rd Semester",
                "role": "Admin",
                "joined": datetime.now().strftime("%Y-%m-%d")
            }
        }
        with open(USERS_FILE, "w") as f:
            json.dump(default_users, f, indent=4)
        return default_users
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_users(users: dict):
    """Persist users dict to JSON."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def show_login_page():
    """Render the ultra-premium executive login / sign-up page and handle auth logic."""
    # Hide the sidebar and style login container
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] { display: none !important; }
        .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 100% !important; }
        
        .auth-container-wrapper {
            max-width: 520px;
            margin: 0 auto;
            padding: 10px;
        }
        .auth-badge-header {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #EEF2FF;
            border: 1px solid #C7D2FE;
            border-radius: 9999px;
            padding: 5px 16px;
            color: #4338CA;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 12px;
        }
        .demo-pill-card {
            background: #F8FAFC;
            border: 1.5px dashed #C7D2FE;
            border-radius: 12px;
            padding: 12px 16px;
            margin-top: 18px;
            text-align: center;
        }
        .auth-feature-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 24px;
        }
        .auth-mini-feat {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 10px 12px;
            font-size: 12px;
            color: #334155;
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 500;
        }
    </style>
    """, unsafe_allow_html=True)

    # ── Centered Container ───────────────────────────
    col_l, col_center, col_r = st.columns([1, 2.2, 1])
    with col_center:
        # ── Page Header ──────────────────────────────
        st.markdown("""
        <div style="text-align:center; padding: 24px 0 16px;">
            <div class="auth-badge-header">
                <span class="live-pulse"></span> Academic Portal · AY 2026
            </div>
            <div class="login-crest">🎓</div>
            <div class="login-title-text">CampusHub</div>
            <div style="font-size:15px; color:#475569; font-weight:600; margin-top:6px;">
                Student Resource Network &amp; Academic Toolkit
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='login-container-card'>", unsafe_allow_html=True)

        tab_choice = st.radio(
            "auth_tab",
            ["🔑  Sign In to CampusHub", "✨  Create New Student Account"],
            horizontal=True,
            label_visibility="collapsed",
            key="auth_tab_radio"
        )

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

        if "Sign In" in tab_choice:
            # ── LOGIN FORM ────────────────────────────
            with st.form("login_form", clear_on_submit=False):
                username_in = st.text_input(
                    "👤 Username",
                    placeholder="Enter your student username (e.g. admin)",
                    key="login_username"
                )
                password_in = st.text_input(
                    "🔒 Password",
                    type="password",
                    placeholder="••••••••••••",
                    key="login_password"
                )
                st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
                submit_login = st.form_submit_button(
                    "Sign In to CampusHub →",
                    use_container_width=True,
                    type="primary"
                )

            if submit_login:
                users = load_users()
                uname = username_in.strip().lower()
                if not uname or not password_in:
                    st.error("⚠️ Please fill in both your username and password.")
                elif uname not in users:
                    st.error("❌ Account not found. Please switch to the 'Create Account' tab.")
                elif users[uname]["password"] != _hash_password(password_in):
                    st.error("❌ Incorrect password. Please verify and try again.")
                else:
                    user_data = users[uname]
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = uname
                    st.session_state["student_name"] = user_data["name"]
                    st.session_state["user_branch"] = user_data.get("branch", "Computer Science & Engg")
                    st.session_state["user_semester"] = user_data.get("semester", "3rd Semester")
                    st.session_state["user_role"] = user_data.get("role", "Student")
                    st.toast(f"Welcome back, {user_data['name']}!", icon="🚀")
                    st.rerun()

            # Demo hint badge
            st.markdown("""
            <div class="demo-pill-card">
                <span style="font-size:13px; color:#334155; font-weight:600;">⚡ Quick Demo Login:</span>
                <span style="font-family:'JetBrains Mono', monospace; font-size:13px; color:#4338CA; font-weight:700; background:#EEF2FF; border:1px solid #C7D2FE; padding:2px 8px; border-radius:6px; margin-left:6px;">admin</span>
                <span style="color:#94A3B8;">/</span>
                <span style="font-family:'JetBrains Mono', monospace; font-size:13px; color:#4338CA; font-weight:700; background:#EEF2FF; border:1px solid #C7D2FE; padding:2px 8px; border-radius:6px;">admin123</span>
            </div>
            """, unsafe_allow_html=True)

        else:
            # ── SIGN-UP FORM ──────────────────────────
            with st.form("signup_form", clear_on_submit=False):
                full_name_in = st.text_input("🎓 Full Name *", placeholder="e.g. Rahul Sharma", key="signup_name")
                new_username_in = st.text_input("👤 Desired Username *", placeholder="e.g. rahul_cs26", key="signup_username")
                
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    new_pass_in = st.text_input("🔒 Password *", type="password", placeholder="Min 6 chars", key="signup_pass")
                with col_p2:
                    confirm_pass_in = st.text_input("🔒 Confirm Password *", type="password", placeholder="Re-enter password", key="signup_confirm")
                
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    branch_in = st.selectbox(
                        "🏛️ Branch / Department",
                        [
                            "Computer Science & Engg",
                            "Information Technology",
                            "AI & Data Science",
                            "Electronics & Comm (ECE)",
                            "Electrical Engg (EEE)",
                            "Mechanical Engineering",
                            "Civil Engineering",
                            "BCA / MCA / Applied Sci",
                            "Other"
                        ],
                        key="signup_branch"
                    )
                with col_b2:
                    sem_in = st.selectbox(
                        "📅 Semester",
                        [f"{i}st Semester" if i == 1 else f"{i}nd Semester" if i == 2 else f"{i}rd Semester" if i == 3 else f"{i}th Semester" for i in range(1, 9)],
                        index=2,
                        key="signup_sem"
                    )
                
                st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
                submit_signup = st.form_submit_button(
                    "Create Student Account ✨",
                    use_container_width=True,
                    type="primary"
                )

            if submit_signup:
                users = load_users()
                uname = new_username_in.strip().lower()
                if not full_name_in.strip() or not uname or not new_pass_in:
                    st.error("⚠️ Please fill in all required fields marked with *.")
                elif len(new_pass_in) < 6:
                    st.error("⚠️ Password must contain at least 6 characters.")
                elif new_pass_in != confirm_pass_in:
                    st.error("❌ Passwords do not match.")
                elif uname in users:
                    st.error("❌ That username is already taken. Please choose another.")
                else:
                    users[uname] = {
                        "name": full_name_in.strip(),
                        "password": _hash_password(new_pass_in),
                        "branch": branch_in,
                        "semester": sem_in,
                        "role": "Student",
                        "joined": datetime.now().strftime("%Y-%m-%d")
                    }
                    save_users(users)
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = uname
                    st.session_state["student_name"] = full_name_in.strip()
                    st.session_state["user_branch"] = branch_in
                    st.session_state["user_semester"] = sem_in
                    st.session_state["user_role"] = "Student"
                    st.toast(f"Welcome to CampusHub, {full_name_in.strip()}!", icon="🎉")
                    st.rerun()

        # Mini Feature Showcase Grid
        st.markdown("""
        <div class="auth-feature-grid">
            <div class="auth-mini-feat">📚 <strong>50+ Verified Notes</strong></div>
            <div class="auth-mini-feat">⚡ <strong>1-Page Cheatsheets</strong></div>
            <div class="auth-mini-feat">📊 <strong>SGPA &amp; Attendance Guard</strong></div>
            <div class="auth-mini-feat">🔒 <strong>SHA-256 Auth Shield</strong></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Footer
        st.markdown("""
        <div style="text-align:center; margin-top:24px;">
            <span style="font-size:13px; color:#64748B;">🔒 CampusHub Platform · Fast, Modern &amp; Encrypted Student Ecosystem</span>
        </div>
        """, unsafe_allow_html=True)


# ==================================================
# 🚪 AUTH GATE — block app until user is logged in
# ==================================================
if not st.session_state.get("authenticated", False):
    show_login_page()
    st.stop()


# ==================================================
# 🛠️ DATA PERSISTENCE & AUTO-SYNC HELPERS
# ==================================================

def load_announcements():
    """Load announcements from JSON file with backward-compatible defaults."""
    if not os.path.exists(ANNOUNCEMENTS_FILE):
        default_data = [
            {
                "title": "Welcome to CampusHub Platform",
                "message": "Access study notes, syllabus copies, previous year papers, request needed materials, and compute academic metrics.",
                "priority": "General",
                "department": "Campus Admin",
                "author": "System Coordinator",
                "date": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "title": "Annual Inter-College Hackathon 2026",
                "message": "Registrations are now open for all 1st-8th semester students. Win cash prizes and internship offers!",
                "priority": "Important",
                "department": "Tech Society",
                "author": "Coding Club",
                "date": datetime.now().strftime("%Y-%m-%d")
            }
        ]
        with open(ANNOUNCEMENTS_FILE, "w") as f:
            json.dump(default_data, f, indent=4)
        return default_data

    try:
        with open(ANNOUNCEMENTS_FILE, "r") as f:
            data = json.load(f)
            for item in data:
                item.setdefault("priority", "General")
                item.setdefault("department", "General")
                item.setdefault("author", "Faculty/Admin")
                item.setdefault("date", datetime.now().strftime("%Y-%m-%d"))
            return data
    except Exception:
        return []

def save_announcements(data):
    """Save announcements data back to JSON."""
    with open(ANNOUNCEMENTS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_attendance(username="admin"):
    """Load per-student subject-wise attendance records with sensible defaults."""
    default_subjects = [
        {"id": "att_1", "subject": "Data Structures & Algorithms", "faculty": "Dr. Ramesh Verma", "attended": 38, "total": 45, "target": 75},
        {"id": "att_2", "subject": "Operating Systems", "faculty": "Prof. Sneha Kulkarni", "attended": 34, "total": 44, "target": 75},
        {"id": "att_3", "subject": "Python Programming", "faculty": "Dr. Ananya Ray", "attended": 42, "total": 45, "target": 75},
        {"id": "att_4", "subject": "Database Management Systems", "faculty": "Prof. Rajesh Kumar", "attended": 30, "total": 42, "target": 75},
        {"id": "att_5", "subject": "Mathematics-III (Discrete Structures)", "faculty": "Dr. M. S. Iyer", "attended": 28, "total": 40, "target": 75}
    ]
    
    if not os.path.exists(ATTENDANCE_FILE):
        store = {username: default_subjects}
        with open(ATTENDANCE_FILE, "w") as f:
            json.dump(store, f, indent=4)
        return default_subjects

    try:
        with open(ATTENDANCE_FILE, "r") as f:
            store = json.load(f)
        if username not in store or not store[username]:
            store[username] = default_subjects
            with open(ATTENDANCE_FILE, "w") as f:
                json.dump(store, f, indent=4)
        return store[username]
    except Exception:
        return default_subjects

def save_attendance(username, data):
    """Save student attendance list to JSON store."""
    store = {}
    if os.path.exists(ATTENDANCE_FILE):
        try:
            with open(ATTENDANCE_FILE, "r") as f:
                store = json.load(f)
        except Exception:
            store = {}
    store[username] = data
    with open(ATTENDANCE_FILE, "w") as f:
        json.dump(store, f, indent=4)

def load_timetable(username="admin"):
    """Load per-student weekly routine timetable with realistic semester defaults."""
    default_routine = {
        "Monday": [
            {"id": "tt_m1", "time": "09:00 AM - 10:00 AM", "subject": "Data Structures & Algorithms", "faculty": "Dr. Ramesh Verma", "room": "LH-302", "type": "Lecture"},
            {"id": "tt_m2", "time": "10:00 AM - 11:00 AM", "subject": "Operating Systems", "faculty": "Prof. Sneha Kulkarni", "room": "LH-302", "type": "Lecture"},
            {"id": "tt_m3", "time": "11:15 AM - 12:15 PM", "subject": "Mathematics-III (Discrete)", "faculty": "Dr. M. S. Iyer", "room": "LH-301", "type": "Tutorial"},
            {"id": "tt_m4", "time": "01:00 PM - 02:00 PM", "subject": "🥪 Lunch & Refreshment", "faculty": "Campus", "room": "Cafeteria", "type": "Break"},
            {"id": "tt_m5", "time": "02:00 PM - 04:00 PM", "subject": "Data Structures Lab (Batch A)", "faculty": "Dr. Ramesh Verma", "room": "Computer Lab 4", "type": "Practical"}
        ],
        "Tuesday": [
            {"id": "tt_t1", "time": "09:00 AM - 10:00 AM", "subject": "Python Programming", "faculty": "Dr. Ananya Ray", "room": "LH-302", "type": "Lecture"},
            {"id": "tt_t2", "time": "10:00 AM - 11:00 AM", "subject": "Database Management Systems", "faculty": "Prof. Rajesh Kumar", "room": "LH-302", "type": "Lecture"},
            {"id": "tt_t3", "time": "11:15 AM - 12:15 PM", "subject": "Operating Systems", "faculty": "Prof. Sneha Kulkarni", "room": "LH-302", "type": "Lecture"},
            {"id": "tt_t4", "time": "01:00 PM - 02:00 PM", "subject": "🥪 Lunch & Refreshment", "faculty": "Campus", "room": "Cafeteria", "type": "Break"},
            {"id": "tt_t5", "time": "02:00 PM - 04:00 PM", "subject": "Python & NumPy Lab (Batch A)", "faculty": "Dr. Ananya Ray", "room": "AI/ML Lab 2", "type": "Practical"}
        ],
        "Wednesday": [
            {"id": "tt_w1", "time": "09:00 AM - 10:00 AM", "subject": "Mathematics-III (Discrete)", "faculty": "Dr. M. S. Iyer", "room": "LH-301", "type": "Lecture"},
            {"id": "tt_w2", "time": "10:00 AM - 11:00 AM", "subject": "Data Structures & Algorithms", "faculty": "Dr. Ramesh Verma", "room": "LH-302", "type": "Lecture"},
            {"id": "tt_w3", "time": "11:15 AM - 12:15 PM", "subject": "Database Management Systems", "faculty": "Prof. Rajesh Kumar", "room": "LH-302", "type": "Lecture"},
            {"id": "tt_w4", "time": "01:00 PM - 02:00 PM", "subject": "🥪 Lunch & Refreshment", "faculty": "Campus", "room": "Cafeteria", "type": "Break"},
            {"id": "tt_w5", "time": "02:00 PM - 04:00 PM", "subject": "DBMS SQL & Schema Lab", "faculty": "Prof. Rajesh Kumar", "room": "Database Lab 1", "type": "Practical"}
        ],
        "Thursday": [
            {"id": "tt_th1", "time": "09:00 AM - 10:00 AM", "subject": "Operating Systems", "faculty": "Prof. Sneha Kulkarni", "room": "LH-302", "type": "Lecture"},
            {"id": "tt_th2", "time": "10:00 AM - 11:00 AM", "subject": "Python Programming", "faculty": "Dr. Ananya Ray", "room": "LH-302", "type": "Lecture"},
            {"id": "tt_th3", "time": "11:15 AM - 12:15 PM", "subject": "Data Structures & Algorithms", "faculty": "Dr. Ramesh Verma", "room": "LH-302", "type": "Lecture"},
            {"id": "tt_th4", "time": "01:00 PM - 02:00 PM", "subject": "🥪 Lunch & Refreshment", "faculty": "Campus", "room": "Cafeteria", "type": "Break"},
            {"id": "tt_th5", "time": "02:00 PM - 03:30 PM", "subject": "Technical Communication & Soft Skills", "faculty": "Prof. Meena Sen", "room": "Seminar Hall B", "type": "Seminar"}
        ],
        "Friday": [
            {"id": "tt_f1", "time": "09:00 AM - 10:00 AM", "subject": "Database Management Systems", "faculty": "Prof. Rajesh Kumar", "room": "LH-302", "type": "Lecture"},
            {"id": "tt_f2", "time": "10:00 AM - 11:00 AM", "subject": "Mathematics-III (Discrete)", "faculty": "Dr. M. S. Iyer", "room": "LH-301", "type": "Lecture"},
            {"id": "tt_f3", "time": "11:15 AM - 12:15 PM", "subject": "Python Programming", "faculty": "Dr. Ananya Ray", "room": "LH-302", "type": "Lecture"},
            {"id": "tt_f4", "time": "01:00 PM - 02:00 PM", "subject": "🥪 Lunch & Refreshment", "faculty": "Campus", "room": "Cafeteria", "type": "Break"},
            {"id": "tt_f5", "time": "02:00 PM - 04:00 PM", "subject": "OS Linux & Shell Scripting Lab", "faculty": "Prof. Sneha Kulkarni", "room": "Open Source Lab", "type": "Practical"}
        ],
        "Saturday": [
            {"id": "tt_s1", "time": "09:30 AM - 11:00 AM", "subject": "Competitive Coding & Project Mentorship", "faculty": "Tech Society & Seniors", "room": "Incubation Center", "type": "Workshop"},
            {"id": "tt_s2", "time": "11:15 AM - 01:00 PM", "subject": "Open Hackathon & Doubt Solving Session", "faculty": "Faculty Mentors", "room": "Central Library Hall", "type": "Remedial"}
        ]
    }

    if not os.path.exists(TIMETABLE_FILE):
        store = {username: default_routine}
        with open(TIMETABLE_FILE, "w") as f:
            json.dump(store, f, indent=4)
        return default_routine

    try:
        with open(TIMETABLE_FILE, "r") as f:
            store = json.load(f)
        if username not in store or not store[username]:
            store[username] = default_routine
            with open(TIMETABLE_FILE, "w") as f:
                json.dump(store, f, indent=4)
        return store[username]
    except Exception:
        return default_routine

def save_timetable(username, data):
    """Save student timetable data back to JSON store."""
    store = {}
    if os.path.exists(TIMETABLE_FILE):
        try:
            with open(TIMETABLE_FILE, "r") as f:
                store = json.load(f)
        except Exception:
            store = {}
    store[username] = data
    with open(TIMETABLE_FILE, "w") as f:
        json.dump(store, f, indent=4)

def load_exam_schedule():
    """Load college exam schedule and important milestone dates."""
    default_exams = [
        {
            "id": "exam_1",
            "title": "Data Structures & Algorithms - Mid-Semester Exam",
            "date": "2026-09-04",
            "time": "10:00 AM - 01:00 PM",
            "hall": "Examination Hall A (Seats 1-60)",
            "syllabus": "Units 1 to 3 (Arrays, Linked Lists, Stacks, Queues, Trees & BST)",
            "type": "Mid-Sem Theory"
        },
        {
            "id": "exam_2",
            "title": "Operating Systems - Mid-Semester Exam",
            "date": "2026-09-08",
            "time": "10:00 AM - 01:00 PM",
            "hall": "Examination Hall B (Seats 61-120)",
            "syllabus": "Processes, CPU Scheduling, Deadlocks & Memory Management",
            "type": "Mid-Sem Theory"
        },
        {
            "id": "exam_3",
            "title": "Database Management Systems (DBMS) - Theory Exam",
            "date": "2026-09-12",
            "time": "02:00 PM - 05:00 PM",
            "hall": "LH-302",
            "syllabus": "ER Modeling, Relational Algebra, SQL Queries & Normalization",
            "type": "Mid-Sem Theory"
        },
        {
            "id": "exam_4",
            "title": "Python & Data Structures Lab Evaluation",
            "date": "2026-09-16",
            "time": "09:00 AM - 12:00 PM",
            "hall": "Computer Lab 4",
            "syllabus": "Hands-on coding, viva voce, and record submission",
            "type": "Lab Practical"
        }
    ]

    if not os.path.exists(EXAM_SCHEDULE_FILE):
        with open(EXAM_SCHEDULE_FILE, "w") as f:
            json.dump(default_exams, f, indent=4)
        return default_exams

    try:
        with open(EXAM_SCHEDULE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return default_exams

def load_materials_meta():
    """Load material metadata, auto-indexing any existing untracked PDFs in materials/."""
    meta = {}
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, "r") as f:
                meta = json.load(f)
        except Exception:
            meta = {}

    disk_files = [f for f in os.listdir(MATERIAL_FOLDER) if f.lower().endswith(".pdf")]
    changed = False

    for filename in disk_files:
        if filename not in meta:
            file_path = os.path.join(MATERIAL_FOLDER, filename)
            file_size_kb = round(os.path.getsize(file_path) / 1024, 1)
            
            inferred_subject = "Other"
            fl = filename.lower()
            if "cpp" in fl or "c++" in fl:
                inferred_subject = "C++ Programming"
            elif fl.startswith("c_") or "c_prog" in fl:
                inferred_subject = "C Programming"
            elif "py" in fl or "python" in fl:
                inferred_subject = "Python"
            elif "ds" in fl or "algo" in fl or "data" in fl:
                inferred_subject = "Data Structures"
            elif "os" in fl or "operating" in fl:
                inferred_subject = "Operating Systems"
            elif "math" in fl:
                inferred_subject = "Mathematics"

            meta[filename] = {
                "title": filename.replace(".pdf", "").replace("_", " ").title(),
                "subject": inferred_subject,
                "semester": "1st Semester",
                "type": "Quick Revision Cheatsheet" if "cheat" in fl or "revision" in fl else "Lecture Notes",
                "uploader": "Faculty / Contributor",
                "upload_date": datetime.now().strftime("%Y-%m-%d"),
                "size_kb": file_size_kb,
                "description": "Complete lecture reference notes and key revision concepts.",
                "likes": 0,
                "downloads": 0
            }
            changed = True

    to_delete = [f for f in meta if f not in disk_files]
    if to_delete:
        for f in to_delete:
            del meta[f]
        changed = True

    if changed:
        save_materials_meta(meta)

    return meta

def save_materials_meta(meta):
    """Save materials metadata dictionary to JSON."""
    with open(METADATA_FILE, "w") as f:
        json.dump(meta, f, indent=4)

def load_material_requests():
    """Load student material requests with backward-compatible defaults."""
    if not os.path.exists(REQUESTS_FILE):
        default_requests = [
            {
                "id": "req_101",
                "title": "Data Structures - AVL Trees & Graph Traversal Notes",
                "subject": "Data Structures",
                "semester": "3rd Semester",
                "type": "Lecture Notes",
                "urgency": "🚨 Urgent",
                "description": "Looking for clear handwritten notes or step-by-step PDF explaining AVL tree rotations and Dijkstra's algorithm.",
                "requester": "Rahul Sharma",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "upvotes": 8,
                "status": "Open",
                "fulfilled_by": None,
                "fulfilled_date": None,
                "fulfillment_note": None
            },
            {
                "id": "req_102",
                "title": "Operating Systems 2025 End-Sem PYQ Solved Paper",
                "subject": "Operating Systems",
                "semester": "4th Semester",
                "type": "Previous Year Question Paper (PYQ)",
                "urgency": "⚠️ Important",
                "description": "Need university question paper from last semester covering Process Synchronization & Deadlock detection numericals.",
                "requester": "Priya Verma",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "upvotes": 14,
                "status": "Open",
                "fulfilled_by": None,
                "fulfilled_date": None,
                "fulfillment_note": None
            },
            {
                "id": "req_103",
                "title": "Python & NumPy Lab Record / Assignment Solutions",
                "subject": "Python",
                "semester": "1st Semester",
                "type": "Lab Manual",
                "urgency": "📌 General",
                "description": "Solved lab manual for Python programming with sample outputs for matrix manipulations.",
                "requester": "Amit Patel",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "upvotes": 5,
                "status": "Fulfilled",
                "fulfilled_by": "Prof. Rao / Teaching Assistant",
                "fulfilled_date": datetime.now().strftime("%Y-%m-%d"),
                "fulfillment_note": "Uploaded into the Study Materials hub under Python subject."
            }
        ]
        with open(REQUESTS_FILE, "w") as f:
            json.dump(default_requests, f, indent=4)
        return default_requests

    try:
        with open(REQUESTS_FILE, "r") as f:
            data = json.load(f)
            for item in data:
                item.setdefault("id", f"req_{int(datetime.now().timestamp())}")
                item.setdefault("urgency", "📌 General")
                item.setdefault("upvotes", 0)
                item.setdefault("status", "Open")
                item.setdefault("date", datetime.now().strftime("%Y-%m-%d"))
            return data
    except Exception:
        return []

def save_material_requests(data):
    """Save student material requests back to JSON."""
    with open(REQUESTS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_pdf_base64(file_path):
    """Read PDF file and return base64 string for embedded preview."""
    try:
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        return base64_pdf
    except Exception:
        return None


# ==================================================
# 🧭 SIDEBAR - NAVIGATION & STUDENT IDENTITY
# ==================================================

materials_meta = load_materials_meta()
announcements_data = load_announcements()
material_requests_data = load_material_requests()

with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
        <h2 style="margin: 0; font-size: 24px; font-weight: 800; color: #4F46E5;">🎓 CampusHub</h2>
        <span style="font-size: 11px; color: #059669; font-weight: 700; background: #D1FAE5; border: 1px solid #A7F3D0; padding: 3px 8px; border-radius: 9999px;"><span class="live-pulse"></span>Live</span>
    </div>
    <p style="font-size: 13px; color: #64748B; margin-top: 0; margin-bottom: 14px; font-weight: 500;">Academic Resource Network &amp; Toolkit</p>
    """, unsafe_allow_html=True)

    nav_option = st.radio(
        "Navigation Menu",
        [
            "🏠 Home Dashboard",
            "📅 Timetable & Schedule",
            "📊 Attendance Tracker",
            "📚 Study Materials",
            "⚡ Quick Revision & Cheatsheets",
            "🙋 Request Materials",
            "🧰 Student Tools",
            "🔗 Useful Resources",
            "📢 Announcements"
        ],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='margin: 16px 0; border: 0; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

    # Student Profile Card (auto-populated from login session)
    student_name = st.session_state.get("student_name", "Student Scholar")
    branch = st.session_state.get("user_branch", "Computer Science & Engg")
    semester = st.session_state.get("user_semester", "3rd Semester")
    user_role = st.session_state.get("user_role", "Student")
    username_display = st.session_state.get("username", "user")

    role_bg = "#FEF3C7" if user_role == "Admin" else "#D1FAE5"
    role_color = "#D97706" if user_role == "Admin" else "#059669"
    role_border = "#FDE68A" if user_role == "Admin" else "#A7F3D0"

    # Visual Profile Badge (Light Theme)
    st.markdown(f"""
    <div class="profile-card">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="font-size: 26px; background: #EEF2FF; border: 1px solid #C7D2FE; border-radius: 12px; padding: 6px 10px;">👨‍🎓</div>
            <div style="flex:1;">
                <div style="font-weight: 700; color: #0F172A; font-size: 15px;">{student_name}</div>
                <div style="font-size: 13px; color: #64748B; font-weight: 500;">{semester} • {branch.split('(')[0].strip()}</div>
                <div style="margin-top:5px;">
                    <span style="font-size:11px; font-weight:700; color:{role_color}; background:{role_bg}; border: 1px solid {role_border}; padding:2px 8px; border-radius:6px;">@{username_display} · {user_role}</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Logout button
    if st.button("🚪 Sign Out of Session", use_container_width=True, key="sidebar_logout_btn"):
        for key in ["authenticated", "username", "student_name", "user_branch", "user_semester", "user_role"]:
            st.session_state.pop(key, None)
        st.rerun()

    st.caption("✨ **Campus Tip:** Upload lecture notes or fulfill peer requests to earn contributor badges and academic karma points.")


# ==================================================
# 1. 🏠 HOME DASHBOARD
# ==================================================

if "Home Dashboard" in nav_option:
    # Contextual Time & Date Greeting
    current_hour = datetime.now().hour
    time_greeting = "Good morning 🌅" if current_hour < 12 else "Good afternoon ☀️" if current_hour < 17 else "Good evening 🌙"
    today_str = datetime.now().strftime("%A, %d %B %Y")
    today_day_name = datetime.now().strftime("%A")
    
    # ── 1. HERO BANNER ─────────────────────────────────
    st.markdown(f"""
    <div class="hero-container">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">
            <div>
                <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.2); backdrop-filter: blur(8px); padding: 5px 16px; border-radius: 9999px; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; border: 1px solid rgba(255,255,255,0.25);">
                    <span class="live-pulse"></span> Academic Portal · {today_str}
                </div>
                <h1 style="margin: 14px 0 8px 0; font-size: 34px; font-weight: 900; letter-spacing: -0.02em;">{time_greeting}, {student_name}! 🚀</h1>
                <p style="margin: 0; font-size: 16px; max-width: 780px; line-height: 1.6; color: #EEF2FF; opacity: 0.95;">
                    Welcome to your centralized academic workspace for <strong>{semester}</strong> ({branch}). Access verified lecture notes, timetable routine, attendance tracking, 1-page formula cheatsheets, and peer requests.
                </p>
                <div style="margin-top: 16px; display: flex; gap: 10px; flex-wrap: wrap;">
                    <span style="background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); border-radius: 8px; padding: 4px 12px; font-size: 13px; font-weight: 600;">🏛️ {branch.split('(')[0].strip()}</span>
                    <span style="background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); border-radius: 8px; padding: 4px 12px; font-size: 13px; font-weight: 600;">📅 {semester}</span>
                    <span style="background: rgba(16,185,129,0.3); border: 1px solid rgba(16,185,129,0.5); border-radius: 8px; padding: 4px 12px; font-size: 13px; font-weight: 700;">✨ Verified Active Scholar</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 2. HORIZONTAL SQUARE PORTAL LAUNCHPAD (8 MODULES) ─────────
    st.markdown("#### 🧭 Academic Portals & Modules")
    
    # Row 1 (4 Square Cards)
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    with p_col1:
        st.markdown("""
        <div class="square-portal-tile">
            <div class="square-logo-box" style="background: #EEF2FF; color: #4F46E5; border: 1px solid #C7D2FE;">📚</div>
            <div class="square-portal-title">Study Materials</div>
            <div class="square-portal-sub">Notes, Books &amp; PYQs</div>
        </div>
        """, unsafe_allow_html=True)
    with p_col2:
        st.markdown("""
        <div class="square-portal-tile">
            <div class="square-logo-box" style="background: #E0E7FF; color: #4338CA; border: 1px solid #C7D2FE;">📅</div>
            <div class="square-portal-title">Class Timetable</div>
            <div class="square-portal-sub">Live Routine &amp; Labs</div>
        </div>
        """, unsafe_allow_html=True)
    with p_col3:
        st.markdown("""
        <div class="square-portal-tile">
            <div class="square-logo-box" style="background: #D1FAE5; color: #059669; border: 1px solid #A7F3D0;">📊</div>
            <div class="square-portal-title">Attendance Tracker</div>
            <div class="square-portal-sub">75% Safe Bunk Guard</div>
        </div>
        """, unsafe_allow_html=True)
    with p_col4:
        st.markdown("""
        <div class="square-portal-tile">
            <div class="square-logo-box" style="background: #FEF3C7; color: #D97706; border: 1px solid #FDE68A;">⚡</div>
            <div class="square-portal-title">Revision Vault</div>
            <div class="square-portal-sub">1-Page Formula Sheets</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Row 2 (4 Square Cards)
    p_col5, p_col6, p_col7, p_col8 = st.columns(4)
    with p_col5:
        st.markdown("""
        <div class="square-portal-tile">
            <div class="square-logo-box" style="background: #E0F2FE; color: #0284C7; border: 1px solid #BAE6FD;">🙋</div>
            <div class="square-portal-title">Peer Wishlist</div>
            <div class="square-portal-sub">Community Requests</div>
        </div>
        """, unsafe_allow_html=True)
    with p_col6:
        st.markdown("""
        <div class="square-portal-tile">
            <div class="square-logo-box" style="background: #FCE7F3; color: #DB2777; border: 1px solid #FBCFE8;">🧰</div>
            <div class="square-portal-title">Student Tools</div>
            <div class="square-portal-sub">SGPA, Guard &amp; Timer</div>
        </div>
        """, unsafe_allow_html=True)
    with p_col7:
        st.markdown("""
        <div class="square-portal-tile">
            <div class="square-logo-box" style="background: #EDE9FE; color: #7C3AED; border: 1px solid #DDD6FE;">🔗</div>
            <div class="square-portal-title">Useful Resources</div>
            <div class="square-portal-sub">Roadmaps &amp; LeetCode</div>
        </div>
        """, unsafe_allow_html=True)
    with p_col8:
        st.markdown("""
        <div class="square-portal-tile">
            <div class="square-logo-box" style="background: #FEF2F2; color: #DC2626; border: 1px solid #FECACA;">📢</div>
            <div class="square-portal-title">Notice Board</div>
            <div class="square-portal-sub">Campus Notices &amp; News</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)

    # ── 3. HORIZONTAL CORE SUBJECTS SQUARE GRID (6 SUBJECTS) ───────
    st.markdown("#### 📖 Semester Core Subjects & Reference Decks")
    sub_col1, sub_col2, sub_col3 = st.columns(3)
    
    with sub_col1:
        st.markdown("""
        <div class="square-subject-tile" style="border-top: 4px solid #3B82F6;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <div class="square-logo-box" style="width: 44px; height: 44px; font-size: 22px; background: #EFF6FF; color: #2563EB; margin: 0;">🐍</div>
                <div>
                    <div style="font-weight: 800; font-size: 16px; color: #0F172A;">Python Programming</div>
                    <span style="font-size: 12px; color: #64748B;">Dr. Ananya Ray</span>
                </div>
            </div>
            <p style="font-size: 13px; color: #475569; margin: 6px 0; line-height: 1.4;">OOP concepts, Decorators, Generators, File I/O &amp; NumPy arrays.</p>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
                <span class="tag-chip">4 Notes Available</span>
                <span style="font-size: 12px; color: #059669; font-weight: 700;">Verified ✅</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with sub_col2:
        st.markdown("""
        <div class="square-subject-tile" style="border-top: 4px solid #4F46E5;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <div class="square-logo-box" style="width: 44px; height: 44px; font-size: 22px; background: #EEF2FF; color: #4F46E5; margin: 0;">🌳</div>
                <div>
                    <div style="font-weight: 800; font-size: 16px; color: #0F172A;">Data Structures &amp; Algorithms</div>
                    <span style="font-size: 12px; color: #64748B;">Dr. Ramesh Verma</span>
                </div>
            </div>
            <p style="font-size: 13px; color: #475569; margin: 6px 0; line-height: 1.4;">Trees, BST, AVL Rotations, Sorting Algorithms &amp; Graph Traversals.</p>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
                <span class="tag-chip">6 Notes Available</span>
                <span style="font-size: 12px; color: #059669; font-weight: 700;">Verified ✅</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with sub_col3:
        st.markdown("""
        <div class="square-subject-tile" style="border-top: 4px solid #0284C7;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <div class="square-logo-box" style="width: 44px; height: 44px; font-size: 22px; background: #E0F2FE; color: #0284C7; margin: 0;">💻</div>
                <div>
                    <div style="font-weight: 800; font-size: 16px; color: #0F172A;">Operating Systems</div>
                    <span style="font-size: 12px; color: #64748B;">Prof. Sneha Kulkarni</span>
                </div>
            </div>
            <p style="font-size: 13px; color: #475569; margin: 6px 0; line-height: 1.4;">Process sync, Semaphore, Deadlocks, Paging &amp; Virtual Memory.</p>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
                <span class="tag-chip">5 Notes Available</span>
                <span style="font-size: 12px; color: #059669; font-weight: 700;">Verified ✅</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    sub_col4, sub_col5, sub_col6 = st.columns(3)
    with sub_col4:
        st.markdown("""
        <div class="square-subject-tile" style="border-top: 4px solid #059669;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <div class="square-logo-box" style="width: 44px; height: 44px; font-size: 22px; background: #D1FAE5; color: #059669; margin: 0;">🗄️</div>
                <div>
                    <div style="font-weight: 800; font-size: 16px; color: #0F172A;">Database Systems (DBMS)</div>
                    <span style="font-size: 12px; color: #64748B;">Prof. Rajesh Kumar</span>
                </div>
            </div>
            <p style="font-size: 13px; color: #475569; margin: 6px 0; line-height: 1.4;">ER diagrams, Relational Algebra, SQL queries &amp; Normalization (1NF-BCNF).</p>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
                <span class="tag-chip">4 Notes Available</span>
                <span style="font-size: 12px; color: #059669; font-weight: 700;">Verified ✅</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with sub_col5:
        st.markdown("""
        <div class="square-subject-tile" style="border-top: 4px solid #D97706;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <div class="square-logo-box" style="width: 44px; height: 44px; font-size: 22px; background: #FEF3C7; color: #D97706; margin: 0;">📐</div>
                <div>
                    <div style="font-weight: 800; font-size: 16px; color: #0F172A;">Mathematics-III (Discrete)</div>
                    <span style="font-size: 12px; color: #64748B;">Dr. M. S. Iyer</span>
                </div>
            </div>
            <p style="font-size: 13px; color: #475569; margin: 6px 0; line-height: 1.4;">Propositional logic, Set theory, Graph theory, Trees &amp; Combinatorics.</p>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
                <span class="tag-chip">3 Notes Available</span>
                <span style="font-size: 12px; color: #059669; font-weight: 700;">Verified ✅</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with sub_col6:
        st.markdown("""
        <div class="square-subject-tile" style="border-top: 4px solid #7C3AED;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <div class="square-logo-box" style="width: 44px; height: 44px; font-size: 22px; background: #EDE9FE; color: #7C3AED; margin: 0;">🔷</div>
                <div>
                    <div style="font-weight: 800; font-size: 16px; color: #0F172A;">C / C++ Core Systems</div>
                    <span style="font-size: 12px; color: #64748B;">Prof. Ankit S.</span>
                </div>
            </div>
            <p style="font-size: 13px; color: #475569; margin: 6px 0; line-height: 1.4;">Pointers, Memory allocation, STL containers &amp; template metaprogramming.</p>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
                <span class="tag-chip">5 Notes Available</span>
                <span style="font-size: 12px; color: #059669; font-weight: 700;">Verified ✅</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)

    # ── 4. HORIZONTAL KEY KPI STATS BAR (4 EQUAL TILES) ────────────
    total_materials = len(materials_meta)
    open_requests_count = len([r for r in material_requests_data if r.get("status") == "Open"])
    total_announcements = len(announcements_data)
    total_likes = sum(item.get("likes", 0) for item in materials_meta.values()) + sum(r.get("upvotes", 0) for r in material_requests_data)

    st.markdown("#### 📊 Academic Performance & Community Health")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon" style="background: #EEF2FF; color: #4F46E5; border: 1px solid #C7D2FE;">📚</div>
            <div>
                <div class="metric-val">{total_materials}</div>
                <div class="metric-label">Study Materials Vault</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon" style="background: #FEF3C7; color: #D97706; border: 1px solid #FDE68A;">⚡</div>
            <div>
                <div class="metric-val">5 Decks</div>
                <div class="metric-label">Exam Cheatsheets</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon" style="background: #E0F2FE; color: #0284C7; border: 1px solid #BAE6FD;">🙋</div>
            <div>
                <div class="metric-val">{open_requests_count}</div>
                <div class="metric-label">Open Peer Wishlist</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with kpi4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon" style="background: #FFE4E6; color: #E11D48; border: 1px solid #FECDD3;">❤️</div>
            <div>
                <div class="metric-val">{total_likes}</div>
                <div class="metric-label">Peer Karma Upvotes</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)

    # ── 5. BALANCED HORIZONTAL SPLIT (TODAY'S SCHEDULE & LATEST NOTES) ─
    dash_col_left, dash_col_right = st.columns([1, 1])

    with dash_col_left:
        st.subheader(f"📍 Today's Live Schedule ({today_day_name})")
        timetable_data_home = load_timetable(curr_user if 'curr_user' in locals() else st.session_state.get("username", "admin"))
        today_home_slots = timetable_data_home.get(today_day_name, [])

        if not today_home_slots or today_day_name == "Sunday":
            st.info(f"🎉 No lectures scheduled for {today_day_name}. Enjoy your study break!")
        else:
            for s_idx, slot in enumerate(today_home_slots[:4]):
                stype = slot.get("type", "Lecture")
                type_bg = "#EDE9FE" if stype == "Practical" else "#FEF3C7" if stype == "Break" else "#EEF2FF"
                type_color = "#6D28D9" if stype == "Practical" else "#D97706" if stype == "Break" else "#4338CA"
                
                st.markdown(f"""
                <div class="glass-card" style="padding: 14px 18px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-family:'JetBrains Mono', monospace; font-size: 12px; font-weight: 700; color: #4F46E5; background: #EEF2FF; padding: 2px 6px; border-radius: 4px;">
                                ⏰ {slot.get('time')}
                            </span>
                            <strong style="margin-left: 8px; font-size: 15px; color: #0F172A;">{slot.get('subject')}</strong>
                        </div>
                        <span style="background: {type_bg}; color: {type_color}; padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: 700;">{stype}</span>
                    </div>
                    <div style="font-size: 12px; color: #64748B; margin-top: 4px;">
                        🏛️ Venue: <strong>{slot.get('room', 'LH-302')}</strong> &nbsp;|&nbsp; 👨‍🏫 <strong>{slot.get('faculty')}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with dash_col_right:
        st.subheader("🔥 Top Material Requests")
        open_requests = [r for r in material_requests_data if r.get("status") == "Open"]
        sorted_requests = sorted(open_requests, key=lambda x: x.get("upvotes", 0), reverse=True)[:3]
        
        if not sorted_requests:
            st.info("No open material requests currently pending. Everything is fulfilled!")
        else:
            for req in sorted_requests:
                with st.container():
                    st.markdown(f"""
                    <div class="glass-card" style="padding: 14px 18px; margin-bottom: 10px; border-left: 4px solid #4F46E5;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong style="color: #0F172A; font-size: 15px;">📌 {req.get('title')}</strong>
                            <span class="tag-chip" style="margin: 0; font-weight:700;">👍 {req.get('upvotes', 0)}</span>
                        </div>
                        <div style="font-size: 12px; color: #64748B; margin-top: 4px;">
                            📚 {req.get('subject')} • 🎓 {req.get('semester')} • By <strong>{req.get('requester')}</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"👍 I Need This Too (+{req.get('upvotes', 0)})", key=f"home_req_up_{req.get('id')}", use_container_width=True):
                        req["upvotes"] = req.get("upvotes", 0) + 1
                        save_material_requests(material_requests_data)
                        st.toast("Upvote registered! This helps prioritize material uploads.", icon="👍")
                        st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("💡 Contributor Leaderboard")
        st.markdown("""
        <div class="glass-card" style="padding: 18px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-size:15px;">
                <span>🥇 <strong style="color:#0F172A;">Rohan S.</strong> (CS 5th Sem)</span>
                <span class="tag-chip">14 Uploads • 82 ❤️</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-size:15px;">
                <span>🥈 <strong style="color:#0F172A;">Ananya M.</strong> (IT 3rd Sem)</span>
                <span class="tag-chip">9 Uploads • 54 ❤️</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:15px;">
                <span>🥉 <strong style="color:#0F172A;">Vikram P.</strong> (ECE 7th Sem)</span>
                <span class="tag-chip">6 Uploads • 39 ❤️</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==================================================
# 2. 📅 CLASS TIMETABLE & SCHEDULE MANAGER
# ==================================================

elif "Timetable & Schedule" in nav_option:
    curr_user = st.session_state.get("username", "admin")
    student_display_name = st.session_state.get("student_name", "Student Scholar")
    branch_name = st.session_state.get("user_branch", "Computer Science & Engg")
    sem_name = st.session_state.get("user_semester", "3rd Semester")
    
    timetable_data = load_timetable(curr_user)
    exam_schedule_data = load_exam_schedule()
    attendance_data = load_attendance(curr_user)

    today_day = datetime.now().strftime("%A")
    today_date_str = datetime.now().strftime("%d %B %Y")

    st.header("📅 Class Timetable & Academic Routine")
    st.write(f"Official weekly timetable, today's live lecture sequence, classroom directions, and upcoming exam schedule for **{student_display_name}** ({sem_name}).")

    # ── Today's Live Schedule Alert Card ─────────────
    today_slots = timetable_data.get(today_day, [])
    
    st.markdown(f"""
    <div class="glass-card" style="background: linear-gradient(135deg, #EEF2FF 0%, #FFFFFF 100%); border-left: 6px solid #4F46E5; padding: 22px 26px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
            <div>
                <span style="background: #E0E7FF; color: #4338CA; border: 1px solid #C7D2FE; padding: 4px 14px; border-radius: 9999px; font-size: 13px; font-weight: 800; text-transform: uppercase;">
                    <span class="live-pulse"></span> Today is {today_day} · {today_date_str}
                </span>
                <h3 style="margin: 10px 0 4px 0; font-size: 26px; font-weight: 900; color: #0F172A;">
                    {len(today_slots)} Scheduled Sessions Today
                </h3>
                <p style="margin: 0; font-size: 14px; color: #475569; font-weight: 500;">
                    {branch_name} • {sem_name} • Room LH-302 &amp; Computing Labs
                </p>
            </div>
            <div style="text-align: right;">
                <span class="tag-chip" style="font-size: 14px; padding: 6px 14px;">🏛️ Academic Year 2026</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs Navigation ──────────────────────────────
    tt_tab_today, tt_tab_week, tt_tab_manage, tt_tab_exams = st.tabs([
        f"📍 Today's Schedule ({today_day})",
        "🗓️ Weekly Full Timetable Matrix",
        "➕ Add & Customize Class Slots",
        "🎯 Mid-Sem & Exam Dates Countdown"
    ])

    # ── TAB 1: TODAY'S LIVE ROUTINE ──────────────────
    with tt_tab_today:
        if today_day in ["Sunday"]:
            st.info("🎉 **Today is Sunday!** No university lectures scheduled. Use today for rest, revisions, or project coding!")
        elif not today_slots:
            st.info(f"No classes logged for {today_day}. You can add slots in the '➕ Add & Customize Class Slots' tab.")
        else:
            st.markdown(f"##### ⏰ Lecture Sequence for {today_day}:")
            for idx, slot in enumerate(today_slots):
                st_id = slot.get("id", f"slot_{idx}")
                sub = slot.get("subject", "Subject")
                timing = slot.get("time", "Time Slot")
                faculty = slot.get("faculty", "Faculty")
                room = slot.get("room", "Room")
                stype = slot.get("type", "Lecture")

                type_bg = "#EDE9FE" if stype == "Practical" else "#FEF3C7" if stype == "Break" else "#E0F2FE" if stype == "Tutorial" else "#EEF2FF"
                type_color = "#6D28D9" if stype == "Practical" else "#D97706" if stype == "Break" else "#0369A1" if stype == "Tutorial" else "#4338CA"
                border_accent = "#7C3AED" if stype == "Practical" else "#D97706" if stype == "Break" else "#4F46E5"

                with st.container():
                    st.markdown(f"""
                    <div class="glass-card" style="border-left: 5px solid {border_accent}; padding: 18px 22px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                            <div>
                                <span style="font-family:'JetBrains Mono', monospace; font-size: 13px; font-weight: 700; color: #4F46E5; background: #EEF2FF; padding: 3px 10px; border-radius: 6px;">
                                    ⏱️ {timing}
                                </span>
                                <h4 style="margin: 8px 0 4px 0; font-size: 19px; font-weight: 800; color: #0F172A;">
                                    {sub}
                                </h4>
                                <div style="font-size: 13px; color: #64748B; font-weight: 500;">
                                    👨‍🏫 Faculty: <strong>{faculty}</strong> &nbsp;|&nbsp; 🏛️ Venue: <strong>{room}</strong>
                                </div>
                            </div>
                            <div>
                                <span style="background: {type_bg}; color: {type_color}; padding: 4px 12px; border-radius: 9999px; font-weight: 700; font-size: 12px; text-transform: uppercase;">
                                    {stype}
                                </span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if stype != "Break":
                        col_mark1, col_mark2 = st.columns([1, 1])
                        with col_mark1:
                            if st.button(f"✅ Mark Present ({sub})", key=f"tt_pres_{st_id}_{idx}", use_container_width=True):
                                # Update attendance for matching subject if present
                                found_match = False
                                for a_sub in attendance_data:
                                    if a_sub.get("subject", "").lower() in sub.lower() or sub.lower() in a_sub.get("subject", "").lower():
                                        a_sub["attended"] = a_sub.get("attended", 0) + 1
                                        a_sub["total"] = a_sub.get("total", 0) + 1
                                        found_match = True
                                        break
                                if found_match:
                                    save_attendance(curr_user, attendance_data)
                                    st.toast(f"Marked Present for {sub}! Attendance updated.", icon="🎉")
                                else:
                                    st.toast(f"Marked Present for {sub}!", icon="✅")
                        with col_mark2:
                            if st.button(f"❌ Mark Absent ({sub})", key=f"tt_abs_{st_id}_{idx}", use_container_width=True):
                                found_match = False
                                for a_sub in attendance_data:
                                    if a_sub.get("subject", "").lower() in sub.lower() or sub.lower() in a_sub.get("subject", "").lower():
                                        a_sub["total"] = a_sub.get("total", 0) + 1
                                        found_match = True
                                        break
                                if found_match:
                                    save_attendance(curr_user, attendance_data)
                                    st.toast(f"Logged Absence for {sub}! Attendance total updated.", icon="⚠️")
                                else:
                                    st.toast(f"Logged Absence for {sub}!", icon="❌")

                    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

    # ── TAB 2: WEEKLY FULL MATRIX ────────────────────
    with tt_tab_week:
        st.subheader("🗓️ Weekly Master Schedule Matrix")
        
        selected_day = st.radio(
            "Select Day",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            horizontal=True,
            index=0 if today_day not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"] else ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].index(today_day)
        )

        day_routine = timetable_data.get(selected_day, [])

        if not day_routine:
            st.info(f"No sessions configured for {selected_day}.")
        else:
            st.markdown(f"**Routine for {selected_day} ({len(day_routine)} classes):**")
            
            for idx, slot in enumerate(day_routine):
                stype = slot.get("type", "Lecture")
                type_bg = "#EDE9FE" if stype == "Practical" else "#FEF3C7" if stype == "Break" else "#E0F2FE" if stype == "Tutorial" else "#EEF2FF"
                type_color = "#6D28D9" if stype == "Practical" else "#D97706" if stype == "Break" else "#0369A1" if stype == "Tutorial" else "#4338CA"

                st.markdown(f"""
                <div class="glass-card" style="padding: 16px 20px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <div>
                            <span style="font-family:'JetBrains Mono', monospace; font-size: 13px; font-weight: 700; color: #4338CA; background: #EEF2FF; padding: 2px 8px; border-radius: 6px;">
                                ⏰ {slot.get('time')}
                            </span>
                            <strong style="margin-left: 12px; font-size: 16px; color: #0F172A;">{slot.get('subject')}</strong>
                        </div>
                        <div style="display: flex; gap: 8px; align-items: center;">
                            <span class="tag-chip">🏛️ {slot.get('room', 'LH-302')}</span>
                            <span style="background: {type_bg}; color: {type_color}; padding: 2px 10px; border-radius: 6px; font-weight: 700; font-size: 12px;">{stype}</span>
                        </div>
                    </div>
                    <div style="font-size: 13px; color: #64748B; margin-top: 6px;">
                        👨‍🏫 Faculty: <strong>{slot.get('faculty', 'Faculty Member')}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 3: ADD / EDIT CLASS SLOTS ─────────────────
    with tt_tab_manage:
        st.subheader("➕ Add or Modify Schedule Period")
        st.write("Customize your weekly lecture slots, lab timings, classroom venues, and faculty details.")

        with st.form("add_timetable_slot_form", clear_on_submit=True):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                slot_day = st.selectbox("Day of Week *", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
                slot_sub = st.text_input("Subject / Class Name *", placeholder="e.g. Data Structures & Algorithms")
                slot_faculty = st.text_input("Faculty In-Charge", placeholder="e.g. Dr. Ramesh Verma")

            with f_col2:
                slot_time = st.text_input("Time Interval *", placeholder="e.g. 09:00 AM - 10:00 AM")
                slot_room = st.text_input("Lecture Hall / Lab Venue *", placeholder="e.g. LH-302 or Computer Lab 4")
                slot_type = st.selectbox("Session Type", ["Lecture", "Practical", "Tutorial", "Seminar", "Workshop", "Break"])

            submit_slot = st.form_submit_button("✨ Save & Append Class Slot", use_container_width=True, type="primary")

            if submit_slot:
                if not slot_sub.strip() or not slot_time.strip():
                    st.error("Please enter both the Subject Name and Time Interval.")
                else:
                    new_slot_obj = {
                        "id": f"tt_{int(datetime.now().timestamp())}",
                        "time": slot_time.strip(),
                        "subject": slot_sub.strip(),
                        "faculty": slot_faculty.strip() if slot_faculty.strip() else "Faculty In-Charge",
                        "room": slot_room.strip() if slot_room.strip() else "LH-302",
                        "type": slot_type
                    }
                    if slot_day not in timetable_data:
                        timetable_data[slot_day] = []
                    timetable_data[slot_day].append(new_slot_obj)
                    save_timetable(curr_user, timetable_data)
                    st.balloons()
                    st.success(f"✅ Added new slot for **{slot_day}** ({slot_sub.strip()}) successfully!")
                    st.rerun()

        st.markdown("<hr style='margin: 20px 0; border: 0; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
        st.markdown("##### 🗑️ Remove an Existing Class Slot:")
        rem_day = st.selectbox("Select Day to Manage", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], key="rem_day_select")
        slots_to_delete = timetable_data.get(rem_day, [])
        if slots_to_delete:
            slot_options = [f"{s.get('time')} - {s.get('subject')} ({s.get('room')})" for s in slots_to_delete]
            chosen_rem = st.selectbox("Select Slot to Delete", slot_options)
            if st.button("🗑️ Delete Selected Slot", key="del_slot_btn", type="secondary"):
                rem_idx = slot_options.index(chosen_rem)
                deleted_item = timetable_data[rem_day].pop(rem_idx)
                save_timetable(curr_user, timetable_data)
                st.success(f"Removed '{deleted_item.get('subject')}' from {rem_day}!")
                st.rerun()
        else:
            st.caption(f"No slots configured for {rem_day}.")

    # ── TAB 4: EXAM DATES & COUNTDOWN ─────────────────
    with tt_tab_exams:
        st.subheader("🎯 Mid-Sem Exam Dates & Milestone Schedule")
        st.write("Track examination dates, room seat allocations, syllabus boundaries, and live days remaining countdowns.")

        for exam in exam_schedule_data:
            exam_title = exam.get("title")
            exam_date_str = exam.get("date")
            exam_time = exam.get("time")
            exam_hall = exam.get("hall")
            exam_syl = exam.get("syllabus")
            exam_type = exam.get("type", "Mid-Sem Theory")

            # Calculate days remaining
            try:
                target_dt = datetime.strptime(exam_date_str, "%Y-%m-%d")
                curr_dt = datetime.now()
                delta_days = (target_dt.date() - curr_dt.date()).days
                
                if delta_days > 0:
                    countdown_badge = f"⏳ In {delta_days} Days"
                    countdown_bg = "#FEF3C7"
                    countdown_color = "#D97706"
                elif delta_days == 0:
                    countdown_badge = "🚨 TODAY!"
                    countdown_bg = "#FEE2E2"
                    countdown_color = "#DC2626"
                else:
                    countdown_badge = "✅ Concluded"
                    countdown_bg = "#D1FAE5"
                    countdown_color = "#059669"
            except Exception:
                countdown_badge = exam_date_str
                countdown_bg = "#EEF2FF"
                countdown_color = "#4F46E5"

            st.markdown(f"""
            <div class="glass-card" style="border-left: 5px solid #4F46E5; padding: 20px 24px; margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 6px;">
                            <span style="background: {countdown_bg}; color: {countdown_color}; padding: 3px 12px; border-radius: 9999px; font-weight: 800; font-size: 13px;">
                                {countdown_badge}
                            </span>
                            <span class="tag-chip">📅 {exam_date_str}</span>
                            <span class="tag-chip">⏱️ {exam_time}</span>
                        </div>
                        <h4 style="margin: 4px 0 6px 0; font-size: 19px; font-weight: 800; color: #0F172A;">
                            📝 {exam_title}
                        </h4>
                        <div style="font-size: 13px; color: #475569; margin-top: 6px; line-height: 1.5;">
                            🏛️ <strong>Venue:</strong> {exam_hall} &nbsp;|&nbsp; 📑 <strong>Category:</strong> {exam_type}
                        </div>
                        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 8px 12px; margin-top: 10px; font-size: 13px; color: #334155;">
                            📚 <strong>Syllabus Scope:</strong> {exam_syl}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ==================================================
# 3. 📊 STUDENT ATTENDANCE TRACKER & 75% GUARD
# ==================================================

elif "Attendance Tracker" in nav_option:
    curr_user = st.session_state.get("username", "admin")
    student_display_name = st.session_state.get("student_name", "Student Scholar")
    attendance_data = load_attendance(curr_user)

    st.header("📊 Student Attendance Tracker & 75% Criteria Guard")
    st.write(f"Real-time subject-wise attendance logs, 1-click class counter, safe bunk limits, and exam eligibility forecaster for **{student_display_name}**.")

    # ── Overall Aggregate Statistics ─────────────────
    total_classes_held = sum(item.get("total", 0) for item in attendance_data)
    total_classes_attended = sum(item.get("attended", 0) for item in attendance_data)
    
    overall_percentage = round((total_classes_attended / total_classes_held * 100), 1) if total_classes_held > 0 else 0.0
    
    # Calculate overall safe bunks or overall deficit
    overall_target = 75.0
    target_ratio = overall_target / 100.0
    
    if overall_percentage >= overall_target:
        overall_safe_bunks = int((total_classes_attended / target_ratio) - total_classes_held) if target_ratio > 0 else 0
        overall_deficit = 0
        status_label = "Eligible for Exams ✅"
        status_color = "#059669"
        status_bg = "#D1FAE5"
        status_border = "#A7F3D0"
    else:
        overall_safe_bunks = 0
        overall_deficit = int(((target_ratio * total_classes_held) - total_classes_attended) / (1.0 - target_ratio)) + 1 if target_ratio < 1.0 else 0
        status_label = "At Risk of Debarment ⚠️"
        status_color = "#DC2626"
        status_bg = "#FEE2E2"
        status_border = "#FECACA"

    subjects_at_risk = len([s for s in attendance_data if (s.get("attended", 0) / s.get("total", 1) * 100) < s.get("target", 75)])

    # Hero Aggregate Banner
    st.markdown(f"""
    <div class="glass-card" style="background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%); border-left: 6px solid {status_color}; padding: 24px 28px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
            <div>
                <span style="background: {status_bg}; color: {status_color}; border: 1px solid {status_border}; padding: 4px 14px; border-radius: 9999px; font-size: 13px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em;">
                    {status_label}
                </span>
                <h2 style="margin: 10px 0 4px 0; font-size: 32px; font-weight: 900; color: #0F172A;">
                    Overall Attendance: <span style="color: {status_color};">{overall_percentage}%</span>
                </h2>
                <p style="margin: 0; font-size: 15px; color: #64748B; font-weight: 500;">
                    Attended <strong>{total_classes_attended}</strong> out of <strong>{total_classes_held}</strong> total conducted lectures across {len(attendance_data)} academic subjects.
                </p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 13px; color: #64748B; font-weight: 700; text-transform: uppercase;">Criteria Requirement</div>
                <div style="font-size: 26px; font-weight: 800; color: #4338CA;">≥ 75.0% Min</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4-KPI Row
    att_kpi1, att_kpi2, att_kpi3, att_kpi4 = st.columns(4)
    with att_kpi1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon" style="background: #EEF2FF; color: #4F46E5; border: 1px solid #C7D2FE;">📈</div>
            <div>
                <div class="metric-val">{overall_percentage}%</div>
                <div class="metric-label">Aggregate Score</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with att_kpi2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon" style="background: #D1FAE5; color: #059669; border: 1px solid #A7F3D0;">✅</div>
            <div>
                <div class="metric-val">{total_classes_attended}/{total_classes_held}</div>
                <div class="metric-label">Classes Attended</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with att_kpi3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon" style="background: #FEF3C7; color: #D97706; border: 1px solid #FDE68A;">🛡️</div>
            <div>
                <div class="metric-val">{overall_safe_bunks} Classes</div>
                <div class="metric-label">Safe Bunk Allowance</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with att_kpi4:
        risk_bg = "#FEE2E2" if subjects_at_risk > 0 else "#D1FAE5"
        risk_color = "#DC2626" if subjects_at_risk > 0 else "#059669"
        risk_border = "#FECACA" if subjects_at_risk > 0 else "#A7F3D0"
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon" style="background: {risk_bg}; color: {risk_color}; border: 1px solid {risk_border};">🚨</div>
            <div>
                <div class="metric-val" style="color: {risk_color};">{subjects_at_risk} Subject(s)</div>
                <div class="metric-label">Below 75% Threshold</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # ── Tabs Interface ───────────────────────────────
    tab_subjects, tab_daily_log, tab_manage, tab_simulator = st.tabs([
        "📋 Subject-Wise Attendance Log & 1-Click Marker",
        "⚡ Daily Quick Bulk Marker",
        "➕ Add & Customize Subjects",
        "🔮 Future Bunk & Leave Forecaster"
    ])

    # ── TAB 1: SUBJECT-WISE CARDS ────────────────────
    with tab_subjects:
        if not attendance_data:
            st.info("No subjects tracked yet. Use the '➕ Add & Customize Subjects' tab to add your courses.")
        else:
            st.markdown(f"**Tracking {len(attendance_data)} subjects for {student_display_name}:**")
            
            for idx, item in enumerate(attendance_data):
                sub_id = item.get("id", f"sub_{idx}")
                sub_name = item.get("subject", "General Subject")
                faculty = item.get("faculty", "Faculty In-Charge")
                att = item.get("attended", 0)
                tot = item.get("total", 0)
                target = item.get("target", 75)
                
                pct = round((att / tot * 100), 1) if tot > 0 else 0.0
                t_ratio = target / 100.0

                is_safe = pct >= target
                card_border = "#059669" if is_safe else "#DC2626"
                card_badge_bg = "#D1FAE5" if is_safe else "#FEE2E2"
                card_badge_color = "#059669" if is_safe else "#DC2626"
                card_badge_text = f"✅ Safe ({pct}%)" if is_safe else f"⚠️ At Risk ({pct}%)"

                if is_safe:
                    safe_miss = int((att / t_ratio) - tot) if t_ratio > 0 else 0
                    advice_text = f"You can safely miss up to <strong>{safe_miss}</strong> upcoming lecture(s) without dropping below {target}%."
                    advice_bg = "#ECFDF5"
                    advice_color = "#065F46"
                else:
                    must_attend = int(((t_ratio * tot) - att) / (1.0 - t_ratio)) + 1 if t_ratio < 1.0 else 1
                    advice_text = f"You must attend the next <strong>{must_attend}</strong> consecutive lecture(s) without missing any to restore {target}% eligibility."
                    advice_bg = "#FEF2F2"
                    advice_color = "#991B1B"

                with st.container():
                    st.markdown(f"""
                    <div class="glass-card" style="border-left: 5px solid {card_border}; padding: 20px 24px; margin-bottom: 14px;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                            <div>
                                <h3 style="margin: 0 0 4px 0; font-size: 20px; font-weight: 800; color: #0F172A;">📖 {sub_name}</h3>
                                <div style="font-size: 13px; color: #64748B; font-weight: 500;">👨‍🏫 Faculty: <strong>{faculty}</strong> • Target Threshold: <strong>{target}%</strong></div>
                            </div>
                            <div style="text-align: right;">
                                <span style="background: {card_badge_bg}; color: {card_badge_color}; padding: 4px 12px; border-radius: 9999px; font-weight: 800; font-size: 13px;">
                                    {card_badge_text}
                                </span>
                                <div style="font-size: 14px; font-weight: 700; color: #0F172A; margin-top: 4px;">{att} / {tot} Lectures</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Visual Progress Bar
                    st.progress(min(pct / 100.0, 1.0), text=f"Attendance: {pct}% | Target: {target}%")

                    st.markdown(f"""
                    <div style="background: {advice_bg}; color: {advice_color}; padding: 10px 14px; border-radius: 10px; font-size: 14px; margin: 8px 0 12px 0;">
                        💡 {advice_text}
                    </div>
                    """, unsafe_allow_html=True)

                    # Quick 1-Click Action Buttons
                    btn_col1, btn_col2, btn_col3 = st.columns([1.2, 1.2, 2])
                    
                    with btn_col1:
                        if st.button(f"✅ +1 Attended (Present)", key=f"att_inc_{sub_id}_{idx}", use_container_width=True):
                            item["attended"] = item.get("attended", 0) + 1
                            item["total"] = item.get("total", 0) + 1
                            save_attendance(curr_user, attendance_data)
                            st.toast(f"Marked Present for {sub_name}! Current: {round(item['attended']/item['total']*100, 1)}%", icon="🎉")
                            st.rerun()

                    with btn_col2:
                        if st.button(f"❌ +1 Missed (Absent)", key=f"att_miss_{sub_id}_{idx}", use_container_width=True):
                            item["total"] = item.get("total", 0) + 1
                            save_attendance(curr_user, attendance_data)
                            st.toast(f"Logged Missed class for {sub_name}! Current: {round(item['attended']/item['total']*100, 1)}%", icon="⚠️")
                            st.rerun()

                    with btn_col3:
                        with st.expander("⚙️ Edit Counts / Remove"):
                            edit_col1, edit_col2 = st.columns(2)
                            with edit_col1:
                                edit_att = st.number_input(f"Attended ({sub_name})", min_value=0, value=item.get("attended", 0), key=f"edit_att_{sub_id}")
                            with edit_col2:
                                edit_tot = st.number_input(f"Total Held ({sub_name})", min_value=1, value=max(item.get("total", 1), 1), key=f"edit_tot_{sub_id}")
                            
                            e_btn1, e_btn2 = st.columns([1, 1])
                            with e_btn1:
                                if st.button(f"💾 Save Changes", key=f"save_edit_{sub_id}", use_container_width=True):
                                    item["attended"] = min(edit_att, edit_tot)
                                    item["total"] = edit_tot
                                    save_attendance(curr_user, attendance_data)
                                    st.success("Updated successfully!")
                                    st.rerun()
                            with e_btn2:
                                if st.button(f"🗑️ Delete Subject", key=f"del_{sub_id}", use_container_width=True):
                                    attendance_data = [s for s in attendance_data if s.get("id") != sub_id]
                                    save_attendance(curr_user, attendance_data)
                                    st.success(f"Removed {sub_name}")
                                    st.rerun()

                    st.markdown("<hr style='margin: 16px 0; border: 0; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

    # ── TAB 2: DAILY QUICK BULK MARKER ───────────────
    with tab_daily_log:
        st.subheader("⚡ Daily Class Attendance Multi-Marker")
        st.write("Mark your presence across multiple lectures held today in one batch submission.")

        if not attendance_data:
            st.info("No subjects found. Please add subjects first.")
        else:
            with st.form("daily_bulk_attendance_form"):
                st.markdown("##### 📝 Select Status for Today's Timetable:")
                status_selections = {}
                
                for idx, item in enumerate(attendance_data):
                    sub_id = item.get("id", f"sub_{idx}")
                    sub_name = item.get("subject")
                    
                    c_name, c_status = st.columns([2, 2])
                    with c_name:
                        st.markdown(f"**📖 {sub_name}**")
                        st.caption(f"Current: {item.get('attended', 0)} / {item.get('total', 0)} ({round(item.get('attended', 0)/max(item.get('total', 1), 1)*100, 1)}%)")
                    with c_status:
                        choice = st.radio(
                            f"Status for {sub_name}",
                            ["🚫 No Lecture Today", "✅ Present (Attended)", "❌ Absent (Missed)"],
                            horizontal=True,
                            key=f"bulk_radio_{sub_id}",
                            label_visibility="collapsed"
                        )
                        status_selections[sub_id] = choice
                    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

                bulk_submit = st.form_submit_button("🚀 Submit Today's Attendance Log", use_container_width=True, type="primary")

                if bulk_submit:
                    updated_count = 0
                    for item in attendance_data:
                        sub_id = item.get("id")
                        chosen = status_selections.get(sub_id)
                        if chosen == "✅ Present (Attended)":
                            item["attended"] = item.get("attended", 0) + 1
                            item["total"] = item.get("total", 0) + 1
                            updated_count += 1
                        elif chosen == "❌ Absent (Missed)":
                            item["total"] = item.get("total", 0) + 1
                            updated_count += 1

                    if updated_count > 0:
                        save_attendance(curr_user, attendance_data)
                        st.balloons()
                        st.success(f"🎉 Successfully logged attendance for {updated_count} course lecture(s) today!")
                        st.rerun()
                    else:
                        st.info("No class status updates selected.")

    # ── TAB 3: ADD NEW SUBJECT ───────────────────────
    with tab_manage:
        st.subheader("➕ Add New Subject or Course to Track")
        st.write("Configure your semester courses, lab practicals, and customized minimum attendance thresholds.")

        with st.form("add_subject_form", clear_on_submit=True):
            add_c1, add_c2 = st.columns(2)
            with add_c1:
                new_sub_name = st.text_input("Subject / Course Name *", placeholder="e.g. Computer Networks & Protocols")
                new_faculty = st.text_input("Faculty In-Charge", placeholder="e.g. Prof. Arvind Swaminathan")
            with add_c2:
                new_att = st.number_input("Classes Already Attended", min_value=0, value=20, step=1)
                new_tot = st.number_input("Total Classes Already Conducted", min_value=1, value=25, step=1)
                new_target = st.slider("Target Minimum % (University Criteria)", min_value=60, max_value=90, value=75, step=5)

            add_submit = st.form_submit_button("✨ Add Subject to Tracker", use_container_width=True, type="primary")

            if add_submit:
                if not new_sub_name.strip():
                    st.error("Please enter a valid subject title.")
                else:
                    new_item = {
                        "id": f"att_{int(datetime.now().timestamp())}",
                        "subject": new_sub_name.strip(),
                        "faculty": new_faculty.strip() if new_faculty.strip() else "Faculty In-Charge",
                        "attended": min(int(new_att), int(new_tot)),
                        "total": int(new_tot),
                        "target": int(new_target)
                    }
                    attendance_data.append(new_item)
                    save_attendance(curr_user, attendance_data)
                    st.balloons()
                    st.success(f"✅ Added **{new_sub_name.strip()}** to your attendance tracker!")
                    st.rerun()

    # ── TAB 4: BUNK & LEAVE FORECASTER ────────────────
    with tab_simulator:
        st.subheader("🔮 Predictive Bunk & Planned Leave Simulator")
        st.write("Simulate future missed lectures (e.g. hackathon travel, illness, campus fest) to see their direct mathematical impact on exam eligibility.")

        if not attendance_data:
            st.info("Please add courses to simulate attendance.")
        else:
            sim_sub_names = [s.get("subject") for s in attendance_data]
            selected_sim_sub = st.selectbox("Select Course to Simulate", sim_sub_names)

            target_sub = next((s for s in attendance_data if s.get("subject") == selected_sim_sub), None)

            if target_sub:
                cur_att = target_sub.get("attended", 0)
                cur_tot = target_sub.get("total", 0)
                cur_pct = round((cur_att / cur_tot * 100), 1) if cur_tot > 0 else 0.0

                sim_c1, sim_c2 = st.columns(2)
                with sim_c1:
                    planned_bunks = st.slider("Proposed Future Classes to Skip / Miss", min_value=1, max_value=15, value=2, step=1)
                with sim_c2:
                    planned_future_attend = st.slider("Additional Future Classes You Will Attend", min_value=0, max_value=20, value=5, step=1)

                projected_tot = cur_tot + planned_bunks + planned_future_attend
                projected_att = cur_att + planned_future_attend
                projected_pct = round((projected_att / projected_tot * 100), 1) if projected_tot > 0 else 0.0

                pct_diff = round(projected_pct - cur_pct, 1)
                diff_sign = f"+{pct_diff}%" if pct_diff >= 0 else f"{pct_diff}%"

                sim_res_c1, sim_res_c2 = st.columns(2)
                with sim_res_c1:
                    st.markdown(f"""
                    <div class="glass-card" style="text-align:center;">
                        <div style="font-size:13px; color:#64748B; font-weight:700; text-transform:uppercase;">Current Attendance</div>
                        <div style="font-size:36px; font-weight:800; color:#4338CA; margin:6px 0;">{cur_pct}%</div>
                        <span class="tag-chip">{cur_att} / {cur_tot} Classes</span>
                    </div>
                    """, unsafe_allow_html=True)
                with sim_res_c2:
                    proj_color = "#059669" if projected_pct >= target_sub.get("target", 75) else "#DC2626"
                    st.markdown(f"""
                    <div class="glass-card" style="text-align:center;">
                        <div style="font-size:13px; color:#64748B; font-weight:700; text-transform:uppercase;">Projected Final Attendance</div>
                        <div style="font-size:36px; font-weight:800; color:{proj_color}; margin:6px 0;">{projected_pct}%</div>
                        <span class="tag-chip" style="color:{proj_color};">Trend: {diff_sign}</span>
                    </div>
                    """, unsafe_allow_html=True)

                if projected_pct >= target_sub.get("target", 75):
                    st.success(f"🎉 **Safe Projection:** Your attendance in **{selected_sim_sub}** will remain at **{projected_pct}%**, satisfying the {target_sub.get('target', 75)}% exam threshold.")
                else:
                    st.error(f"🚨 **Warning Threshold Breach:** Missing {planned_bunks} lecture(s) will lower your attendance in **{selected_sim_sub}** to **{projected_pct}%**, which is below the mandatory {target_sub.get('target', 75)}% criteria!")


# ==================================================
# 3. 📚 STUDY MATERIALS HUB (WITH LATEST NOTES FILTER)
# ==================================================

elif "Study Materials" in nav_option:
    st.header("📚 Study Materials & Latest Notes Hub")
    st.write("Browse, search, download, preview, and contribute academic PDFs, lecture notes, and revision sheets.")

    tab_browse, tab_upload, tab_request_jump = st.tabs([
        "🔍 Browse & Search Materials",
        "📤 Contribute / Upload Material",
        "🙋 Quick Material Request"
    ])

    # --- TAB 1: BROWSE MATERIALS ---
    with tab_browse:
        f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1, 1, 1])

        with f_col1:
            search_query = st.text_input("🔎 Search by Title, Keyword, or Uploader", placeholder="e.g. Python, C++, Trees, Calculus, DBMS...")

        with f_col2:
            all_subjects = ["All Subjects"] + sorted(list(set(info.get("subject", "Other") for info in materials_meta.values()) | {"C Programming", "C++ Programming", "Python", "Data Structures", "Mathematics", "Computer Science", "Database Systems", "Operating Systems", "Computer Networks", "Web Development", "AI / Machine Learning", "Other"}))
            selected_subject = st.selectbox("Subject", all_subjects)

        with f_col3:
            all_semesters = ["All Semesters"] + [f"{i}st Semester" if i == 1 else f"{i}nd Semester" if i == 2 else f"{i}rd Semester" if i == 3 else f"{i}th Semester" for i in range(1, 9)]
            selected_semester = st.selectbox("Semester", all_semesters)

        with f_col4:
            all_types = ["All Types", "Lecture Notes", "Quick Revision Cheatsheet", "Previous Year Question Paper (PYQ)", "Lab Manual", "Syllabus", "Reference Book / Summary"]
            selected_type = st.selectbox("Type", all_types)

        # Filter Logic
        filtered_materials = {}
        for fname, info in materials_meta.items():
            q = search_query.lower().strip()
            match_search = (
                not q or 
                q in fname.lower() or 
                q in info.get("title", "").lower() or 
                q in info.get("description", "").lower() or
                q in info.get("uploader", "").lower() or
                q in info.get("subject", "").lower()
            )
            match_subject = (selected_subject == "All Subjects") or (info.get("subject") == selected_subject)
            match_semester = (selected_semester == "All Semesters") or (info.get("semester") == selected_semester)
            match_type = (selected_type == "All Types") or (info.get("type") == selected_type)

            if match_search and match_subject and match_semester and match_type:
                filtered_materials[fname] = info

        st.markdown(f"**Showing {len(filtered_materials)} verified study resource(s)**")

        if not filtered_materials:
            st.info("No matching study materials found. Can't find what you need? Post a request in the '🙋 Quick Material Request' tab!")
        else:
            # 2-Column Responsive Card Grid
            mat_cols = st.columns(2)
            for idx, (filename, info) in enumerate(filtered_materials.items()):
                file_path = os.path.join(MATERIAL_FOLDER, filename)
                col = mat_cols[idx % 2]

                with col:
                    with st.container():
                        st.markdown(f"""
                        <div class="glass-card">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                                <div>
                                    <h3 style="margin: 0 0 6px 0; font-size: 20px; font-weight: 800; color: #0F172A;">📄 {info.get('title', filename)}</h3>
                                    <span class="tag-new">🆕 Latest Notes</span>
                                    <span class="tag-chip">📚 {info.get('subject', 'General')}</span>
                                    <span class="tag-chip">🎓 {info.get('semester', 'All')}</span>
                                    <span class="tag-chip">📑 {info.get('type', 'Notes')}</span>
                                </div>
                            </div>
                            <p style="font-size: 14px; color: #334155; margin: 10px 0 14px 0; line-height: 1.5;">
                                {info.get('description', 'Comprehensive reference study materials.')}
                            </p>
                            <div style="font-size: 13px; color: #64748B; margin-bottom: 14px; display: flex; justify-content: space-between; flex-wrap: wrap; font-weight: 500;">
                                <span>👤 Contributor: <strong style="color:#0F172A;">{info.get('uploader', 'Peer')}</strong></span>
                                <span>💾 {info.get('size_kb', 0)} KB • ❤️ {info.get('likes', 0)} Upvotes</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        btn_c1, btn_c2 = st.columns([1, 1])
                        with btn_c1:
                            if os.path.exists(file_path):
                                with open(file_path, "rb") as f:
                                    if st.download_button(
                                        label="⬇️ Download PDF",
                                        data=f,
                                        file_name=filename,
                                        mime="application/pdf",
                                        key=f"grid_dl_{filename}",
                                        use_container_width=True
                                    ):
                                        materials_meta[filename]["downloads"] = materials_meta[filename].get("downloads", 0) + 1
                                        save_materials_meta(materials_meta)

                        with btn_c2:
                            if st.button(f"❤️ Upvote ({info.get('likes', 0)})", key=f"grid_like_{filename}", use_container_width=True):
                                materials_meta[filename]["likes"] = materials_meta[filename].get("likes", 0) + 1
                                save_materials_meta(materials_meta)
                                st.rerun()

                        # In-browser Preview
                        if os.path.exists(file_path):
                            with st.expander("👁️ View PDF In-Browser Preview"):
                                pdf_b64 = get_pdf_base64(file_path)
                                if pdf_b64:
                                    pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_b64}" width="100%" height="500" type="application/pdf" style="border: 1px solid rgba(255,255,255,0.1); border-radius: 10px;"></iframe>'
                                    st.markdown(pdf_display, unsafe_allow_html=True)
                                else:
                                    st.warning("Preview unavailable for this PDF format.")
                        
                        st.markdown("<br>", unsafe_allow_html=True)

    # --- TAB 2: UPLOAD MATERIAL ---
    with tab_upload:
        st.subheader("📤 Share Study Material with Peers")
        st.write("Help expand the campus knowledge bank by uploading verified notes, syllabus summaries, and question papers.")

        with st.form("upload_material_form", clear_on_submit=True):
            up_col1, up_col2 = st.columns(2)
            with up_col1:
                doc_title = st.text_input("Document Title *", placeholder="e.g. Unit 4 - Dynamic Programming & Graphs")
                doc_subject = st.selectbox(
                    "Academic Subject *",
                    [
                        "C Programming",
                        "C++ Programming",
                        "Python",
                        "Data Structures",
                        "Mathematics",
                        "Computer Science",
                        "Database Systems",
                        "Operating Systems",
                        "Computer Networks",
                        "Web Development",
                        "AI / Machine Learning",
                        "Software Engineering",
                        "Other"
                    ]
                )
                doc_semester = st.selectbox("Target Semester *", [f"{i}st Semester" if i == 1 else f"{i}nd Semester" if i == 2 else f"{i}rd Semester" if i == 3 else f"{i}th Semester" for i in range(1, 9)], index=2)

            with up_col2:
                doc_type = st.selectbox(
                    "Resource Category *",
                    [
                        "Lecture Notes",
                        "Quick Revision Cheatsheet",
                        "Previous Year Question Paper (PYQ)",
                        "Lab Manual",
                        "Syllabus",
                        "Reference Book / Summary"
                    ]
                )
                doc_uploader = st.text_input("Contributor Name", value=student_name if student_name else "Student Contributor")
                doc_description = st.text_area("Brief Summary / Key Topics Included", placeholder="e.g. Detailed handwritten notes with diagrams, code snippets, and practice problems.")

            uploaded_pdf = st.file_uploader("Select PDF File * (Max 25MB)", type=["pdf"])
            submitted = st.form_submit_button("🚀 Publish & Share Study Resource", use_container_width=True)

            if submitted:
                if not doc_title.strip():
                    st.error("Please enter a descriptive document title.")
                elif uploaded_pdf is None:
                    st.error("Please select a valid PDF file to upload.")
                else:
                    clean_filename = "".join(c for c in uploaded_pdf.name if c.isalnum() or c in ('.', '_', '-')).strip()
                    if not clean_filename.lower().endswith(".pdf"):
                        clean_filename += ".pdf"
                    
                    save_path = os.path.join(MATERIAL_FOLDER, clean_filename)
                    with open(save_path, "wb") as f:
                        f.write(uploaded_pdf.getbuffer())

                    file_size_kb = round(len(uploaded_pdf.getbuffer()) / 1024, 1)

                    materials_meta[clean_filename] = {
                        "title": doc_title.strip(),
                        "subject": doc_subject,
                        "semester": doc_semester,
                        "type": doc_type,
                        "uploader": doc_uploader.strip() if doc_uploader.strip() else "Anonymous Contributor",
                        "upload_date": datetime.now().strftime("%Y-%m-%d"),
                        "size_kb": file_size_kb,
                        "description": doc_description.strip() if doc_description.strip() else "Verified academic study material.",
                        "likes": 0,
                        "downloads": 0
                    }
                    save_materials_meta(materials_meta)

                    st.balloons()
                    st.success(f"🎉 **{clean_filename}** has been published successfully! Thank you for contributing to the student community.")

    # --- TAB 3: QUICK MATERIAL REQUEST ---
    with tab_request_jump:
        st.subheader("🙋 Can't find what you need? Request it here!")
        st.write("Post an academic resource request so classmates, seniors, or professors can upload it.")

        with st.form("quick_request_form", clear_on_submit=True):
            qr_col1, qr_col2 = st.columns(2)
            with qr_col1:
                qr_title = st.text_input("Requested Topic / Material Title *", placeholder="e.g. Unit 3 - Memory Management & Paging Notes")
                qr_subject = st.selectbox("Subject *", ["C Programming", "C++ Programming", "Python", "Data Structures", "Mathematics", "Computer Science", "Database Systems", "Operating Systems", "Computer Networks", "Web Development", "AI / Machine Learning", "Other"], key="qr_sub")
                qr_semester = st.selectbox("Semester *", [f"{i}st Semester" if i == 1 else f"{i}nd Semester" if i == 2 else f"{i}rd Semester" if i == 3 else f"{i}th Semester" for i in range(1, 9)], index=2, key="qr_sem")
            with qr_col2:
                qr_type = st.selectbox("Resource Type", ["Lecture Notes", "Quick Revision Cheatsheet", "Previous Year Question Paper (PYQ)", "Lab Manual", "Reference Book / Summary", "Assignment Solutions"], key="qr_type")
                qr_urgency = st.selectbox("Urgency Level", ["🚨 Urgent (Exam in <3 days)", "⚠️ Important (Upcoming test/lab)", "📌 General (Regular study)"], key="qr_urg")
                qr_desc = st.text_area("Specific Requirements or Chapter Numbers", placeholder="e.g. Need step-by-step solved numericals on FIFO, LRU, and Optimal page replacement.", key="qr_desc")

            qr_submit = st.form_submit_button("📢 Broadcast Material Request to Community", use_container_width=True)

            if qr_submit:
                if not qr_title.strip():
                    st.error("Please enter the title or topic of the requested material.")
                else:
                    new_req = {
                        "id": f"req_{int(datetime.now().timestamp())}",
                        "title": qr_title.strip(),
                        "subject": qr_subject,
                        "semester": qr_semester,
                        "type": qr_type,
                        "urgency": "🚨 Urgent" if "Urgent" in qr_urgency else "⚠️ Important" if "Important" in qr_urgency else "📌 General",
                        "description": qr_desc.strip() if qr_desc.strip() else "Requested by student for exam preparation.",
                        "requester": student_name if student_name else "Student Scholar",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "upvotes": 1,
                        "status": "Open",
                        "fulfilled_by": None,
                        "fulfilled_date": None,
                        "fulfillment_note": None
                    }
                    material_requests_data.insert(0, new_req)
                    save_material_requests(material_requests_data)

                    st.balloons()
                    st.success("✅ Your material request has been posted to the campus community wishlist!")
                    st.rerun()


# ==================================================
# 3. ⚡ QUICK REVISION & EXAM CHEATSHEETS (NEW)
# ==================================================

elif "Quick Revision" in nav_option:
    st.header("⚡ Quick Revision & Exam Cheatsheet Vault")
    st.write("Master key algorithms, syntax, Big-O tables, and core engineering concepts in 5 minutes before your exams.")

    rev_tab_python, rev_tab_cpp, rev_tab_dsa, rev_tab_os, rev_tab_dbms, rev_tab_flashcards = st.tabs([
        "🐍 Python Syntax & OOP",
        "🔷 C & C++ Core",
        "🌳 DSA & Sorting Matrix",
        "💻 OS & Deadlocks",
        "🗄️ DBMS & Normalization",
        "🧠 Interactive Flashcards"
    ])

    # --- TAB 1: PYTHON QUICK REVISION ---
    with rev_tab_python:
        st.subheader("🐍 Python Fast-Track Cheatsheet")
        
        py_c1, py_c2 = st.columns(2)
        with py_c1:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color:#4338CA; margin-top:0; font-size:18px;">📦 Python Core Collections</h4>
                <table>
                    <tr>
                        <th>Type</th><th>Syntax</th><th>Mutable?</th><th>Lookup Time</th>
                    </tr>
                    <tr>
                        <td><strong>List</strong></td><td><code>[1, 2, 3]</code></td><td>✅ Yes</td><td>O(1) index, O(n) search</td>
                    </tr>
                    <tr>
                        <td><strong>Tuple</strong></td><td><code>(1, 2, 3)</code></td><td>❌ No</td><td>O(1) index, O(n) search</td>
                    </tr>
                    <tr>
                        <td><strong>Dict</strong></td><td><code>{'k': 'v'}</code></td><td>✅ Yes</td><td>O(1) Avg (Hash Map)</td>
                    </tr>
                    <tr>
                        <td><strong>Set</strong></td><td><code>{1, 2, 3}</code></td><td>✅ Yes</td><td>O(1) Avg (Unique elements)</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="glass-card">
                <h4 style="color:#059669; margin-top:0; font-size:18px;">⚡ List & Dict Comprehension</h4>
                <p style="font-size:14px; color:#334155; margin-bottom:8px;">Fast syntax shortcuts:</p>
            </div>
            """, unsafe_allow_html=True)
            st.code("""# Squares of even numbers
evens_sq = [x**2 for x in range(10) if x % 2 == 0]

# Dict from list of pairs
word_lengths = {word: len(word) for word in ['apple', 'banana', 'cherry']}

# Matrix transpose
transpose = [[row[i] for row in matrix] for i in range(len(matrix[0]))]""", language="python")

        with py_c2:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color:#7C3AED; margin-top:0; font-size:18px;">🎯 OOP & Magic / Dunder Methods</h4>
                <p style="font-size:14px; color:#334155;">Quick reference for object customisation:</p>
            </div>
            """, unsafe_allow_html=True)
            st.code("""class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        
    def __str__(self):
        return f"Account({self.owner}, Balance: {self.balance})"
        
    def __len__(self):
        return int(self.balance)
        
    def __add__(self, other):
        return self.balance + other.balance

acc = Account("Alex", 1500)
print(acc)  # Calls __str__""", language="python")

            if os.path.exists("materials/Python_Complete_Programming_Handbook.pdf"):
                with open("materials/Python_Complete_Programming_Handbook.pdf", "rb") as f:
                    st.download_button("⬇️ Download Python Complete Handbook PDF", f, file_name="Python_Complete_Handbook.pdf", mime="application/pdf", use_container_width=True)

    # --- TAB 2: C & C++ QUICK REVISION ---
    with rev_tab_cpp:
        st.subheader("🔷 C & C++ Exam Summary")
        
        cpp_c1, cpp_c2 = st.columns(2)
        with cpp_c1:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color:#4338CA; margin-top:0; font-size:18px;">📌 Pointers & Memory Management</h4>
                <table>
                    <tr>
                        <th>Feature</th><th>C Language</th><th>C++ Language</th>
                    </tr>
                    <tr>
                        <td>Heap Alloc</td><td><code>malloc(size)</code> / <code>calloc</code></td><td><code>new Type[size]</code></td>
                    </tr>
                    <tr>
                        <td>Heap Free</td><td><code>free(ptr)</code></td><td><code>delete / delete[] ptr</code></td>
                    </tr>
                    <tr>
                        <td>I/O Speed</td><td><code>printf / scanf</code></td><td><code>cin / cout</code> (use fast I/O)</td>
                    </tr>
                    <tr>
                        <td>Pass Type</td><td>Pointers (<code>*ptr</code>)</td><td>References (<code>&ref</code>)</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            
            st.code("""// C++ Fast I/O for Competitive Programming
#include <iostream>
using namespace std;
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    // write your solution here
    return 0;
}""", language="cpp")

        with cpp_c2:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color:#059669; margin-top:0; font-size:18px;">⚡ C++ STL Container Complexity Matrix</h4>
                <table>
                    <tr>
                        <th>STL Container</th><th>Internal Structure</th><th>Access Time</th><th>Insert / Delete</th>
                    </tr>
                    <tr>
                        <td><code>vector</code></td><td>Dynamic Array</td><td>O(1)</td><td>O(1) Back, O(n) Middle</td>
                    </tr>
                    <tr>
                        <td><code>deque</code></td><td>Chunked Arrays</td><td>O(1)</td><td>O(1) Front & Back</td>
                    </tr>
                    <tr>
                        <td><code>set / map</code></td><td>Red-Black Tree</td><td>O(log n)</td><td>O(log n)</td>
                    </tr>
                    <tr>
                        <td><code>unordered_map</code></td><td>Hash Table</td><td>O(1) Avg</td><td>O(1) Avg</td>
                    </tr>
                    <tr>
                        <td><code>priority_queue</code></td><td>Binary Max/Min Heap</td><td>O(1) Top</td><td>O(log n) Push/Pop</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

            if os.path.exists("materials/CPP_OOPs_and_STL_Guide.pdf"):
                with open("materials/CPP_OOPs_and_STL_Guide.pdf", "rb") as f:
                    st.download_button("⬇️ Download C++ OOPs & STL Guide PDF", f, file_name="CPP_OOPs_and_STL_Guide.pdf", mime="application/pdf", use_container_width=True)

    # --- TAB 3: DSA & SORTING MATRIX ---
    with rev_tab_dsa:
        st.subheader("🌳 Data Structures & Algorithms Revision Matrix")
        
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#4338CA; margin-top:0; font-size:18px;">📊 Master Sorting Algorithms Comparison</h4>
            <table>
                <tr>
                    <th>Algorithm</th><th>Best Time</th><th>Average Time</th><th>Worst Time</th><th>Space</th><th>Stable?</th>
                </tr>
                <tr>
                    <td><strong>Quick Sort</strong></td><td>O(n log n)</td><td>O(n log n)</td><td>O(n²)</td><td>O(log n)</td><td>❌ No</td>
                </tr>
                <tr>
                    <td><strong>Merge Sort</strong></td><td>O(n log n)</td><td>O(n log n)</td><td>O(n log n)</td><td>O(n)</td><td>✅ Yes</td>
                </tr>
                <tr>
                    <td><strong>Heap Sort</strong></td><td>O(n log n)</td><td>O(n log n)</td><td>O(n log n)</td><td>O(1)</td><td>❌ No</td>
                </tr>
                <tr>
                    <td><strong>Insertion Sort</strong></td><td>O(n)</td><td>O(n²)</td><td>O(n²)</td><td>O(1)</td><td>✅ Yes</td>
                </tr>
                <tr>
                    <td><strong>Bubble Sort</strong></td><td>O(n)</td><td>O(n²)</td><td>O(n²)</td><td>O(1)</td><td>✅ Yes</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        dsa_col1, dsa_col2 = st.columns(2)
        with dsa_col1:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color:#059669; margin-top:0; font-size:18px;">🌲 Tree Traversals</h4>
                <p style="font-size:14px; color:#334155; line-height:1.6;">
                    • <strong>Inorder:</strong> Left -> Root -> Right (Yields sorted order in BST)<br>
                    • <strong>Preorder:</strong> Root -> Left -> Right (Used for serialization)<br>
                    • <strong>Postorder:</strong> Left -> Right -> Root (Used for deleting/bottom-up DP)<br>
                    • <strong>Level Order:</strong> Breadth-First Search using Queue
                </p>
            </div>
            """, unsafe_allow_html=True)

        with dsa_col2:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color:#E11D48; margin-top:0; font-size:18px;">🕸️ Graph Algorithms</h4>
                <p style="font-size:14px; color:#334155; line-height:1.6;">
                    • <strong>BFS:</strong> Queue, Shortest Path in unweighted graph — <code>O(V + E)</code><br>
                    • <strong>DFS:</strong> Stack/Recursion, Connected components & cycles — <code>O(V + E)</code><br>
                    • <strong>Dijkstra:</strong> Min-Heap, Single-source shortest path — <code>O((V+E) log V)</code><br>
                    • <strong>Kruskal / Prim:</strong> Minimum Spanning Tree (MST)
                </p>
            </div>
            """, unsafe_allow_html=True)

        if os.path.exists("materials/DSA_and_Core_CS_Quick_Revision_Cheatsheet.pdf"):
            with open("materials/DSA_and_Core_CS_Quick_Revision_Cheatsheet.pdf", "rb") as f:
                st.download_button("⬇️ Download DSA 1-Page Cheatsheet PDF", f, file_name="DSA_Quick_Revision_Cheatsheet.pdf", mime="application/pdf", use_container_width=True)

    # --- TAB 4: OS & DEADLOCKS ---
    with rev_tab_os:
        st.subheader("💻 Operating Systems Core Exam Cheatsheet")
        
        os_c1, os_c2 = st.columns(2)
        with os_c1:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color:#DC2626; margin-top:0; font-size:18px;">🚨 4 Coffman Deadlock Conditions</h4>
                <p style="font-size:14px; color:#334155; line-height:1.6;">
                    1. <strong>Mutual Exclusion:</strong> At least one resource must be held non-shareably.<br>
                    2. <strong>Hold and Wait:</strong> Process holds ≥1 resource and waits for others.<br>
                    3. <strong>No Preemption:</strong> Resources cannot be forcibly taken from a process.<br>
                    4. <strong>Circular Wait:</strong> P0 waits for P1, P1 waits for P2... Pn waits for P0.
                </p>
                <div style="background:#FEE2E2; border-left:4px solid #DC2626; padding:10px 14px; border-radius:8px; font-size:13px; color:#991B1B; font-weight:500;">
                    💡 <em>Deadlock Prevention breaks at least ONE of these four conditions.</em>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with os_c2:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color:#059669; margin-top:0; font-size:18px;">📊 CPU Scheduling & Memory Formulae</h4>
                <p style="font-size:14px; color:#334155; line-height:1.6;">
                    • <strong>Turnaround Time (TAT)</strong> = Completion Time (CT) - Arrival Time (AT)<br>
                    • <strong>Waiting Time (WT)</strong> = Turnaround Time (TAT) - Burst Time (BT)<br>
                    • <strong>Banker's Algorithm:</strong> <code>Need[i][j] = Max[i][j] - Allocation[i][j]</code><br>
                    • <strong>Belady's Anomaly:</strong> Increasing page frames causes MORE page faults in FIFO.
                </p>
            </div>
            """, unsafe_allow_html=True)

        if os.path.exists("materials/OS_and_DBMS_Exam_CheatSheet.pdf"):
            with open("materials/OS_and_DBMS_Exam_CheatSheet.pdf", "rb") as f:
                st.download_button("⬇️ Download OS & DBMS Exam Revision Sheet PDF", f, file_name="OS_and_DBMS_Exam_CheatSheet.pdf", mime="application/pdf", use_container_width=True)

    # --- TAB 5: DBMS & NORMALIZATION ---
    with rev_tab_dbms:
        st.subheader("🗄️ Database Management Systems (DBMS) Cheatsheet")
        
        db_c1, db_c2 = st.columns(2)
        with db_c1:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color:#4338CA; margin-top:0; font-size:18px;">💎 ACID Properties of Transactions</h4>
                <p style="font-size:14px; color:#334155; line-height:1.6;">
                    • <strong>A - Atomicity:</strong> "All or Nothing" — transaction completes wholly or rolls back.<br>
                    • <strong>C - Consistency:</strong> State transitions preserve integrity constraints.<br>
                    • <strong>I - Isolation:</strong> Concurrent transactions execute as if isolated.<br>
                    • <strong>D - Durability:</strong> Once committed, changes persist even across crashes.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with db_c2:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color:#D97706; margin-top:0; font-size:18px;">📐 Normalization Quick Checklist</h4>
                <p style="font-size:14px; color:#334155; line-height:1.6;">
                    • <strong>1NF:</strong> Atomic column values, no repeating groups.<br>
                    • <strong>2NF:</strong> 1NF + No partial dependency (all non-key attributes fully depend on primary key).<br>
                    • <strong>3NF:</strong> 2NF + No transitive dependency (X -> Y, Y -> Z where Z is non-prime).<br>
                    • <strong>BCNF:</strong> For every Functional Dependency <code>X -> Y</code>, <code>X</code> must be a Super Key.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # --- TAB 6: INTERACTIVE FLASHCARDS ---
    with rev_tab_flashcards:
        st.subheader("🧠 Rapid Concept Recall Flashcards")
        st.write("Click any flashcard to expand and test your exam recall.")

        flashcards = [
            {
                "topic": "Python",
                "q": "What is the difference between shallow copy and deep copy in Python?",
                "a": "A shallow copy creates a new object but inserts references into it to the objects found in the original. A deep copy creates a new object and recursively copies all objects found within the original."
            },
            {
                "topic": "C++",
                "q": "Why is a destructor made virtual in a base class in C++?",
                "a": "To ensure that when deleting a derived class object through a base class pointer, the derived class's destructor is executed first, preventing memory leaks."
            },
            {
                "topic": "Data Structures",
                "q": "Why is HeapSort preferred over QuickSort when worst-case time is critical?",
                "a": "HeapSort guarantees O(n log n) in the worst case and operates in-place O(1) extra space, whereas standard QuickSort can degrade to O(n²) on poor pivot choices."
            },
            {
                "topic": "Operating Systems",
                "q": "What is the Convoy Effect in CPU scheduling?",
                "a": "The Convoy Effect occurs in FCFS when smaller I/O-bound processes wait for a long CPU-bound process to finish, resulting in poor CPU and device utilization."
            },
            {
                "topic": "DBMS",
                "q": "What is the difference between WHERE and HAVING in SQL?",
                "a": "WHERE filters rows before grouping occurs (cannot use aggregate functions), while HAVING filters aggregated groups after GROUP BY."
            }
        ]

        for idx, fc in enumerate(flashcards):
            with st.expander(f"🃏 Flashcard {idx+1} [{fc['topic']}]: {fc['q']}"):
                st.markdown(f"""
                <div style="background: #EEF2FF; border-left: 4px solid #4F46E5; padding: 14px; border-radius: 10px; font-size: 14px; color: #1E293B;">
                    💡 <strong>Answer &amp; Concept:</strong><br>{fc['a']}
                </div>
                """, unsafe_allow_html=True)


# ==================================================
# 4. 🙋 REQUEST A MATERIAL PORTAL
# ==================================================

elif "Request Materials" in nav_option:
    st.header("🙋 Student Material Requests & Wishlist Portal")
    st.write("Can't find specific handwritten notes, past papers, or lab manuals? Post your request, upvote needed materials, or fulfill peer requests to earn contributor badges.")

    total_reqs = len(material_requests_data)
    open_reqs = len([r for r in material_requests_data if r.get("status") == "Open"])
    fulfilled_reqs = len([r for r in material_requests_data if r.get("status") == "Fulfilled"])
    total_req_upvotes = sum(r.get("upvotes", 0) for r in material_requests_data)

    req_kpi1, req_kpi2, req_kpi3, req_kpi4 = st.columns(4)
    with req_kpi1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon">📋</div>
            <div>
                <div class="metric-val">{total_reqs}</div>
                <div class="metric-label">Total Requests</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with req_kpi2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon">🟢</div>
            <div>
                <div class="metric-val">{open_reqs}</div>
                <div class="metric-label">Open / In-Demand</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with req_kpi3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon">✅</div>
            <div>
                <div class="metric-val">{fulfilled_reqs}</div>
                <div class="metric-label">Fulfilled by Peers</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with req_kpi4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon">🌟</div>
            <div>
                <div class="metric-val">{total_req_upvotes}</div>
                <div class="metric-label">Peer Upvotes</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    req_tab_browse, req_tab_post, req_tab_hall = st.tabs([
        "📋 Community Wishlist (Browse & Fulfill)",
        "➕ Post New Material Request",
        "🏆 Contributor Impact & Hall of Fame"
    ])

    # --- TAB 1: BROWSE & FULFILL REQUESTS ---
    with req_tab_browse:
        rf_col1, rf_col2, rf_col3, rf_col4 = st.columns([2, 1, 1, 1])
        with rf_col1:
            req_search = st.text_input("Search Requests", placeholder="Search by topic, keyword, requester, or subject...", key="req_search_bar")
        with rf_col2:
            status_filter = st.selectbox("Status Filter", ["All Statuses", "🟢 Open (Needed)", "🟣 Fulfilled (Resolved)"])
        with rf_col3:
            urg_filter = st.selectbox("Urgency Filter", ["All Urgencies", "🚨 Urgent", "⚠️ Important", "📌 General"])
        with rf_col4:
            sort_req = st.selectbox("Sort By", ["🔥 Most Upvoted (Highest Demand)", "🕒 Most Recent", "🚨 Urgency"])

        # Filter logic
        filtered_requests = []
        for req in material_requests_data:
            q = req_search.lower().strip()
            match_q = (
                not q or
                q in req.get("title", "").lower() or
                q in req.get("description", "").lower() or
                q in req.get("subject", "").lower() or
                q in req.get("requester", "").lower()
            )
            req_st = req.get("status", "Open")
            match_st = (
                status_filter == "All Statuses" or
                (status_filter == "🟢 Open (Needed)" and req_st == "Open") or
                (status_filter == "🟣 Fulfilled (Resolved)" and req_st == "Fulfilled")
            )
            req_urg = req.get("urgency", "General")
            match_urg = (
                urg_filter == "All Urgencies" or
                (urg_filter == "🚨 Urgent" and "Urgent" in req_urg) or
                (urg_filter == "⚠️ Important" and "Important" in req_urg) or
                (urg_filter == "📌 General" and "General" in req_urg)
            )

            if match_q and match_st and match_urg:
                filtered_requests.append(req)

        # Sorting
        if sort_req == "🔥 Most Upvoted (Highest Demand)":
            filtered_requests.sort(key=lambda x: x.get("upvotes", 0), reverse=True)
        elif sort_req == "🚨 Urgency":
            urg_weight = {"🚨 Urgent": 3, "⚠️ Important": 2, "📌 General": 1}
            filtered_requests.sort(key=lambda x: urg_weight.get(x.get("urgency", "📌 General"), 0), reverse=True)
        else:
            filtered_requests.sort(key=lambda x: x.get("date", ""), reverse=True)

        st.markdown(f"**Showing {len(filtered_requests)} student material request(s)**")

        if not filtered_requests:
            st.info("No requests match your current filters. Be the first to post a new request!")
        else:
            for req in filtered_requests:
                req_id = req.get("id")
                is_fulfilled = req.get("status") == "Fulfilled"
                urg = req.get("urgency", "📌 General")
                urg_badge = "badge-urgent" if "Urgent" in urg else "badge-important" if "Important" in urg else "badge-general"
                status_badge = "badge-fulfilled" if is_fulfilled else "badge-open"
                status_text = "✅ Fulfilled" if is_fulfilled else "🟢 Open Request"
                border_color = "#8B5CF6" if is_fulfilled else "#EF4444" if "Urgent" in urg else "#F59E0B" if "Important" in urg else "#3B82F6"

                with st.container():
                    st.markdown(f"""
                    <div class="glass-card" style="border-left: 5px solid {border_color}; padding: 22px;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                            <div>
                                <h3 style="margin: 0 0 6px 0; font-size: 20px; font-weight: 800; color: #0F172A;">📌 {req.get('title')}</h3>
                                <span class="tag-chip">📚 {req.get('subject')}</span>
                                <span class="tag-chip">🎓 {req.get('semester')}</span>
                                <span class="tag-chip">📑 {req.get('type', 'Notes')}</span>
                            </div>
                            <div style="display: flex; gap: 8px; align-items: center;">
                                <span class="{urg_badge}">{urg}</span>
                                <span class="{status_badge}">{status_text}</span>
                            </div>
                        </div>
                        <p style="margin: 12px 0 10px 0; font-size: 15px; color: #334155; line-height: 1.5;">
                            {req.get('description')}
                        </p>
                        <div style="font-size: 13px; color: #64748B; display: flex; justify-content: space-between; flex-wrap: wrap; margin-bottom: 12px; font-weight: 500;">
                            <span>👤 Requested by: <strong style="color:#0F172A;">{req.get('requester', 'Student')}</strong> on {req.get('date', 'Recent')}</span>
                            <span>👍 <strong style="color:#4F46E5;">{req.get('upvotes', 0)}</strong> student(s) need this</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if is_fulfilled:
                        st.success(f"🎉 **Fulfilled by {req.get('fulfilled_by', 'Contributor')}** on {req.get('fulfilled_date', 'Recently')}\n\n💡 **Note:** {req.get('fulfillment_note', 'Available in Study Materials Hub.')}")
                    else:
                        act_c1, act_c2 = st.columns([1, 2])
                        with act_c1:
                            if st.button(f"👍 I Need This Too (+{req.get('upvotes', 0)})", key=f"req_upvote_{req_id}", use_container_width=True):
                                req["upvotes"] = req.get("upvotes", 0) + 1
                                save_material_requests(material_requests_data)
                                st.toast(f"Upvoted '{req.get('title')}'! Community priority increased.", icon="🚀")
                                st.rerun()

                        with act_c2:
                            with st.expander("🎁 Fulfill this Request (Upload or Link)"):
                                with st.form(f"fulfill_form_{req_id}", clear_on_submit=True):
                                    f_author = st.text_input("Your Contributor Name", value=student_name if student_name else "Helpful Peer", key=f"f_auth_{req_id}")
                                    f_note = st.text_area("Fulfillment Note / Solution Details", placeholder="e.g. Uploaded 'AVL_Tree_Rotations.pdf' in the Study Materials section, or link to notes.", key=f"f_note_{req_id}")
                                    fulfill_btn = st.form_submit_button("✅ Mark Request as Fulfilled", use_container_width=True)

                                    if fulfill_btn:
                                        if not f_note.strip():
                                             st.error("Please provide a note or file location to help the student find it.")
                                        else:
                                            req["status"] = "Fulfilled"
                                            req["fulfilled_by"] = f_author.strip() if f_author.strip() else "Helpful Contributor"
                                            req["fulfilled_date"] = datetime.now().strftime("%Y-%m-%d")
                                            req["fulfillment_note"] = f_note.strip()
                                            save_material_requests(material_requests_data)

                                            st.balloons()
                                            st.success("🌟 Thank you! This material request is now marked as resolved and fulfilled.")
                                            st.rerun()

                    st.markdown("<br>", unsafe_allow_html=True)

    # --- TAB 2: POST NEW REQUEST ---
    with req_tab_post:
        st.subheader("➕ Create a New Material Request")
        st.write("Let your college peers, seniors, and faculties know what study resources or question papers you are searching for.")

        with st.form("full_request_form", clear_on_submit=True):
            r_col1, r_col2 = st.columns(2)
            with r_col1:
                r_title = st.text_input("Topic / Material Title *", placeholder="e.g. Unit 2 - Process Scheduling & Semaphores Notes")
                r_subject = st.selectbox("Academic Subject *", ["C Programming", "C++ Programming", "Python", "Data Structures", "Mathematics", "Computer Science", "Database Systems", "Operating Systems", "Computer Networks", "Web Development", "AI / Machine Learning", "Software Engineering", "Other"], key="post_req_sub")
                r_semester = st.selectbox("Academic Semester *", [f"{i}st Semester" if i == 1 else f"{i}nd Semester" if i == 2 else f"{i}rd Semester" if i == 3 else f"{i}th Semester" for i in range(1, 9)], index=2, key="post_req_sem")

            with r_col2:
                r_type = st.selectbox("Resource Category *", ["Lecture Notes", "Quick Revision Cheatsheet", "Previous Year Question Paper (PYQ)", "Lab Manual", "Reference Book / Summary", "Assignment Solutions", "Syllabus Copy"], key="post_req_type")
                r_urgency = st.selectbox("Urgency Level *", ["🚨 Urgent (Exam in <3 days)", "⚠️ Important (Test or lab coming up)", "📌 General (Regular semester prep)"], key="post_req_urg")
                r_requester = st.text_input("Your Name", value=student_name if student_name else "Student Scholar", key="post_req_name")

            r_description = st.text_area("Detailed Description & Specific Chapters *", placeholder="Mention specific topics, formulas, professor name, or textbook references to help peers find the right file.")

            submit_req = st.form_submit_button("🚀 Submit Request to Community Wishlist", use_container_width=True)

            if submit_req:
                if not r_title.strip() or not r_description.strip():
                    st.error("Please fill in both the title and a detailed description.")
                else:
                    new_entry = {
                        "id": f"req_{int(datetime.now().timestamp())}",
                        "title": r_title.strip(),
                        "subject": r_subject,
                        "semester": r_semester,
                        "type": r_type,
                        "urgency": "🚨 Urgent" if "Urgent" in r_urgency else "⚠️ Important" if "Important" in r_urgency else "📌 General",
                        "description": r_description.strip(),
                        "requester": r_requester.strip() if r_requester.strip() else "Student Scholar",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "upvotes": 1,
                        "status": "Open",
                        "fulfilled_by": None,
                        "fulfilled_date": None,
                        "fulfillment_note": None
                    }
                    material_requests_data.insert(0, new_entry)
                    save_material_requests(material_requests_data)

                    st.balloons()
                    st.success("🎉 Material request successfully broadcasted! Peers and faculty will be notified on the dashboard.")
                    st.rerun()

    # --- TAB 3: HALL OF FAME ---
    with req_tab_hall:
        st.subheader("🏆 Contributor Hall of Fame")
        st.write("Special recognition to students and contributors who resolved peer requests and enriched our campus resource bank.")

        hof_col1, hof_col2 = st.columns(2)
        with hof_col1:
            st.markdown("""
            <div class="glass-card">
                <h4 style="margin-top:0; color:#4338CA; font-size:18px;">🌟 Top Request Solvers</h4>
                <div style="display:flex; justify-content:space-between; margin-bottom:12px; font-size:15px;">
                    <span>🥇 <strong style="color:#0F172A;">Rohan Sharma</strong> (CS 5th Sem)</span>
                    <span class="tag-chip">8 Requests Resolved</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:12px; font-size:15px;">
                    <span>🥈 <strong style="color:#0F172A;">Ananya Mishra</strong> (IT 3rd Sem)</span>
                    <span class="tag-chip">5 Requests Resolved</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:15px;">
                    <span>🥉 <strong style="color:#0F172A;">Vikram Patel</strong> (ECE 7th Sem)</span>
                    <span class="tag-chip">4 Requests Resolved</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with hof_col2:
            st.markdown("""
            <div class="glass-card">
                <h4 style="margin-top:0; color:#059669; font-size:18px;">💡 How to Earn Contributor Badges</h4>
                <p style="font-size:14px; color:#334155; line-height:1.6;">
                    • <strong>Bronze Contributor:</strong> Fulfill 2 community requests.<br>
                    • <strong>Silver Contributor:</strong> Fulfill 5 requests &amp; maintain 4+ upvotes.<br>
                    • <strong>Gold Contributor:</strong> Top 3 contributors of the semester receive campus hackathon credits &amp; certificates.
                </p>
            </div>
            """, unsafe_allow_html=True)


# ==================================================
# 5. 🧰 STUDENT PRODUCTIVITY TOOLS
# ==================================================

elif "Student Tools" in nav_option:
    st.header("🧰 Student Productivity Suite")
    st.write("Interactive utilities to calculate SGPA, safeguard attendance, run focus sessions, and test tech knowledge.")

    tool_tab1, tool_tab2, tool_tab3, tool_tab4 = st.tabs([
        "🎓 SGPA & CGPA Planner",
        "📊 75% Attendance Guard",
        "⏱️ Pomodoro Focus Studio",
        "🧠 Daily Tech Quiz Mini-Game"
    ])

    # --- TOOL 1: SGPA & CGPA CALCULATOR ---
    with tool_tab1:
        st.subheader("🎓 Semester SGPA & Target Planner")
        st.write("Enter your course credits and anticipated grades to compute your official Semester Grade Point Average (SGPA).")

        grade_points = {
            "O (Outstanding) [10.0]": 10.0,
            "A+ (Excellent) [9.0]": 9.0,
            "A (Very Good) [8.0]": 8.0,
            "B+ (Good) [7.0]": 7.0,
            "B (Above Average) [6.0]": 6.0,
            "C (Average) [5.0]": 5.0,
            "P (Pass) [4.0]": 4.0,
            "F (Fail) [0.0]": 0.0
        }

        num_courses = st.number_input("Number of Courses / Labs this Semester", min_value=1, max_value=12, value=5, step=1)

        total_credits = 0.0
        weighted_points = 0.0

        st.markdown("##### 📝 Course Grade Roster:")
        for i in range(int(num_courses)):
            c1, c2, c3 = st.columns([2, 1, 2])
            with c1:
                course_name = st.text_input(f"Course {i+1}", value=f"Course {i+1}", key=f"sgpa_name_{i}")
            with c2:
                course_credit = st.number_input(f"Credits", min_value=1.0, max_value=6.0, value=3.0 if i < 4 else 1.5, step=0.5, key=f"sgpa_cred_{i}")
            with c3:
                course_grade = st.selectbox(f"Grade", list(grade_points.keys()), key=f"sgpa_grd_{i}")

            total_credits += course_credit
            weighted_points += (course_credit * grade_points[course_grade])

        if total_credits > 0:
            calculated_sgpa = round(weighted_points / total_credits, 2)
            calculated_pct = round((calculated_sgpa - 0.75) * 10, 1) if calculated_sgpa >= 0.75 else 0.0

            st.markdown("<br>", unsafe_allow_html=True)
            res_c1, res_c2, res_c3 = st.columns(3)
            with res_c1:
                st.markdown(f"""
                <div class="glass-card" style="text-align:center;">
                    <div style="font-size:13px; color:#64748B; font-weight:700; text-transform:uppercase;">Calculated SGPA</div>
                    <div style="font-size:36px; font-weight:800; color:#4338CA; margin:8px 0;">{calculated_sgpa} / 10.0</div>
                    <span class="tag-chip">Total Credits: {total_credits}</span>
                </div>
                """, unsafe_allow_html=True)
            with res_c2:
                st.markdown(f"""
                <div class="glass-card" style="text-align:center;">
                    <div style="font-size:13px; color:#64748B; font-weight:700; text-transform:uppercase;">Approximate Percentage</div>
                    <div style="font-size:36px; font-weight:800; color:#059669; margin:8px 0;">{max(calculated_pct, 0.0)}%</div>
                    <span class="tag-chip">AICTE / UGC Formula</span>
                </div>
                """, unsafe_allow_html=True)
            with res_c3:
                classification = "🥇 First Class with Distinction" if calculated_sgpa >= 8.5 else "🥈 First Class" if calculated_sgpa >= 6.75 else "🥉 Second Class" if calculated_sgpa >= 5.0 else "⚠️ Pass / Reappear"
                st.markdown(f"""
                <div class="glass-card" style="text-align:center;">
                    <div style="font-size:13px; color:#64748B; font-weight:700; text-transform:uppercase;">Academic Standing</div>
                    <div style="font-size:20px; font-weight:800; color:#D97706; margin:14px 0;">{classification}</div>
                </div>
                """, unsafe_allow_html=True)

    # --- TOOL 2: ATTENDANCE GUARD ---
    with tool_tab2:
        st.subheader("📊 75% Mandatory Attendance Forecaster")
        st.write("Ensure you never fall below the threshold required to sit for college end-semester examinations.")

        att_col1, att_col2, att_col3 = st.columns(3)
        with att_col1:
            total_held = st.number_input("Total Lectures Conducted", min_value=1, value=45, step=1)
        with att_col2:
            total_attended = st.number_input("Lectures You Attended", min_value=0, max_value=int(total_held), value=36, step=1)
        with att_col3:
            target_pct = st.slider("Target Minimum %", min_value=60, max_value=90, value=75, step=5)

        current_pct = round((total_attended / total_held) * 100, 1)
        target_ratio = target_pct / 100.0

        st.markdown("<br>", unsafe_allow_html=True)
        # Visual Progress Bar
        st.progress(min(current_pct / 100.0, 1.0), text=f"Current Status: {current_pct}% (Target: {target_pct}%)")

        st.markdown("<br>", unsafe_allow_html=True)
        g_c1, g_c2 = st.columns(2)

        if current_pct >= target_pct:
            safe_bunks = int((total_attended / target_ratio) - total_held)
            with g_c1:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 5px solid #059669;">
                    <h3 style="color:#059669; margin:0 0 6px 0; font-size:20px;">✅ Safe Attendance Buffer</h3>
                    <p style="font-size:15px; margin:0; color:#1E293B; line-height:1.5;">
                        You can safely miss up to <strong style="font-size:20px; color:#059669;">{safe_bunks}</strong> upcoming lecture(s) without dropping below {target_pct}%.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            with g_c2:
                st.info("💡 **Attendance Pro Tip:** Save your bunk allowance for crunch exam weeks or project submission crunches!")
        else:
            must_attend = int(((target_ratio * total_held) - total_attended) / (1.0 - target_ratio)) + 1
            with g_c1:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 5px solid #DC2626;">
                    <h3 style="color:#DC2626; margin:0 0 6px 0; font-size:20px;">⚠️ Attendance Warning Zone</h3>
                    <p style="font-size:15px; margin:0; color:#1E293B; line-height:1.5;">
                        You must attend the next <strong style="font-size:20px; color:#DC2626;">{must_attend}</strong> consecutive lecture(s) without missing any to restore eligibility.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            with g_c2:
                st.warning("⚠️ **Action Required:** Inform your faculty advisor or submit medical certificates if applicable.")

    # --- TOOL 3: POMODORO FOCUS STUDIO ---
    with tool_tab3:
        st.subheader("⏱️ Pomodoro Focus Studio")
        st.write("Eliminate distractions with interval study cycles, task tracking, and ambient study soundscapes.")

        p_col1, p_col2 = st.columns([1, 1])

        with p_col1:
            st.markdown("""
            <div class="glass-card" style="text-align:center;">
                <div style="font-size:13px; color:#64748B; font-weight:700; text-transform:uppercase;">Focus Interval</div>
                <div style="font-size:52px; font-weight:800; font-family:'Outfit'; color:#4338CA; margin:8px 0;">25:00</div>
                <span class="tag-chip">🍅 Deep Work Cycle</span>
            </div>
            """, unsafe_allow_html=True)

            study_task = st.text_input("🎯 Today's Main Study Objective", placeholder="e.g. Master Binary Search Trees & Solve 4 LeetCode problems")

            st.markdown("##### 📝 Active Checklist:")
            st.checkbox("Read Chapter / Lecture Slide Deck", value=False)
            st.checkbox("Write Key Formulas & Summaries", value=False)
            st.checkbox("Implement Code / Solve Practice Questions", value=False)
            st.checkbox("Review Mistakes & Self-Test", value=False)

        with p_col2:
            st.markdown("#### 🎧 Curated Focus Soundscapes")
            st.markdown("""
            <div class="glass-card">
                <p style="margin:0 0 12px 0; font-size:15px; color:#334155;">Boost focus and block background noise:</p>
                <div style="margin-bottom:10px;">• 🎧 <a href="https://www.youtube.com/watch?v=jfKfPfyJRdk" target="_blank" style="color:#4338CA; font-weight:700;">Lofi Girl Study Stream (YouTube)</a></div>
                <div style="margin-bottom:10px;">• 🌧️ <a href="https://rainymood.com/" target="_blank" style="color:#4338CA; font-weight:700;">Rainymood (Ambient Rain &amp; Thunder)</a></div>
                <div style="margin-bottom:0;">• ☕ <a href="https://coffitivity.com/" target="_blank" style="color:#4338CA; font-weight:700;">Coffitivity (Ambient Cafe Sounds)</a></div>
            </div>
            """, unsafe_allow_html=True)

    # --- TOOL 4: DAILY CS QUIZ MINI-GAME ---
    with tool_tab4:
        st.subheader("🧠 Daily Computer Science & Tech Quiz")
        st.write("Test your core knowledge in Data Structures, Algorithms, Python, and Operating Systems.")

        quiz_questions = [
            {
                "q": "1. What is the time complexity of searching an element in a balanced Binary Search Tree (BST)?",
                "options": ["O(1)", "O(n)", "O(log n)", "O(n log n)"],
                "answer": "O(log n)",
                "explanation": "In a balanced BST, each comparison halves the search space, giving logarithmic time O(log n)."
            },
            {
                "q": "2. Which of the following is NOT an immutable data type in Python?",
                "options": ["Tuple", "String", "List", "Integer"],
                "answer": "List",
                "explanation": "Lists in Python are mutable, meaning their elements can be changed, added, or removed in-place."
            },
            {
                "q": "3. Which scheduling algorithm may suffer from the 'Convoy Effect'?",
                "options": ["First-Come, First-Served (FCFS)", "Round Robin (RR)", "Shortest Job First (SJF)", "Priority Scheduling"],
                "answer": "First-Come, First-Served (FCFS)",
                "explanation": "In FCFS, when a long CPU-bound process holds the CPU, all shorter processes wait behind it."
            }
        ]

        score = 0
        with st.form("tech_quiz_form"):
            user_answers = []
            for idx, q in enumerate(quiz_questions):
                st.markdown(f"**{q['q']}**")
                choice = st.radio(f"Select your answer for Q{idx+1}", q["options"], key=f"quiz_opt_{idx}", label_visibility="collapsed")
                user_answers.append(choice)
                st.markdown("<br>", unsafe_allow_html=True)

            quiz_submit = st.form_submit_button("🏁 Submit Quiz & Check Score", use_container_width=True)

            if quiz_submit:
                for idx, q in enumerate(quiz_questions):
                    if user_answers[idx] == q["answer"]:
                        score += 1

                if score == len(quiz_questions):
                    st.balloons()
                    st.success(f"🎉 **Perfect Score! {score}/{len(quiz_questions)}** — Excellent grasp of core CS fundamentals!")
                else:
                    st.info(f"📊 **Your Score: {score}/{len(quiz_questions)}**")

                st.markdown("##### 📖 Solution Explanations:")
                for idx, q in enumerate(quiz_questions):
                    status = "✅ Correct" if user_answers[idx] == q["answer"] else f"❌ Incorrect (Correct: {q['answer']})"
                    st.markdown(f"**Q{idx+1}:** {status} — *{q['explanation']}*")


# ==================================================
# 6. 🔗 CURATED USEFUL RESOURCES
# ==================================================

elif "Useful Resources" in nav_option:
    st.header("🔗 Curated Academic & Career Resources")
    st.write("Verified learning platforms, interview prep portals, open courseware, and student developer perks.")

    res_category = st.radio(
        "Resource Categories",
        ["All", "💻 DSA & Coding Practice", "🌐 Web & Software Engineering", "🎓 Free Courses & Open Source", "🎁 Student Developer Perks"],
        horizontal=True
    )

    resources = [
        # DSA & Coding Practice
        {
            "category": "💻 DSA & Coding Practice",
            "title": "LeetCode",
            "tag": "Interview DSA",
            "desc": "The gold-standard platform for practicing data structure and algorithm problems asked in technical interviews.",
            "url": "https://leetcode.com/"
        },
        {
            "category": "💻 DSA & Coding Practice",
            "title": "NeetCode 150",
            "tag": "DSA Roadmap",
            "desc": "A systematically organized 150-question roadmap with video tutorials covering arrays, trees, graphs, and DP.",
            "url": "https://neetcode.io/"
        },
        {
            "category": "💻 DSA & Coding Practice",
            "title": "GeeksforGeeks",
            "tag": "CS Fundamentals",
            "desc": "In-depth tutorials and code implementations for DBMS, OS, Computer Networks, and competitive programming.",
            "url": "https://www.geeksforgeeks.org/"
        },
        {
            "category": "💻 DSA & Coding Practice",
            "title": "HackerRank",
            "tag": "Certifications",
            "desc": "Great for beginners to test language syntax proficiency and earn verified domain skill badges.",
            "url": "https://www.hackerrank.com/"
        },

        # Web & Software Engineering
        {
            "category": "🌐 Web & Software Engineering",
            "title": "Developer Roadmaps (Roadmap.sh)",
            "tag": "Career Visuals",
            "desc": "Community-driven visual step-by-step roadmaps for Frontend, Backend, DevOps, AI, and Cybersecurity.",
            "url": "https://roadmap.sh/"
        },
        {
            "category": "🌐 Web & Software Engineering",
            "title": "MDN Web Docs",
            "tag": "Web Standards",
            "desc": "Mozilla's premier documentation for HTML, CSS, JavaScript, Web APIs, and best development practices.",
            "url": "https://developer.mozilla.org/"
        },
        {
            "category": "🌐 Web & Software Engineering",
            "title": "Python Official Documentation",
            "tag": "Language Docs",
            "desc": "The definitive language tutorial, library reference index, and standard library documentation.",
            "url": "https://docs.python.org/3/"
        },

        # Free Courses & Open Source
        {
            "category": "🎓 Free Courses & Open Source",
            "title": "Harvard CS50",
            "tag": "World Famous Intro",
            "desc": "Harvard University's world-famous introduction to computer science and algorithmic thinking.",
            "url": "https://cs50.harvard.edu/"
        },
        {
            "category": "🎓 Free Courses & Open Source",
            "title": "MIT OpenCourseWare",
            "tag": "MIT Lectures",
            "desc": "Free complete MIT lecture recordings, syllabus problem sets, and exam archives across engineering.",
            "url": "https://ocw.mit.edu/"
        },
        {
            "category": "🎓 Free Courses & Open Source",
            "title": "NPTEL / SWAYAM",
            "tag": "IIT & IISc Courses",
            "desc": "Curated national university curriculum courses taught by distinguished professors from IITs and IISc.",
            "url": "https://nptel.ac.in/"
        },
        {
            "category": "🎓 Free Courses & Open Source",
            "title": "freeCodeCamp",
            "tag": "Hands-on Certs",
            "desc": "Learn responsive web design, scientific computing with Python, and backend APIs through interactive challenges.",
            "url": "https://www.freecodecamp.org/"
        },

        # Student Developer Perks
        {
            "category": "🎁 Student Developer Perks",
            "title": "GitHub Student Developer Pack",
            "tag": "Free Pro Tools ($1000+ Value)",
            "desc": "Free GitHub Copilot, Canva Pro, Namecheap domains, JetBrains IDEs, DigitalOcean cloud credits, and more.",
            "url": "https://education.github.com/pack"
        },
        {
            "category": "🎁 Student Developer Perks",
            "title": "JetBrains Free Educational License",
            "tag": "Pro IDEs",
            "desc": "Complimentary pro licenses for PyCharm Professional, IntelliJ IDEA Ultimate, WebStorm, and CLion.",
            "url": "https://www.jetbrains.com/community/education/#students"
        }
    ]

    filtered_res = [r for r in resources if res_category == "All" or r["category"] == res_category]

    rc1, rc2 = st.columns(2)
    for idx, item in enumerate(filtered_res):
        col = rc1 if idx % 2 == 0 else rc2
        with col:
            with st.container():
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; color: #4338CA; font-size: 20px; font-weight: 800;">{item['title']}</h4>
                        <span class="tag-chip">{item['tag']}</span>
                    </div>
                    <p style="font-size: 14px; color: #334155; margin: 10px 0 14px 0; line-height: 1.5;">{item['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.link_button(f"🚀 Open {item['title']}", item["url"], use_container_width=True)
                st.markdown("<br>", unsafe_allow_html=True)


# ==================================================
# 7. 📢 CAMPUS ANNOUNCEMENTS
# ==================================================

elif "Announcements" in nav_option:
    st.header("📢 Campus Notice Board & Announcements")
    st.write("Stay informed about upcoming hackathons, lab exams, university holidays, and campus placement drives.")

    ann_tab_view, ann_tab_post = st.tabs(["📋 College Notice Board", "➕ Post Campus Notice"])

    # --- TAB 1: VIEW ANNOUNCEMENTS ---
    with ann_tab_view:
        p_col1, p_col2 = st.columns([1, 2])
        with p_col1:
            p_filter = st.selectbox("Priority Filter", ["All Priorities", "🚨 Urgent", "⚠️ Important", "📌 General"])
        with p_col2:
            search_ann = st.text_input("Search Notices", placeholder="e.g. lab, hackathon, holiday, exam...")

        filtered_announcements = []
        for a in announcements_data:
            pri = a.get("priority", "General")
            match_pri = (
                (p_filter == "All Priorities") or
                (p_filter == "🚨 Urgent" and pri.lower() == "urgent") or
                (p_filter == "⚠️ Important" and pri.lower() == "important") or
                (p_filter == "📌 General" and pri.lower() == "general")
            )
            q = search_ann.lower().strip()
            match_q = not q or (q in a.get("title", "").lower()) or (q in a.get("message", "").lower()) or (q in a.get("department", "").lower())

            if match_pri and match_q:
                filtered_announcements.append(a)

        st.markdown(f"**Showing {len(filtered_announcements)} active campus notice(s)**")

        if not filtered_announcements:
            st.info("No notices match your current search or filter.")
        else:
            for item in filtered_announcements:
                pri = item.get("priority", "General").title()
                badge_class = "badge-urgent" if pri.lower() == "urgent" else "badge-important" if pri.lower() == "important" else "badge-general"
                border_color = "#DC2626" if pri.lower() == "urgent" else "#D97706" if pri.lower() == "important" else "#2563EB"
                
                with st.container():
                    st.markdown(f"""
                    <div class="glass-card" style="border-left: 5px solid {border_color};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h3 style="margin: 0; font-size: 20px; font-weight: 800; color: #0F172A;">📌 {item.get('title', 'Untitled Notice')}</h3>
                            <span class="{badge_class}">{pri}</span>
                        </div>
                        <p style="margin: 10px 0; font-size: 15px; color: #334155; line-height: 1.6;">{item.get('message', '')}</p>
                        <div style="font-size: 13px; color: #64748B; font-weight: 500;">
                            🏛️ <strong>Department:</strong> {item.get('department', 'General')} &nbsp;|&nbsp; 
                            👤 <strong>Posted By:</strong> {item.get('author', 'Admin')} &nbsp;|&nbsp; 
                            📅 <strong>Date:</strong> {item.get('date', 'Recent')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # --- TAB 2: POST ANNOUNCEMENT ---
    with ann_tab_post:
        st.subheader("➕ Create Official Notice")
        st.write("Student club leads, class representatives, and faculty members can broadcast official college updates.")

        with st.form("post_announcement_form", clear_on_submit=True):
            f_title = st.text_input("Notice Title *", placeholder="e.g. End-Semester Lab Exam Schedule Released")
            f_message = st.text_area("Detailed Announcement *", placeholder="Include all instructions, room numbers, dates, timings, and required documents.")
            
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                f_priority = st.selectbox("Priority Level *", ["General", "Important", "Urgent"])
            with f_col2:
                f_department = st.selectbox("Issuing Department *", ["Computer Science Dept", "Examination Cell", "Training & Placement Cell", "Coding Club / Tech Society", "Cultural & Sports Council", "General Administration"])
            with f_col3:
                f_author = st.text_input("Issued By", value=student_name if student_name else "Campus Lead")

            post_submitted = st.form_submit_button("📢 Broadcast Announcement", use_container_width=True)

            if post_submitted:
                if not f_title.strip() or not f_message.strip():
                    st.error("Please fill in both the title and notice message.")
                else:
                    new_notice = {
                        "title": f_title.strip(),
                        "message": f_message.strip(),
                        "priority": f_priority,
                        "department": f_department,
                        "author": f_author.strip() if f_author.strip() else "Admin",
                        "date": datetime.now().strftime("%Y-%m-%d")
                    }
                    announcements_data.insert(0, new_notice)
                    save_announcements(announcements_data)

                    st.balloons()
                    st.success("✅ Announcement published and immediately broadcasted to the college notice board!")
                    st.rerun()