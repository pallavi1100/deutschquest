
import streamlit as st

st.set_page_config(
    page_title="DeutschQuest",
    page_icon="🎮",
    layout="wide"
)

# Remember which screen the player is on
if "page" not in st.session_state:
    st.session_state.page = "home"

# Function to change screens
def navigate(page):
    st.session_state.page = page
    st.rerun()

# SCREEN 1: HOME
if st.session_state.page == "home":

    st.title("🎮 DeutschQuest")
    st.subheader("Learn German through adventure!")

    st.write("Your journey from A1 to B1 begins here.")

    st.divider()

    st.header("🌍 Choose Your Adventure")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🌱 A1 — Beginner")
        st.write("Your first steps in Germany.")

        if st.button("Start A1 Adventure"):
            navigate("a1")

    with col2:
        st.subheader("🏙️ A2 — Elementary")
        st.write("Explore everyday German life.")
        st.button("🔒 Coming Soon", disabled=True)

    with col3:
        st.subheader("🏆 B1 — Intermediate")
        st.write("Become confident in German.")
        st.button("🔒 Locked", disabled=True)

# SCREEN 2: A1 ADVENTURE
elif st.session_state.page == "a1":

    st.title("🌱 Welcome to A1 Adventure!")

    st.write("📍 Location: Welcome Street, Germany")

    st.info("Your first mission: Introduce yourself!")

    st.subheader("🎯 Mission 1: Hallo!")

    st.write("How do you say 'My name is Anna' in German?")

    answer = st.radio(
        "Choose the correct answer:",
        [
            "Ich bin heißen Anna",
            "Ich heiße Anna",
            "Ich habe Anna"
        ],
        index=None
    )

    if st.button("Check Answer"):

        if answer == "Ich heiße Anna":
            st.success("🎉 Richtig! You earned 10 XP!")
        elif answer is None:
            st.warning("Please select an answer.")
        else:
            st.error("Try again!")

    st.divider()

    if st.button("⬅ Back to Home"):
        navigate("home")
