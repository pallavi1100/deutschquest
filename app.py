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

    st.session_state.mission_idx = index
    st.session_state.attempt += 1
    st.session_state.question_idx = 0
    st.session_state.checked = False
    st.session_state.was_correct = False
    st.session_state.round_correct = 0
    st.session_state.hearts = 5
    go("quiz")


def card(hero, side=False):
    accent = html.escape(hero["color"])
    return f"""
    <div class="character-card {'side' if side else ''}" style="--accent:{accent}">
      <div class="avatar">{html.escape(hero['avatar'])}</div>
      <div class="character-name">{html.escape(hero['name'])}</div>
      <div class="character-role">{html.escape(hero['role'])}</div>
      <span class="skill-pill">✦ {html.escape(hero['skill'])}</span>
    </div>
    """


def scoreboard():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="score-card">⭐ XP<br><strong>{st.session_state.xp}</strong></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="score-card">🏅 Completed<br><strong>{len(st.session_state.completed)}/{len(MISSIONS)}</strong></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="score-card">🧑 Hero<br><strong>{html.escape(st.session_state.equipped or "None")}</strong></div>', unsafe_allow_html=True)


if st.session_state.screen == "lobby":
    st.markdown('<div class="eyebrow">✦ DEUTSCHQUEST · HERO LOBBY ✦</div>', unsafe_allow_html=True)
    st.markdown('<div class="game-title">Choose your hero</div>', unsafe_allow_html=True)
    st.markdown('<div class="game-sub">Rotate the roster. Your German adventure starts with you.</div>', unsafe_allow_html=True)

    selected = st.session_state.hero_idx
    left, center, right = st.columns([1, 1.35, 1], vertical_alignment="center")
    with left:
        st.markdown(card(HEROES[(selected - 1) % len(HEROES)], side=True), unsafe_allow_html=True)
        if st.button("← Previous hero", key="previous"):
            st.session_state.hero_idx = (selected - 1) % len(HEROES)
            st.rerun()
    with center:
        st.markdown(card(HEROES[selected]), unsafe_allow_html=True)
        if st.button(f"⚡ Equip {HEROES[selected]['name']} & Play", key="equip"):
            st.session_state.equipped = HEROES[selected]["name"]
            go("map")
    with right:
        st.markdown(card(HEROES[(selected + 1) % len(HEROES)], side=True), unsafe_allow_html=True)
        if st.button("Next hero →", key="next"):
            st.session_state.hero_idx = (selected + 1) % len(HEROES)
            st.rerun()
    st.markdown('<div class="game-sub">A1 is playable now · A2 and B1 worlds unlock in later updates.</div>', unsafe_allow_html=True)

elif st.session_state.screen == "map":
    st.markdown('<div class="small-label">🗺️ ADVENTURE MAP · WORLD 1</div>', unsafe_allow_html=True)
    st.title("🇩🇪 Welcome to DeutschQuest")
    st.write(f"Ready, {st.session_state.equipped}? Start in Germany and learn by completing real-life missions.")
    scoreboard()
    st.markdown("### 🌱 A1 — New in Germany")
    for i, mission in enumerate(MISSIONS):
        unlocked = i == 0 or MISSIONS[i-1]["id"] in st.session_state.completed
        completed = mission["id"] in st.session_state.completed
        label = "✅ Completed" if completed else ("🎯 Play mission" if unlocked else "🔒 Locked")
        info_col, btn_col = st.columns([3.5, 1], vertical_alignment="center")
        with info_col:
            cls = "mission-card" if unlocked else "mission-card locked"
            st.markdown(f"""<div class="{cls}">
              <div class="mission-title">{mission['emoji']} {html.escape(mission['title'])}</div>
              <div class="mission-sub">📍 {html.escape(mission['location'])} — {html.escape(mission['subtitle'])}</div>
              <div class="mission-grammar">📚 {html.escape(mission['grammar'])}</div>
              </div>""", unsafe_allow_html=True)
        with btn_col:
            if st.button(label if not completed else "↻ Replay", key=f"mission_{i}", disabled=not unlocked):
                start_mission(i)
    st.markdown("### 🔒 Next worlds")
    st.write("🏙️ A2 · Living in Germany — coming later")
    st.write("🏆 B1 · Independent in Germany — coming later")
    if st.button("← Change hero"):
        go("lobby")

