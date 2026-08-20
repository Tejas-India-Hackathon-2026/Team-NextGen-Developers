import streamlit as st
import os
import json
import base64
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

os.makedirs(MATERIAL_FOLDER, exist_ok=True)

# ==================================================
# 💎 ULTRA-PREMIUM MODERN DESIGN SYSTEM (CSS)
# ==================================================
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700;
        letter-spacing: -0.02em;
    }

    /* Keyframe Animations */
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.08); opacity: 0.7; }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-4px); }
    }

    /* Live Status Indicator */
    .live-pulse {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10B981;
        box-shadow: 0 0 10px #10B981;
        animation: pulse 2s infinite ease-in-out;
        margin-right: 6px;
    }

    /* Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 40%, #DB2777 100%);
        border-radius: 20px;
        padding: 30px 34px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 20px 40px -15px rgba(79, 70, 229, 0.4);
        position: relative;
        overflow: hidden;
    }
    .hero-container::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .glass-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 16px 32px rgba(0, 0, 0, 0.2);
        border-color: rgba(99, 102, 241, 0.4);
    }

    /* Metric Glass Box */
    .metric-box {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 18px 20px;
        display: flex;
        align-items: center;
        gap: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease;
    }
    .metric-box:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.5);
    }
    .metric-icon {
        font-size: 32px;
        background: rgba(99, 102, 241, 0.12);
        border-radius: 12px;
        padding: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .metric-val {
        font-size: 26px;
        font-weight: 800;
        font-family: 'Outfit', sans-serif;
        color: #F8FAFC;
        line-height: 1.1;
    }
    .metric-label {
        font-size: 13px;
        color: #94A3B8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    /* Badges & Pills */
    .badge-urgent {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: white;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.35);
    }
    .badge-important {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.35);
    }
    .badge-general {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.35);
    }
    .badge-open {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.35);
    }
    .badge-fulfilled {
        background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
        color: white;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        box-shadow: 0 2px 8px rgba(139, 92, 246, 0.35);
    }
    .tag-chip {
        display: inline-flex;
        align-items: center;
        background: rgba(99, 102, 241, 0.12);
        color: #A5B4FC;
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 8px;
        padding: 3px 10px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 4px;
    }

    /* Grade Points Highlight Chips */
    .grade-chip-gold {
        background: rgba(234, 179, 8, 0.15);
        color: #FACC15;
        border: 1px solid rgba(234, 179, 8, 0.3);
        border-radius: 6px;
        padding: 2px 8px;
        font-weight: 700;
    }
    .grade-chip-green {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 6px;
        padding: 2px 8px;
        font-weight: 700;
    }

    /* Sidebar profile avatar container */
    .profile-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    /* Smooth buttons & tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.4);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 600;
        color: #94A3B8;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: #4F46E5 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
    }
</style>
""", unsafe_allow_html=True)


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
            if "py" in filename.lower() or "python" in filename.lower():
                inferred_subject = "Python"
            elif "ds" in filename.lower() or "algo" in filename.lower() or "data" in filename.lower():
                inferred_subject = "Data Structures"
            elif "math" in filename.lower():
                inferred_subject = "Mathematics"

            meta[filename] = {
                "title": filename.replace(".pdf", "").replace("_", " ").title(),
                "subject": inferred_subject,
                "semester": "1st Semester",
                "type": "Lecture Notes",
                "uploader": "Faculty / Contributor",
                "upload_date": datetime.now().strftime("%Y-%m-%d"),
                "size_kb": file_size_kb,
                "description": "Complete lecture reference notes with core concepts.",
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
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
        <h2 style="margin: 0; font-size: 24px; color: #818CF8;">🎓 CampusHub</h2>
        <span style="font-size: 12px; color: #10B981; font-weight: 600;"><span class="live-pulse"></span>Live</span>
    </div>
    <p style="font-size: 13px; color: #94A3B8; margin-top: 0;">Academic Resource Network & Toolkit</p>
    """, unsafe_allow_html=True)

    nav_option = st.radio(
        "Navigation Menu",
        [
            "🏠 Home Dashboard",
            "📚 Study Materials",
            "🙋 Request Materials",
            "🧰 Student Tools",
            "🔗 Useful Resources",
            "📢 Announcements"
        ],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='margin: 14px 0; border: 0; border-top: 1px solid rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

    # Student Profile Card
    st.markdown("#### 👤 Student Profile")
    student_name = st.text_input("Your Full Name", value=st.session_state.get("student_name", "Student Scholar"), placeholder="e.g. Alex Kumar")
    st.session_state["student_name"] = student_name

    branch = st.selectbox(
        "Branch / Department",
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
        ]
    )

    semester = st.selectbox(
        "Current Semester",
        [f"{i}st Semester" if i == 1 else f"{i}nd Semester" if i == 2 else f"{i}rd Semester" if i == 3 else f"{i}th Semester" for i in range(1, 9)],
        index=2
    )

    # Visual Profile Badge
    st.markdown(f"""
    <div class="profile-card">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="font-size: 26px; background: rgba(99,102,241,0.2); border-radius: 50%; padding: 6px 10px;">👨‍🎓</div>
            <div>
                <div style="font-weight: 700; color: #F1F5F9; font-size: 14px;">{student_name}</div>
                <div style="font-size: 12px; color: #94A3B8;">{semester} • {branch.split('(')[0].strip()}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("🚀 **Contribute notes or fulfill requests** to earn campus recognition and help fellow peers succeed.")


# ==================================================
# 1. 🏠 HOME DASHBOARD
# ==================================================

if "Home Dashboard" in nav_option:
    # Contextual Time Greeting
    current_hour = datetime.now().hour
    time_greeting = "Good morning 🌅" if current_hour < 12 else "Good afternoon ☀️" if current_hour < 17 else "Good evening 🌙"
    
    # Hero Banner
    st.markdown(f"""
    <div class="hero-container">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
            <div>
                <span style="background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Campus Portal • Academic Year 2026</span>
                <h1 style="margin: 10px 0 6px 0; font-size: 32px; font-weight: 800;">{time_greeting}, {student_name}! 🚀</h1>
                <p style="margin: 0; opacity: 0.95; font-size: 15px; max-width: 650px; line-height: 1.5;">
                    Your centralized college hub for <strong>{semester}</strong> ({branch}). Discover peer-reviewed notes, request needed materials, calculate GPA projections, and never miss an official notice.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Key KPI Metric Cards
    total_materials = len(materials_meta)
    open_requests_count = len([r for r in material_requests_data if r.get("status") == "Open"])
    total_announcements = len(announcements_data)
    total_likes = sum(item.get("likes", 0) for item in materials_meta.values()) + sum(r.get("upvotes", 0) for r in material_requests_data)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon">📚</div>
            <div>
                <div class="metric-val">{total_materials}</div>
                <div class="metric-label">Study Materials</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon">🙋</div>
            <div>
                <div class="metric-val">{open_requests_count}</div>
                <div class="metric-label">Open Material Requests</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon">📢</div>
            <div>
                <div class="metric-val">{total_announcements}</div>
                <div class="metric-label">Active Notices</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with kpi4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon">❤️</div>
            <div>
                <div class="metric-val">{total_likes}</div>
                <div class="metric-label">Peer Upvotes</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Urgent Notices Alert Ticker
    urgent_notices = [a for a in announcements_data if a.get("priority", "").lower() == "urgent"]
    if urgent_notices:
        for u in urgent_notices:
            st.error(f"🚨 **URGENT NOTICE:** **{u.get('title')}** — {u.get('message')} *(Posted by {u.get('author', 'Admin')} on {u.get('date', 'Today')})*")

    # Semester Progress Bar
    st.markdown("#### 🎯 Semester Milestones & Academic Progress")
    sem_progress_col1, sem_progress_col2 = st.columns([3, 1])
    with sem_progress_col1:
        st.progress(0.65, text="Semester Timeline: Week 11 of 16 (Mid-terms completed • End-sem finals in 4 weeks)")
    with sem_progress_col2:
        st.caption("💡 Recommended: Complete 2 PYQ sets this week.")

    st.markdown("<hr style='margin: 20px 0; border: 0; border-top: 1px solid rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

    # 2-Column Home Layout
    dash_col_left, dash_col_right = st.columns([3, 2])

    with dash_col_left:
        st.subheader("🔥 Featured & Recent Study Materials")
        if not materials_meta:
            st.info("No study materials found. Be the first student to upload!")
        else:
            recent_items = sorted(
                materials_meta.items(),
                key=lambda x: x[1].get("upload_date", ""),
                reverse=True
            )[:3]

            for filename, info in recent_items:
                file_path = os.path.join(MATERIAL_FOLDER, filename)
                with st.container():
                    st.markdown(f"""
                    <div class="glass-card" style="padding: 16px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div>
                                <h4 style="margin: 0 0 6px 0; color: #F1F5F9; font-size: 16px;">📄 {info.get('title', filename)}</h4>
                                <span class="tag-chip">📚 {info.get('subject', 'General')}</span>
                                <span class="tag-chip">🎓 {info.get('semester', 'All')}</span>
                                <span class="tag-chip">📑 {info.get('type', 'Notes')}</span>
                            </div>
                            <div style="text-align: right; font-size: 12px; color: #94A3B8;">
                                💾 {info.get('size_kb', 0)} KB<br>
                                ❤️ {info.get('likes', 0)} Upvotes
                            </div>
                        </div>
                        <p style="font-size: 13px; color: #CBD5E1; margin: 8px 0 10px 0;">{info.get('description', '')}</p>
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
                                    key=f"dash_dl_{filename}",
                                    use_container_width=True
                                ):
                                    materials_meta[filename]["downloads"] = materials_meta[filename].get("downloads", 0) + 1
                                    save_materials_meta(materials_meta)
                    with btn_c2:
                        if st.button(f"❤️ Upvote ({info.get('likes', 0)})", key=f"dash_like_{filename}", use_container_width=True):
                            materials_meta[filename]["likes"] = materials_meta[filename].get("likes", 0) + 1
                            save_materials_meta(materials_meta)
                            st.rerun()

    with dash_col_right:
        st.subheader("🙋 Top Requested Student Materials")
        open_requests = [r for r in material_requests_data if r.get("status") == "Open"]
        sorted_requests = sorted(open_requests, key=lambda x: x.get("upvotes", 0), reverse=True)[:3]
        
        if not sorted_requests:
            st.info("No open material requests currently pending. Everything is fulfilled!")
        else:
            for req in sorted_requests:
                with st.container():
                    st.markdown(f"""
                    <div class="glass-card" style="padding: 14px; margin-bottom: 10px; border-left: 3px solid #818CF8;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong style="color: #F8FAFC; font-size: 14px;">📌 {req.get('title')}</strong>
                            <span class="tag-chip" style="margin: 0;">👍 {req.get('upvotes', 0)}</span>
                        </div>
                        <div style="font-size: 12px; color: #94A3B8; margin-top: 4px;">
                            📚 {req.get('subject')} • 🎓 {req.get('semester')} • Requested by {req.get('requester')}
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
        <div class="glass-card" style="padding: 14px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span>🥇 <strong>Rohan S.</strong> (CS 5th Sem)</span>
                <span class="tag-chip">14 Uploads • 82 ❤️</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span>🥈 <strong>Ananya M.</strong> (IT 3rd Sem)</span>
                <span class="tag-chip">9 Uploads • 54 ❤️</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span>🥉 <strong>Vikram P.</strong> (ECE 7th Sem)</span>
                <span class="tag-chip">6 Uploads • 39 ❤️</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==================================================
# 2. 📚 STUDY MATERIALS HUB
# ==================================================

elif "Study Materials" in nav_option:
    st.header("📚 Study Materials Hub")
    st.write("Browse, search, download, preview, and contribute academic PDFs across all semesters.")

    tab_browse, tab_upload, tab_request_jump = st.tabs([
        "🔍 Browse & Search Materials",
        "📤 Contribute / Upload Material",
        "🙋 Quick Material Request"
    ])

    # --- TAB 1: BROWSE MATERIALS ---
    with tab_browse:
        f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1, 1, 1])

        with f_col1:
            search_query = st.text_input("🔎 Search by Title, Keyword, or Uploader", placeholder="e.g. Python, Trees, Calculus, DBMS...")

        with f_col2:
            all_subjects = ["All Subjects"] + sorted(list(set(info.get("subject", "Other") for info in materials_meta.values()) | {"Python", "Data Structures", "Mathematics", "Computer Science", "Database Systems", "Operating Systems", "Computer Networks", "Web Development", "AI / Machine Learning", "Other"}))
            selected_subject = st.selectbox("Subject", all_subjects)

        with f_col3:
            all_semesters = ["All Semesters"] + [f"{i}st Semester" if i == 1 else f"{i}nd Semester" if i == 2 else f"{i}rd Semester" if i == 3 else f"{i}th Semester" for i in range(1, 9)]
            selected_semester = st.selectbox("Semester", all_semesters)

        with f_col4:
            all_types = ["All Types", "Lecture Notes", "Previous Year Question Paper (PYQ)", "Lab Manual", "Syllabus", "Reference Book / Summary"]
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
            st.info("No matching study materials found. Can't find what you need? Go to '🙋 Quick Material Request' tab to ask peers to upload it!")
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
                                    <h3 style="margin: 0 0 6px 0; font-size: 18px; color: #F8FAFC;">📄 {info.get('title', filename)}</h3>
                                    <span class="tag-chip">📚 {info.get('subject', 'General')}</span>
                                    <span class="tag-chip">🎓 {info.get('semester', 'All')}</span>
                                    <span class="tag-chip">📑 {info.get('type', 'Notes')}</span>
                                </div>
                            </div>
                            <p style="font-size: 13px; color: #CBD5E1; margin: 10px 0 12px 0; line-height: 1.4;">
                                {info.get('description', 'Comprehensive reference study materials.')}
                            </p>
                            <div style="font-size: 12px; color: #94A3B8; margin-bottom: 12px; display: flex; justify-content: space-between; flex-wrap: wrap;">
                                <span>👤 Contributor: <strong>{info.get('uploader', 'Peer')}</strong></span>
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
                qr_subject = st.selectbox("Subject *", ["Python", "Data Structures", "Mathematics", "Computer Science", "Database Systems", "Operating Systems", "Computer Networks", "Web Development", "AI / Machine Learning", "Other"], key="qr_sub")
                qr_semester = st.selectbox("Semester *", [f"{i}st Semester" if i == 1 else f"{i}nd Semester" if i == 2 else f"{i}rd Semester" if i == 3 else f"{i}th Semester" for i in range(1, 9)], index=2, key="qr_sem")
            with qr_col2:
                qr_type = st.selectbox("Resource Type", ["Lecture Notes", "Previous Year Question Paper (PYQ)", "Lab Manual", "Reference Book / Summary", "Assignment Solutions"], key="qr_type")
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
# 3. 🙋 REQUEST A MATERIAL PORTAL (DEDICATED)
# ==================================================

elif "Request Materials" in nav_option:
    st.header("🙋 Student Material Requests & Wishlist Portal")
    st.write("Can't find specific handwritten notes, past papers, or lab manuals? Post your request, upvote needed materials, or fulfill peer requests to earn contributor badges.")

    # Metric summary for requests
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
                    <div class="glass-card" style="border-left: 4px solid {border_color};">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                            <div>
                                <h3 style="margin: 0 0 6px 0; font-size: 19px; color: #F8FAFC;">📌 {req.get('title')}</h3>
                                <span class="tag-chip">📚 {req.get('subject')}</span>
                                <span class="tag-chip">🎓 {req.get('semester')}</span>
                                <span class="tag-chip">📑 {req.get('type', 'Notes')}</span>
                            </div>
                            <div style="display: flex; gap: 8px; align-items: center;">
                                <span class="{urg_badge}">{urg}</span>
                                <span class="{status_badge}">{status_text}</span>
                            </div>
                        </div>
                        <p style="margin: 12px 0 10px 0; font-size: 14px; color: #E2E8F0; line-height: 1.5;">
                            {req.get('description')}
                        </p>
                        <div style="font-size: 12px; color: #94A3B8; display: flex; justify-content: space-between; flex-wrap: wrap; margin-bottom: 12px;">
                            <span>👤 Requested by: <strong>{req.get('requester', 'Student')}</strong> on {req.get('date', 'Recent')}</span>
                            <span>👍 <strong>{req.get('upvotes', 0)}</strong> student(s) need this</span>
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
                r_subject = st.selectbox("Academic Subject *", ["Python", "Data Structures", "Mathematics", "Computer Science", "Database Systems", "Operating Systems", "Computer Networks", "Web Development", "AI / Machine Learning", "Software Engineering", "Other"], key="post_req_sub")
                r_semester = st.selectbox("Academic Semester *", [f"{i}st Semester" if i == 1 else f"{i}nd Semester" if i == 2 else f"{i}rd Semester" if i == 3 else f"{i}th Semester" for i in range(1, 9)], index=2, key="post_req_sem")

            with r_col2:
                r_type = st.selectbox("Resource Category *", ["Lecture Notes", "Previous Year Question Paper (PYQ)", "Lab Manual", "Reference Book / Summary", "Assignment Solutions", "Syllabus Copy"], key="post_req_type")
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
                <h4 style="margin-top:0; color:#818CF8;">🌟 Top Request Solvers</h4>
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span>🥇 <strong>Rohan Sharma</strong> (CS 5th Sem)</span>
                    <span class="tag-chip">8 Requests Resolved</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span>🥈 <strong>Ananya Mishra</strong> (IT 3rd Sem)</span>
                    <span class="tag-chip">5 Requests Resolved</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span>🥉 <strong>Vikram Patel</strong> (ECE 7th Sem)</span>
                    <span class="tag-chip">4 Requests Resolved</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with hof_col2:
            st.markdown("""
            <div class="glass-card">
                <h4 style="margin-top:0; color:#34D399;">💡 How to Earn Contributor Badges</h4>
                <p style="font-size:13px; color:#CBD5E1; line-height:1.5;">
                    • <strong>Bronze Contributor:</strong> Fulfill 2 community requests.<br>
                    • <strong>Silver Contributor:</strong> Fulfill 5 requests & maintain 4+ upvotes.<br>
                    • <strong>Gold Contributor:</strong> Top 3 contributors of the semester receive campus hackathon credits & certificates.
                </p>
            </div>
            """, unsafe_allow_html=True)


# ==================================================
# 4. 🧰 STUDENT PRODUCTIVITY TOOLS
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
                    <div style="font-size:13px; color:#94A3B8; text-transform:uppercase;">Calculated SGPA</div>
                    <div style="font-size:32px; font-weight:800; color:#818CF8; margin:6px 0;">{calculated_sgpa} / 10.0</div>
                    <span class="tag-chip">Total Credits: {total_credits}</span>
                </div>
                """, unsafe_allow_html=True)
            with res_c2:
                st.markdown(f"""
                <div class="glass-card" style="text-align:center;">
                    <div style="font-size:13px; color:#94A3B8; text-transform:uppercase;">Approximate Percentage</div>
                    <div style="font-size:32px; font-weight:800; color:#34D399; margin:6px 0;">{max(calculated_pct, 0.0)}%</div>
                    <span class="tag-chip">AICTE / UGC Formula</span>
                </div>
                """, unsafe_allow_html=True)
            with res_c3:
                classification = "🥇 First Class with Distinction" if calculated_sgpa >= 8.5 else "🥈 First Class" if calculated_sgpa >= 6.75 else "🥉 Second Class" if calculated_sgpa >= 5.0 else "⚠️ Pass / Reappear"
                st.markdown(f"""
                <div class="glass-card" style="text-align:center;">
                    <div style="font-size:13px; color:#94A3B8; text-transform:uppercase;">Academic Standing</div>
                    <div style="font-size:18px; font-weight:700; color:#FACC15; margin:12px 0;">{classification}</div>
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
                <div class="glass-card" style="border-left: 4px solid #10B981;">
                    <h3 style="color:#34D399; margin:0 0 6px 0;">✅ Safe Attendance Buffer</h3>
                    <p style="font-size:14px; margin:0; color:#E2E8F0;">
                        You can safely miss up to <strong style="font-size:18px; color:#34D399;">{safe_bunks}</strong> upcoming lecture(s) without dropping below {target_pct}%.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            with g_c2:
                st.info("💡 **Attendance Pro Tip:** Save your bunk allowance for crunch exam weeks or project submission crunches!")
        else:
            must_attend = int(((target_ratio * total_held) - total_attended) / (1.0 - target_ratio)) + 1
            with g_c1:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #EF4444;">
                    <h3 style="color:#F87171; margin:0 0 6px 0;">⚠️ Attendance Warning Zone</h3>
                    <p style="font-size:14px; margin:0; color:#E2E8F0;">
                        You must attend the next <strong style="font-size:18px; color:#F87171;">{must_attend}</strong> consecutive lecture(s) without missing any to restore eligibility.
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
                <div style="font-size:13px; color:#94A3B8; text-transform:uppercase;">Focus Interval</div>
                <div style="font-size:48px; font-weight:800; font-family:'Outfit'; color:#818CF8; margin:8px 0;">25:00</div>
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
                <p style="margin:0 0 10px 0; font-size:14px;">Boost focus and block background noise:</p>
                <div style="margin-bottom:8px;">• 🎧 <a href="https://www.youtube.com/watch?v=jfKfPfyJRdk" target="_blank" style="color:#818CF8; font-weight:600;">Lofi Girl Study Stream (YouTube)</a></div>
                <div style="margin-bottom:8px;">• 🌧️ <a href="https://rainymood.com/" target="_blank" style="color:#818CF8; font-weight:600;">Rainymood (Ambient Rain & Thunder)</a></div>
                <div style="margin-bottom:0;">• ☕ <a href="https://coffitivity.com/" target="_blank" style="color:#818CF8; font-weight:600;">Coffitivity (Ambient Cafe Sounds)</a></div>
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
# 5. 🔗 CURATED USEFUL RESOURCES
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
                        <h4 style="margin: 0; color: #818CF8; font-size: 18px;">{item['title']}</h4>
                        <span class="tag-chip">{item['tag']}</span>
                    </div>
                    <p style="font-size: 13px; color: #CBD5E1; margin: 10px 0 14px 0; line-height: 1.4;">{item['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.link_button(f"🚀 Open {item['title']}", item["url"], use_container_width=True)
                st.markdown("<br>", unsafe_allow_html=True)


# ==================================================
# 6. 📢 CAMPUS ANNOUNCEMENTS
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
                
                with st.container():
                    st.markdown(f"""
                    <div class="glass-card" style="border-left: 4px solid {'#EF4444' if pri.lower()=='urgent' else '#F59E0B' if pri.lower()=='important' else '#3B82F6'};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h3 style="margin: 0; font-size: 18px; color: #F8FAFC;">📌 {item.get('title', 'Untitled Notice')}</h3>
                            <span class="{badge_class}">{pri}</span>
                        </div>
                        <p style="margin: 10px 0; font-size: 14px; color: #E2E8F0; line-height: 1.5;">{item.get('message', '')}</p>
                        <div style="font-size: 12px; color: #94A3B8;">
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