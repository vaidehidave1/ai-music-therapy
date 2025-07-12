# db.py

import sqlite3

def create_connection():
    conn = sqlite3.connect('emotion_data.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS emotions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        emotion TEXT,
                        goal TEXT,
                        text TEXT
                      )''')
    conn.commit()
    conn.close()

def insert_emotion(timestamp, emotion, goal, text):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO emotions (timestamp, emotion, goal, text) VALUES (?, ?, ?, ?)',
                   (timestamp, emotion, goal, text))
    conn.commit()
    conn.close()

def get_today_emotions():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emotions WHERE DATE(timestamp) = DATE('now')")
    results = cursor.fetchall()
    conn.close()
    return results
