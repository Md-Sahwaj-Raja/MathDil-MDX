import re
import base64
import textwrap
from pathlib import Path
from PIL import Image
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import sympy as sp

st.set_page_config(page_title="MathDil MDX", page_icon="∑", layout="wide")

# -------------------- MathDil MDX dark neon styling --------------------
st.markdown("""
<style>
:root { color-scheme: dark; }
.stApp { background: radial-gradient(ellipse at 12% 0%, #0b2447 0%, #050d20 42%, #020617 100%); color: #e8f4ff; }
.block-container { max-width: 1650px; padding-top: 4.25rem; padding-bottom: 2rem; }
header[data-testid="stHeader"] { background: rgba(2,6,23,.88); }
section[data-testid="stSidebar"] { background: linear-gradient(180deg,#07152e,#0b1730); border-right: 1px solid #12385d; }
section[data-testid="stSidebar"] * { color: #e8f4ff; }
.stMarkdown, .stText, p, label, li { color: #d8e8fa; }
h1,h2,h3,h4 { color: #f4f9ff !important; }
.mdx-topbar { display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:.8rem 1.2rem; min-height:82px; padding:1rem 1.3rem; margin:0 0 1rem; border:1px solid #164e78; border-radius:18px; background:linear-gradient(100deg,rgba(3,14,35,.98),rgba(8,32,65,.96)); box-shadow:0 10px 35px rgba(0,0,0,.25); box-sizing:border-box; }
.mdx-brand { display:flex; align-items:center; gap:.9rem; min-width:0; flex:1 1 340px; }
.mdx-logo { font-size:3.4rem; line-height:1; font-weight:700; background:linear-gradient(120deg,#ffd166,#00d9ff); -webkit-background-clip:text; color:transparent; }
.mdx-brand-title { font-size:clamp(1.45rem,2.2vw,2rem); line-height:1.2; font-weight:800; letter-spacing:.02em; overflow-wrap:anywhere; }
.mdx-brand-title span { color:#00d9ff; }
.mdx-subtitle { color:#9fc8e8; letter-spacing:.10em; font-size:clamp(.58rem,.8vw,.76rem); line-height:1.5; margin-top:.28rem; overflow-wrap:anywhere; }
.mdx-hero { position:relative; overflow:hidden; background:linear-gradient(115deg,rgba(5,20,47,.98),rgba(7,48,83,.94) 58%,rgba(10,20,53,.98)); border:1px solid #145b86; padding:1.6rem 1.8rem; border-radius:22px; color:white; margin-bottom:1rem; box-shadow:0 12px 35px rgba(0,0,0,.25); }
.mdx-hero h1 { color:#fff !important; margin:0; font-size:2.4rem; }
.mdx-hero p { color:#b9ddf7; margin:.45rem 0 0; }
.mdx-tagline { font-size:1.2rem; font-weight:800; color:#00d9ff; margin-top:1rem; }
.mdx-card { height:100%; min-height:205px; border-radius:18px; padding:1.1rem; background:linear-gradient(160deg,rgba(8,27,55,.98),rgba(3,12,29,.98)); border:1px solid #174b70; box-shadow:0 8px 26px rgba(0,0,0,.18); }
.mdx-card h3 { margin:.35rem 0 .55rem; font-size:1.18rem; }
.mdx-card p { color:#bad0e6; font-size:.94rem; }
.mdx-cyan { border-color:#00d9ff; } .mdx-gold { border-color:#ffd166; } .mdx-pink { border-color:#ff4d8d; } .mdx-purple { border-color:#a855f7; } .mdx-teal { border-color:#00d6c9; }
.mdx-footer { border:1px solid #145b86; background:rgba(3,17,39,.94); padding:1rem 1.3rem; border-radius:16px; margin:1rem 0 1.4rem; color:#b8d9f2; }
div[data-testid="stMetric"], div[data-testid="stDataFrame"], div[data-testid="stTable"] { background:#08172e; border:1px solid #173a5b; border-radius:12px; }
.stTabs [data-baseweb="tab-list"] { gap:.25rem; background:rgba(3,12,29,.9); border-bottom:1px solid #164e78; }
.stTabs [data-baseweb="tab"] { color:#b9d8f0; border-radius:8px 8px 0 0; }
.stTabs [aria-selected="true"] { color:#00d9ff !important; border-bottom:2px solid #00d9ff !important; }
.stButton > button, .stDownloadButton > button { border:1px solid #087eaa; border-radius:10px; background:linear-gradient(100deg,#07345c,#075985); color:#f5fbff; }
.stButton > button:hover { border-color:#00d9ff; color:white; }
.stLinkButton a { background:linear-gradient(100deg,#ff173d,#d90429) !important; color:#ffffff !important; border:1px solid #ff6b81 !important; border-radius:10px !important; font-weight:800 !important; box-shadow:0 0 14px rgba(255,23,61,.18); }
.stLinkButton a:hover { background:linear-gradient(100deg,#ff3658,#ef1238) !important; border-color:#ffb3bf !important; color:#ffffff !important; }
input, textarea, [data-baseweb="select"] > div { background-color:#0b1b33 !important; color:#eef8ff !important; border-color:#245071 !important; }
[data-testid="stAlert"] { background:#0a2341; border:1px solid #1c547d; }
hr { border-color:#173a5b; }

.mdx-logo-img { width:68px; height:68px; object-fit:cover; border-radius:50%; border:2px solid #d7ad53; box-shadow:0 0 18px rgba(0,217,255,.18); flex:0 0 auto; }
.mdx-home-hero { display:grid; grid-template-columns:minmax(0,1.45fr) minmax(440px,1fr); gap:1.5rem; align-items:stretch; padding:1.7rem; margin-bottom:1rem; border:1px solid #155681; border-radius:22px; background:linear-gradient(110deg,rgba(3,14,35,.98),rgba(6,37,72,.96) 60%,rgba(5,15,37,.98)); box-shadow:0 14px 40px rgba(0,0,0,.25); }
.mdx-home-copy { max-width:760px; font-size:1.06rem; line-height:1.8; color:#c4def5; }
.mdx-home-actions { display:flex; flex-wrap:wrap; align-items:center; gap:.7rem; margin-top:1rem; }
.mdx-founder-panel { display:flex; flex-direction:row; gap:1.15rem; align-items:center; min-width:0; width:100%; min-height:260px; padding:1.2rem; border:1px solid #b58a39; border-radius:18px; background:linear-gradient(145deg,rgba(12,31,58,.98),rgba(3,12,28,.98)); box-sizing:border-box; }
.mdx-founder-photo { display:block; width:clamp(120px,13vw,175px); height:220px; flex:0 0 clamp(120px,13vw,175px); object-fit:cover; object-position:center 20%; border-radius:14px; border:1px solid #00d9ff; box-shadow:0 0 22px rgba(0,217,255,.14); }
.mdx-founder-copy { flex:1 1 auto; min-width:0; overflow-wrap:anywhere; }
.mdx-founder-copy .mdx-kicker { line-height:1.5; margin-bottom:.45rem; }
.mdx-founder-name { font-size:clamp(1.2rem,1.5vw,1.65rem); font-weight:850; color:#fff; line-height:1.25; margin:.2rem 0 .5rem; }
.mdx-founder-role { color:#ffd166; font-weight:750; line-height:1.5; margin:.35rem 0 .6rem; }
.mdx-profile-meta { color:#c6def4; font-size:.94rem; line-height:1.65; }
.mdx-kicker { text-transform:uppercase; letter-spacing:.16em; font-size:.78rem; color:#00d9ff; font-weight:800; }
.mdx-home-title { font-size:clamp(2rem,4vw,3.6rem); line-height:1.08; font-weight:900; margin:.45rem 0 .65rem; color:#f6fbff; }
.mdx-home-title span { color:#00d9ff; }
.mdx-home-copy { font-size:1.04rem; line-height:1.65; color:#c4def5; }
.mdx-founder-panel { display:grid; grid-template-columns:112px minmax(0,1fr); gap:1rem; align-items:center; padding:1rem; border:1px solid #b58a39; border-radius:18px; background:linear-gradient(145deg,rgba(12,31,58,.98),rgba(3,12,28,.98)); }
.mdx-founder-photo { width:112px; height:152px; object-fit:cover; object-position:center 24%; border-radius:12px; border:1px solid #00d9ff; }
.mdx-founder-name { font-size:1.2rem; font-weight:850; color:#fff; line-height:1.3; }
.mdx-founder-role { color:#ffd166; font-weight:700; margin:.35rem 0; }
.mdx-profile-meta { color:#c6def4; font-size:.9rem; line-height:1.5; }
.mdx-youtube { display:inline-flex; align-items:center; gap:.5rem; margin-top:.65rem; padding:.55rem .8rem; border:1px solid #ff4d8d; border-radius:10px; background:rgba(255,77,141,.09); color:#fff !important; text-decoration:none !important; font-weight:750; }
.mdx-youtube:hover { background:rgba(255,77,141,.2); }
.mdx-section-label { color:#e9f5ff; font-size:1.25rem; font-weight:850; margin:1.1rem 0 .7rem; }
@media (max-width: 1050px) { .mdx-home-hero { grid-template-columns:1fr; } .mdx-founder-panel { max-width:100%; } }
@media (max-width: 620px) { .mdx-founder-panel { flex-direction:column; align-items:flex-start; } .mdx-founder-photo { width:150px; height:190px; flex-basis:auto; } }
@media (max-width: 700px) {
  .block-container { padding-top: 3.8rem; padding-left: .8rem; padding-right: .8rem; }
  .mdx-topbar { align-items:flex-start; padding:.9rem 1rem; }
  .mdx-logo { font-size:2.6rem; }
  .mdx-brand { flex-basis:100%; }
  .mdx-topbar > div:last-child { flex-basis:100%; font-size:.82rem; }
  .mdx-hero h1 { font-size:1.7rem; line-height:1.2; }
  .mdx-tagline { font-size:1rem; }
}

/* Home hero and founder panel refinements */
.mdx-home-hero {
  grid-template-columns: minmax(0, 1.45fr) minmax(390px, 1fr);
  gap: 1.35rem;
  align-items: stretch;
}
.mdx-home-intro { min-width: 0; display:flex; flex-direction:column; justify-content:center; }
.mdx-home-title { font-size:clamp(2rem,3.4vw,3.2rem); letter-spacing:-.025em; }
.mdx-founder-panel {
  display:grid;
  grid-template-columns:minmax(125px, 34%) minmax(0, 1fr);
  gap:1.15rem;
  align-items:center;
  min-height:300px;
  padding:1.35rem;
  width:100%;
  box-sizing:border-box;
}
.mdx-founder-photo {
  width:100%;
  height:245px;
  max-width:190px;
  object-fit:cover;
  object-position:center 18%;
}
.mdx-founder-copy { min-width:0; overflow-wrap:normal; word-break:normal; }
.mdx-founder-copy .mdx-kicker { letter-spacing:.12em; font-size:.72rem; margin-bottom:.55rem; }
.mdx-founder-name { font-size:clamp(1.25rem,1.65vw,1.7rem); line-height:1.2; margin:.2rem 0 .55rem; overflow-wrap:normal; }
.mdx-founder-role { font-size:1rem; line-height:1.45; margin:.35rem 0 .65rem; }
.mdx-profile-meta { font-size:.94rem; line-height:1.65; overflow-wrap:normal; }
.mdx-contact-line { color:#b9d9f4; margin-top:.55rem; font-size:.9rem; overflow-wrap:anywhere; }
@media (max-width: 1100px) {
  .mdx-home-hero { grid-template-columns:1fr; }
  .mdx-founder-panel { grid-template-columns:minmax(125px, 180px) minmax(0, 1fr); min-height:240px; }
}
@media (max-width: 620px) {
  .mdx-founder-panel { grid-template-columns:1fr; justify-items:start; }
  .mdx-founder-photo { width:150px; height:185px; }
}

/* Final responsive educator portrait: fill the available card height */
.mdx-portrait-frame { width:100%; height:100%; min-height:390px; overflow:hidden; border-radius:14px; border:1px solid #00d9ff; background:#061226; }
.mdx-portrait-frame img { display:block; width:100%; height:100%; min-height:390px; object-fit:cover; object-position:center 22%; }
.mdx-course-group { border:1px solid #ff4d8d; border-radius:18px; padding:1.15rem; background:linear-gradient(145deg,rgba(35,7,28,.72),rgba(5,14,32,.98)); margin:.6rem 0 1rem; }
.mdx-course-group h3 { margin-top:0; }
.stLinkButton a { background:linear-gradient(100deg,#ff173d,#d90429) !important; color:#fff !important; border:1px solid #ff6b81 !important; }
@media (max-width: 900px) { .mdx-portrait-frame, .mdx-portrait-frame img { min-height:320px; } }
@media (max-width: 620px) { .mdx-portrait-frame, .mdx-portrait-frame img { min-height:280px; } }

</style>""", unsafe_allow_html=True)

