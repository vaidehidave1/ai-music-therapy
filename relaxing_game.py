# relaxing_game.py
import streamlit as st
import random
def relaxing_game_ui():
    st.header("🎮 Relaxing Games")
    st.subheader("🧠 Mood Quiz")
    if "mood_quiz_score" not in st.session_state:
        st.session_state.mood_quiz_score = 0

    question = "What's your comfort activity?"
    options = ["Listening to music", "Talking to someone", "Being alone", "Sleeping"]
    answer = st.radio(question, options, key="quiz_q1")
    if st.button("Submit Answer"):
        if answer == "Listening to music":
            st.success("Great choice! Music heals the soul. 🎵")
        elif answer == "Talking to someone":
            st.success("Connecting with others is powerful. 💬")
        elif answer == "Being alone":
            st.success("Me-time is important. 🌱")
        elif answer == "Sleeping":
            st.success("Rest is essential. 💤")

        st.balloons()

    st.markdown("---")
    st.subheader("🌤 Flash Card Game")
    flashcards = {
        "What color is the sky?": "blue",
        "2 + 2 equals?": "4",
        "What do bees make?": "honey",
        "Opposite of hot?": "cold",
        "Synonym of happy?": "joyful"
    }
    if "flashcard_q" not in st.session_state:
        st.session_state.flashcard_q = random.choice(list(flashcards.keys()))

    st.write(f"**Question:** {st.session_state.flashcard_q}")
    flash_ans = st.text_input("Your Answer:", key="flash_input")
    if st.button("Check Answer"):
        correct = flashcards[st.session_state.flashcard_q].lower()
        if flash_ans.lower().strip() == correct:
            st.success("Correct! 🎉")
        else:
            st.warning(f"Oops! The correct answer is: {correct}")
        st.session_state.flashcard_q = random.choice(list(flashcards.keys()))

    st.markdown("---")
    st.subheader("🌤 Word Builder Game")
    target_word = "relax"
    st.markdown(f"Form new words from the letters of: **{target_word.upper()}**")

    user_word = st.text_input("Enter a word:", key="word_builder")
    valid_words = {"real", "axe", "ale", "lax", "ear", "are", "lex", "rex"}  # Example subset

    if st.button("Submit Word"):
        if user_word.lower() in valid_words:
            st.success(f"✅ Great! '{user_word}' is a valid word.")
        else:
            st.warning(f"❌ '{user_word}' isn't a valid word from '{target_word}'. Try again!")

    st.markdown("---")
    st.subheader("🧱 Block Blast (Mini Grid Puzzle)")
    st.write("Place blocks on the grid. Complete rows or columns to score!")

    grid_size = 5
    if "block_blast_grid" not in st.session_state:
        st.session_state.block_blast_grid = [[0]*grid_size for _ in range(grid_size)]
    if "block_blast_score" not in st.session_state:
        st.session_state.block_blast_score = 0

    def render_grid():
        for i in range(grid_size):
            cols = st.columns(grid_size)
            for j in range(grid_size):
                color = "💚" if st.session_state.block_blast_grid[i][j] else "⬜"
                with cols[j]:
                    if st.button(color, key=f"block_{i}_{j}"):
                        if st.session_state.block_blast_grid[i][j] == 0:
                            st.session_state.block_blast_grid[i][j] = 1
                            check_and_clear()

    def check_and_clear():
        score = 0
        # Clear full rows
        for i in range(grid_size):
            if all(st.session_state.block_blast_grid[i]):
                for j in range(grid_size):
                    st.session_state.block_blast_grid[i][j] = 0
                score += 10

        # Clear full columns
        for j in range(grid_size):
            if all(st.session_state.block_blast_grid[i][j] for i in range(grid_size)):
                for i in range(grid_size):
                    st.session_state.block_blast_grid[i][j] = 0
                score += 10

        st.session_state.block_blast_score += score

    render_grid()
    st.markdown(f"### 🎯 Score: {st.session_state.block_blast_score}")
