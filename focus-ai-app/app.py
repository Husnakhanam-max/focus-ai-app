from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        count INTEGER
    )''')

    conn.commit()
    conn.close()

init_db()

# ---------- AUTH ----------
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
              (data['username'], data['password']))

    conn.commit()
    conn.close()

    return jsonify({"message": "Signup successful"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (data['username'], data['password']))

    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login success"})
    return jsonify({"message": "Invalid credentials"}), 401


# ---------- AI PLAN ----------
@app.route('/plan', methods=['POST'])
def plan():
    data = request.json
    text = data['input'].lower()

    if "exam" in text:
        response = "Focus on important topics first. Use 25-5 Pomodoro cycles."
    elif "tired" in text:
        response = "Try shorter sessions (15 min) with quick breaks."
    elif "bored" in text:
        response = "Gamify your study. Switch subjects every session."
    else:
        response = "Start small and stay consistent."

    return jsonify({"plan": response})


# ---------- TRACK ----------
@app.route('/track', methods=['POST'])
def track():
    data = request.json
    username = data['username']

    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    c.execute("SELECT * FROM sessions WHERE username=?", (username,))
    row = c.fetchone()

    if row:
        c.execute("UPDATE sessions SET count = count + 1 WHERE username=?", (username,))
    else:
        c.execute("INSERT INTO sessions (username, count) VALUES (?, ?)", (username, 1))

    conn.commit()
    conn.close()

    return jsonify({"message": "Session saved"})


# ---------- GET STATS ----------
@app.route('/stats/<username>', methods=['GET'])
def stats(username):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    c.execute("SELECT count FROM sessions WHERE username=?", (username,))
    row = c.fetchone()

    conn.close()

    if row:
        return jsonify({"sessions": row[0]})
    return jsonify({"sessions": 0})


if __name__ == '__main__':
    import os
app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))