# -------------------- App navigation and Home --------------------
APP_DIR = Path(__file__).resolve().parent
LOGO_PATH = APP_DIR / "MathDil logo.jpg"
PROFILE_PATH = APP_DIR / "exist.jpg"
YOUTUBE_URL = "https://www.youtube.com/@Mathdil"
CONTACT_EMAIL = ""  # Add the email address here when provided

def load_valid_image(path):
    """Return a validated RGB image, or None if the file is missing/corrupt."""
    if not path.is_file():
        return None
    try:
        with Image.open(path) as img:
            img.load()  # Force decoding here so Streamlit doesn't crash later.
            return img.convert("RGB").copy()
    except Exception:
        return None


def show_local_image(path, *, width=None, use_container_width=False):
    """Display a local image safely; show a useful warning if invalid."""
    image = load_valid_image(path)
    if image is None:
        st.warning(
            f"Image '{path.name}' missing or unreadable. "
            "Check that the image is in the same folder as app.py and that its exact filename and extension match the configured path."
        )
        return False
    st.image(image, width=width, use_container_width=use_container_width)
    return True


def show_portrait_fill(path):
    """Display the real local portrait cropped to fill a tall profile frame."""
    image = load_valid_image(path)
    if image is None:
        st.warning(f"Unable to load the image '{path.name}'. Please place the file in the same folder as app.py.")
        return False
    from io import BytesIO
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=92)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    st.markdown(
        '<div class="mdx-portrait-frame"><img alt="Md Sahwaj Raja profile photo" '
        f'src="data:image/jpeg;base64,{encoded}"></div>',
        unsafe_allow_html=True,
    )
    return True

if "mdx_page" not in st.session_state:
    st.session_state.mdx_page = "Home"

# Render local images with Streamlit's native image component (more reliable than data-URI HTML).
head_logo, head_brand, head_tag = st.columns([0.09, 0.62, 0.29], vertical_alignment="center")
with head_logo:
    if not show_local_image(LOGO_PATH, width=68):
        st.markdown('<div class="mdx-logo">∞</div>', unsafe_allow_html=True)
with head_brand:
    st.markdown('<div class="mdx-brand-title">MathDil <span>MDX</span></div><div class="mdx-subtitle">MATHEMATICS DISCOVERY EXPERIENCE</div>', unsafe_allow_html=True)
with head_tag:
    st.markdown('<div style="text-align:right;color:#c7e8ff;font-weight:700;line-height:1.5;padding-top:.6rem">Explore · Learn · Practise · Master</div>', unsafe_allow_html=True)
st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
nav_cols = st.columns([.8, 1.2, .8, 1.15, .8, .8, .9])
nav_items = [("⌂ Home", "Home"), ("📚 Courses", "Courses"), ("🎯 Test & Learn", "Test & Learn"), ("📈 Graph Studio", "Graph Studio"), ("📊 Progress", "Progress"), ("🛠 Tools", "Tools"), ("👤 My Profile", "My Profile")]
for col, (label, page_name) in zip(nav_cols, nav_items):
    with col:
        if st.button(label, key=f"nav_{page_name}", use_container_width=True, type="primary" if st.session_state.mdx_page == page_name else "secondary"):
            st.session_state.mdx_page = page_name
            st.rerun()

if st.session_state.mdx_page == "Home":
    # Build the hero with Streamlit columns/containers. Do not open an HTML div
    # around Streamlit widgets: Streamlit renders each widget separately.
    with st.container(border=True):
        intro_col, profile_col = st.columns([1.55, 1], gap="large", vertical_alignment="center")

        with intro_col:
            st.markdown('<div class="mdx-kicker">YOUR PERSONAL MATHEMATICS LEARNING SPACE</div>', unsafe_allow_html=True)
            st.markdown('<div class="mdx-home-title">Mathematics, <span>Made Understandable</span></div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:1.15rem;color:#ffd166;font-weight:800;letter-spacing:.04em">Explore · Learn · Practise · Master</div>', unsafe_allow_html=True)
            st.markdown(
                '<p class="mdx-home-copy">Build strong mathematical intuition—not just formula memory. '
                'Learn concepts step by step, practise with purpose, understand why mistakes happen, '
                'and develop the confidence to solve unfamiliar problems across school, university, '
                'and competitive exams.</p>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div style="font-size:1rem;color:#00d9ff;font-weight:800;line-height:1.6;margin-top:.8rem">'
                'Every mistake is a clue. Every concept can become clear.</div>',
                unsafe_allow_html=True,
            )
            st.link_button("▶ Visit MathDil on YouTube ↗", YOUTUBE_URL)
            st.caption("Concepts · Practice · Visual Learning")

        with profile_col:
            with st.container(border=True):
                st.markdown('<div class="mdx-kicker">THE EDUCATOR BEHIND MATHDIL</div>', unsafe_allow_html=True)
                pic_col, text_col = st.columns([0.9, 1.1], gap="medium", vertical_alignment="center")
                with pic_col:
                    show_portrait_fill(PROFILE_PATH)
                with text_col:
                    st.markdown('<div class="mdx-founder-name" style="white-space:nowrap;font-size:clamp(1rem,1.45vw,1.55rem);letter-spacing:-.025em">Md Sahwaj Raja</div>', unsafe_allow_html=True)
                    st.markdown('<div class="mdx-founder-role">Founder · Mathematics Educator</div>', unsafe_allow_html=True)
                    st.markdown("**M.Sc. Applied Mathematics**  \nNIT Warangal · 2025–2027")
                    st.write(
                        "My mission is to make mathematics clearer through intuitive explanations, "
                        "visual learning, and thoughtful practice—helping learners understand the why, "
                        "not just memorise the how."
                    )
                    st.link_button("▶ YouTube · @Mathdil ↗", YOUTUBE_URL, use_container_width=True)

    st.markdown('<div class="mdx-section-label">Choose your workspace</div>', unsafe_allow_html=True)
    home_cols = st.columns(4)
    home_cards = [
        ("📚", "Courses", "Explore mathematics courses and preparation tracks.", "mdx-gold", "Courses"),
        ("🎯", "Test & Diagnose", "Find knowledge gaps and practise the skills you need.", "mdx-pink", "Test & Learn"),
        ("📈", "Graph Studio", "Open your separate graph workspace with existing plotting and analysis tools.", "mdx-cyan", "Graph Studio"),
        ("📊", "Progress", "Track your practice and learning progress over time.", "mdx-teal", "Progress"),
    ]
    for col, (icon, title, desc, accent, page_name) in zip(home_cols, home_cards):
        with col:
            st.markdown(
                f'<div class="mdx-card {accent}"><div style="font-size:2rem">{icon}</div>'
                f'<h3>{title}</h3><p>{desc}</p></div>',
                unsafe_allow_html=True,
            )
            if st.button("Open " + title + " →", key=f"home_open_{page_name}", use_container_width=True):
                st.session_state.mdx_page = page_name
                st.rerun()
    st.markdown(
        '<div class="mdx-footer"><b style="color:#00d9ff">Built for Mathematics Learners</b>　'
        'Clear Concepts　│　Adaptive Practice　│　Visual Learning　│　Mastery Checks</div>',
        unsafe_allow_html=True,
    )
elif st.session_state.mdx_page == "My Profile":
    st.markdown("## 👨‍🏫 The Educator Behind MathDil")
    profile_cols = st.columns([1, 2])
    with profile_cols[0]:
        show_portrait_fill(PROFILE_PATH)
    with profile_cols[1]:
        st.markdown('<div style="font-size:clamp(1.5rem,3vw,2.3rem);font-weight:900;white-space:nowrap;letter-spacing:-.025em">Md Sahwaj Raja</div>', unsafe_allow_html=True)
        st.markdown("### Founder · Mathematics Educator · MathDil MDX")
        st.write("M.Sc. Applied Mathematics, NIT Warangal (2025–2027).")
        st.write("Building a learning experience that helps students understand mathematics, identify the reason behind mistakes, and improve through targeted practice.")
        st.link_button("▶ Visit my YouTube channel — @Mathdil", YOUTUBE_URL, use_container_width=False)
    if st.button("← Back to Home", key="profile_back_home"):
        st.session_state.mdx_page = "Home"
        st.rerun()
