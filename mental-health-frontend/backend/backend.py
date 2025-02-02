from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI, OpenAIError
import sqlite3
from utils import predict_emotional_trends, store_location, get_heatmap_data

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load fine-tuned model
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model_path = "./fine_tuned_llama"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)
chatbot = pipeline("text-generation", model=model, tokenizer=tokenizer)

def generate_response(prompt):
    response = chatbot(prompt, max_length=150, do_sample=True, temperature=0.7)
    return response[0]['generated_text']

# API Key Configuration
api_key = os.environ.get("NEBIUS_API_KEY")
if not api_key:
    raise ValueError("NEBIUS_API_KEY not found! Set it as an environment variable.")

client = OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=api_key
)

# Database Configuration
conn = sqlite3.connect('feedback.db', check_same_thread=False)
cursor = conn.cursor()

# Create Feedback Table
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

# ✅ Create Location Data Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS location_data (
        user_id TEXT,
        latitude REAL,
        longitude REAL,
        stress_level INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()

# Data Models
class ChatMessage(BaseModel):
    user_id: str
    message: str
    consent: bool

class Feedback(BaseModel):
    user_id: str
    prompt: str
    response: str
    rating: int

class LocationData(BaseModel):
    user_id: str
    latitude: float
    longitude: float
    stress_level: int

# 🚀 Chat Endpoint
@app.post("/chat")
async def chat_response(data: ChatMessage):
    try:
        system_prompt = """
        You are an empathetic and thoughtful mental health companion. 
        Your role is to actively listen, understand the user's emotions, and create a safe, supportive environment. 

        Guidelines:
        1. Respond with compassion, validating the user's feelings without judgment.
        2. Ask thoughtful, open-ended follow-up questions to encourage deeper reflection.
        3. Keep responses concise—no more than 2 sentences unless the user requests more detail.
        4. If the user shares a struggle, acknowledge it and gently guide them with supportive suggestions.
        5. Use the user's previous messages to personalize your responses.

        Example Responses:
        - "That sounds overwhelming. How are you coping with it right now?"
        - "I hear that you're feeling anxious. What do you think is contributing to that?"
        - "It’s okay to feel this way. Would you like to talk more about what’s been on your mind?"
        """

        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct-fast",
            temperature=0.6,
            top_p=0.9,
            max_tokens=150,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": data.message}
            ]
        )

        llama_reply = response.choices[0].message.content

    except Exception as e:
        llama_reply = "Sorry, something went wrong."

    return {"response": llama_reply}

# ✅ Feedback Endpoint
@app.post("/feedback")
async def feedback(data: Feedback):
    try:
        cursor.execute('''
            INSERT INTO feedback (user_id, prompt, response, rating)
            VALUES (?, ?, ?, ?)
        ''', (data.user_id, data.prompt, data.response, data.rating))
        conn.commit()
        print(f"✅ Feedback received from {data.user_id}")
        return {"message": "Feedback recorded successfully!"}
    except Exception as e:
        print("⚠️ Feedback Error:", e)
        return {"error": "Failed to record feedback."}

# ✅ Emotional Trends Endpoint
@app.get("/emotional-trends/{user_id}")
async def emotional_trends(user_id: str):
    try:
        trend = predict_emotional_trends(user_id)
        return {"trend": trend}
    except Exception as e:
        print(f"Trend Error: {e}")
        return {"trend": "Unable to fetch emotional trends at the moment."}

# ✅ Location Tracking Endpoint
@app.post("/location")
async def save_location(data: LocationData):
    try:
        store_location(data.user_id, data.latitude, data.longitude, data.stress_level)
        return {"status": "Location data saved!"}
    except Exception as e:
        print("⚠️ Location Save Error:", e)
        return {"error": "Failed to save location data."}

# ✅ Heat Map Data Endpoint
@app.get("/heatmap")
async def heatmap_data():
    try:
        heatmap = get_heatmap_data()
        return {"heatmap": heatmap}
    except Exception as e:
        print(f"Heatmap Error: {e}")
        return {"error": "Failed to fetch heatmap data."}

# Root Endpoint
@app.get("/")
async def root():
    return {"message": "Mental Health Chatbot with LLaMA is running!"}
