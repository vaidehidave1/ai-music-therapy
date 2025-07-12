# chat_buddy.py
import streamlit as st

def chat_buddy_ui():
    st.header("💬 Chat Buddy")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for q, a in st.session_state.chat_history:
        st.markdown(f"**You:** {q}")
        st.markdown(f"**Buddy:** {a}")

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Ask me anything...", key="chat_input")
        send = st.form_submit_button("Send")

    if send and user_input:
        if "how are you" in user_input.lower():
            reply = "I'm doing great! Always here for you 😊"
        elif "hi" in user_input.lower():
            reply = "Hello how are you?"
        elif "your name" in user_input.lower():
            reply = "I'm your friendly Chat Buddy!"
        elif "sad" in user_input.lower():
            reply = "I'm sorry to hear that. I'm here for you."
        elif "fear" in user_input.lower():
            reply = "Don't worry, you will be fine."
        elif "happy" in user_input.lower():
            reply = "That's wonderful! Keep smiling! 😄"
        else:
            reply = "I might not have all the answers i am still developing myself, but I’m listening!"

        st.session_state.chat_history.append((user_input, reply))
