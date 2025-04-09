#getting info for the frontend, heart of the backend
from inspect import _void
import json
from dataclasses import dataclass, field
from fastapi import Response, FastAPI, HTTPException, Request
from user import *
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()
templates = Jinja2Templates(directory="../frontend")
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")


client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["db"]
collection_kanji = db["kanji"]
collection_hiragana = db["hiragana"]
collection_katakana = db["katakana"]

# Test de connexion, taper http://127.0.0.1:8080/test-db pour voir si ça marche
@app.get("/test-db")
async def test_db():
    # Tester la connexion à MongoDB
    collection = db["kanji"]
    count = await collection.count_documents({})
    return {"message": f"Connexion MongoDB réussie, documents kanji: {count}"}



@dataclass
class Kanji:
    id: int
    kanji: str
    onyomi: list[str]
    kunyomi: list[str]
    meaning: str
    JLPT: str

kanjis: dict[int, Kanji] = {}

@dataclass
class Hiragana:
    id: int
    kana: str
    romaji: str

hiraganas: dict[int, str, Hiragana] = {}

@dataclass
class Katakana:
    id: int
    kana: str
    romaji: str

katakanas: dict[int, str, Katakana] = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """return server running"""
    message = "Bienvenue sur ma page avec FastAPI et Jinja2!"

    hiragana_list = []
    cursor = collection_hiragana.find({})
    async for doc in cursor:
        doc["id"] = doc.get("id", [])
        doc["kana"] = doc.get("kana", [])
        doc["romaji"] = doc.get("romaji",[])
        doc.pop("_id", None)  # supprimer l'_id sinon Pydantic râle
        hiragana_list.append(doc)

    return templates.TemplateResponse("index.html", {"request": request, "message": message, "hiragana_list": hiragana_list})


#what frontend will have to do
@app.get("/kanji/{kanji_id}", response_model=Kanji)
def read_kanji(kanji_id: int) -> Kanji:
    """return knajis based on kanji id"""
    if kanji_id not in kanjis:
        raise HTTPException(status_code=404, detail="Kanji not found")
    return kanjis[kanji_id]



@app.get("/hiragana", response_class=HTMLResponse)
async def read_hiragana(request: Request):
    """return hiraganas based on hiragana id"""

    message = "Bienvenue sur ma page avec FastAPI et Jinja2!"
    arg_hiragana = hiraganas

    return templates.TemplateResponse("flashcard.html", {"request": request, "message": message, "hiragana": arg_hiragana})



@app.get("/katakana/{katakana_id}", response_model=Katakana)
def read_katakana(katakana_id: str) -> Katakana:
    """return katakanas based on katakana id"""
    if katakana_id not in katakanas:
        raise HTTPException(status_code=404, detail="Katakana not found")
    return katakanas[katakana_id]


@app.get("/exists/{username}", response_model=str)
def read_username(username: str) ->Response:
    """return username if username exist."""
    u = User(username=username)
    if u.username_exists():
        return Response("valid username: " + username)
    raise HTTPException(status_code=404, detail="Username not found")

#post for user sending info
@app.post("/user/add", response_model=User)
def user_add(user: User) -> User:
    """add new user."""
    try:
        user.add()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}") #returns error message of ValueError of user.py
    return user
