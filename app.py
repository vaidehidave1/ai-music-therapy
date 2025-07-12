# app.py
import streamlit as st
import datetime
import pandas as pd
import altair as alt
from firebase_config import auth  # Firebase Authentication
from db import create_table, insert_emotion, get_today_emotions
from emotion_detector import detect_emotion
from music_recommender import get_music_recommendation
from voice_input import get_voice_input
from chat_buddy import chat_buddy_ui  # Changed from wellness_chat to simple Chat Buddy
from relaxing_game import relaxing_game_ui

create_table()

# ----------------- EMOTION HELPERS -----------------
def get_emotion_display(emotion):
    emoji_map = {
        "happy": "😄", "joy": "😊", "sadness": "😢", "fear": "😨",
        "anger": "😠", "love": "❤️", "surprise": "😲", "neutral": "😐"
    }
    return f"{emoji_map.get(emotion, '')} {emotion.upper()}"

def get_emotion_tip(emotion):
    tips = {
        "happy": "Keep spreading your joy to others!",
        "sadness": "It's okay to feel sad. Take time to rest and reflect. 💙",
        "fear": "Take deep breaths and ground yourself. You're safe. 🧘",
        "anger": "Try releasing your anger through journaling or movement. 🔥",
        "love": "Cherish the warmth. Maybe tell someone you love them today. ❤️",
        "surprise": "Unexpected things bring growth. Stay curious. 🌱",
        "neutral": "A calm mind is a powerful thing. 🧘",
        "joy": "Let your joy be contagious! ✨"
    }
    return tips.get(emotion, "Emotions are natural. You're doing great.")

# ----------------- AUTHENTICATION -----------------
if 'user' not in st.session_state:
    st.session_state.user = None
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_ui():
    st.sidebar.title("🔐 Login or Sign Up")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.user = user
            st.session_state.logged_in = True
            st.session_state.login_message = "success"
            st.rerun()
        except:
            st.session_state.login_message = "failed"
            st.rerun()

    if st.sidebar.button("Sign Up"):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            st.session_state.user = user
            st.session_state.logged_in = True
            st.session_state.login_message = "created"
            st.rerun()
        except:
            st.session_state.login_message = "create_failed"
            st.rerun()

if not st.session_state.logged_in:
    login_ui()

    if 'login_message' in st.session_state:
        if st.session_state.login_message == "success":
            st.success("✅ Logged in successfully!")
        elif st.session_state.login_message == "failed":
            st.error("❌ Login failed. Check your credentials.")
        elif st.session_state.login_message == "created":
            st.success("✅ Account created!")
        elif st.session_state.login_message == "create_failed":
            st.error("❌ Account creation failed. Email may already exist.")
    st.stop()

# ----------------- LOGOUT OPTION -----------------
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.rerun()

# ----------------- MAIN APP -----------------
if 'emotion_log' not in st.session_state:
    st.session_state.emotion_log = []
if 'last_emotion' not in st.session_state:
    st.session_state.last_emotion = None

st.title("🎵 AI-Powered Emotion-Based Music Therapy Assistant")
tabs = st.tabs(["🎧 Therapy", "💬 Chat Buddy", "🎮 Relaxing Game", "📝 Feedback"])

