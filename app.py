"""DeutschQuest v0.3 — A1 adventure, 105 challenges, voice practice.

Deploy with Render: streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true
"""
import difflib
import html
import json
import random
import re
from collections import Counter

import streamlit as st
import streamlit.components.v1 as components
from bonus_lessons import EXTRA_MISSIONS, PHRASES
from lessons import MISSIONS as STARTER_MISSIONS

try:
    from streamlit_mic_recorder import speech_to_text
except ImportError:
    speech_to_text = None

MISSIONS = STARTER_MISSIONS + EXTRA_MISSIONS

st.set_page_config(page_title="DeutschQuest | Play German", page_icon="🎮", layout="wide", initial_sidebar_state="collapsed")

CSS = """
<style>
:root {color-scheme:dark;}
.stApp {background:radial-gradient(ellipse at 14% 9%,#123d54 0,transparent 28%),radial-gradient(ellipse at 88% 11%,#341b59 0,transparent 34%),radial-gradient(ellipse at 50% 100%,#101a49 0,transparent 38%),#090d1e; color:#f4f6ff;}
[data-testid="stHeader"] {background:transparent;}
[data-testid="stDecoration"] {display:none;}
.block-container {max-width:1240px; padding-top:1.2rem;padding-bottom:4rem;}
h1,h2,h3 {color:#f6f5ff !important; letter-spacing:-.03em;}
p,li,[data-testid="stMarkdownContainer"] {color:#dee4ff;}
.stButton>button {border-radius:16px; border:1px solid #5b6486;color:#fbfbff;background:linear-gradient(125deg,#272c54,#1a203b);min-height:44px;font-weight:750;transition:all .2s ease;}
.stButton>button:hover:not(:disabled) {background:#293b6c; border-color:#5fe8e3;color:white;box-shadow:0 0 23px #40ecdf30;transform:translateY(-1px);}
.stButton>button:disabled {opacity:.36;}
.stButton>button[kind="primary"] {background:linear-gradient(100deg,#6b5af1,#a14ee7);color:#fff;border:0;box-shadow:0 8px 24px #7554f433;}
[data-testid="stRadio"] {background:#151b35;border:1px solid #36416a;border-radius:20px;padding:18px 23px;}
[data-testid="stRadio"] label {padding:7px 0;}
[data-testid="stProgress"] {padding-top:6px;}
[data-testid="stAlert"] {border-radius:15px;}
[data-testid="stTextInput"] input {border-radius:12px;background:#161b33;color:#fff;}
[data-testid="stExpander"] {border-radius:14px;border-color:#465276;background:#111730;}
.arc-top {font-weight:800;color:#66edec;letter-spacing:4px;text-transform:uppercase;font-size:12px;margin:10px 0;}
.neon-title {font-weight:950;color:#fff;font-size:clamp(2.2rem,5.5vw,4.25rem);line-height:1.12;letter-spacing:-2px;margin:12px 0;}
.lead {color:#b6c4ed;font-size:1.07rem;line-height:1.65;max-width:790px;}
.frosted {background:linear-gradient(140deg,#1c2449dd,#171b35ee);border:1px solid #4c537e;border-radius:23px;padding:26px;box-shadow:0 15px 35px #0003;}
.hero-scene {position:relative; min-height:295px;border:1px solid #465577;border-radius:22px; padding:22px 16px;overflow:hidden;text-align:center;background:radial-gradient(ellipse at 50% 33%, var(--hero-glow) 0,transparent 55%),linear-gradient(155deg,#1a2044,#0e1531 72%);box-shadow:inset 0 0 30px #10192d,0 0 30px #2442ad33;}
.hero-scene:before {content:'✦  ✦  ✦';position:absolute;top:10px;left:0;width:100%;font-size:23px;letter-spacing:52px;color:#abccfd65;}
.hero-scene.side {transform:scale(.86);opacity:.76;}
.hero-scene.main {border:2px solid var(--hero-border);box-shadow:0 0 55px var(--hero-glow);}
.hero-avatar {font-size:clamp(72px,10vw,135px);filter:drop-shadow(0 8px 20px #0008);animation:float 3s ease-in-out infinite;line-height:1.6;}
.hero-name {font-size:28px;font-weight:950;color:white;letter-spacing:2px;}
.hero-class {font-size:12px;color:var(--hero-border);font-weight:800;letter-spacing:2px;}
.hero-tag {font-size:12px;color:#ebeeff;background:#212e57;border:1px solid #46618f;border-radius:30px;padding:6px 15px;display:inline-block;margin-top:15px;}
@keyframes float {0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.quest-card {background:linear-gradient(135deg,#1b2447,#151831);border:1px solid #3e4d7f;border-radius:19px;padding:20px;margin:9px 0;min-height:155px;box-shadow:0 12px 25px #0002;}
.quest-card.locked {opacity:.55;filter:grayscale(.55)}
.quest-no {color:#80dbea;font-weight:800;letter-spacing:2px;font-size:11px;}
.quest-title {font-size:20px;color:#fff;font-weight:900;margin:10px 0 4px;}
.quest-sub {color:#b0c1e0;font-size:14px;}
.quest-tag {color:#b9a6ff;font-size:12px;padding-top:10px;}
.hud {border:1px solid #405179;border-radius:16px;background:linear-gradient(120deg,#1d2951,#151b3a);padding:14px 13px;text-align:center;margin:10px 0;}
.hud-num {color:#fff;font-size:24px;font-weight:900;}
.hud-title {color:#9bc5f4;font-size:11px;font-weight:850;letter-spacing:1px;text-transform:uppercase;}
.lesson-box {background:linear-gradient(140deg,#1c2446,#181c3a);border:1px solid #415b91;border-radius:24px;padding:23px 26px;margin:12px 0;}
.grammar-box {background:linear-gradient(110deg,#154342,#1b2b4c);border:1px solid #237b7a;border-radius:18px;padding:20px 22px;margin:16px 0;line-height:1.68;}
.grammar-box strong {color:#79ffdc;}
.feedback-answer {font-size:17px;font-weight:800;color:white;margin:8px 0;}
.pill {display:inline-block;background:#212d54;color:#99ebff;border:1px solid #47668b;border-radius:15px;padding:6px 13px;font-size:12px;font-weight:900;margin:5px 4px 8px 0;}
.divider-art {height:3px;background:linear-gradient(90deg,transparent,#67f1e3,#a264ef,transparent);margin:25px 0;border-radius:3px;}
.voice-label {color:#78f5ec;letter-spacing:2px;font-weight:850;font-size:12px;text-transform:uppercase;}
.speak-phrase {font-weight:900;font-size:clamp(1.3rem,3vw,2.1rem);color:#fff;line-height:1.4;margin:10px 0;}
@media(max-width:780px) {.hero-scene{min-height:230px;padding:12px 4px}.hero-avatar{font-size:65px}.hero-name{font-size:16px}.hero-class{font-size:9px;letter-spacing:0}.hero-tag{display:none}.block-container{padding-top:1rem}.frosted{padding:15px}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

HEROES = [
    {"name": "LENA", "role": "THE EXPLORER", "avatar": "🧑‍🚀", "color": "#62eff4", "glow": "#1db8e452", "tag": "Curiosity · 100"},
    {"name": "MAX", "role": "THE WIZARD", "avatar": "🧙‍♂️", "color": "#ffcf7c", "glow": "#ba773d54", "tag": "Grammar · 100"},
    {"name": "MIA", "role": "THE STORYTELLER", "avatar": "🦸‍♀️", "color": "#fa91eb", "glow": "#da4ed553", "tag": "Confidence · 100"},
]
DEFAULTS = {
    "screen": "lobby", "hero_idx": 0, "hero": None, "xp": 0,
    "completed": [], "awarded": [], "practice_mode": False,
    "mission_idx": 0, "question_idx": 0, "checked": False,
    "was_correct": False, "round_correct": 0, "hearts": 5,
    "attempt": 0, "picked_words": [], "last_answer": "",
    "voice_idx": 0, "voice_result": "", "voice_best": {},
}
for key, default in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = default


def go(page):
    st.session_state.screen = page
    st.rerun()


def start_mission(index):
    if not st.session_state.practice_mode and index and MISSIONS[index - 1]["id"] not in st.session_state.completed:
        return
    st.session_state.mission_idx = index
    st.session_state.question_idx = 0
    st.session_state.hearts = 5
    st.session_state.round_correct = 0
    st.session_state.checked = False
    st.session_state.was_correct = False
    st.session_state.last_answer = ""
    st.session_state.picked_words = []
    st.session_state.attempt += 1
    go("quiz")


def clean(text):
    return re.sub(r"[^\wäöüß]+", " ", text.lower(), flags=re.UNICODE).strip()


def hero_card(hero, side=False):
    color = hero["color"]
    return f'''<div class="hero-scene {'side' if side else 'main'}" style="--hero-border:{color};--hero-glow:{hero['glow']}">
      <div class="hero-avatar">{html.escape(hero['avatar'])}</div>
      <div class="hero-name">{html.escape(hero['name'])}</div>
      <div class="hero-class">{html.escape(hero['role'])}</div>
      <div class="hero-tag">✦ {html.escape(hero['tag'])}</div></div>'''


def hud():
    for col, icon, title, value in zip(st.columns(4), ["⚡", "🏆", "🗺️", "🎭"],
                                       ["Experience", "Cleared", "A1 challenges", "Hero"],
                                       [st.session_state.xp, f"{len(st.session_state.completed)}/{len(MISSIONS)}", sum(len(m["questions"]) for m in MISSIONS), st.session_state.hero or "Guest"]):
        with col:
            st.markdown(f'<div class="hud"><div class="hud-title">{icon} {title}</div><div class="hud-num">{html.escape(str(value))}</div></div>', unsafe_allow_html=True)


def speech_buttons(phrase, key):
    # Speech synthesis happens in the user's browser after clicking a button.
    safe_js = json.dumps(phrase, ensure_ascii=False).replace("<", "\\u003c")
    components.html(f'''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"/>
    <style>body{{margin:0;background:transparent;font-family:system-ui;color:#e6edff;}}
    button{{cursor:pointer;border:1px solid #53d8d3;background:#192f56;color:#fff;font-weight:800;border-radius:14px;padding:12px 18px;margin:3px 7px 3px 0;}}
    button:hover{{background:#29548a}}</style></head><body>
    <button onclick="speak(0.88)">🔊 Hear German</button><button onclick="speak(0.63)">🐢 Hear slowly</button>
    <script>const line={safe_js}; function speak(rate){{if(!('speechSynthesis' in window)){{alert('Audio not available in this browser');return;}}
    speechSynthesis.cancel();const utter=new SpeechSynthesisUtterance(line);utter.lang='de-DE';utter.rate=rate;
    const voices=speechSynthesis.getVoices();const german=voices.find(v=>v.lang.toLowerCase().startsWith('de'));
    if(german) utter.voice=german; speechSynthesis.speak(utter);}}</script></body></html>''', height=66, scrolling=False)


def nav_bar():
    with st.container():
        c0, c1, c2, c3, c4 = st.columns([2.3, 1.1, 1.1, 1.1, 1.1], vertical_alignment="center")
        with c0:
            st.markdown('<span style="color:white;font-weight:950;font-size:23px">🎮 Deutsch<span style="color:#69f0ec">Quest</span></span>', unsafe_allow_html=True)
        for col, name, dest in [(c1, "🏠 Lobby", "lobby"), (c2, "🗺️ Quests", "map"), (c3, "🎙️ Speak", "voice"), (c4, "📈 Progress", "progress")]:
            with col:
                if st.button(name, key=f"nav_{dest}", use_container_width=True):
                    go(dest)
    st.markdown('<div class="divider-art"></div>', unsafe_allow_html=True)


def finish_answer(item, raw, correct):
    st.session_state.checked = True
    st.session_state.was_correct = correct
    st.session_state.last_answer = raw
    if correct:
        st.session_state.round_correct += 1
        unique = f"{MISSIONS[st.session_state.mission_idx]['id']}:{st.session_state.question_idx}"
        if unique not in st.session_state.awarded:
            st.session_state.awarded.append(unique)
            st.session_state.xp += 10
    else:
        st.session_state.hearts -= 1
    st.rerun()


def display_question(item, attempt_key):
    mode = item.get("mode", "choice")
    if mode == "listen":
        st.markdown('<span class="pill">🎧 Listening quest</span>', unsafe_allow_html=True)
        speech_buttons(item["listen_text"], attempt_key)
    elif mode == "order":
        st.markdown('<span class="pill">🧩 Sentence builder</span>', unsafe_allow_html=True)
    elif mode == "type":
        st.markdown('<span class="pill">✍️ Type the missing word</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="pill">🎯 Decision challenge</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="lesson-box"><div class="voice-label">YOUR CHALLENGE</div><h3>{html.escape(item["prompt"])}</h3></div>', unsafe_allow_html=True)
    if mode in ("choice", "listen"):
        options = item["options"]
        # Do not shuffle options from the original bank: answer indexes are authoritative.
        answer = st.radio("Choose your answer", options, index=None, disabled=st.session_state.checked, key=f"radio_{attempt_key}")
        if not st.session_state.checked and st.button("Check answer →", key="check_choice", type="primary", use_container_width=True):
            if answer is None:
                st.warning("Choose an answer first.")
            else:
                finish_answer(item, answer, answer == options[item["answer"]])
    elif mode == "type":
        answer = st.text_input("Type your answer", key=f"input_{attempt_key}", disabled=st.session_state.checked, placeholder=item.get("hint", "Write the missing German word"))
        if not st.session_state.checked and st.button("Check spelling →", type="primary", key="check_type", use_container_width=True):
            if not answer.strip():
                st.warning("Write your answer first.")
            else:
                finish_answer(item, answer, clean(answer) == clean(item["answer_text"]))
    elif mode == "order":
        tokens = item["tokens"]
        selected = st.session_state.picked_words
        st.write("**Your sentence:**")
        st.info(" ".join(tokens[i] for i in selected) if selected else "Tap the words below in the correct order")
        ids = [i for i in range(len(tokens)) if i not in selected]
        rng = random.Random(sum(ord(ch) for ch in item["prompt"]))
        rng.shuffle(ids)
        for start in range(0, len(ids), 4):
            cols = st.columns(4)
            for col, i in zip(cols, ids[start:start + 4]):
                with col:
                    if st.button(tokens[i], key=f"word_{attempt_key}_{i}", disabled=st.session_state.checked, use_container_width=True):
                        st.session_state.picked_words.append(i)
                        st.rerun()
        uc, cc = st.columns([1, 2])
        with uc:
            if st.button("↶ Undo", key="undo", disabled=not selected or st.session_state.checked, use_container_width=True):
                st.session_state.picked_words.pop()
                st.rerun()
        with cc:
            if not st.session_state.checked and st.button("Check sentence →", type="primary", key="check_order", use_container_width=True):
                if len(selected) != len(tokens):
                    st.warning("Use all words before checking.")
                else:
                    spoken = " ".join(tokens[i] for i in selected)
                    finish_answer(item, spoken, selected == list(range(len(tokens))))


def explain(item):
    if st.session_state.was_correct:
        st.success("✨ Richtig! Correct answer — +10 XP if it's your first time solving it.")
    else:
        right = item.get("answer_text", item.get("options", [None])[item.get("answer", 0)])
        st.error(f"Not quite! Correct answer: {right}")
        if st.session_state.last_answer:
            st.caption(f"Your answer: {st.session_state.last_answer}")
    st.markdown(f'''<div class="grammar-box"><strong>🧠 LEARN THE RULE</strong><p>{html.escape(item['grammar'])}</p>
      <strong>💬 EXAMPLE</strong><p>{html.escape(item['example'])}</p></div>''', unsafe_allow_html=True)
    with st.expander("🎙️ Practice saying the example in German"):
        phrase = item["example"].split(" — ")[0].strip()
        st.write(f"**Say:** {phrase}")
        speech_buttons(phrase, f"quiz_pron_{st.session_state.attempt}_{st.session_state.question_idx}")
        if speech_to_text is not None:
            heard = speech_to_text(language="de-DE", start_prompt="🎤 Speak the sentence", stop_prompt="⏹️ Stop speaking",
                                  just_once=True, use_container_width=True,
                                  key=f"q_speech_{st.session_state.attempt}_{st.session_state.question_idx}")
            if heard:
                match, missing = word_match(phrase, heard)
                st.write(f"**Speech recognition heard:** {heard}")
                st.write(f"**Word match:** {match}% (not an accent score)")
                if missing:
                    st.write("**Try these words again:** " + ", ".join(missing))
        else:
            st.caption("Speech recognition is unavailable until its package is installed.")


def word_match(expected, heard):
    a, b = clean(expected).split(), clean(heard).split()
    score = round(100 * difflib.SequenceMatcher(None, a, b).ratio()) if a and b else 0
    missing = list((Counter(a) - Counter(b)).elements())
    return score, missing


nav_bar()

if st.session_state.screen == "lobby":
    st.markdown('<div class="arc-top" style="text-align:center">✦ HERO SELECT · WELCOME TO YOUR NEXT LEVEL ✦</div>', unsafe_allow_html=True)
    st.markdown('<div class="neon-title" style="text-align:center">Choose your German hero</div>', unsafe_allow_html=True)
    st.markdown('<p class="lead" style="margin:0 auto 30px;text-align:center">Explore Germany like a game. Solve quests, defeat grammar bosses and train your pronunciation — all in one adventure.</p>', unsafe_allow_html=True)
    idx = st.session_state.hero_idx
    left, center, right = st.columns([1, 1.28, 1], vertical_alignment="center")
    with left:
        st.markdown(hero_card(HEROES[(idx - 1) % 3], True), unsafe_allow_html=True)
        if st.button("← Previous", key="prev", use_container_width=True):
            st.session_state.hero_idx = (idx - 1) % 3
            st.rerun()
    with center:
        st.markdown(hero_card(HEROES[idx]), unsafe_allow_html=True)
        if st.button(f"⚡ Equip {HEROES[idx]['name']} & start", type="primary", key="equip", use_container_width=True):
            st.session_state.hero = HEROES[idx]["name"]
            go("map")
    with right:
        st.markdown(hero_card(HEROES[(idx + 1) % 3], True), unsafe_allow_html=True)
        if st.button("Next →", key="next", use_container_width=True):
            st.session_state.hero_idx = (idx + 1) % 3
            st.rerun()
    st.markdown('<div class="divider-art"></div>', unsafe_allow_html=True)
    st.markdown("### 🌟 Your adventure includes")
    c1, c2, c3 = st.columns(3)
    for col, title, desc in [(c1, "🗺️ 15 story missions", "From your first hello to an A1 boss battle"),
                             (c2, "🧠 105 challenges", "Grammar, writing, word order and listening"),
                             (c3, "🎙️ Speak & improve", "Hear real German sounds and get speech-to-text feedback")]:
        with col:
            st.markdown(f'<div class="frosted"><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

elif st.session_state.screen == "map":
    st.markdown('<div class="arc-top">WORLD 01 · A1 GERMANY</div>', unsafe_allow_html=True)
    st.markdown('<div class="neon-title">🗺️ Explore your quest map</div>', unsafe_allow_html=True)
    st.markdown('<p class="lead">Each chapter is a real-life mission. The second half is harder A1+ practice — unlock it or use Free Practice to jump straight in.</p>', unsafe_allow_html=True)
    hud()
    st.session_state.practice_mode = st.toggle("🔓 Free Practice — access any A1 mission", value=st.session_state.practice_mode,
                                                help="Practice any mission without completing earlier chapters. Pass missions to earn completion badges.")
    st.markdown("### 🌱 Chapter One · First steps")
    for section, subset in [("starter", list(enumerate(MISSIONS[:5]))), ("advanced", list(enumerate(MISSIONS[5:], start=5)))]:
        if section == "advanced":
            st.markdown("### 🔥 Chapter Two · A1+ Challenge Island")
        for row_start in range(0, len(subset), 2):
            cols = st.columns(2)
            for col, (idx, mission) in zip(cols, subset[row_start:row_start+2]):
                unlocked = st.session_state.practice_mode or idx == 0 or MISSIONS[idx-1]["id"] in st.session_state.completed
                completed = mission["id"] in st.session_state.completed
                with col:
                    tag = "A1+" if idx >= 5 else "A1"
                    state = "✅ Cleared" if completed else ("🟣 Available" if unlocked else "🔒 Locked")
                    st.markdown(f'''<div class="quest-card {'locked' if not unlocked else ''}">
                        <div class="quest-no">LEVEL {idx+1:02} · {tag} · {state}</div>
                        <div class="quest-title">{mission['emoji']} {html.escape(mission['title'])}</div>
                        <div class="quest-sub">📍 {html.escape(mission['location'])} · {len(mission['questions'])} challenges</div>
                        <div class="quest-tag">📚 {html.escape(mission['grammar'])}</div></div>''', unsafe_allow_html=True)
                    if st.button("↻ Replay mission" if completed else ("⚡ Start quest" if unlocked else "🔒 Complete previous quest"),
                                 disabled=not unlocked, key=f"quest_{idx}", use_container_width=True):
                        start_mission(idx)
    st.markdown("### 🎙️ Train before the next mission")
    if st.button("Open pronunciation dojo →", type="primary"):
        go("voice")
    st.caption("A2 and B1 are planned future worlds. Current lessons cover A1 and selected harder A1+ topics.")

elif st.session_state.screen == "quiz":
    mi = st.session_state.mission_idx
    mission = MISSIONS[mi]
    qi = st.session_state.question_idx
    questions = mission["questions"]
    item = questions[qi]
    st.markdown(f'<div class="arc-top">{mission["emoji"]} QUEST {mi + 1:02} / {len(MISSIONS)} · {html.escape(mission["location"])}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="neon-title">{html.escape(mission["title"])}</div>', unsafe_allow_html=True)
    st.write(mission["subtitle"])
    st.progress((qi + 1) / len(questions), text=f"Challenge {qi+1} of {len(questions)}")
    cols = st.columns(3)
    with cols[0]:
        st.markdown(f'<div class="hud"><div class="hud-title">❤️ Lives</div><div class="hud-num">{st.session_state.hearts} / 5</div></div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f'<div class="hud"><div class="hud-title">⚡ XP</div><div class="hud-num">{st.session_state.xp}</div></div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f'<div class="hud"><div class="hud-title">✅ Correct this round</div><div class="hud-num">{st.session_state.round_correct}</div></div>', unsafe_allow_html=True)
    key = f"{st.session_state.attempt}_{mi}_{qi}"
    display_question(item, key)
    if st.session_state.checked:
        explain(item)
        if st.session_state.hearts <= 0:
            st.warning("❤️ You're out of lives. Review the rule and try the mission again!")
            if st.button("↻ Restart mission", type="primary"):
                start_mission(mi)
        elif st.button("🏁 View results" if qi == len(questions)-1 else "Next challenge →", key="advance", type="primary", use_container_width=True):
            if qi == len(questions)-1:
                passed = st.session_state.round_correct >= (len(questions) * 0.6)
                if passed and mission["id"] not in st.session_state.completed:
                    st.session_state.completed.append(mission["id"])
                    st.session_state.xp += 20
                go("results")
            else:
                st.session_state.question_idx += 1
                st.session_state.checked = False
                st.session_state.picked_words = []
                st.session_state.last_answer = ""
                st.rerun()
    if st.button("← Return to quest map", key="return_map"):
        go("map")

elif st.session_state.screen == "results":
    mi = st.session_state.mission_idx
    mission = MISSIONS[mi]
    total = len(mission["questions"])
    passed = st.session_state.round_correct >= total * 0.6
    st.markdown('<div class="arc-top" style="text-align:center">✦ MISSION REPORT ✦</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="neon-title" style="text-align:center">{"🏆 QUEST COMPLETE" if passed else "💪 KEEP PRACTICING"}</div>', unsafe_allow_html=True)
    st.markdown(f'<p class="lead" style="margin:0 auto;text-align:center">{html.escape(mission["title"])} · {st.session_state.round_correct} / {total} correct</p>', unsafe_allow_html=True)
    hud()
    st.progress(st.session_state.round_correct / total, text="Accuracy this attempt")
    if passed:
        st.success("Mission passed! The next stage is available. +20 XP on your first completion.")
        if mi + 1 < len(MISSIONS) and st.button("🚀 Next mission", type="primary", use_container_width=True):
            start_mission(mi+1)
    else:
        st.warning("Earn at least 60% to unlock the next stage. Review the grammar and try again.")
    st.markdown(f'<div class="grammar-box"><strong>📚 WHAT YOU PRACTICED</strong><p>{html.escape(mission["grammar"])}</p></div>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca:
        if st.button("↻ Replay this mission", use_container_width=True):
            start_mission(mi)
    with cb:
        if st.button("🗺️ Back to map", use_container_width=True):
            go("map")

elif st.session_state.screen == "voice":
    st.markdown('<div class="arc-top">SPEAKING ZONE · FREE PRACTICE</div>', unsafe_allow_html=True)
    st.markdown('<div class="neon-title">🎙️ Pronunciation Dojo</div>', unsafe_allow_html=True)
    st.markdown('<p class="lead">Hear an everyday German sentence, repeat it using your microphone, and see which words the speech recognizer understood.</p>', unsafe_allow_html=True)
    hud()
    options = [f"{i+1:02} · {p['de']}" for i,p in enumerate(PHRASES)]
    selection = st.selectbox("Choose a speaking challenge", options, index=st.session_state.voice_idx, key=f"voice_select_{st.session_state.voice_idx}")
    idx = options.index(selection)
    if idx != st.session_state.voice_idx:
        st.session_state.voice_idx = idx
        st.session_state.voice_result = ""
        st.rerun()
    phrase = PHRASES[idx]
    st.markdown(f'''<div class="frosted"><span class="voice-label">SAY THIS IN GERMAN</span>
        <div class="speak-phrase">{html.escape(phrase['de'])}</div>
        <div class="lead">{html.escape(phrase['en'])}</div></div>''', unsafe_allow_html=True)
    st.markdown("#### 1 · Listen, then listen slowly")
    speech_buttons(phrase["de"], f"voice_{idx}")
    st.markdown("#### 2 · Say it out loud")
    st.info("Allow microphone access when Chrome asks. Speak in German, then stop the recording and wait for the recognized text.")
    if speech_to_text is None:
        st.warning("Speech recognition component is not installed yet. Check that streamlit-mic-recorder==0.0.8 is in requirements.txt.")
    else:
        heard = speech_to_text(language="de-DE", start_prompt="🎙️ Start speaking", stop_prompt="⏹️ Finish speaking",
                              just_once=True, use_container_width=True, key=f"speech_{idx}")
        if heard:
            st.session_state.voice_result = heard
    if st.session_state.voice_result:
        score, missing = word_match(phrase["de"], st.session_state.voice_result)
        st.markdown(f'<div class="hud"><div class="hud-title">WORD RECOGNITION MATCH (NOT ACCENT SCORE)</div><div class="hud-num">{score}%</div></div>', unsafe_allow_html=True)
        st.write(f'**The recognizer heard:** {st.session_state.voice_result}')
        if score >= 90:
            st.success("🌟 Your words were recognized very closely! Try again at a natural speed.")
        elif score >= 65:
            st.warning("Nearly there! Repeat slowly, then speak naturally.")
        else:
            st.warning("Let's try once more. Focus on one phrase at a time and check your mic.")
        if missing:
            st.write("**Words to practise:** " + ", ".join(missing))
        best = st.session_state.voice_best.get(idx, 0)
        st.session_state.voice_best[idx] = max(score, best)
    st.markdown(f'<div class="grammar-box"><strong>🔎 PRONUNCIATION TIP</strong><p>{html.escape(phrase["tip"])}</p></div>', unsafe_allow_html=True)
    with st.expander("🎧 Record and hear your own voice (optional)"):
        recorded = st.audio_input("Record your voice for self-review", key=f"self_audio_{idx}")
        if recorded:
            st.audio(recorded, format="audio/wav")
    st.caption("This is a speech-to-text word recognition check, not a medical, phonetic or accent assessment. The third-party speech service may process microphone audio. Browser support and German voices vary; Chrome/Edge usually work best. Do not record private information.")
    left, right = st.columns(2)
    with left:
        if st.button("← Previous phrase", disabled=idx == 0, use_container_width=True):
            st.session_state.voice_idx = idx - 1
            st.session_state.voice_result = ""
            st.rerun()
    with right:
        if st.button("Next phrase →", disabled=idx == len(PHRASES)-1, type="primary", use_container_width=True):
            st.session_state.voice_idx = idx + 1
            st.session_state.voice_result = ""
            st.rerun()

elif st.session_state.screen == "progress":
    st.markdown('<div class="arc-top">PLAYER PROFILE · ADVENTURE TRACKER</div>', unsafe_allow_html=True)
    st.markdown('<div class="neon-title">📈 Your progress</div>', unsafe_allow_html=True)
    hud()
    st.progress(len(st.session_state.completed)/len(MISSIONS), text="A1 missions completed")
    st.markdown("#### 🏅 Mission badges")
    cols = st.columns(3)
    for i,m in enumerate(MISSIONS):
        with cols[i%3]:
            done = m["id"] in st.session_state.completed
            st.markdown(f'<div class="quest-card"><div class="quest-no">{"🏅 COMPLETED" if done else "🔒 NOT YET"}</div><div class="quest-title">{m["emoji"]} {html.escape(m["title"])}</div></div>', unsafe_allow_html=True)
    st.write(f"**Speaking phrases practiced:** {len(st.session_state.voice_best)} / {len(PHRASES)}")
    st.caption("Progress is currently saved only in this browser's active Streamlit session. Permanent accounts and cloud saving are planned for a later update.")
    if st.button("🗺️ Continue adventure", type="primary"):
        go("map")
