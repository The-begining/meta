from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from utils import store_location, get_heatmap_data, store_feedback, predict_emotional_trends

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Connection
conn = sqlite3.connect('database/user_data.db', check_same_thread=False)
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

# Data Models
class ChatMessage(BaseModel):
    user_id: str
    message: str

class LocationData(BaseModel):
    user_id: str
    latitude: float
    longitude: float
    stress_level: int

class Feedback(BaseModel):
    user_id: str
    prompt: str
    response: str
    rating: int

from utils import fetch_user_context  # ✅ Import function to retrieve user history

# Dynamic System Prompt Function
def create_dynamic_prompt(user_id, user_message):
    user_context = fetch_user_context(user_id)

    prompt = {
        "type": "text",
        "prompt": "Hei der, venn! Jeg er her for å lytte og hjelpe med alt som har vært på ditt sinne. Du kan dele så mye eller så lite du vil, og jeg vil gjøre mitt beste for å forstå og støtte deg. Hva har vært på gang som du vil snakke om?",
        "response_type": "text",
        "response_format": {
            "acknowledgment": "Jeg er så glad du delte det med meg. Det tar mye mot å snakke om {}.",
            "reflection": "Bare for å sikre at jeg forstår, du føler {} fordi {}.",
            "open_question": "Kan du fortelle meg mer om {}?",
            "empathy": "Jeg kan forestille meg hvordan {} det må være for deg. Det høres veldig tøft ut.",
            "summary": "Bare for å gjøre en oppsummering, du har følt {} fordi {}, og du sliter med {}."
        },
        "follow_up_questions": [
            {"question": "Hva har vært det hardeste med {} for deg?", "response_type": "text"},
            {"question": "Hvordan følte du når {} skjedde?", "response_type": "text"},
            {"question": "Hva tror du kan hjelpe deg å føle deg bedre om {}?", "response_type": "text"}
        ]
    }

    return prompt

# FastAPI Endpoint with Dynamic Prompt
@app.post("/chat")
async def chat_response(data: ChatMessage):
    try:
        dynamic_prompt = create_dynamic_prompt(data.user_id, data.message)

        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.3-70B-Instruct",
            temperature=0.7,
            top_p=0.9,
            max_tokens=80,
            messages=[
                {"role": "system", "content": dynamic_prompt["prompt"]},
                {"role": "user", "content": data.message}
            ]
        )
        llama_reply = response.choices[0].message.content

    except Exception as e:
        llama_reply = "Oops, something went wrong. But hey, at least it's not a spilled coffee situation, right? ☕"

    return {"response": llama_reply}

@app.post("/location")
async def save_location(data: LocationData):
    store_location(data.user_id, data.latitude, data.longitude, data.stress_level)
    return {"status": "Location saved!"}

@app.get("/heatmap")
async def heatmap_data():
    data = get_heatmap_data()
    return {"heatmap": data}

@app.post("/feedback")
async def feedback(data: Feedback):
    store_feedback(data.user_id, data.prompt, data.response, data.rating)
    return {"message": "Feedback saved!"}

@app.get("/emotional-trends/{user_id}")
async def emotional_trends(user_id: str):
    trend = predict_emotional_trends(user_id)
    return {"trend": trend}