with tabs[0]:
    st.write("Choose how you want to share your feelings:")
    goal = st.selectbox("🎯 What do you want help with?", ["Sleep", "Focus", "Healing", "Therapy"])
    mode = st.radio("Select Input Mode:", ["Type", "Speak"])

    if mode == "Type":
        user_input = st.text_input("How are you feeling today?", "")
        if user_input:
            emotion = detect_emotion(user_input)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_emotion(timestamp, emotion, goal, user_input)
            st.session_state.emotion_log.append({"Time": timestamp, "Emotion": emotion, "Goal": goal, "Text": user_input})
            st.session_state.last_emotion = emotion

            st.write(f"🧠 Detected Emotion: **{get_emotion_display(emotion)}**")
            st.info(get_emotion_tip(emotion))

            music_link = get_music_recommendation(emotion, goal)
            if music_link and isinstance(music_link, str):
                st.video(music_link)
            else:
                st.warning("⚠️ No valid video link found.")

    elif mode == "Speak":
        if st.button("🎤 Record Voice"):
            with st.spinner("Listening..."):
                voice_text = get_voice_input()
            st.write(f"📝 You said: **{voice_text}**")

            if "Sorry" not in voice_text:
                emotion = detect_emotion(voice_text)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                insert_emotion(timestamp, emotion, goal, voice_text)
                st.session_state.emotion_log.append({"Time": timestamp, "Emotion": emotion, "Goal": goal, "Text": voice_text})
                st.session_state.last_emotion = emotion

                st.write(f"🧠 Detected Emotion: **{get_emotion_display(emotion)}**")
                st.info(get_emotion_tip(emotion))

                music_link = get_music_recommendation(emotion, goal)
                if music_link and isinstance(music_link, str):
                    st.video(music_link)
                else:
                    st.warning("⚠️ No valid video link found.")

    st.subheader("📊 Emotion Frequency Chart")
    if st.session_state.emotion_log:
        df = pd.DataFrame(st.session_state.emotion_log)
        emotion_counts = df['Emotion'].value_counts().reset_index()
        emotion_counts.columns = ['Emotion', 'Count']

        if not emotion_counts.empty:
            chart = alt.Chart(emotion_counts).mark_bar().encode(
                x=alt.X('Emotion:N', title='Emotion'),
                y=alt.Y('Count:Q', title='Count'),
                color='Emotion:N',
                tooltip=['Emotion', 'Count']
            ).properties(width=600, height=400)

            st.altair_chart(chart, use_container_width=True)

    st.subheader("⏳ Mood Timeline")
    if st.session_state.emotion_log:
        df['Time'] = pd.to_datetime(df['Time'])
        line_chart = alt.Chart(df).mark_line(point=True).encode(
            x='Time:T', y='Emotion:N', color='Goal:N', tooltip=['Time', 'Emotion', 'Goal']
        ).properties(width=700, height=300)
        st.altair_chart(line_chart, use_container_width=True)

    st.subheader("🧠 Emotion History")
    if st.session_state.emotion_log:
        st.dataframe(st.session_state.emotion_log)

    st.subheader("📝 Reflective Journal (Optional)")
    journal = st.text_area("Write your thoughts today...")
    if journal:
        st.success("Journal saved (temporary). In future we can save it to file or cloud.")

    with st.expander("🧘 Guided Breathing Exercise"):
        st.markdown("""
        <style>
        @keyframes breathe {
            0% { transform: scale(1); opacity: 0.4; }
            50% { transform: scale(1.3); opacity: 1; }
            100% { transform: scale(1); opacity: 0.4; }
        }
        .circle {
            margin: auto;
            margin-top: 20px;
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background-color: #6c63ff;
            animation: breathe 4s infinite;
        }
        </style>
        <div class="circle"></div>
        <p style='text-align: center; font-size: 20px;'>Inhale... Exhale...</p>
        """, unsafe_allow_html=True)

    if st.session_state.emotion_log:
        df = pd.DataFrame(st.session_state.emotion_log)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Emotion Log as CSV", data=csv, file_name="emotion_log.csv", mime="text/csv")
        df.to_csv('emotion_log_saved.csv', index=False)

    st.markdown("---")
    st.subheader("📅 Today's Mood Summary")
    today_logs = get_today_emotions()

    if today_logs:
        mood_df = pd.DataFrame(today_logs, columns=["ID", "Time", "Emotion", "Goal", "Text"])
        st.dataframe(mood_df[["Time", "Emotion", "Goal", "Text"]])
        emotion_counts = mood_df["Emotion"].value_counts()
        st.success(f"🧠 Most Frequent Mood Today: {emotion_counts.idxmax().upper()} ({emotion_counts.max()} times)")
    else:
        st.info("No mood data recorded today.")

# ----------------- CHAT BUDDY -----------------
with tabs[1]:
    chat_buddy_ui()

# ----------------- FEEDBACK FORM -----------------
with tabs[3]:
    st.subheader("📝 We value your feedback!")
    feedback_text = st.text_area("Please share your thoughts or suggestions:")
    if st.button("Submit Feedback"):
        if feedback_text:
            st.success("✅ Thank you for your feedback!")
        else:
            st.warning("⚠️ Feedback cannot be empty.")
with tabs[2]:
    relaxing_game_ui()
