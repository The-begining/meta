from fastapi import FastAPI, Request
import json

app = FastAPI()

# In-memory data stores
feedback_data = []
user_profiles = {}
knowledge_graph = {
    "anxiety": {
        "symptoms": ["racing heart", "sweating", "nervousness"],
        "coping": ["deep breathing", "mindfulness", "progressive relaxation"]
    },
    "stress": {
        "symptoms": ["irritability", "fatigue", "sleep issues"],
        "coping": ["time management", "exercise", "talking to a friend"]
    }
}

# 1. Cognitive Behavioral Therapy (CBT) Detection
def detect_cognitive_distortion(message):
    distortions = {
        "all-or-nothing": ["always", "never", "completely"],
        "overgeneralization": ["everyone", "nobody", "everything"],
        "catastrophizing": ["disaster", "ruined", "hopeless"]
    }
    for distortion, keywords in distortions.items():
        if any(word in message.lower() for word in keywords):
            return distortion
    return None

def cbt_reframe(distortion):
    strategies = {
        "all-or-nothing": "Try to see the shades of gray in the situation. What small successes can you identify?",
        "overgeneralization": "Is this really true in every case? Can you think of exceptions?",
        "catastrophizing": "What’s the worst that could realistically happen? How would you handle it?"
    }
    return strategies.get(distortion, "Let's explore this further together.")

@app.post("/cbt")
async def cbt_support(request: Request):
    data = await request.json()
    message = data.get("message", "")
    distortion = detect_cognitive_distortion(message)
    if distortion:
        return {"response": cbt_reframe(distortion)}
    else:
        return {"response": "Tell me more about how you're feeling."}

# 2. Knowledge Graph for Mental Health Topics
@app.post("/knowledge")
async def knowledge_base(request: Request):
    data = await request.json()
    topic = data.get("topic", "").lower()
    if topic in knowledge_graph:
        return {
            "response": f"Common symptoms include {', '.join(knowledge_graph[topic]['symptoms'])}. Coping strategies: {', '.join(knowledge_graph[topic]['coping'])}."
        }
    return {"response": "Tell me more about your concern so I can assist you better."}

# 3. Adaptive User Profiles
@app.post("/update_profile")
async def update_profile(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    preference = data.get("preference")

    if user_id not in user_profiles:
        user_profiles[user_id] = {"preferences": []}
    user_profiles[user_id]["preferences"].append(preference)

    return {"status": "Profile updated!"}

@app.get("/get_profile/{user_id}")
async def get_profile(user_id: str):
    profile = user_profiles.get(user_id, {"preferences": []})
    return {"profile": profile}

# 4. Crisis Detection System
@app.post("/crisis_check")
async def crisis_check(request: Request):
    data = await request.json()
    message = data.get("message", "").lower()
    crisis_keywords = ["suicide", "kill myself", "can't go on", "end it all"]

    if any(kw in message for kw in crisis_keywords):
        return {
            "response": "It sounds like you're going through a very difficult time. If you are in immediate danger, please contact emergency services or reach out to a crisis helpline: 988 (Suicide & Crisis Lifeline)."
        }
    return {"response": "I'm here to listen. Tell me more about what you're feeling."}

# 5. Feedback Collection for RLHF
@app.post("/feedback")
async def collect_feedback(request: Request):
    data = await request.json()
    feedback_data.append(data)
    with open("feedback.json", "w") as f:
        json.dump(feedback_data, f)
    return {"status": "Feedback received!"}
