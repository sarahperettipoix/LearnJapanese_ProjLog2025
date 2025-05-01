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
#pour le login
from passlib.context import CryptContext

app = FastAPI()
templates = Jinja2Templates(directory="../frontend")
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")


client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["db"]
collection_kanji = db["kanji"]
collection_hiragana = db["hiragana"]     
collection_katakana = db["katakana"]
collection_users = db["users"]

# Test de connexion, taper http://127.0.0.1:8080/test-db pour voir si ça marche
@app.get("/test-db")
async def test_db():
    # Tester la connexion à MongoDB
    collection = db["kanji"]
    count = await collection.count_documents({})
    return {"message": f"Connexion MongoDB réussie, documents kanji: {count}"}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

@dataclass
class User:
    id: int
    username: str
    password: str
    # favorites : list


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

@app.get("/kanji/{level}", response_class=HTMLResponse)
async def read_kanji_by_level(request: Request, level: str):
    """return kanji """

    # sécurité : s'assurer que level est bien N1 → N5
    valid_levels = {"N1", "N2", "N3", "N4", "N5"}
    if level.upper() not in valid_levels:
        raise HTTPException(status_code=400, detail="Invalid JLPT level")


    kanji_list = []
    cursor = collection_kanji.find({"JLPT": level.upper()})
    async for doc in cursor:
        doc["id"] = doc.get("id", [])
        doc["kanji"] = doc.get("kanji", [])
        doc["onyomi"] = doc.get("onyomi",[])
        doc["kunyomi"] = doc.get("kunyomi", [])
        doc["meaning"] = doc.get("meaning",[])
        doc["JLPT"] = doc.get("JLPT", [])
        doc.pop("_id", None)
        kanji_list.append(doc)


    return templates.TemplateResponse("flashcard.html", {"request": request, "kana": kanji_list})

# j'ai essayé de faire des fonctions pour pas devoir réécrire 2 fois le meme code, mais ça fait tout planter donc ¯\_(ツ)_/¯
@app.get("/browse", response_class=HTMLResponse)
async def browse_everything(request: Request):
    """return all"""

    hiragana_list = []
    cursor = collection_hiragana.find({})
    async for doc in cursor:
        doc["id"] = doc.get("id", [])
        doc["kana"] = doc.get("kana", [])
        doc["romaji"] = doc.get("romaji",[])
        doc.pop("_id", None)  # supprimer l'_id sinon Pydantic râle
        hiragana_list.append(doc)

    katakana_list = []
    cursor = collection_katakana.find({})
    async for doc in cursor:
        doc["id"] = doc.get("id", [])
        doc["kana"] = doc.get("kana", [])
        doc["romaji"] = doc.get("romaji",[])
        doc.pop("_id", None)  # supprimer l'_id sinon Pydantic râle
        katakana_list.append(doc)

    kanji_list = []
    cursor = collection_kanji.find({})
    async for doc in cursor:
        doc["id"] = doc.get("id", [])
        doc["kanji"] = doc.get("kanji", [])
        doc["onyomi"] = doc.get("onyomi",[])
        doc["kunyomi"] = doc.get("kunyomi", [])
        doc["meaning"] = doc.get("meaning",[])
        doc["JLPT"] = doc.get("JLPT", [])
        doc.pop("_id", None)
        kanji_list.append(doc)


    return templates.TemplateResponse("browse.html", {"request": request, "hiragana": hiragana_list, "katakana":katakana_list, "kanji":kanji_list})

""" learn html """
@app.get("/learn", response_class=HTMLResponse)
async def learn_everything(request: Request):
    return templates.TemplateResponse("learn.html", {"request": request})

""" about html """
@app.get("/about", response_class=HTMLResponse)
async def learn_everything(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/signup")
async def signup(user: User):
    existing = await collection_users.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")
    hashed_pw = pwd_context.hash(user.password)
    await collection_users.insert_one({
        "username": user.username,
        "hashed_password": hashed_pw
    })
    return {"message": "Utilisateur créé"}


@app.get("/login")
async def login(user: User):
    found = await collection_users.find_one({"username": user.username})
    if not found or not pwd_context.verify(user.password, found["hashed_password"]):
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")
    return {"message": "Connexion réussie"}



# """ login html """
# @app.get("/login", response_class=HTMLResponse)
# async def login(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})

# @app.get("/exists/{username}", response_model=str)
# def read_username(username: str) ->Response:
#     """return username if username exist."""
#     u = User(username=username)
#     if u.username_exists():
#         return Response("valid username: " + username)
#     raise HTTPException(status_code=404, detail="Username not found")

#post for user sending info
# @app.post("/user/add", response_model=User)
# def user_add(user: User) -> User:
#     """add new user."""
#     try:
#         user.add()
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=f"{e}") #returns error message of ValueError of user.py
#     return user
