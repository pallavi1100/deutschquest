# DeutschQuest v0.3 — A1 Challenge Island + Speaking Dojo

An interactive German-learning adventure built with Streamlit for deployment on Render.

## What's inside
- **15 A1/A1+ missions, 105 challenges:** keep your original 25 questions in `lessons.py` and add 80 harder ones from `bonus_lessons.py`.
- **Four question formats:** multiple choice, listen and answer, fill in the missing word, and tap words into the correct order.
- **Feedback after every question:** the correct answer, the grammar rule, and a German example.
- **Speak inside the game:** every question's explanation has optional spoken practice; the separate Pronunciation Dojo has 12 useful phrases.
- **Listen in normal speed or slowly:** relies on browser speech synthesis with `de-DE` language.
- **Voice recognition feedback:** uses `streamlit-mic-recorder` with browser-based/Google speech recognition. Scores are *transcript word matching*, not scientifically valid phonetic/accent scores.
- **New look:** neon gaming UI, animated hero lobby, quest cards, XP, hearts, replay and achievements.

## Upgrade existing GitHub/Render repository

Do not delete your existing repository. Keep the existing `lessons.py` file as-is.

1. Unzip the download.
2. In your existing `deutschquest` GitHub repository, select **Add file → Upload files**.
3. Upload the three root files **`app.py`**, **`bonus_lessons.py`**, and **`requirements.txt`** from this package. Confirm replacing `app.py` and `requirements.txt`, then **Commit changes**.
4. You do NOT need to upload `test_content.py`, `smoke_app.py` or this README for the application to run.
5. Wait for Render's new deployment to show Live. Your existing Start Command should stay:
   `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true`
6. Open your app, use Ctrl+Shift+R, choose a hero, select **Free Practice** on the map to try later missions.
7. Open **🎙️ Speak**; allow microphone access to test speech recognition in Chrome. Click Listen/Speech buttons *inside the game*, not in VS Code.

## Caveats
- The third-party speech recognition feature requires browser microphone access and may transfer speech to the browser's recognition provider. Its support depends on the device/browser and network. Normal and slow playback depends on installed/browser-provided German TTS voices.
- Word matching cannot objectively detect exact accent/phoneme pronunciation. For rigorous feedback you would need a specialized speech evaluation service, potentially paid.
- Current XP, progress and badge states are stored in an active Streamlit session; they can reset on refresh, disconnect, or service restart. Persistent login/database can be a future feature.
- This is A1 + some stretch A1+ exercises, not yet a complete CEFR accredited curriculum or A2/B1.
- Latest local checks: Python syntax compilation, 4 content tests and mock Streamlit smoke tests for all screens/modes; live Render/browser behavior not yet verified.

## Files
- `app.py` — Entire new visual game and pronunciation flow.
- `bonus_lessons.py` — 80 additional questions and 12 pronunciation phrases.
- `requirements.txt` — Streamlit and speech-recognition component.
- `test_content.py`, `smoke_app.py` — optional local content and mock UI test harness.
