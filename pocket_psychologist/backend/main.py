from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
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

# Chat Route
@app.post("/chat")
async def chat_response(data: ChatMessage):
    from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

    model_name = "meta-llama/Llama-3.3-70B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    chatbot = pipeline("text-generation", model=model, tokenizer=tokenizer)

    system_prompt = """
    Du er en empatisk og lyttende psykolog. Din rolle er å forstå brukerens følelser.
    Still åpne spørsmål og gi korte svar (maks 2 setninger) med ekte interesse for brukerens historie.
    """

    response = chatbot(system_prompt + data.message, max_length=150, do_sample=True, temperature=0.7)
    reply = response[0]['generated_text']

    return {"response": reply}

# Location Tracking
@app.post("/location")
async def save_location(data: LocationData):
    store_location(data.user_id, data.latitude, data.longitude, data.stress_level)
    return {"status": "Location saved!"}

# Heatmap Data
@app.get("/heatmap")
async def heatmap_data():
    data = get_heatmap_data()
    return {"heatmap": data}

# Feedback Submission
@app.post("/feedback")
async def feedback(data: Feedback):
    store_feedback(data.user_id, data.prompt, data.response, data.rating)
    return {"message": "Feedback saved!"}

# Emotional Trends
@app.get("/emotional-trends/{user_id}")
async def emotional_trends(user_id: str):
    trend = predict_emotional_trends(user_id)
    return {"trend": trend}
