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
        # Fetch user memory
        c.execute("SELECT key, value FROM user_memory WHERE user_id = ?", (user_id,))
        memory = dict(c.fetchall())

        # Prepare the prompt for Nebius API
        prompt = f"""
        User ID: {user_id}
        Previous Context: {memory}
        Current Message: {message}
        Provide an empathetic and helpful response based on the user's history.
        """

        # Generate response
        response = generate_response(prompt)

        # Save the latest message in memory
        c.execute("INSERT INTO user_memory (user_id, key, value) VALUES (?, ?, ?)",
                  (user_id, "last_message", message))
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
