"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        # Sports activities
        "Soccer Team": {
            "description": "Join the school soccer team and compete in local leagues",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": []
        },
        "Basketball Club": {
            "description": "Practice basketball skills and play friendly matches",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": []
        },
        # Artistic activities
        "Drama Club": {
            "description": "Participate in school plays and improve acting skills",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": []
        },
        "Art Workshop": {
            "description": "Explore painting, drawing, and other visual arts",
            "schedule": "Fridays, 2:00 PM - 3:30 PM",
            "max_participants": 16,
            "participants": []
        },
        # Intellectual activities
        "Math Olympiad": {
            "description": "Prepare for math competitions and solve challenging problems",
            "schedule": "Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 25,
            "participants": []
        },
        "Debate Club": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Wednesdays, 4:00 PM - 5:00 PM",
            "max_participants": 14,
            "participants": []
        }
    }





# Root endpoint
@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

# Get all activities
@app.get("/activities")
def get_activities():
    return activities

# Signup for an activity
@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = activities[activity_name]
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}

# Unregister from an activity
@app.post("/activities/{activity_name}/unregister")
async def unregister_participant(activity_name: str, request: Request):
    email = None
    try:
        data = await request.json()
        email = data.get("email")
    except Exception:
        pass
    if not email:
        email = request.query_params.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found")
    activity["participants"].remove(email)
    return {"success": True, "message": f"Unregistered {email} from {activity_name}"}
