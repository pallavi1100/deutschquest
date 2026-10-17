"""DeutschQuest v0.2 — playable A1 missions with a game-style character lobby.

Run on Render: streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true
"""

import html
import streamlit as st
from lessons import MISSIONS

st.set_page_config(page_title="DeutschQuest · A1 Adventure", page_icon="🎮", layout="wide")

STYLES = """
<style>
.stApp {
  background:
    radial-gradient(ellipse at 17% 14%, rgba(0,219,255,.18) 0, transparent 31%),
    radial-gradient(ellipse at 85% 18%, rgba(232,65,248,.14) 0, transparent 34%),
    radial-gradient(ellipse at 48% 95%, rgba(60,85,255,.12) 0, transparent 44%),
    #090b16;
  color:#f4f2ff;
}
.block-container { max-width: 1120px; padding-top: 2.0rem; padding-bottom: 4rem; }
[data-testid="stHeader"] { background: transparent; }
h1,h2,h3 { color: #f8f7ff !important; }
p, label, [data-testid="stMarkdownContainer"] { color: #d7d7ec; }
.stButton > button {
  background:linear-gradient(120deg,#16263b,#19172d);
  color:#fff; border:1px solid rgba(73,221,252,.42);
  border-radius:13px; padding:.65rem 1rem; font-weight:700;
  transition:all .2s ease; width:100%;
}
.stButton > button:hover:not(:disabled) {
  border-color:#45edfa; background:#19374d; color:white;
  box-shadow:0 0 18px rgba(19,216,245,.24);
}
.stButton > button:disabled { opacity:.48; cursor:not-allowed; }
[data-testid="stRadio"] { background:#11172b; padding:18px 22px; border-radius:16px; border:1px solid #2e3451; }
[data-testid="stRadio"] label { padding:6px 0; }
[data-testid="stProgress"] { margin-top:4px; }
[data-testid="stAlert"] { border-radius:12px; }
.eyebrow { text-align:center; color:#40e3ff; font-size:12px; letter-spacing:5px; font-weight:800; margin:10px 0; }
.game-title { color:#fff; font-size:clamp(35px,5vw,58px); text-align:center; font-weight:900; line-height:1.1; margin:14px 0 4px; }
.game-sub { color:#a4abc7; text-align:center; font-size:16px; margin:6px 0 28px; }
.small-label { color:#69e6ff; font-size:12px; text-transform:uppercase; letter-spacing:2px; font-weight:900; margin:5px 0 10px; }
.character-card {
  background:linear-gradient(155deg,rgba(21,36,62,.96),rgba(15,13,34,.98));
  border:2px solid var(--accent); border-radius:20px; overflow:hidden;
  min-height:305px; box-shadow:0 0 28px color-mix(in srgb,var(--accent) 19%, transparent);
  text-align:center; padding:16px 14px; margin-top:5px;
}
.character-card.side {opacity:.75; transform:scale(.92); border-width:1px;}
.avatar {font-size:112px; line-height:1.5; filter: drop-shadow(0 0 20px var(--accent)); animation:bob 2.8s ease-in-out infinite;}
.character-card.side .avatar {font-size:86px;}
.character-name {font-size:25px; color:#fff; font-weight:900; letter-spacing:1px;}
.character-role {font-size:11px; font-weight:800; letter-spacing:3px; color:var(--accent); margin:5px 0 14px;}
.skill-pill {display:inline-block; padding:4px 10px; border-radius:99px; font-size:11px; color:#bdebf2; background:#182e46; border:1px solid #34617b;}
@keyframes bob {0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.mission-card {background:linear-gradient(100deg,#151f36,#151329); border:1px solid #303956; padding:17px 20px; border-radius:15px; margin:6px 0; min-height:126px;}
.mission-card.locked {opacity:.50;}
.mission-title {color:#fff; font-size:19px; font-weight:800; margin-bottom:4px;}
.mission-sub {color:#a8b1ce; font-size:14px;}
.mission-grammar {color:#56d6e7; font-size:12px; margin-top:11px;}
.game-panel {background:#121a30; border:1px solid #304562; border-radius:15px; padding:20px 22px; margin:14px 0;}
.grammar-panel {background:linear-gradient(115deg,#122d33,#17213c); border-left:4px solid #46e0cd; border-radius:12px; padding:19px; margin:12px 0;}
.score-card {border:1px solid #364663; background:rgba(18,29,49,.9);border-radius:12px;padding:10px 14px; text-align:center;color:#e8efff;}
.score-card strong {font-size:23px;color:white;}
@media(max-width:680px) { .avatar {font-size:65px} .character-card{min-height:250px;padding:10px 4px;} .character-name{font-size:17px} .character-card.side .avatar{font-size:50px} .character-role{font-size:9px; letter-spacing:1px;} .block-container{padding-top:1.2rem;} }
</style>
"""
st.markdown(STYLES, unsafe_allow_html=True)

HEROES = [
    {"name": "LENA", "role": "THE EXPLORER", "avatar": "🧑‍🚀", "color": "#40e4fc", "skill": "Curiosity 10"},
    {"name": "MAX", "role": "THE WORD WIZARD", "avatar": "🧙", "color": "#ffa83c", "skill": "Vocabulary 10"},
    {"name": "MIA", "role": "THE STORYTELLER", "avatar": "🦸‍♀️", "color": "#f26de3", "skill": "Confidence 10"},
]

# Streamlit session state persists while the browser session is active.
DEFAULTS = {
    "screen": "lobby", "hero_idx": 0, "equipped": None, "mission_idx": 0,
    "question_idx": 0, "checked": False, "was_correct": False,
    "hearts": 5, "xp": 0, "completed": [], "awarded": [], "round_correct": 0, "attempt": 0,
}
for key, default in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = default


def go(screen):
    st.session_state.screen = screen
    st.rerun()


def start_mission(index):
    if index > 0 and MISSIONS[index - 1]["id"] not in st.session_state.completed:
        return
