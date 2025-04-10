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

kanjis: dict[int, str, Kanji] = {}

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

    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/hiragana", response_class=HTMLResponse)
async def read_hiragana(request: Request):
    """return hiraganas based on hiragana id"""

    hiragana_list = []
    cursor = collection_hiragana.find({})
    async for doc in cursor:
        doc["id"] = doc.get("id", [])
        doc["kana"] = doc.get("kana", [])
        doc["romaji"] = doc.get("romaji",[])
        doc.pop("_id", None)  # supprimer l'_id sinon Pydantic râle
        hiragana_list.append(doc)

    return templates.TemplateResponse("flashcard.html", {"request": request, "kana": hiragana_list})


@app.get("/katakana", response_class=HTMLResponse)
async def read_katakana(request: Request):
    """return katakana based on hiragana id"""

    katakana_list = []
    cursor = collection_katakana.find({})
    async for doc in cursor:
        doc["id"] = doc.get("id", [])
        doc["kana"] = doc.get("kana", [])
        doc["romaji"] = doc.get("romaji",[])
        doc.pop("_id", None)  # supprimer l'_id sinon Pydantic râle
        katakana_list.append(doc)

    return templates.TemplateResponse("flashcard.html", {"request": request, "kana": katakana_list})


@app.get("/kanji", response_class=HTMLResponse)
async def read_kanji(request: Request):
    """return kanji based on hiragana id"""

    return templates.TemplateResponse("kanji.html", {"request": request})

@app.get("/kanjiN5", response_class=HTMLResponse)
async def read_kanji(request: Request):
    """return kanji based on hiragana id"""

    kanji_list = []
    cursor = collection_kanji.find({})
    async for doc in cursor:
        doc["id"] = doc.get("id", [])
        doc["kanji"] = doc.get("kanji", [])
        doc["onyomi"] = doc.get("onyomi",[])
        doc["kunyomi"] = doc.get("kunyomi",[])
        doc["meaning"] = doc.get("meaning",[])
        doc["JLPT"] = doc.get("JLPT",[])
        doc.pop("_id", None)  # supprimer l'_id sinon Pydantic râle
        kanji_list.append(doc)


    return templates.TemplateResponse("flashcard.html", {"request": request, "kana": kanji_list})


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
