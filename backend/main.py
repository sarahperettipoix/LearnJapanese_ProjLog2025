#getting info for the frontend, heart of the backend
from inspect import _void
import json
from dataclasses import dataclass, field
from fastapi import Response, FastAPI, HTTPException, Request, Form, status, Cookie
from user import *
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse
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
collection_favourites = db["favourites"]

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

@dataclass
class KanaItem(BaseModel):
    id: str
    contenu: str
    romaji: str | None = None  # si c'est un hira ou kata
    kanji: str | None = None    #si c'est un kanji


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

# Route GET : afficher le formulaire HTML
@app.get("/login", response_class=HTMLResponse)
async def get_login_form(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request, "form": "login"})
@app.post("/login")
async def post_login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = await collection_users.find_one({"username": username})
    if not user or not pwd_context.verify(password, user["hashed_password"]):
        return templates.TemplateResponse("auth.html", {
            "request": request,
            "error": "Nom d'utilisateur ou mot de passe incorrect",
            "form": "login"
        })

    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="user", value=username, httponly=True)
    return response

@app.post("/signup")
async def post_signup(request: Request, username: str = Form(...), password: str = Form(...)):
    existing_user = await collection_users.find_one({"username": username})
    if existing_user:
        return templates.TemplateResponse("auth.html", {
            "request": request,
            "error": "Nom d'utilisateur déjà pris",
            "form": "signup"
        })

    hashed_password = pwd_context.hash(password)
    await collection_users.insert_one({
        "username": username,
        "hashed_password": hashed_password
    })

    return templates.TemplateResponse("auth.html", {
        "request": request,
        "message": "Compte créé avec succès !",
        "form": "signup"
    })


@app.get("/profile")
async def profile(request: Request, user: str = Cookie(None)):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    cursor = collection_favourites.find({"username": user})
    user_favourites = []
    async for doc in cursor:
        doc.pop("_id", None)
        user_favourites.append(doc["item"])
    return templates.TemplateResponse("profile.html", {"request": request, "username": user,"favourites": user_favourites})


@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("user")
    return response


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


@app.post("/add-favourite")
async def add_favourite(request: Request):
    data = await request.json()

    # tu peux récupérer l’utilisateur via les cookies si nécessaire
    username = request.cookies.get("user", "anonymous")

    # Vérifie si ce favori existe déjà pour cet utilisateur
    #TODO C'est infernal, car il faut tester une combinaison de username et qqch en commun 
    # des hiragana et katakana, donc il faudrait une entrée commune, genre "contenu"
    # existing = await collection_favourites.find_one({
    #     "username": username,
    #     "item": data,
    # })

    # if existing:
    #     return {"message": "Déjà dans les favoris"}


    # tu ajoutes l’élément dans une collection "favourites"
    await collection_favourites.insert_one({
        "username": username,
        "item": data
    })

    return JSONResponse(content={"message": "Ajouté"}, status_code=200)