elif st.session_state.screen == "quiz":
    mission = MISSIONS[st.session_state.mission_idx]
    qidx = st.session_state.question_idx
    questions = mission["questions"]
    item = questions[qidx]
    st.markdown(f'<div class="small-label">{mission["emoji"]} {html.escape(mission["location"])} · A1 MISSION</div>', unsafe_allow_html=True)
    st.title(mission["title"])
    st.write(mission["subtitle"])
    st.progress((qidx + 1) / len(questions), text=f"Question {qidx + 1} of {len(questions)}")
    st.markdown(f"**❤️ Lives:** {st.session_state.hearts} / 5 · **⭐ XP:** {st.session_state.xp}")
    st.markdown(f'<div class="game-panel"><div class="small-label">CHALLENGE {qidx + 1}</div><h3>{html.escape(item["prompt"])}</h3></div>', unsafe_allow_html=True)
    answer = st.radio("Choose the best answer:", item["options"], index=None, key=f"answer_{st.session_state.attempt}_{mission['id']}_{qidx}", disabled=st.session_state.checked)

    if not st.session_state.checked:
        if st.button("✅ Check answer", key="check"):
            if answer is None:
                st.warning("Choose an answer first.")
            else:
                correct = answer == item["options"][item["answer"]]
                st.session_state.checked = True
                st.session_state.was_correct = correct
                if correct:
                    st.session_state.round_correct += 1
                    unique = f"{mission['id']}:{qidx}"
                    if unique not in st.session_state.awarded:
                        st.session_state.awarded.append(unique)
                        st.session_state.xp += 10
                else:
                    st.session_state.hearts -= 1
                st.rerun()
    else:
        if st.session_state.was_correct:
            st.success("🎉 Richtig! Correct! +10 XP (first successful completion only).")
        else:
            st.error(f"Not quite. ✅ Correct answer: {item['options'][item['answer']]}")
        st.markdown(f"""<div class="grammar-panel">
           <strong>📚 Why? Grammar explained</strong><p>{html.escape(item['grammar'])}</p>
           <strong>💬 Example</strong><p>{html.escape(item['example'])}</p>
           </div>""", unsafe_allow_html=True)
        if st.session_state.hearts == 0:
            st.warning("Your five lives are used up. Review the explanations and try again!")
            if st.button("🔁 Retry mission"):
                start_mission(st.session_state.mission_idx)
        else:
            if st.button("Finish mission 🏆" if qidx == len(questions)-1 else "Next question →", key="advance"):
                if qidx == len(questions)-1:
                    if mission["id"] not in st.session_state.completed:
                        st.session_state.completed.append(mission["id"])
                        st.session_state.xp += 20
                    go("results")
                else:
                    st.session_state.question_idx += 1
                    st.session_state.checked = False
                    st.session_state.was_correct = False
                    st.rerun()
    if st.button("← Adventure map"):
        go("map")

elif st.session_state.screen == "results":
    mission = MISSIONS[st.session_state.mission_idx]
    st.markdown('<div class="eyebrow">✦ LEVEL COMPLETE ✦</div>', unsafe_allow_html=True)
    st.markdown('<div class="game-title">🏆 Mission cleared!</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="game-sub">{html.escape(mission["title"])} — {st.session_state.round_correct} out of {len(mission["questions"])} correct this round.</div>', unsafe_allow_html=True)
    scoreboard()
    st.markdown(f'<div class="grammar-panel"><strong>🧠 Grammar mastered in this mission</strong><p>{html.escape(mission["grammar"])}</p></div>', unsafe_allow_html=True)
    if st.session_state.mission_idx < len(MISSIONS) - 1:
        if st.button("🚀 Start next mission"):
            start_mission(st.session_state.mission_idx + 1)
    if st.button("🗺️ Back to adventure map"):
        go("map")
