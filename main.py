from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.templating import Jinja2Templates
import requests


class TalkApplication(BaseModel):
    name: str
    email: str
    topic: Optional[str] = None


app = FastAPI()

# allow cross origin access while in development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://pythonwa.com",
        "http://www.pythonwa.com",
        "https://pythonwa.com",
        "https://www.pythonwa.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/talks/future")
def talks_future():
    response = requests.get("https://api.meetup.com/Perth-Django-Users-Group/events/")
    if response.status_code == 200:
        data = response.json()
        sorted_data = sorted(data, key=lambda d: d["time"])
        events = []
        for event in sorted_data:
            events.append(
                {
                    "name": event["name"],
                    "time": event["time"],
                    "venue": event.get("venue", ""),
                    "attendance": event["yes_rsvp_count"],
                    "description": event["description"],
                    "link": event["link"],
                }
            )
    return events


@app.post("/api/talks/apply")
def talks_apply(application: TalkApplication):
    return application


templates = Jinja2Templates(directory="frontend/dist")


@app.get("/")
def index():
    return templates.TemplateResponse("index.html", {"request": {}})


app.mount("/", StaticFiles(directory="frontend/dist"), name="static")
