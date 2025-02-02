from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI, OpenAIError

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key Configuration
api_key = os.environ.get("NEBIUS_API_KEY")
if not api_key:
    raise ValueError("NEBIUS_API_KEY not found! Set it as an environment variable.")

client = OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=api_key
)

# Data Model
class ChatMessage(BaseModel):
    user_id: str
    message: str
    consent: bool

@app.post("/chat")
async def chat_response(data: ChatMessage):
    try:
        print(f"✅ Received message: {data.message}")

        # Concise, empathetic, and engaging system prompt
        system_prompt = (
    "You are a compassionate, thoughtful psychologist. "
    "Your goal is to deeply understand the user's feelings by actively listening and asking thoughtful, open-ended questions. "
    "Focus on creating a safe, supportive space where the user feels heard and understood. "
    "Do not rush to give advice. Only offer suggestions after gathering enough personal details, or if the user explicitly asks for help. "
    "Keep responses concise—no more than 2 sentences. Always respond with empathy and curiosity, showing genuine interest in the user's story."
)


        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct-fast",
            temperature=0.6,
            top_p=0.9,
            max_tokens=150,  # Limit response length
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": data.message}
            ]
        )

        print(f"🎯 API Response: {response}")
        llama_reply = response.choices[0].message.content

    except OpenAIError as e:
        print("🚨 API Error:", e)
        llama_reply = "Sorry, there was an issue connecting to the AI."

    except Exception as general_error:
        print("⚠️ General Error:", general_error)
        llama_reply = f"An unexpected error occurred: {general_error}"

    return {"response": llama_reply}




@app.get("/")
async def root():
    return {"message": "Mental Health Chatbot with LLaMA is running!"}
