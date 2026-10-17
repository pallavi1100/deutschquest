
import streamlit as st

st.set_page_config(
    page_title="DeutschQuest",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 DeutschQuest")
st.subheader("Learn German through adventure!")

st.write("Your journey from A1 to B1 begins here.")

if st.button("🌱 Start A1 Adventure"):
    st.success("Welcome to your first German mission!")
