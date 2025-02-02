from fastapi import FastAPI, Request
from pydantic import BaseModel
import sqlite3
import hashlib
import random
from datetime import datetime

# Initialize FastAPI app
app = FastAPI()

# Database setup
conn = sqlite3.connect('mental_health.db', check_same_thread=False)
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    consent INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    message TEXT,
    emotion TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    area TEXT,
    stress_level INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()

# Pydantic models
class ChatRequest(BaseModel):
    user_id: str
    message: str
    consent: bool

class TrackContentRequest(BaseModel):
    user_id: str
    content: str
    location: str

# Helper functions
def anonymize_user(user_id):
    return hashlib.sha256(user_id.encode()).hexdigest()

def mock_emotion_analysis(message):
    emotions = ["happy", "sad", "anxious", "neutral", "stressed"]
    return random.choice(emotions)

# API Endpoints
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_id_hashed = anonymize_user(request.user_id)
    emotion = mock_emotion_analysis(request.message)

    # Store user consent
    cursor.execute('INSERT OR IGNORE INTO users (id, consent) VALUES (?, ?)', (user_id_hashed, int(request.consent)))

    # Store message
    cursor.execute('INSERT INTO messages (user_id, message, emotion) VALUES (?, ?, ?)',
                   (user_id_hashed, request.message, emotion))
    conn.commit()

    # Mock AI response
    ai_response = f"I sense you're feeling {emotion}. How can I support you further?"
    return {"response": ai_response, "emotion": emotion}

@app.post("/track")
async def track_content(request: TrackContentRequest):
    user_id_hashed = anonymize_user(request.user_id)
    stress_level = random.randint(1, 10)  # Mock stress level

    # Store content tracking
    cursor.execute('INSERT INTO locations (user_id, area, stress_level) VALUES (?, ?, ?)',
                   (user_id_hashed, request.location, stress_level))
    conn.commit()

    return {"status": "tracked", "stress_level": stress_level}

@app.get("/heatmap")
async def get_heatmap():
    cursor.execute('SELECT area, AVG(stress_level) as avg_stress FROM locations GROUP BY area')
    data = cursor.fetchall()
    
    heatmap_data = [{"area": row[0], "avg_stress": row[1]} for row in data]
    return {"heatmap": heatmap_data}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Run using: uvicorn mental_health_chatbot:app --reload
