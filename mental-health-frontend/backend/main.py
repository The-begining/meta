from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils import combined_analysis, delete_user_data, predict_emotional_trends

app = FastAPI()

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class UserMessage(BaseModel):
    user_id: str
    message: str
    consent: bool = False

@app.post("/chat")
async def chat(user_message: UserMessage):
    try:
        response = combined_analysis(user_message.user_id, user_message.message)
        return {"response": response}
    except Exception as e:
        print(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete-data/{user_id}")
async def delete_data(user_id: str):
    try:
        delete_user_data(user_id)
        return {"message": "Your data has been deleted successfully."}
    except Exception as e:
        print(f"Delete Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/emotional-trends/{user_id}")
async def emotional_trends(user_id: str):
    try:
        trend = predict_emotional_trends(user_id)
        return {"trend": trend}
    except Exception as e:
        print(f"Trend Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
