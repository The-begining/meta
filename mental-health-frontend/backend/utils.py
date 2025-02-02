import os
import sqlite3
import requests

# ✅ Use the correct Nebius API endpoint
NEBIUS_API_KEY = os.environ.get("NEBIUS_API_KEY")
NEBIUS_API_URL = "https://api.studio.nebius.ai/v1/chat/completions"

# Database connection
conn = sqlite3.connect('user_data.db', check_same_thread=False)
c = conn.cursor()

# ✅ Ensure the user_memory table exists
c.execute('''
    CREATE TABLE IF NOT EXISTS user_memory (
        user_id TEXT,
        key TEXT,
        value TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# ✅ Ensure the feedback table exists
c.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        prompt TEXT,
        response TEXT,
        rating INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# ✅ Create location_data table
c.execute('''
    CREATE TABLE IF NOT EXISTS location_data (
        user_id TEXT,
        latitude REAL,
        longitude REAL,
        stress_level INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()

# 🚀 Function to generate responses via Nebius API
def generate_response(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {NEBIUS_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "meta-llama/Llama-3.3-70B-Instruct",
            "max_tokens": 705,
            "temperature": 0.37,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(NEBIUS_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print(f"API Error {response.status_code}: {response.text}")
            return "Sorry, something went wrong."

    except Exception as e:
        print(f"Generate Response Error: {e}")
        return "Sorry, something went wrong."

# ✅ Combined Analysis
def combined_analysis(user_id, message):
    try:
        c.execute("SELECT key, value FROM user_memory WHERE user_id = ?", (user_id,))
        memory = dict(c.fetchall())

        prompt = f"""
        User ID: {user_id}
        Previous Context: {memory}
        Current Message: {message}
        Provide an empathetic and helpful response based on the user's history.
        """

        response = generate_response(prompt)

        # Save latest message
        c.execute("INSERT INTO user_memory (user_id, key, value) VALUES (?, ?, ?)",
                  (user_id, "last_message", message))
        conn.commit()

        # 🚀 NEW: Store sentiment (mock example)
        sentiment = "stressed" if "stress" in message.lower() else "neutral"
        c.execute("INSERT INTO user_memory (user_id, key, value) VALUES (?, ?, ?)",
                  (user_id, "sentiment", sentiment))
        conn.commit()

        return response

    except Exception as e:
        print(f"Combined Analysis Error: {e}")
        return "Sorry, something went wrong."

# ✅ Delete User Data
def delete_user_data(user_id):
    c.execute("DELETE FROM user_memory WHERE user_id = ?", (user_id,))
    conn.commit()

# ✅ Predict Emotional Trends
def predict_emotional_trends(user_id):
    c.execute("SELECT value, timestamp FROM user_memory WHERE user_id = ? AND key = 'sentiment' ORDER BY timestamp DESC", (user_id,))
    sentiments = c.fetchall()

    if len(sentiments) < 3:
        return "Not enough data to predict trends yet."

    prompt = f"Based on these sentiments over time: {sentiments}, predict emotional trends."
    return generate_response(prompt)

# ✅ Store User Feedback
def store_feedback(user_id, prompt, response, rating):
    try:
        c.execute('''
            INSERT INTO feedback (user_id, prompt, response, rating)
            VALUES (?, ?, ?, ?)
        ''', (user_id, prompt, response, rating))
        conn.commit()
        print(f"✅ Feedback stored for user {user_id}")
    except Exception as e:
        print(f"⚠️ Failed to store feedback: {e}")

# ✅ Store User Location Data
def store_location(user_id, latitude, longitude, stress_level):
    try:
        c.execute('''
            INSERT INTO location_data (user_id, latitude, longitude, stress_level)
            VALUES (?, ?, ?, ?)
        ''', (user_id, latitude, longitude, stress_level))
        conn.commit()
        print(f"✅ Location data stored for user {user_id}")
    except Exception as e:
        print(f"⚠️ Failed to store location: {e}")

# ✅ Retrieve Heat Map Data
def get_heatmap_data():
    try:
        c.execute('''
            SELECT latitude, longitude, AVG(stress_level) as avg_stress
            FROM location_data
            GROUP BY latitude, longitude
        ''')
        data = c.fetchall()
        return [{"latitude": row[0], "longitude": row[1], "avg_stress": row[2]} for row in data]
    except Exception as e:
        print(f"⚠️ Failed to fetch heatmap data: {e}")
        return []
