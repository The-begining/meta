import sqlite3

# Database connection
conn = sqlite3.connect('backend/database/user_data.db', check_same_thread=False)
cursor = conn.cursor()

# Create Tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS location_data (
        user_id TEXT,
        latitude REAL,
        longitude REAL,
        stress_level INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        prompt TEXT,
        response TEXT,
        rating INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()

# Functions
def store_location(user_id, latitude, longitude, stress_level):
    cursor.execute('''
        INSERT INTO location_data (user_id, latitude, longitude, stress_level)
        VALUES (?, ?, ?, ?)
    ''', (user_id, latitude, longitude, stress_level))
    conn.commit()

def get_heatmap_data():
    cursor.execute('''
        SELECT latitude, longitude, AVG(stress_level) as avg_stress
        FROM location_data
        GROUP BY latitude, longitude
    ''')
    return [{"latitude": row[0], "longitude": row[1], "avg_stress": row[2]} for row in cursor.fetchall()]

def store_feedback(user_id, prompt, response, rating):
    cursor.execute('''
        INSERT INTO feedback (user_id, prompt, response, rating)
        VALUES (?, ?, ?, ?)
    ''', (user_id, prompt, response, rating))
    conn.commit()

def predict_emotional_trends(user_id):
    cursor.execute('SELECT rating FROM feedback WHERE user_id = ?', (user_id,))
    ratings = [r[0] for r in cursor.fetchall()]
    if len(ratings) < 3:
        return "Not enough data to predict trends yet."
    avg_rating = sum(ratings) / len(ratings)
    return "Positive" if avg_rating > 3 else "Negative"
