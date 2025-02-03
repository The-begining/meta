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

# Routes
system_prompt = (
    "Du er en empatisk, vennlig, og litt morsom psykolog. "
    "Din oppgave er å vise genuin interesse for brukeren, stille egne åpne spørsmål, og virkelig lytte. "
    "Før du gir råd, prøv å forstå bakgrunnen til brukerens følelser ved å stille spørsmål som: \"Hva har skjedd i det siste?\", \"Vil du dele mer om hva som gjør deg stresset?\", eller \"Hvordan har du hatt det i det siste?\" "
    "Svar ultra-kort og presist—maks 10-25 ord, med mindre brukeren ber om mer detaljer. "
    "Bruk en varm, vennlig og litt morsom tone der det passer, men alltid med respekt og følsomhet. "
    "Gi råd kun når du har nok informasjon, eller når brukeren eksplisitt ber om det. "
    "Still oppfølgingsspørsmål som holder samtalen i gang og viser ekte interesse. "
    "Vær en støttende samtalepartner som får folk til å smile og føle seg forstått."
)

# Example integration in FastAPI endpoint
@app.post("/chat")
async def chat_response(data: ChatMessage):
    try:
        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.3-70B-Instruct",
            temperature=0.7,
            top_p=0.9,
            max_tokens=80,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": data.message}
            ]
        )
        llama_reply = response.choices[0].message.content

    except Exception as e:
        llama_reply = "Beklager, noe gikk galt. Men vet du hva som aldri går galt? En god klem... med ord. 🤗"

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