elif st.session_state.mdx_page == "Courses":
    st.markdown("## 📚 Courses")
    st.markdown("Choose a preparation path. IIT JEE Main and IIT JEE Advanced are grouped under IIT JEE; CSIR-NET and GATE have their own tracks.")

    st.markdown('<div class="mdx-section-label">🎯 IIT JEE</div>', unsafe_allow_html=True)
    st.markdown('<div class="mdx-course-group"><h3>Prepare for the IIT Joint Entrance Examination</h3><p>Build concepts, sharpen problem-solving, and practise at the level required for your target exam.</p></div>', unsafe_allow_html=True)
    jee_cols = st.columns(2, gap="large")
    jee_cards = [
        ("🎯", "IIT JEE Main", "Strengthen fundamentals, speed, accuracy, and question-selection strategy.", "mdx-cyan"),
        ("🚀", "IIT JEE Advanced", "Develop deeper reasoning, multi-step solutions, and advanced applications.", "mdx-gold"),
    ]
    for col, (icon, title, desc, accent) in zip(jee_cols, jee_cards):
        with col:
            st.markdown(f'<div class="mdx-card {accent}" style="min-height:170px"><div style="font-size:2rem">{icon}</div><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
            if st.button(f"Open {title} →", key=f"course_{title}", use_container_width=True):
                st.session_state["selected_course"] = title
                st.session_state.mdx_page = "Course Details"
                st.rerun()

        jam_col = st.container()

    with jam_col:
        st.markdown(
            '<div class="mdx-card mdx-cyan" style="min-height:175px">'
            '<div style="font-size:2rem">🎓</div><h3>IIT JAM Mathematics</h3>'
            '<p>Explore Vector Space, Subspace, and Matrices with topic-wise lectures and study materials.</p></div>',
            unsafe_allow_html=True,
        )

    if st.button(
        "Open IIT JAM Mathematics →",
        key="course_iit_jam",
        use_container_width=True,
        type="primary",
    ):
        st.session_state["selected_course"] = "IIT JAM Mathematics"
        st.session_state["selected_jam_topic"] = None
        st.session_state["selected_jam_section"] = "Lectures"
        st.session_state["jam_stage"] = "roadmap"
        st.session_state.mdx_page = "Course Details"
        st.rerun()

    st.markdown('<div class="mdx-section-label">📘 Other Competitive Mathematics Exams</div>', unsafe_allow_html=True)
    other_cols = st.columns(2, gap="large")
    other_cards = [
        ("📘", "CSIR-UGC NET Mathematics", "Prepare core mathematical concepts and exam-oriented problem solving.", "mdx-pink"),
        ("📐", "GATE Mathematics", "Strengthen undergraduate mathematics and practise topic by topic.", "mdx-teal"),
    ]
    for col, (icon, title, desc, accent) in zip(other_cols, other_cards):
        with col:
            st.markdown(f'<div class="mdx-card" style="min-height:170px;border-color:{"#ff4d8d" if accent == "mdx-pink" else "#00d6c9"}"><div style="font-size:2rem">{icon}</div><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
            if st.button(f"Open {title} →", key=f"course_{title}", use_container_width=True):
                st.session_state["selected_course"] = title
                st.session_state.mdx_page = "Course Details"
                st.rerun()
    if st.button("← Back to Home", key="courses_back_home"):
        st.session_state.mdx_page = "Home"
        st.rerun()
elif st.session_state.mdx_page == "Course Details":
    course = st.session_state.get("selected_course", "Mathematics")
    st.markdown(f"## 📚 {course}")

    if course == "IIT JAM Mathematics":
        jam_topics = ["Vector Space", "Subspace", "Matrices"]
        topic_icons = {"Vector Space": "🧭", "Subspace": "🧩", "Matrices": "▦"}

        # Keep the roadmap alongside the three topic cards on the same page.
        roadmap_col, topics_col = st.columns([1.05, 3], gap="large")
        with roadmap_col:
            st.markdown(
                '<div class="mdx-card mdx-cyan" style="min-height:190px;margin:.6rem 0 1rem">'
                '<div style="font-size:2.2rem">🗺️</div><h2>Roadmap to Linear Algebra</h2>'
                '<p>Vector Space → Subspace → Matrices. Follow this learning path for IIT JAM Mathematics.</p></div>',
                unsafe_allow_html=True,
            )
            if st.button("🗺️ Roadmap overview", key="open_linear_algebra_roadmap", use_container_width=True):
                st.session_state.selected_jam_topic = None
                st.session_state.selected_jam_section = "Lectures"
                st.info("Roadmap: first Vector Space, then Subspace, and finally Matrices. Topic cards are alongside this roadmap.")

        with topics_col:
            st.markdown('<div class="mdx-section-label">Choose a topic to open its contents</div>', unsafe_allow_html=True)
            topic_cols = st.columns(3, gap="medium")
            for col, topic_name in zip(topic_cols, jam_topics):
                with col:
                    is_selected = st.session_state.get("selected_jam_topic") == topic_name
                    st.markdown(
                        f'<div class="mdx-card mdx-cyan" style="min-height:105px;text-align:center;padding:.8rem">'
                        f'<div style="font-size:1.8rem">{topic_icons[topic_name]}</div><h3 style="margin:.35rem 0">{topic_name}</h3>'
                        f'<p style="margin:0">Click to open</p></div>', unsafe_allow_html=True
                    )
                    if st.button(
                        f"Open {topic_name} →", key=f"jam_topic_{topic_name}",
                        use_container_width=True, type="primary" if is_selected else "secondary",
                    ):
                        st.session_state.selected_jam_topic = topic_name
                        st.session_state.selected_jam_section = "Lectures"
                        st.rerun()
        topic = st.session_state.get("selected_jam_topic")
        if topic not in jam_topics:
            st.markdown(
                """
                <div style="background:linear-gradient(110deg,#0B2447,#123C69,#075985);
                            border:1px solid #00D9FF;border-left:5px solid #FFD166;
                            border-radius:12px;padding:20px 24px;margin:18px 0;">
                  <div style="color:#FFD166;font-size:12px;font-weight:800;letter-spacing:2px;margin-bottom:8px;">
                    ✦ YOUR LEARNING JOURNEY
                  </div>
                  <div style="color:white;font-size:19px;font-weight:750;margin-bottom:8px;">
                    🎯 Your Journey to Linear Algebra Mastery Starts Here
                  </div>
                  <div style="color:#D7E9FF;font-size:15px;line-height:1.8;">
                    Select a topic to explore its lectures and study materials.
                    Learn step by step, strengthen your concepts, and master Linear Algebra with MathDil MDX.
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="mdx-course-group" style="border-color:#00d9ff;background:linear-gradient(145deg,rgba(3,55,78,.62),rgba(5,14,32,.98))">'
                f'<h3>{topic}</h3><p>IIT JAM Mathematics · Topic-wise learning workspace</p></div>',
                unsafe_allow_html=True,
            )
            section = st.radio(
                "Choose learning section",
                ["Lectures", "Study Materials"],
                horizontal=True,
                key="jam_section_radio",
                index=0 if st.session_state.get("selected_jam_section", "Lectures") == "Lectures" else 1,
            )
            st.session_state.selected_jam_section = section

            if section == "Lectures":
                st.markdown("### 🎥 Lectures")
                st.caption(f"Video lectures for **{topic}** will appear here as they become available.")
                video_url = st.text_input(
                    "YouTube lecture URL (optional)",
                    key=f"lecture_url_{topic}",
                    placeholder="https://www.youtube.com/watch?v=...",
                )
                if video_url.strip():
                    if "youtube.com" in video_url or "youtu.be" in video_url:
                        st.video(video_url.strip())
                    else:
                        st.warning("Please enter a valid YouTube video URL.")
                else:
                    st.info("No lecture has been added for this topic yet. Please check back soon for updates.")

            else:
                st.markdown("### 📄 Study Materials")
            st.caption("Access and download the study materials provided by MathDil for this topic.")
            materials_root = APP_DIR / "study_materials" / "IIT_JAM_Mathematics"
            topic_folder_names = {
                "Vector Space": "Vector_Space",
                "Subspace": "Subspace",
                "Matrices": "Matrices",
            }
            topic_folder = materials_root / topic_folder_names[topic]
            topic_folder.mkdir(parents=True, exist_ok=True)

            # Student-facing area: read-only access. No upload, rename, replace, move, or delete controls.
            pdf_paths = sorted(topic_folder.glob("*.pdf"), key=lambda q: q.name.lower())
            st.markdown("#### 📚 Available Study Materials")
            if not pdf_paths:
                st.info("No study materials are available for this topic yet. Please check back soon for updates.")
            else:
                chosen_name = st.selectbox(
                    "Choose a PDF",
                    [q.name for q in pdf_paths],
                    key=f"view_pdf_select_{topic}",
                )
                selected_pdf = topic_folder / chosen_name
                pdf_data = selected_pdf.read_bytes()
                st.write(f"**📄 {selected_pdf.name}**")
                st.caption(f"File size: {pdf_data.__len__() / 1024:.1f} KB")
                st.download_button(
                    "⬇️ Download PDF",
                    data=pdf_data,
                    file_name=selected_pdf.name,
                    mime="application/pdf",
                    key=f"download_study_pdf_{topic}_{selected_pdf.name}",
                    use_container_width=True,
                )
                if len(pdf_data) <= 8 * 1024 * 1024:
                    if st.checkbox("Preview PDF", key=f"preview_pdf_{topic}_{selected_pdf.name}"):
                        encoded_pdf = base64.b64encode(pdf_data).decode("ascii")
                        st.markdown(
                            f'<iframe src="data:application/pdf;base64,{encoded_pdf}" '
                            'width="100%" height="560" style="border:1px solid #164e78;'
                            'border-radius:12px;background:white"></iframe>',
                            unsafe_allow_html=True,
                        )
                else:
                    st.info("This PDF is large, so preview is disabled to keep the app responsive. Please download it to view.")

        st.markdown("---")
        if st.button("← Back to Courses", key="course_details_back"):
            st.session_state.mdx_page = "Courses"
            st.rerun()
    else:
        st.info("This course workspace is being built step by step. The next stage will add the topic list, lectures, study materials, diagnostic questions, and targeted practice. Graph Studio remains a separate workspace.")
        if st.button("← Back to Courses", key="course_details_back"):
            st.session_state.mdx_page = "Courses"
            st.rerun()
elif st.session_state.mdx_page == "Tools":
    st.markdown("## 🛠 Mathematical Tools")
    st.markdown("Explore the supported function syntax used in MathDil MDX Graph Studio.")
    with st.expander("📘 Function Syntax Guide — click to view instructions", expanded=False):
        st.markdown("""
        <div style="padding:1rem 1.2rem;border:1px solid #087ea4;border-radius:16px;background:linear-gradient(120deg,rgba(4,45,78,.92),rgba(38,20,79,.88));margin:.5rem 0 1rem">
          <div style="font-size:1.25rem;font-weight:800;color:#67e8f9">📘 Function Syntax Guide</div>
          <div style="color:#d7eaff">Use <code>**</code> for powers and <code>*</code> for multiplication. You can use <code>^</code> for powers too; the graph parser converts it to <code>**</code>. Trigonometric functions use radians.</div>
        </div>
        """, unsafe_allow_html=True)
        guide_tabs = st.tabs(["Algebra", "Trigonometry", "Exponential & Log", "Constants & Parameters", "Implicit Equations"])
        with guide_tabs[0]:
            st.table([
                {"Mathematics": "x²", "Enter this": "x**2"},
                {"Mathematics": "x³", "Enter this": "x**3"},
                {"Mathematics": "x⁴ + 2x² − 1", "Enter this": "x**4 + 2*x**2 - 1"},
                {"Mathematics": "Square root of x", "Enter this": "sqrt(x)"},
                {"Mathematics": "Absolute value |x|", "Enter this": "abs(x)"},
                {"Mathematics": "1 divided by x", "Enter this": "1/x"},
                {"Mathematics": "(x² − 1)/(x + 1)", "Enter this": "(x**2 - 1)/(x + 1)"},
            ])
        with guide_tabs[1]:
            st.table([
                {"Mathematics": "Sine", "Enter this": "sin(x)"},
                {"Mathematics": "Cosine", "Enter this": "cos(x)"},
                {"Mathematics": "Tangent", "Enter this": "tan(x)"},
                {"Mathematics": "Inverse sine", "Enter this": "asin(x)"},
                {"Mathematics": "Inverse cosine", "Enter this": "acos(x)"},
                {"Mathematics": "Inverse tangent", "Enter this": "atan(x)"},
                {"Mathematics": "Hyperbolic functions", "Enter this": "sinh(x), cosh(x), tanh(x)"},
            ])
        with guide_tabs[2]:
            st.table([
                {"Mathematics": "eˣ", "Enter this": "exp(x)"},
                {"Mathematics": "Natural logarithm ln(x)", "Enter this": "log(x) or ln(x)"},
                {"Mathematics": "e to the power −x²", "Enter this": "exp(-x**2)"},
                {"Mathematics": "x multiplied by e⁻ˣ", "Enter this": "x*exp(-x)"},
            ])
        with guide_tabs[3]:
            st.table([
                {"Symbol": "pi", "Meaning": "π (pi)"},
                {"Symbol": "E", "Meaning": "Euler's number e"},
                {"Symbol": "a, b", "Meaning": "Adjustable parameters in Graph Studio, when enabled"},
            ])
        with guide_tabs[4]:
            st.table([
                {"Curve": "Circle", "Enter this equation": "x**2 + y**2 = 25"},
                {"Curve": "Ellipse", "Enter this equation": "x**2/9 + y**2/4 = 1"},
                {"Curve": "Hyperbola", "Enter this equation": "x**2 - y**2 = 1"},
                {"Curve": "Straight line", "Enter this equation": "y = 2*x + 1"},
            ])
            st.caption("Implicit equations use both x and y. Write multiplication explicitly with * where needed.")
        st.markdown("### Try these examples")
        st.code("""x**2 - 4
    x**3 - 3*x
    sin(x) + cos(x)
    exp(-x**2)
    (x**2 - 1)/(x + 1)
    x**2 + y**2 = 25""", language="text")
        st.info("This guide lists functions currently supported by the Graph Studio parser. Other functions may need to be added to the parser before they can be plotted.")
    if st.button("← Back to Home", key="back_home_tools"):
        st.session_state.mdx_page = "Home"
        st.rerun()
elif st.session_state.mdx_page in ("Test & Learn", "Progress"):
    st.markdown(f"## {st.session_state.mdx_page}")
    st.info("This section will be built step by step based on your instructions. The existing Graph Studio is kept separate.")
    if st.button("← Back to Home", key="back_home"):
        st.session_state.mdx_page = "Home"
        st.rerun()

if st.session_state.mdx_page == "Graph Studio":
    x, y = sp.symbols("x y", real=True)
    a_sym, b_sym = sp.symbols("a b", real=True)
    COLORS = ["#00D9FF", "#FF4D8D", "#FFD166", "#A855F7", "#00D6C9", "#60A5FA", "#FB923C", "#E879F9", "#34D399", "#F472B6"]

    # -------------------- Core helpers --------------------
    def parse_expr(text):
        """Parse explicit y=f(x) expressions or implicit equations F(x,y)=0."""
        text = text.strip().replace("^", "**")
        if not text:
            raise ValueError("Please enter a function or equation.")
        # An equation is stored as left side minus right side, so its graph is F(x,y)=0.
        if text.count("=") == 1:
            left, right = text.split("=")
            text = f"({left.strip()}) - ({right.strip()})"
        elif "=" in text:
            raise ValueError("Enter only one equals sign, e.g. (3*x-1)^2+(3*y)^2=a^2+b^2")
        text = re.sub(r"(?<=\d)\s*(?=[xyab]\b)", "*", text)
        text = re.sub(r"(?<=\d)\s*(?=\()", "*", text)
        text = re.sub(r"(?<=\))\s*(?=[xyab]\b|\d|\()", "*", text)
        aval = float(st.session_state.get("parameter_a", 2.0))
        bval = float(st.session_state.get("parameter_b", 1.0))
        allowed = {"x": x, "y": y, "a": sp.Float(aval), "b": sp.Float(bval),
                   "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
                   "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
                   "sqrt": sp.sqrt, "exp": sp.exp, "log": sp.log, "ln": sp.log,
                   "abs": sp.Abs, "pi": sp.pi, "E": sp.E, "sinh": sp.sinh,
                   "cosh": sp.cosh, "tanh": sp.tanh}
        return sp.sympify(text, locals=allowed)

    def numeric_y(expr, xs):
        fn = sp.lambdify(x, expr, modules=["numpy"])
        with np.errstate(all="ignore"):
            vals = fn(xs)
        if np.isscalar(vals):
            vals = np.full(np.shape(xs), vals)
        vals = np.asarray(vals)
        if np.iscomplexobj(vals):
            vals = np.where(np.abs(vals.imag) < 1e-8, vals.real, np.nan)
        vals = np.asarray(vals, dtype=float)
        vals[~np.isfinite(vals)] = np.nan
        vals[np.abs(vals) > 1e7] = np.nan
        return vals

    def safe_value(expr, at):
        try:
            value = sp.N(expr.subs(x, at))
            if value.is_real and value.is_finite:
                return float(value)
        except Exception:
            pass
        return None

    def fmt_num(v):
        return f"{float(v):.8g}"

    def make_graph(items, xlo, xhi, ylo=None, yhi=None, height=500, title=None):
        fig = go.Figure()
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(3,12,29,0.96)", font=dict(color="#D8E8FA"), legend=dict(bgcolor="rgba(3,12,29,0.7)"), margin=dict(l=25,r=20,t=45,b=30))
        xs = np.linspace(float(xlo), float(xhi), 1200)
        for item in items:
            try:
                item_expr = item["expr"]
                if y in item_expr.free_symbols:
                    # Implicit curve: evaluate F(x,y) on a grid and draw the zero contour.
                    ys_grid = np.linspace(float(ylo if ylo is not None else -10), float(yhi if yhi is not None else 10), 500)
                    X, Y = np.meshgrid(xs, ys_grid)
                    fn2 = sp.lambdify((x, y), item_expr, modules=["numpy"])
                    with np.errstate(all="ignore"):
                        Z = np.asarray(fn2(X, Y), dtype=float)
                    fig.add_trace(go.Contour(
                        x=xs, y=ys_grid, z=Z, contours=dict(start=0, end=0, size=1, coloring="none"),
                        line=dict(color=item.get("color", COLORS[0]), width=3),
                        showscale=False, name=item["label"], hoverinfo="skip"
                    ))
                else:
                    ys = numeric_y(item_expr, xs)
                    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name=item["label"],
                        line=dict(color=item.get("color", COLORS[0]), width=3), connectgaps=False,
                        hovertemplate=f"<b>{item['label']}</b><br>x=%{{x:.4f}}<br>y=%{{y:.4f}}<extra></extra>"))
            except Exception:
                continue
        fig.add_hline(y=0, line_color="#475569", line_width=1)
        fig.add_vline(x=0, line_color="#475569", line_width=1)
        yrange = [ylo, yhi] if ylo is not None and yhi is not None and ylo < yhi else None
        grid_on = st.session_state.get("graph_show_grid", True)
        bg_choice = st.session_state.get("graph_background_theme", "Current navy")
        is_white = bg_choice == "White"
        plot_bg = "#FFFFFF" if is_white else ("#000000" if bg_choice == "Pure black" else "rgba(5,16,38,0.98)")
        grid_color = "rgba(71,85,105,0.22)" if is_white else "rgba(103,232,249,0.22)"
        axis_text = "#172033" if is_white else "#E6F4FF"
        axis_line = "#64748B" if is_white else "#54718F"
        zero_line = "#64748B" if is_white else "#FFD166"
        fig.update_layout(template="plotly_white" if is_white else "plotly_dark", height=height, title=title,
            margin=dict(l=15, r=15, t=45 if title else 15, b=15),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=plot_bg,
            font=dict(color=axis_text), hovermode="closest",
            xaxis=dict(title="x", range=[xlo, xhi], showgrid=grid_on,
                       gridcolor=grid_color, zeroline=True,
                       zerolinecolor=zero_line, zerolinewidth=1.5, linecolor=axis_line),
            yaxis=dict(title="y", range=yrange, showgrid=grid_on,
                       gridcolor=grid_color, zeroline=True,
                       zerolinecolor=zero_line, zerolinewidth=1.5, linecolor=axis_line),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                        bgcolor="rgba(255,255,255,0.78)" if is_white else "rgba(3,12,29,0.72)"))
        return fig

    def make_graph_3d(items, xlo, xhi, ylo, yhi, height=570):
        """Plot entered expressions as surfaces z=f(x,y) in 3D mode."""
        fig = go.Figure()
        grid_on = st.session_state.get("graph_show_grid", True)
        bg_choice = st.session_state.get("graph_background_theme", "Current navy")
        is_white = bg_choice == "White"
        bg = "#FFFFFF" if is_white else ("#000000" if bg_choice == "Pure black" else "#051026")
        grid_color = "rgba(71,85,105,.28)" if is_white else "rgba(103,232,249,.28)"
        font_color = "#172033" if is_white else "#E6F4FF"
        xs = np.linspace(float(xlo), float(xhi), 100)
        ys = np.linspace(float(ylo), float(yhi), 100)
        X, Y = np.meshgrid(xs, ys)
        for item in items:
            try:
                fn = sp.lambdify((x, y), item["expr"], modules=["numpy"])
                with np.errstate(all="ignore"):
                    Z = np.asarray(fn(X, Y))
                if np.isscalar(Z):
                    Z = np.full(X.shape, Z)
                if np.iscomplexobj(Z):
                    Z = np.where(np.abs(Z.imag) < 1e-8, Z.real, np.nan)
                Z = np.asarray(Z, dtype=float)
                Z[~np.isfinite(Z)] = np.nan
                Z[np.abs(Z) > 1e6] = np.nan
                fig.add_trace(go.Surface(x=X, y=Y, z=Z, name=item["label"],
                    showscale=False, opacity=0.92, colorscale=[[0, item.get("color", COLORS[0])], [1, "#f8fafc"]],
                    hovertemplate="x=%{x:.3f}<br>y=%{y:.3f}<br>z=%{z:.3f}<extra></extra>"))
            except Exception:
                continue
        fig.update_layout(template="plotly_white" if is_white else "plotly_dark", height=height,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=bg,
            font=dict(color=font_color), margin=dict(l=0,r=0,t=35,b=0),
            scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z",
                xaxis=dict(showbackground=True, showgrid=grid_on, gridcolor=grid_color, backgroundcolor=bg),
                yaxis=dict(showbackground=True, showgrid=grid_on, gridcolor=grid_color, backgroundcolor=bg),
                zaxis=dict(showbackground=True, showgrid=grid_on, gridcolor=grid_color, backgroundcolor=bg),
                bgcolor=bg))
        return fig

    def real_roots_in_window(expr, lo, hi):
        roots = []
        try:
            solset = sp.solveset(sp.Eq(expr, 0), x, domain=sp.Interval(lo, hi))
            if isinstance(solset, sp.FiniteSet):
                for r in solset:
                    rn = sp.N(r)
                    if rn.is_real and rn.is_finite:
                        rv = float(rn)
                        if lo - 1e-8 <= rv <= hi + 1e-8:
                            roots.append(rv)
        except Exception:
            pass
        # Numeric sign-change scan catches many additional roots. Tangential roots can be missed.
        try:
            from scipy.optimize import brentq
            fn = sp.lambdify(x, expr, modules=["numpy"])
            xs = np.linspace(lo, hi, 2500)
            with np.errstate(all="ignore"):
                vals = fn(xs)
            if np.isscalar(vals): vals = np.full(xs.shape, vals)
            vals = np.asarray(vals)
            if np.iscomplexobj(vals): vals = np.where(np.abs(vals.imag) < 1e-8, vals.real, np.nan)
            vals = np.asarray(vals, dtype=float)
            for i in range(len(xs)-1):
                a, b, fa, fb = xs[i], xs[i+1], vals[i], vals[i+1]
                if not (np.isfinite(fa) and np.isfinite(fb)): continue
                if abs(fa) < 1e-8: roots.append(float(a))
                elif fa * fb < 0:
                    try: roots.append(float(brentq(lambda z: float(sp.N(expr.subs(x, z))), a, b)))
                    except Exception: pass
            if np.isfinite(vals[-1]) and abs(vals[-1]) < 1e-8: roots.append(float(xs[-1]))
        except Exception:
            pass
        roots.sort()
        unique = []
        for r in roots:
            if not unique or abs(r - unique[-1]) > 1e-4:
                unique.append(r)
        return unique

    # -------------------- Multi-function workspace --------------------
    if "mdx_functions" not in st.session_state:
        st.session_state.mdx_functions = [{"text": "x**2 - 4", "visible": True}]

    st.session_state.setdefault("graph_dimension", "2D")
    st.session_state.setdefault("graph_background_theme", "Current navy")
    st.session_state.setdefault("graph_show_grid", True)
    with st.sidebar:
        st.header("⚙️ Graph settings")
        x_min = st.number_input("x minimum", value=-10.0, step=1.0, key="x_min")
        x_max = st.number_input("x maximum", value=10.0, step=1.0, key="x_max")
        y_min = st.number_input("y minimum", value=-10.0, step=1.0, key="y_min")
        y_max = st.number_input("y maximum", value=10.0, step=1.0, key="y_max")
        st.caption("Use x**2 or x^2. Trigonometric functions use radians.")
        st.caption("Explicit example: x**2 - 4")
        st.caption("Implicit example: (3*x-1)^2+(3*y)^2=a^2+b^2")
        st.number_input("Parameter a", value=2.0, step=0.5, key="parameter_a")
        st.number_input("Parameter b", value=1.0, step=0.5, key="parameter_b")
        st.caption("For implicit equations, use x and y. Parameters a and b use the values above.")
    if x_min >= x_max or y_min >= y_max:
        st.error("Minimum values must be smaller than maximum values.")
        st.stop()

    st.markdown("""
    <div style="padding:1rem 1.2rem;border:1px solid #0e7490;border-radius:16px;background:linear-gradient(115deg,rgba(3,48,77,.96),rgba(48,22,84,.94) 55%,rgba(83,29,67,.9));margin:.2rem 0 1rem">
      <div style="font-size:1.45rem;font-weight:850;color:#67e8f9">📈 MathDil Graph Studio</div>
      <div style="color:#e2e8f0">Plot functions in vivid colours, compare curves, and toggle the coordinate grid from Graph settings.</div>
    </div>
    """, unsafe_allow_html=True)
    st.subheader("🧮 Function workspace")
    st.caption("Add multiple functions. All visible functions appear together in Graph Studio; choose one function below for detailed analysis.")

    # One expander/card per function; each has a visibility toggle and remove button.
    for i in range(len(st.session_state.mdx_functions)):
        entry = st.session_state.mdx_functions[i]
        c1, c2, c3, c4 = st.columns([5, 1.5, 1, 1.15])
        with c1:
            entry["text"] = st.text_input(
                f"Function f{i+1}(x) / Equation F{i+1}(x,y)=0",
                value=entry["text"], key=f"function_text_{i}",
                help="Explicit: x**2 - 4 | Implicit: (3*x-1)**2+(3*y)**2=5"
            )
        with c2:
            entry["visible"] = st.checkbox("Show on graph", value=entry["visible"], key=f"function_visible_{i}")
        with c3:
            st.write("")
            if st.button("↻ Refresh", key=f"refresh_function_{i}", help="Recalculate this function and refresh the app"):
                st.rerun()
        with c4:
            st.write("")
            if st.button("✖ Remove", key=f"remove_function_{i}", disabled=len(st.session_state.mdx_functions) == 1):
                st.session_state.mdx_functions.pop(i)
                st.rerun()

    add_col, clear_col, refresh_all_col, active_col = st.columns([1.3, 1.2, 1.65, 2.5])
    with add_col:
        if st.button("➕ Add function", type="primary", use_container_width=True):
            st.session_state.mdx_functions.append({"text": "sin(x)", "visible": True})
            st.rerun()
    with clear_col:
        if st.button("↺ Reset functions", use_container_width=True):
            st.session_state.mdx_functions = [{"text": "x**2 - 4", "visible": True}]
            st.rerun()
    with refresh_all_col:
        if st.button("🔄 Refresh all", use_container_width=True, help="Re-parse all functions and refresh graphs and analysis results"):
            st.rerun()

    parsed_functions = []
    parse_errors = []
    for i, entry in enumerate(st.session_state.mdx_functions):
        try:
            parsed = parse_expr(entry["text"])
            is_implicit = y in parsed.free_symbols
            parsed_functions.append({"index": i, "expr": parsed, "text": entry["text"],
                                     "label": (f"F{i+1}(x,y) = 0" if is_implicit else f"f{i+1}(x) = {sp.sstr(parsed)}"),
                                     "implicit": is_implicit,
                                     "color": COLORS[i % len(COLORS)], "visible": entry["visible"]})
        except Exception as exc:
            parse_errors.append(f"f{i+1}(x): {exc}")
    if parse_errors:
        for err in parse_errors: st.error("Function input error — " + err)
    if not parsed_functions:
        st.warning("Enter at least one valid function.")
        st.stop()

    # Build a single-variable analysis list. Explicit inputs are used directly; for
    # implicit equations F(x,y)=0, try solving symbolically for y and expose each
    # real-valued branch as a derived function for derivative/integration/inverse/etc.
    explicit_functions = [p.copy() for p in parsed_functions if not p.get("implicit", False)]
    implicit_branches = []
    for p in parsed_functions:
        if not p.get("implicit", False):
            continue
        try:
            branches = sp.solve(sp.Eq(p["expr"], 0), y)
            for branch_no, branch in enumerate(branches, start=1):
                branch = sp.simplify(branch)
                if y in branch.free_symbols or not branch.free_symbols.issubset({x}):
                    continue
                implicit_branches.append({
                    "index": p["index"], "expr": branch,
                    "text": f"{p['text']} [y-branch {branch_no}]",
                    "label": f"f{p['index']+1} branch {branch_no}(x) = {sp.sstr(branch)}",
                    "implicit": False, "derived_implicit": True,
                    "color": COLORS[(p["index"] + branch_no) % len(COLORS)],
                    "visible": p["visible"]
                })
        except Exception:
            continue
    # Keep explicit functions first, then add the branches solved from implicit equations.
    explicit_functions.extend(implicit_branches)
    if explicit_functions:
        valid_labels = [f"f{p['index']+1}(x) = {sp.sstr(p['expr'])}" for p in explicit_functions]
        selected_label = st.selectbox("Function to analyse in the tabs below", valid_labels, key="selected_analysis_function")
        selected = explicit_functions[valid_labels.index(selected_label)]
        expr = selected["expr"]
    else:
        # Keep the implicit-curve plotting workspace usable even when no y=f(x) function is entered.
        selected = {"index": 0, "expr": x**2 - 4, "text": "x**2 - 4", "label": "analysis placeholder", "color": COLORS[0]}
        expr = selected["expr"]
        if implicit_branches:
            st.info("All inputs are implicit equations. Where possible, MathDil MDX has solved F(x,y)=0 into y=f(x) branches; analysis tabs use those branches. The full implicit curve remains available in Graph Studio.")
        else:
            st.info("All entered expressions are implicit equations. They are plotted in Graph Studio. MathDil MDX could not isolate y into explicit branches for single-variable analysis; add an explicit function such as x**2 or sin(x).")
    point_x = st.number_input("Evaluate selected function at x =", value=1.0, step=0.5, key="shared_point_x")
    visible_items = [{"expr": p["expr"], "label": p["label"], "color": p["color"]} for p in parsed_functions if p["visible"]]
    if not visible_items:
        st.info("All functions are hidden. Turn on 'Show on graph' for at least one function.")

    # -------------------- Main modules: same integrated app and style --------------------
    tabs = st.tabs(["📈 Graph Studio", "🎯 Roots", "↔️ Increasing / Decreasing", "🔁 Inverse Function", "📐 Derivative", "∫ Integration", "📊 Value Table", "🎞️ Video Plotter", "📘 Algorithm Guide", "➗ Operations", "🎓 Topic Learning"])

    with tabs[0]:
        st.markdown("### Interactive Graph Studio")
        st.caption("Hover to inspect coordinates; scroll to zoom and drag to pan. Use the camera icon to export a graph image.")
        if visible_items:
            if st.session_state.get("graph_dimension", "2D") == "3D":
                st.caption("3D mode interprets each entered expression as a surface z = f(x, y). For example: x**2 + y**2 or sin(x)*cos(y).")
                st.plotly_chart(make_graph_3d(visible_items, x_min, x_max, y_min, y_max, height=600), use_container_width=True,
                    config={"scrollZoom": True, "displaylogo": False, "toImageButtonOptions": {"format": "png", "filename": "MathDil_MDX_graph_3D", "scale": 2}})
            else:
                st.plotly_chart(make_graph(visible_items, x_min, x_max, y_min, y_max, height=570), use_container_width=True,
                    config={"scrollZoom": True, "displaylogo": False, "toImageButtonOptions": {"format": "png", "filename": "MathDil_MDX_graph", "scale": 2}})

        # Graph controls are intentionally placed directly below the plot for easy access.
        st.markdown("#### 🎛️ Graph display options")
        control_2d3d, control_bg, control_grid = st.columns([1.15, 1.6, 1.1])
        with control_2d3d:
            st.selectbox("Graph dimension", ["2D", "3D"], key="graph_dimension",
                         help="2D plots y=f(x) and implicit curves. 3D plots z=f(x,y) surfaces.")
        with control_bg:
            st.selectbox("Background colour", ["Current navy", "Pure black", "White"],
                         key="graph_background_theme", help="Choose navy, black, or white graph background.")
        with control_grid:
            st.checkbox("Show coordinate grid", key="graph_show_grid",
                        help="Turn the coordinate grid on or off.")
        st.caption("Choose 2D/3D, background colour, and grid options here below the graph. Changes apply automatically.")

        if explicit_functions:
            val = safe_value(expr, point_x)
            m1, m2, m3 = st.columns(3)
            m1.metric("Selected function", f"f{selected['index']+1}(x)")
            m2.metric("f(x)", fmt_num(val) if val is not None else "undefined")
            m3.metric("Input x", fmt_num(point_x))
            if val is not None:
                st.latex(f"f_{{{selected['index']+1}}}({sp.latex(sp.sympify(point_x))}) = {sp.latex(sp.N(expr.subs(x, point_x)))}")
        else:
            st.info("Implicit equations are curves F(x,y)=0, not single-valued functions f(x). Use the graph and the parameter controls to explore them.")
        with st.expander("Show all functions and expressions"):
            for p in parsed_functions:
                st.markdown(f"**{p['label']}:** `{p['text']}` — {'Visible' if p['visible'] else 'Hidden'}")

    with tabs[1]:
        st.markdown("### Roots / x-intercepts — all entered equations")
        st.write("**Algorithm:** explicit functions: solve f(x)=0. Implicit equations: set y=0 in F(x,y)=0 to find x-axis intersections.")
        root_items = []
        for p in parsed_functions:
            with st.expander(f"{'Equation' if p.get('implicit') else 'Function'} {p['index']+1}: {p['text']}", expanded=True):
                root_expr = sp.simplify(p['expr'].subs(y, 0)) if p.get('implicit') else p['expr']
                st.latex((sp.latex(p['expr']) + r'ig|_{y=0}=0') if p.get('implicit') else (sp.latex(root_expr) + '=0'))
                roots = real_roots_in_window(root_expr, x_min, x_max)
                if roots:
                    root_df = pd.DataFrame({"Root number": [f"x{i+1}" for i in range(len(roots))], "x-coordinate": roots,
                                            "f(x) at root": [safe_value(root_expr, r) for r in roots]})
                    st.dataframe(root_df, use_container_width=True, hide_index=True)
                    root_items.append({"expr": p['expr'], "label": p['label'], "color": p['color']})
                    st.markdown("**Calculation:** solve the resulting equation for real x-values in the selected range.")
                    st.latex(r"x\in" + sp.latex(sp.FiniteSet(*[sp.Float(r, 8) for r in roots])))
                else:
                    st.info("No real x-intercepts detected in the selected range.")
        if root_items:
            fig = make_graph([{"expr": p['expr'], "label": p['label'], "color": p['color']} for p in parsed_functions], x_min, x_max, y_min, y_max, height=470)
            for p in parsed_functions:
                root_expr = sp.simplify(p['expr'].subs(y, 0)) if p.get('implicit') else p['expr']
                roots = real_roots_in_window(root_expr, x_min, x_max)
                if roots:
                    fig.add_trace(go.Scatter(x=roots, y=[0]*len(roots), mode="markers+text", name=f"Roots f{p['index']+1}",
                                             text=[fmt_num(r) for r in roots], textposition="top center", marker=dict(size=10, color=p['color'])))
            st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True, "displaylogo": False})

    with tabs[2]:
        st.markdown("### Increasing and Decreasing — all functions / solvable branches")
        st.write("For each explicit function or branch solved from an implicit equation, calculate f′(x), find critical points, and test the derivative sign on each interval.")
        if not explicit_functions:
            st.info("This analysis needs explicit functions of x, such as x**2 or sin(x). Implicit equations can still be plotted in Graph Studio.")
        for p in explicit_functions:
            with st.expander(f"f{p['index']+1}(x) = {sp.sstr(p['expr'])}", expanded=True):
                e = p['expr']; derivative = sp.simplify(sp.diff(e, x))
                st.markdown("**Step 1 — Derivative**"); st.latex("f'(x)=" + sp.latex(derivative))
                critical = real_roots_in_window(derivative, x_min, x_max) if derivative != 0 else []
                critical = [c for c in critical if x_min + 1e-6 < c < x_max - 1e-6]
                boundaries = [x_min] + critical + [x_max]; rows=[]; inc=[]; dec=[]
                for left, right in zip(boundaries[:-1], boundaries[1:]):
                    mid=(left+right)/2; dval=safe_value(derivative, mid)
                    if dval is None: status="Undefined / cannot determine"
                    elif dval > 1e-7: status="Increasing"; inc.append((left,right))
                    elif dval < -1e-7: status="Decreasing"; dec.append((left,right))
                    else: status="Derivative zero / inconclusive"
                    rows.append({"Interval":f"({fmt_num(left)}, {fmt_num(right)})", "Test point":fmt_num(mid), "f′(test point)":fmt_num(dval) if dval is not None else "undefined", "Behaviour":status})
                st.markdown("**Step 2 — Test derivative sign**"); st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
                st.markdown("**Step 3 — Conclusion**")
                st.write("**Increasing:** " + (", ".join(f"({fmt_num(a)}, {fmt_num(b)})" for a,b in inc) if inc else "No increasing interval detected."))
                st.write("**Decreasing:** " + (", ".join(f"({fmt_num(a)}, {fmt_num(b)})" for a,b in dec) if dec else "No decreasing interval detected."))
                fig=make_graph([{"expr":e,"label":f"f{p['index']+1}(x)","color":p['color']},{"expr":derivative,"label":f"f{p['index']+1}′(x)","color":COLORS[(p['index']+1)%len(COLORS)]}],x_min,x_max,y_min,y_max,height=400)
                for c in critical: fig.add_vline(x=c,line_dash="dash",line_color="#d97706")
                st.plotly_chart(
    fig,
    use_container_width=True,
    config={"scrollZoom": True, "displaylogo": False},
   key=f"roots_chart_{len(critical)}_{x_min}_{x_max}"
)
        st.caption("Numerical interval testing is limited to the selected range; discontinuities or missed critical points can affect results.")

    with tabs[3]:
        st.markdown("### 🔁 Inverse Function Explorer")
        st.caption("Choose f₁, f₂, or any other explicit function. Its inverse steps and graph are shown here.")
        if not explicit_functions:
            st.info("Add at least one explicit function of x, such as x**2 or sin(x). Implicit curves F(x,y)=0 do not directly have an inverse-function expression in this module.")
        else:
            inverse_labels = [f"f{p['index']+1}(x) = {sp.sstr(p['expr'])}" for p in explicit_functions]
            inverse_target_label = st.selectbox("Inverse of which function?", inverse_labels, key="inverse_target_function")
            inverse_target = explicit_functions[inverse_labels.index(inverse_target_label)]
            inverse_source = inverse_target["expr"]
            st.write("**Algorithm:** (1) Write y=f(x). (2) Swap x and y. (3) Solve for y. (4) Check whether a domain restriction is needed.")
            domain_choice = st.selectbox("Original function domain restriction", ["No restriction", "x ≥ 0", "x ≤ 0"], key="inverse_domain_choice")
            st.markdown("**Step 1 — Original function**")
            st.latex("y=" + sp.latex(inverse_source))
            st.markdown("**Step 2 — Swap x and y**")
            st.latex("x=" + sp.latex(inverse_source.subs(x, y)))
            try:
                solutions = sp.solve(sp.Eq(x, inverse_source.subs(x, y)), y)
                real_solutions = [sol for sol in solutions if not sol.has(sp.I)]
                inverse_expr = None
                if len(real_solutions) == 1:
                    inverse_expr = real_solutions[0]
                elif len(real_solutions) > 1 and domain_choice == "x ≥ 0":
                    inverse_expr = max(real_solutions, key=lambda q: float(sp.N(q.subs(x, 10))) if safe_value(q, 10) is not None else -float("inf"))
                elif len(real_solutions) > 1 and domain_choice == "x ≤ 0":
                    inverse_expr = min(real_solutions, key=lambda q: float(sp.N(q.subs(x, 10))) if safe_value(q, 10) is not None else float("inf"))
                if inverse_expr is not None:
                    st.markdown("**Step 3 — Solve for the inverse**")
                    st.latex("f^{-1}(x)=" + sp.latex(inverse_expr))
                    if len(real_solutions) > 1 and domain_choice == "No restriction":
                        st.warning("Multiple inverse branches found: the function is not one-to-one on its full domain. Choose x ≥ 0 or x ≤ 0 where appropriate.")
                    elif len(real_solutions) > 1:
                        st.caption("A branch has been selected. Confirm that the restriction makes the original function one-to-one.")
                    inverse_items = [
                        {"expr": inverse_source, "label": f"f{inverse_target['index']+1}(x)", "color": COLORS[0]},
                        {"expr": inverse_expr, "label": f"f{inverse_target['index']+1}⁻¹(x)", "color": COLORS[2]},
                        {"expr": x, "label": "y = x", "color": "#64748b"},
                    ]
                    st.markdown("**Graph: original function, inverse, and y=x**")
                    st.plotly_chart(make_graph(inverse_items, x_min, x_max, y_min, y_max, height=480), use_container_width=True,
                                    config={"scrollZoom": True, "displaylogo": False, "toImageButtonOptions": {"format": "png", "filename": "MathDil_MDX_inverse_graph", "scale": 2}})
                else:
                    st.warning("No single explicit inverse branch was returned. Try a different function or domain restriction.")
            except Exception as exc:
                st.warning(f"Could not derive an explicit inverse: {exc}")
            with st.expander("Why check one-to-one?"):
                st.write("If different inputs produce the same output, swapping x and y gives multiple y-values. Restricting the domain may make the inverse a function.")

    with tabs[4]:
        st.markdown("### Derivative Explorer — all functions / solvable branches")
        if not explicit_functions:
            st.info("Derivative analysis needs y=f(x). For implicit equations, the app attempts to solve for y and analyze each branch; add an explicit function if no branch can be isolated.")
        for p in explicit_functions:
            with st.expander(f"Derivative of f{p['index']+1}(x) = {sp.sstr(p['expr'])}", expanded=True):
                e=p['expr']; derivative=sp.simplify(sp.diff(e,x)); second=sp.simplify(sp.diff(e,x,2))
                st.write("**Step 1 — First derivative**"); st.latex("f'(x)="+sp.latex(derivative))
                st.write("**Step 2 — Second derivative**"); st.latex("f''(x)="+sp.latex(second))
                val=safe_value(e,point_x); slope=safe_value(derivative,point_x)
                c1,c2,c3=st.columns(3); c1.metric(f"f{p['index']+1}: x",fmt_num(point_x)); c2.metric("f(x)",fmt_num(val) if val is not None else "undefined"); c3.metric("f′(x)",fmt_num(slope) if slope is not None else "undefined")
                if val is not None and slope is not None:
                    tangent=sp.simplify(e.subs(x,point_x)+derivative.subs(x,point_x)*(x-point_x))
                    st.write("**Step 3 — Tangent line at the chosen x**"); st.latex("y="+sp.latex(tangent))
                fig=make_graph([{"expr":e,"label":f"f{p['index']+1}(x)","color":p['color']},{"expr":derivative,"label":f"f{p['index']+1}′(x)","color":COLORS[(p['index']+1)%len(COLORS)]}],x_min,x_max,y_min,y_max,height=400)
                st.plotly_chart(fig,use_container_width=True,config={"scrollZoom":True,"displaylogo":False})

    with tabs[5]:
        st.markdown("### Integration Explorer — all explicit functions")
        if not explicit_functions:
            st.info("Integration analysis needs explicit functions of x. Implicit equations remain available in Graph Studio.")
        c1,c2=st.columns(2)
        with c1: lower=st.number_input("Lower limit a",value=0.0,step=.5,key="integral_lower_all")
        with c2: upper=st.number_input("Upper limit b",value=2.0,step=.5,key="integral_upper_all")
        for p in explicit_functions:
            with st.expander(f"Integrate f{p['index']+1}(x) = {sp.sstr(p['expr'])}", expanded=True):
                e=p['expr']
                try:
                    antiderivative=sp.integrate(e,x)
                    st.write("**Step 1 — Indefinite integral**"); st.latex(r"\int f(x)\,dx="+sp.latex(antiderivative)+"+C")
                    if lower != upper:
                        definite=sp.integrate(e,(x,lower,upper))
                        st.write("**Step 2 — Apply limits F(b) − F(a)**"); st.latex(r"\int_{"+sp.latex(lower)+r"}^{"+sp.latex(upper)+r"} f(x)\,dx="+sp.latex(definite))
                        dn=sp.N(definite)
                        if dn.is_real and dn.is_finite: st.metric(f"f{p['index']+1}: definite integral",fmt_num(float(dn)))
                        xx=np.linspace(min(lower,upper),max(lower,upper),500); yy=numeric_y(e,xx)
                        fig=go.Figure(); fig.add_trace(go.Scatter(x=xx,y=yy,mode="lines",name=f"f{p['index']+1}(x)",line=dict(color=p['color'],width=3),fill="tozeroy",fillcolor="rgba(37,99,235,.18)")); fig.add_hline(y=0,line_color="#475569")
                        fig.update_layout(template="plotly_white",height=330,margin=dict(l=10,r=10,t=15,b=15),xaxis_title="x",yaxis_title="f(x)")
                        st.plotly_chart(fig,use_container_width=True,config={"displaylogo":False})
                    else: st.info("Choose different limits to calculate a definite integral.")
                except Exception as exc: st.warning(f"Integral could not be evaluated: {exc}")
        st.caption("The definite integral is signed area; portions below the x-axis contribute negatively.")

    with tabs[6]:
        st.markdown("### Value Table — all functions")
        c1, c2, c3 = st.columns(3)
        start = c1.number_input("Start x", value=-5.0, step=1.0, key="table_start")
        end = c2.number_input("End x", value=5.0, step=1.0, key="table_end")
        step = c3.number_input("Step size", value=1.0, min_value=.01, step=.5, key="table_step")
        if st.button("Generate value table", type="primary", key="generate_table"):
            if start > end: st.error("Start x must be ≤ End x.")
            else:
                xs = np.arange(start, end + step*.5, step)[:2000]
                table_data = {"x": xs}
                for p in parsed_functions:
                    table_expr = sp.simplify(p["expr"].subs(y, 0)) if p.get("implicit") else p["expr"]
                    col_label = f"F{p['index']+1}(x,0)" if p.get("implicit") else f"f{p['index']+1}(x) = {sp.sstr(p['expr'])}"
                    table_data[col_label] = [safe_value(table_expr, float(v)) for v in xs]
                df = pd.DataFrame(table_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode("utf-8"), file_name="MathDil_MDX_value_table.csv", mime="text/csv")

    with tabs[7]:
        st.markdown("### Video Plotter — progressive graph animation")
        st.write("Choose whether to create a 2D curve animation or a 3D surface animation. The selected mode is used for the preview and downloaded HTML.")
        animation_dimension = st.radio(
            "Animation dimension", ["2D", "3D"], horizontal=True,
            key="video_animation_dimension",
            help="2D animates y=f(x) curves. 3D progressively reveals surfaces z=f(x,y)."
        )
        frame_count = st.slider("Animation frames", min_value=10, max_value=80, value=35, step=5, key="animation_frames")
        duration = st.slider("Milliseconds per frame", min_value=30, max_value=250, value=80, step=10, key="animation_duration")
        if animation_dimension == "2D":
            st.caption("2D mode: animates explicit functions y = f(x). Implicit equations are not included in this animation.")
        else:
            st.caption("3D mode: animates surfaces z = f(x, y). Expressions depending only on x are shown as surfaces constant along y.")

        if st.button("Build animation", type="primary", key="build_animation"):
            animation_functions = [p for p in parsed_functions if p["visible"] and not p.get("implicit", False)]
            if not animation_functions:
                st.warning("Show at least one explicit function before building the animation.")
            elif animation_dimension == "2D":
                xs = np.linspace(x_min, x_max, 500)
                traces = [go.Scatter(x=[], y=[], mode="lines", line=dict(color=p["color"], width=3), name=p["label"]) for p in animation_functions]
                frames = []
                for k in range(1, frame_count + 1):
                    upto = max(2, int(len(xs) * k / frame_count))
                    frame_data = []
                    for p in animation_functions:
                        ys_curve = numeric_y(p["expr"], xs)
                        frame_data.append(go.Scatter(x=xs[:upto], y=ys_curve[:upto], mode="lines", line=dict(color=p["color"], width=3), name=p["label"]))
                    frames.append(go.Frame(data=frame_data, name=str(k)))
                fig = go.Figure(data=traces, frames=frames)
                bg_choice = st.session_state.get("graph_background_theme", "Current navy")
                is_white = bg_choice == "White"
                plot_bg = "#FFFFFF" if is_white else ("#000000" if bg_choice == "Pure black" else "#051026")
                font_color = "#172033" if is_white else "#E6F4FF"
                grid_on = st.session_state.get("graph_show_grid", True)
                grid_color = "rgba(71,85,105,.28)" if is_white else "rgba(103,232,249,.22)"
                fig.update_layout(template="plotly_white" if is_white else "plotly_dark", paper_bgcolor=plot_bg, plot_bgcolor=plot_bg,
                    font=dict(color=font_color), height=520, title="MathDil MDX — 2D curve animation",
                    xaxis=dict(title="x", range=[x_min, x_max], showgrid=grid_on, gridcolor=grid_color),
                    yaxis=dict(title="y", range=[y_min, y_max], showgrid=grid_on, gridcolor=grid_color),
                    updatemenus=[dict(type="buttons", showactive=False, buttons=[
                        dict(label="▶ Play", method="animate", args=[None, {"frame": {"duration": duration, "redraw": True}, "fromcurrent": True}]),
                        dict(label="↻ Reset", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}])])])
                html = fig.to_html(include_plotlyjs=True, full_html=True).encode("utf-8")
                st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})
                st.download_button("⬇️ Download 2D animated HTML", data=html, file_name="MathDil_MDX_2D_graph_animation.html", mime="text/html")
                st.success("2D animation created. Download the HTML file and open it in a browser.")
            else:
                # 3D: start with a genuinely blank surface, then reveal it row-by-row.
                # Keeping the same full grid in every frame prevents Plotly from stretching
                # or shifting the surface while the animation is playing.
                grid_n = 90
                xs3 = np.linspace(float(x_min), float(x_max), grid_n)
                ys3 = np.linspace(float(y_min), float(y_max), grid_n)
                X3, Y3 = np.meshgrid(xs3, ys3)
                z_values = []

                for p in animation_functions:
                    try:
                        fn3 = sp.lambdify((x, y), p["expr"], modules=["numpy"])
                        with np.errstate(all="ignore"):
                            Z3 = np.asarray(fn3(X3, Y3))
                        if np.isscalar(Z3):
                            Z3 = np.full(X3.shape, Z3)
                        if np.iscomplexobj(Z3):
                            Z3 = np.where(np.abs(Z3.imag) < 1e-8, Z3.real, np.nan)
                        Z3 = np.asarray(Z3, dtype=float)
                        Z3[~np.isfinite(Z3)] = np.nan
                        Z3[np.abs(Z3) > 1e6] = np.nan
                        if np.count_nonzero(np.isfinite(Z3)) < 4:
                            continue
                        z_values.append((p, Z3))
                    except Exception:
                        continue

                if not z_values:
                    st.warning(
                        "Could not evaluate the selected functions as 3D surfaces. "
                        "Try expressions such as x**2 + y**2 or sin(x)*cos(y)."
                    )
                else:
                    # First frame is fully blank. Each following frame reveals more rows.
                    blank_z = np.full((grid_n, grid_n), np.nan, dtype=float)
                    surface_data = []
                    for p, Z3 in z_values:
                        surface_data.append(go.Surface(
                            x=X3, y=Y3, z=blank_z.copy(),
                            name=p["label"], showscale=False, opacity=0.96,
                            connectgaps=False,
                            colorscale=[[0, p["color"]], [1, "#f8fafc"]],
                            cmin=float(np.nanmin(Z3)), cmax=float(np.nanmax(Z3)) if float(np.nanmax(Z3)) > float(np.nanmin(Z3)) else float(np.nanmin(Z3)) + 1,
                            hovertemplate="x=%{x:.3f}<br>y=%{y:.3f}<br>z=%{z:.3f}<extra></extra>"
                        ))

                    frames = []
                    for k in range(1, frame_count + 1):
                        # Grow from the first row to the complete surface. At least two
                        # adjacent rows are revealed so Plotly can render a visible patch.
                        upto = max(2, min(grid_n, int(np.ceil(grid_n * k / frame_count))))
                        frame_surfaces = []
                        for p, Z3 in z_values:
                            Z_step = Z3.copy()
                            Z_step[upto:, :] = np.nan
                            frame_surfaces.append(go.Surface(
                                x=X3, y=Y3, z=Z_step,
                                name=p["label"], showscale=False, opacity=0.96,
                                connectgaps=False,
                                colorscale=[[0, p["color"]], [1, "#f8fafc"]],
                                cmin=float(np.nanmin(Z3)),
                                cmax=float(np.nanmax(Z3)) if float(np.nanmax(Z3)) > float(np.nanmin(Z3)) else float(np.nanmin(Z3)) + 1,
                                hovertemplate="x=%{x:.3f}<br>y=%{y:.3f}<br>z=%{z:.3f}<extra></extra>"
                            ))
                        frames.append(go.Frame(
                            data=frame_surfaces,
                            traces=list(range(len(z_values))),
                            name=str(k)
                        ))

                    bg_choice = st.session_state.get("graph_background_theme", "Current navy")
                    is_white = bg_choice == "White"
                    bg = "#FFFFFF" if is_white else ("#000000" if bg_choice == "Pure black" else "#051026")
                    font_color = "#172033" if is_white else "#E6F4FF"
                    grid_on = st.session_state.get("graph_show_grid", True)
                    grid_color = "rgba(71,85,105,.28)" if is_white else "rgba(103,232,249,.28)"
                    fig = go.Figure(data=surface_data, frames=frames)
                    fig.update_layout(
                        template="plotly_white" if is_white else "plotly_dark",
                        paper_bgcolor=bg, plot_bgcolor=bg,
                        font=dict(color=font_color), height=620,
                        title="MathDil MDX — 3D surface animation",
                        scene=dict(
                            xaxis_title="x", yaxis_title="y", zaxis_title="z",
                            xaxis=dict(showbackground=True, showgrid=grid_on, gridcolor=grid_color, backgroundcolor=bg),
                            yaxis=dict(showbackground=True, showgrid=grid_on, gridcolor=grid_color, backgroundcolor=bg),
                            zaxis=dict(showbackground=True, showgrid=grid_on, gridcolor=grid_color, backgroundcolor=bg),
                            bgcolor=bg,
                            aspectmode="auto",
                            camera=dict(eye=dict(x=1.55, y=1.55, z=1.15))
                        ),
                        updatemenus=[dict(type="buttons", showactive=False, x=0.02, y=1.12, buttons=[
                            dict(label="▶ Play", method="animate", args=[None, {
                                "frame": {"duration": duration, "redraw": True},
                                "transition": {"duration": 0},
                                "fromcurrent": False,
                                "mode": "immediate"
                            }]),
                            dict(label="↻ Replay", method="animate", args=[[str(i) for i in range(1, frame_count + 1)], {
                                "frame": {"duration": duration, "redraw": True},
                                "transition": {"duration": 0},
                                "fromcurrent": False,
                                "mode": "immediate"
                            }]),
                            dict(label="■ Stop", method="animate", args=[[None], {
                                "frame": {"duration": 0, "redraw": True},
                                "transition": {"duration": 0},
                                "mode": "immediate"
                            }])
                        ])],
                        sliders=[dict(
                            active=0, x=0.12, y=0, len=0.82,
                            currentvalue=dict(prefix="Frame: "),
                            steps=[dict(
                                method="animate", label=str(i),
                                args=[[str(i)], {
                                    "frame": {"duration": 0, "redraw": True},
                                    "transition": {"duration": 0},
                                    "mode": "immediate"
                                }]
                            ) for i in range(1, frame_count + 1)]
                        )]
                    )
                    html = fig.to_html(include_plotlyjs=True, full_html=True).encode("utf-8")
                    st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False, "scrollZoom": True})
                    st.download_button(
                        "⬇️ Download 3D animated HTML",
                        data=html,
                        file_name="MathDil_MDX_3D_surface_animation.html",
                        mime="text/html"
                    )
                    st.success("3D animation created. Press Play to reveal the surface from a blank plot, or use Replay to watch it again.")
    with tabs[8]:
        st.markdown("### MathDil MDX — Algorithms")
        st.markdown("**Roots algorithm**")
        st.code("1. Input f(x)\n2. Set f(x) = 0\n3. Solve symbolically / numerically\n4. Keep real roots in the selected interval\n5. Display roots, table, and graph markers", language="text")
        st.markdown("**Increasing / decreasing algorithm**")
        st.code("1. Compute f′(x)\n2. Find critical points from f′(x) = 0\n3. Split the selected interval at critical points\n4. Test f′ at one point in each subinterval\n5. Positive → increasing; negative → decreasing", language="text")
        st.markdown("**Inverse function algorithm**")
        st.code("1. Write y = f(x)\n2. Swap x and y\n3. Solve for y\n4. Check one-to-one property\n5. Restrict the domain if multiple branches occur", language="text")
        st.markdown("**Derivative and integration algorithm**")
        st.code("Derivative: differentiate f(x)\nTangent: y = f(a) + f′(a)(x − a)\nIndefinite integral: find F(x) with F′(x) = f(x)\nDefinite integral: evaluate F(b) − F(a)", language="text")
        st.markdown("**Multiple functions**")
        st.code("1. Add f1(x), f2(x), f3(x), ...\n2. Toggle visibility for each function\n3. Graph Studio plots all visible functions together\n4. Roots, monotonicity, derivatives, and integration show results for every entered explicit function\n5. Inverse lets you select any explicit function; Value Table and Video Plotter support multiple functions", language="text")
        st.warning("Symbolic/numerical methods cannot guarantee closed-form results for every function. Root and monotonicity detection are limited to the selected x-range; verify advanced cases mathematically.")


    with tabs[9]:
        st.markdown("### ➗ Function Operations")
        st.caption("Choose an operation and two functions. The result, algorithm, symbolic steps, and graph are shown here—inside the same MathDil MDX app.")

        operation = st.selectbox(
            "Select operation",
            ["Addition  f(x) + g(x)", "Subtraction  f(x) − g(x)", "Multiplication  f(x) × g(x)",
             "Division  f(x) / g(x)", "Composition  f(g(x))", "Composition  g(f(x))"],
            key="operation_kind"
        )
        function_labels = [f"f{p['index']+1}(x) = {sp.sstr(p['expr'])}" for p in explicit_functions]
        if not function_labels:
            st.info("Operations need at least one explicit function of x. Add a function such as x**2 or sin(x) in the workspace.")
            st.stop()
        op_c1, op_c2 = st.columns(2)
        with op_c1:
            first_label = st.selectbox("Choose first function f(x)", function_labels, index=0, key="operation_first")
        with op_c2:
            second_default = 1 if len(function_labels) > 1 else 0
            second_label = st.selectbox("Choose second function g(x)", function_labels, index=second_default, key="operation_second")

        first = explicit_functions[function_labels.index(first_label)]
        second_fn = explicit_functions[function_labels.index(second_label)]
        f_expr, g_expr = first["expr"], second_fn["expr"]
        op_key = operation.split("  ")[0]

        st.markdown("#### Algorithm")
        if op_key == "Addition":
            result_expr = sp.simplify(f_expr + g_expr)
            st.code("1. Select f(x) and g(x).\n2. Write f(x) + g(x).\n3. Substitute both expressions.\n4. Combine like terms and simplify.\n5. Plot f(x), g(x), and the result.", language="text")
            st.latex(r"(f+g)(x)=" + sp.latex(f_expr) + "+" + sp.latex(g_expr))
            st.latex(r"(f+g)(x)=" + sp.latex(result_expr))
            result_label = "(f + g)(x)"
            graph_items = [
                {"expr": f_expr, "label": f"f(x) = {sp.sstr(f_expr)}", "color": COLORS[0]},
                {"expr": g_expr, "label": f"g(x) = {sp.sstr(g_expr)}", "color": COLORS[1]},
                {"expr": result_expr, "label": f"(f+g)(x) = {sp.sstr(result_expr)}", "color": COLORS[2]},
            ]
        elif op_key == "Subtraction":
            result_expr = sp.simplify(f_expr - g_expr)
            st.code("1. Select f(x) and g(x).\n2. Write f(x) − g(x).\n3. Substitute both expressions with the correct signs.\n4. Expand brackets and simplify.\n5. Plot f(x), g(x), and the result.", language="text")
            st.latex(r"(f-g)(x)=" + sp.latex(f_expr) + "-" + r"\left(" + sp.latex(g_expr) + r"\right)")
            st.latex(r"(f-g)(x)=" + sp.latex(result_expr))
            result_label = "(f − g)(x)"
            graph_items = [
                {"expr": f_expr, "label": f"f(x) = {sp.sstr(f_expr)}", "color": COLORS[0]},
                {"expr": g_expr, "label": f"g(x) = {sp.sstr(g_expr)}", "color": COLORS[1]},
                {"expr": result_expr, "label": f"(f-g)(x) = {sp.sstr(result_expr)}", "color": COLORS[2]},
            ]
        elif op_key == "Multiplication":
            result_expr = sp.simplify(f_expr * g_expr)
            st.code("1. Select f(x) and g(x).\n2. Write f(x) × g(x).\n3. Multiply the expressions.\n4. Expand/factor and simplify where possible.\n5. Plot both functions and their product.", language="text")
            st.latex(r"(fg)(x)=" + r"\left(" + sp.latex(f_expr) + r"\right)\left(" + sp.latex(g_expr) + r"\right)")
            st.latex(r"(fg)(x)=" + sp.latex(result_expr))
            result_label = "(fg)(x)"
            graph_items = [
                {"expr": f_expr, "label": f"f(x) = {sp.sstr(f_expr)}", "color": COLORS[0]},
                {"expr": g_expr, "label": f"g(x) = {sp.sstr(g_expr)}", "color": COLORS[1]},
                {"expr": result_expr, "label": f"(fg)(x) = {sp.sstr(result_expr)}", "color": COLORS[2]},
            ]
        elif op_key == "Division":
            result_expr = sp.simplify(f_expr / g_expr)
            st.code("1. Select f(x) and g(x).\n2. Write f(x)/g(x).\n3. Form the quotient.\n4. Simplify the expression.\n5. Exclude every x where g(x) = 0.\n6. Plot both functions and the quotient.", language="text")
            st.latex(r"\left(\frac{f}{g}\right)(x)=\frac{" + sp.latex(f_expr) + "}{" + sp.latex(g_expr) + "}")
            st.latex(r"\left(\frac{f}{g}\right)(x)=" + sp.latex(result_expr))
            result_label = "(f/g)(x)"
            try:
                denominator_roots = sp.solveset(sp.Eq(g_expr, 0), x, domain=sp.S.Reals)
                st.write("**Domain note:** exclude real values where g(x) = 0.")
                st.latex(r"g(x)=0\quad\Rightarrow\quad x\in " + sp.latex(denominator_roots))
            except Exception:
                st.info("Domain note: the denominator must be nonzero; exact excluded values could not be determined automatically.")
            graph_items = [
                {"expr": f_expr, "label": f"f(x) = {sp.sstr(f_expr)}", "color": COLORS[0]},
                {"expr": g_expr, "label": f"g(x) = {sp.sstr(g_expr)}", "color": COLORS[1]},
                {"expr": result_expr, "label": f"(f/g)(x) = {sp.sstr(result_expr)}", "color": COLORS[2]},
            ]
        else:
            if operation.startswith("Composition  f"):
                result_expr = sp.simplify(f_expr.subs(x, g_expr))
                st.code("1. Select f(x) and g(x).\n2. For f(g(x)), replace every x in f(x) by g(x).\n3. Simplify the nested expression.\n4. Check the inner function's output is allowed in the outer function's domain.\n5. Plot f(x), g(x), and f(g(x)).", language="text")
                st.latex(r"f(g(x))=" + sp.latex(f_expr.subs(x, sp.Symbol("g(x)"))))
                st.latex(r"f(g(x))=" + sp.latex(result_expr))
                result_label = "f(g(x))"
            else:
                result_expr = sp.simplify(g_expr.subs(x, f_expr))
                st.code("1. Select f(x) and g(x).\n2. For g(f(x)), replace every x in g(x) by f(x).\n3. Simplify the nested expression.\n4. Check the inner function's output is allowed in the outer function's domain.\n5. Plot g(x), f(x), and g(f(x)).", language="text")
                st.latex(r"g(f(x))=" + sp.latex(g_expr.subs(x, sp.Symbol("f(x)"))))
                st.latex(r"g(f(x))=" + sp.latex(result_expr))
                result_label = "g(f(x))"
            graph_items = [
                {"expr": f_expr, "label": f"f(x) = {sp.sstr(f_expr)}", "color": COLORS[0]},
                {"expr": g_expr, "label": f"g(x) = {sp.sstr(g_expr)}", "color": COLORS[1]},
                {"expr": result_expr, "label": f"{result_label} = {sp.sstr(result_expr)}", "color": COLORS[2]},
            ]

        st.markdown("#### Final result")
        st.latex(result_label + "=" + sp.latex(result_expr))
        st.markdown("#### Graph comparison")
        st.caption("The graph shows the two selected functions and the operation result together. The visible x-range is controlled by the Graph settings in the sidebar.")
        try:
            st.plotly_chart(make_graph(graph_items, x_min, x_max, y_min, y_max, height=520, title=f"Function operation: {result_label}"),
                            use_container_width=True, config={"scrollZoom": True, "displaylogo": False,
                            "toImageButtonOptions": {"format": "png", "filename": "MathDil_MDX_operation_graph", "scale": 2}})
        except Exception as exc:
            st.warning(f"Could not plot this operation over the selected range: {exc}")
        st.markdown("#### 🔁 Inverse of this operation")
        st.caption("Use this for the selected sum, difference, product, quotient, or composition. The inverse may require a domain restriction.")
        show_operation_inverse = st.checkbox("Show inverse graph of the operation result", value=False, key="show_operation_inverse")
        if show_operation_inverse:
            inverse_branch = st.selectbox("Choose inverse branch if multiple solutions exist", ["No restriction / automatic", "Choose larger branch (x ≥ 0)", "Choose smaller branch (x ≤ 0)"], key="operation_inverse_branch")
            st.write("**Step 1 — Start with the operation result**")
            st.latex("y=" + sp.latex(result_expr))
            st.write("**Step 2 — Swap x and y**")
            st.latex("x=" + sp.latex(result_expr.subs(x, y)))
            try:
                op_solutions = sp.solve(sp.Eq(x, result_expr.subs(x, y)), y)
                op_real_solutions = [sol for sol in op_solutions if not sol.has(sp.I)]
                op_inverse = None
                if len(op_real_solutions) == 1:
                    op_inverse = op_real_solutions[0]
                elif len(op_real_solutions) > 1 and inverse_branch == "Choose larger branch (x ≥ 0)":
                    op_inverse = max(op_real_solutions, key=lambda q: float(sp.N(q.subs(x, 10))) if safe_value(q, 10) is not None else -float("inf"))
                elif len(op_real_solutions) > 1 and inverse_branch == "Choose smaller branch (x ≤ 0)":
                    op_inverse = min(op_real_solutions, key=lambda q: float(sp.N(q.subs(x, 10))) if safe_value(q, 10) is not None else float("inf"))
                if op_inverse is None:
                    st.warning("A single inverse expression could not be determined. The result may not be one-to-one, or the inverse may not have a simple symbolic form. Try a branch restriction.")
                else:
                    st.write("**Step 3 — Inverse result**")
                    st.latex(result_label + r"^{-1}(x)=" + sp.latex(op_inverse))
                    if len(op_real_solutions) > 1 and inverse_branch == "No restriction / automatic":
                        st.warning("Multiple branches exist. The operation result is not one-to-one on its full domain; select a branch to graph an inverse function.")
                    op_inverse_items = [
                        {"expr": result_expr, "label": f"Operation result: {result_label}", "color": COLORS[0]},
                        {"expr": op_inverse, "label": f"Inverse of {result_label}", "color": COLORS[2]},
                        {"expr": x, "label": "y = x", "color": "#64748b"},
                    ]
                    st.plotly_chart(make_graph(op_inverse_items, x_min, x_max, y_min, y_max, height=470, title=f"Inverse graph of {result_label}"),
                                    use_container_width=True, config={"scrollZoom": True, "displaylogo": False,
                                    "toImageButtonOptions": {"format": "png", "filename": "MathDil_MDX_operation_inverse_graph", "scale": 2}})
            except Exception as exc:
                st.warning(f"Could not calculate the operation inverse: {exc}")

        with st.expander("Operation summary and domain notes"):
            st.write(f"First function: f(x) = `{sp.sstr(f_expr)}`")
            st.write(f"Second function: g(x) = `{sp.sstr(g_expr)}`")
            st.write(f"Operation result: `{sp.sstr(result_expr)}`")
            if op_key == "Division":
                st.write("For division, the result is defined only where the denominator is not zero.")
            if op_key.startswith("Composition"):
                st.write("For composition, the output of the inner function must lie in the domain of the outer function.")


    with tabs[10]:
        st.markdown("### 🎓 MathDil Learn & Master")
        st.write("**JEE Main + JEE Advanced** · Test → Diagnose → Short Explanation → Targeted Practice → Mastery Check")
        st.info("Graph Studio remains a separate tab exactly for exploring graphs. This section is for topic-wise adaptive learning; it does not replace the graph tools.")

        topic = st.selectbox("Choose topic", [
            "Differentiation", "Integration", "Limits and Continuity", "Application of Derivatives",
            "Definite Integral and Area", "Differential Equations"
        ], key="learn_topic")
        level = st.radio("Target level", ["JEE Main", "JEE Advanced"], horizontal=True, key="learn_level")

        # Small, transparent diagnostic bank. The feedback diagnoses a likely misconception,
        # not a permanent label; later questions should confirm it.
        banks = {
            "Differentiation": [
                {"q":"Differentiate f(x)=x³−6x²+9x+2.","choices":["3x²−12x+9","3x²−12x+2","x²−12x+9","3x²−6x+9"],"ans":0,"reason":"You may be differentiating the constant incorrectly or applying the power rule inconsistently.","hint":"Use d(xⁿ)/dx = n·xⁿ⁻¹ term by term. The derivative of a constant is 0.","practice":"Differentiate g(x)=2x⁴−3x²+7.","pchoices":["8x³−6x","8x³−6x+7","2x³−3x","8x⁴−6x"],"pans":0,"advanced":"For JEE Advanced, also check differentiability at piecewise points and use chain/product/implicit rules when needed."},
                {"q":"If y=(3x²+1)⁵, what is dy/dx?","choices":["30x(3x²+1)⁴","5(3x²+1)⁴","15x(3x²+1)⁴","30x(3x²+1)⁵"],"ans":0,"reason":"A likely gap is the chain rule: differentiate the outer power and multiply by the derivative of the inner expression.","hint":"If y=[u(x)]⁵, then y′=5[u(x)]⁴·u′(x).","practice":"Differentiate (2x+1)⁴.","pchoices":["8(2x+1)³","4(2x+1)³","8(2x+1)⁴","(2x+1)³"],"pans":0,"advanced":"Next challenge: combine chain rule with product/quotient or implicit differentiation."}
            ],
            "Integration": [
                {"q":"Evaluate ∫(3x²−4x+2) dx.","choices":["x³−2x²+2x+C","6x−4+C","x³−2x²+2+C","x³−4x²+2x+C"],"ans":0,"reason":"A likely gap is the reverse power rule: increase the exponent by one, then divide by the new exponent.","hint":"∫xⁿ dx = xⁿ⁺¹/(n+1)+C for n≠−1. Integrate each term separately.","practice":"Evaluate ∫(4x³+2x) dx.","pchoices":["x⁴+x²+C","12x²+2+C","x⁴+2x²+C","4x⁴+x²+C"],"pans":0,"advanced":"Next challenge: choose substitution, parts, partial fractions, or symmetry based on the integrand."},
                {"q":"Which is ∫2x·cos(x²) dx?","choices":["sin(x²)+C","2sin(x²)+C","−sin(x²)+C","x²sin(x²)+C"],"ans":0,"reason":"A likely gap is recognising substitution: the derivative of the inner expression x² is present as a factor.","hint":"Set u=x², so du=2x dx. Then integrate cos(u) du.","practice":"Evaluate ∫3x²·e^(x³) dx.","pchoices":["e^(x³)+C","3e^(x³)+C","x³e^(x³)+C","e^(3x²)+C"],"pans":0,"advanced":"For JEE Advanced, practise choosing substitutions and combining methods, not just identifying patterns."}
            ],
            "Limits and Continuity": [
                {"q":"Evaluate lim(x→2) (x²−4)/(x−2).","choices":["4","0","2","Does not exist"],"ans":0,"reason":"A likely gap is simplifying a 0/0 form before substituting.","hint":"Factor x²−4=(x−2)(x+2), cancel x−2 for x≠2, then take the limit.","practice":"Evaluate lim(x→3) (x²−9)/(x−3).","pchoices":["6","3","0","Does not exist"],"pans":0,"advanced":"Advanced follow-up: investigate one-sided limits and parameter-based continuity."}
            ],
            "Application of Derivatives": [
                {"q":"At an interior local maximum of a differentiable function, which condition is necessary?","choices":["f′(a)=0","f′′(a)>0 always","f(a)=0","f′(a)=1"],"ans":0,"reason":"You may be confusing the stationary-point condition with the second-derivative test.","hint":"At an interior extremum, Fermat's theorem gives f′(a)=0 when the derivative exists. This alone does not guarantee a maximum.","practice":"For f(x)=x², what does f′(0)=0 tell you?","pchoices":["It is a stationary point; here it is a minimum","It is definitely a maximum","f(0)=0 is required","No conclusion that it is stationary"],"pans":0,"advanced":"Advanced follow-up: classify stationary points using sign changes or higher derivatives."}
            ],
            "Definite Integral and Area": [
                {"q":"What does ∫ₐᵇ f(x) dx represent geometrically?","choices":["Signed area between curve and x-axis","Always the total positive area","Slope of the curve","Always the length of the curve"],"ans":0,"reason":"A likely gap is confusing signed area with total geometric area.","hint":"Regions below the x-axis contribute negatively to a definite integral.","practice":"If f(x)≤0 on [a,b], what is true about ∫ₐᵇ f(x)dx?","pchoices":["It is ≤0","It is ≥0","It must be 0","It is undefined"],"pans":0,"advanced":"Advanced follow-up: split at intersections and use symmetry or properties of definite integrals."}
            ],
            "Differential Equations": [
                {"q":"The order of (dy/dx)² + y = x is:","choices":["1","2","3","Cannot determine"],"ans":0,"reason":"Order is the highest derivative present, not the power to which that derivative is raised.","hint":"The highest derivative is dy/dx, which is first order even though it is squared.","practice":"What is the order of d²y/dx² + (dy/dx)³ = 0?","pchoices":["2","3","1","6"],"pans":0,"advanced":"Advanced follow-up: practise degree, order, and formation/solution of differential equations."}
            ]
        }
        question_set = banks[topic]
        if level == "JEE Advanced":
            st.caption("Advanced mode emphasises reasoning and multi-step follow-ups. This starter question bank is a foundation; broader Advanced coverage can be added topic-wise.")
        q_index = st.selectbox("Diagnostic question", list(range(1, len(question_set)+1)), format_func=lambda i: f"Question {i}", key=f"diag_index_{topic}") - 1
        qdata = question_set[q_index]
        st.markdown(f"#### 🧪 Diagnostic test — {topic}")
        st.write(qdata["q"])
        answer = st.radio("Choose your answer", qdata["choices"], key=f"diag_answer_{topic}_{q_index}")
        if st.button("Check my understanding", type="primary", key=f"diag_submit_{topic}_{q_index}"):
            is_correct = qdata["choices"].index(answer) == qdata["ans"]
            st.session_state[f"diag_result_{topic}_{q_index}"] = is_correct
            st.session_state[f"diag_reason_{topic}_{q_index}"] = "correct" if is_correct else "needs_practice"
        result_key = f"diag_result_{topic}_{q_index}"
        if result_key in st.session_state:
            if st.session_state[result_key]:
                st.success("Correct! Your answer is right for this question. Try the follow-up to confirm mastery.")
            else:
                st.warning("Not quite. We won't reveal a full solution immediately; first, let's target the concept that may be causing the mistake.")
                st.markdown("**Likely reason to check:** " + qdata["reason"])
                st.markdown("**Short concept reminder:** " + qdata["hint"])
            st.markdown("### 🎯 Targeted practice — try without looking up the answer")
            st.write(qdata["practice"])
            practice_answer = st.radio("Follow-up answer", qdata["pchoices"], key=f"practice_answer_{topic}_{q_index}")
            if st.button("Check practice", type="primary", key=f"practice_submit_{topic}_{q_index}"):
                practice_ok = qdata["pchoices"].index(practice_answer) == qdata["pans"]
                st.session_state[f"practice_result_{topic}_{q_index}"] = practice_ok
            practice_key = f"practice_result_{topic}_{q_index}"
            if practice_key in st.session_state:
                if st.session_state[practice_key]:
                    st.success("Practice correct! You are improving. Move to another diagnostic question to verify the concept again.")
                    if level == "JEE Advanced": st.info(qdata["advanced"])
                else:
                    st.warning("The concept may not be secure yet. Re-read the short reminder and retry with a fresh question before moving on.")
                    st.write("**Reminder:** " + qdata["hint"])
            st.caption("Mastery is not declared from one answer: use multiple questions and varied problems to confirm understanding.")

        st.markdown("---")
        st.markdown("### 📚 Topic roadmap")
        if topic == "Differentiation":
            st.write("Limits of difference quotients → standard derivatives → chain/product/quotient rules → implicit and logarithmic differentiation → higher derivatives → tangents/normals → monotonicity and extrema → JEE mixed problems.")
        elif topic == "Integration":
            st.write("Antiderivatives → standard integrals → substitution → integration by parts → partial fractions → definite-integral properties → area under/between curves → JEE mixed problems.")
        else:
            st.write("Concept check → core rules → worked micro-example → targeted practice → mixed JEE Main/Advanced questions → readiness reassessment.")
        st.markdown("### 📈 Need visual exploration?")
        st.write("Open the separate **Graph Studio** tab to plot functions, compare curves, zoom/pan, and use the existing graph analysis tools. The graph workspace remains independent of this topic-wise test flow.")

    st.markdown('<div style="text-align:center;color:#64748b;font-size:.82rem;padding:1rem 0;">MathDil MDX · Mathematics Discovery eXperience</div>', unsafe_allow_html=True)
