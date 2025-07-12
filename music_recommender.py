# music_recommender.py

def get_music_recommendation(emotion, goal="Therapy"):
    music_library = {
        "happy": {
            "Focus": "https://www.youtube.com/watch?v=hHW1oY26kxQ",
            "Sleep": "https://www.youtube.com/watch?v=1ZYbU82GVz4",
            "Healing": "https://www.youtube.com/watch?v=8T9SV5Wf9n8",
            "Therapy": "https://www.youtube.com/watch?v=fLexgOxsZu0"
        },
        "sadness": {
            "Focus": "https://www.youtube.com/watch?v=lTRiuFIWV54",
            "Sleep": "https://www.youtube.com/watch?v=1ZYbU82GVz4",
            "Healing": "https://www.youtube.com/watch?v=2OEL4P1Rz04",
            "Therapy": "https://www.youtube.com/watch?v=ho9rZjlsyYY"
        },
         "fear": {
            "Sleep": "https://www.youtube.com/watch?v=1ZYbU82GVz4",
            "Focus": "https://www.youtube.com/watch?v=b9t8lN1uJVI",
            "Healing": "https://www.youtube.com/watch?v=RksyMaJiD-8",
            "Therapy": "https://www.youtube.com/watch?v=aNXKjGFUlMs"
        },
        "anger": {
            "Focus": "https://www.youtube.com/watch?v=5qap5aO4i9A",
            "Sleep": "https://www.youtube.com/watch?v=1ZYbU82GVz4",
            "Healing": "https://www.youtube.com/watch?v=BOFeH2xXGnc",
            "Therapy": "https://www.youtube.com/watch?v=hlWiI4xVXKY"
        },
        "neutral": {
            "Focus": "https://www.youtube.com/watch?v=DWcJFNfaw9c",
            "Sleep": "https://www.youtube.com/watch?v=ZpT1N7XBaO8",
            "Healing": "https://www.youtube.com/watch?v=8T9SV5Wf9n8",
            "Therapy": "https://www.youtube.com/watch?v=5qap5aO4i9A"
        },
        "joy": {
            "Focus": "https://www.youtube.com/watch?v=2OEL4P1Rz04",
            "Sleep": "https://www.youtube.com/watch?v=lFcSrYw-ARY",
            "Healing": "https://www.youtube.com/watch?v=fLexgOxsZu0",
            "Therapy": "https://www.youtube.com/watch?v=ZbZSe6N_BXs"
        },
        "surprise": {
            "Focus": "https://www.youtube.com/watch?v=hHW1oY26kxQ",
            "Sleep": "https://www.youtube.com/watch?v=lFcSrYw-ARY",
            "Healing": "https://www.youtube.com/watch?v=Wv2rLZmbPMA",
            "Therapy": "https://www.youtube.com/watch?v=ZbZSe6N_BXs"
        },
        "love": {
            "Focus": "https://www.youtube.com/watch?v=DWcJFNfaw9c",
            "Sleep": "https://www.youtube.com/watch?v=ZpT1N7XBaO8",
            "Healing": "https://www.youtube.com/watch?v=450p7goxZqg",
            "Therapy": "https://www.youtube.com/watch?v=fLexgOxsZu0"
        },
    }

    # Fallbacks
    if emotion not in music_library:
        emotion = "neutral"

    if goal not in music_library[emotion]:
        goal = "Therapy"

    return music_library[emotion][goal]
