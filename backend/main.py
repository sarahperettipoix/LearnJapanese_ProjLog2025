"""
    Module principal de l'application backend pour un site d'apprentissage du japonais.

    Ce module implémente : 
    - Les routes FastAPI pour le frontend
    - La gestion des utilisateurs (login/signup)
    - L'accès aux données des kanas (hiragana, katakana) et kanjis
    - Le système de favoris

    Dépendances principales :
     - FastAPI : framework web
     - Motor : client MongoDB asynchrone
     - Passlib  : gestion du hachage des mots de passe
"""
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
    """
    Teste la connexion à la base de données MongoDB.

    Returns:
        dict: Message confirmant la connexion et le nombre de documents dans la collection kanji
    """
    # Tester la connexion à MongoDB
    collection = db["kanji"]
    count = await collection.count_documents({})
    return {"message": f"Connexion MongoDB réussie, documents kanji: {count}"}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@dataclass
class Kanji:
    """
    Représente un kanji avec ses propriétés.

    Attributes:
        id (int):  Identifiant un kanji
        kanji (str) : Caractère kanji
        onyomi(list[str]) : Lectures on'yomi(chinoise)
        kunyomi(list[str]) : Lectures kun'yomi (japonaise)
        JLPT (str) : Niveau JLPT (N1 à N5)
    """
    id: int
    kanji: str
    onyomi: list[str]
    kunyomi: list[str]
    meaning: str
    JLPT: str

kanjis: dict[int, str, Kanji] = {}

@dataclass
class Hiragana:
    """
    Représente un caractère hiragana.
    
    Attributes:
        id (int): Identifiant unique
        kana (str): Caractère hiragana
        romaji (str): Transcription en romaji
    """
    id: int
    kana: str
    romaji: str

hiraganas: dict[int, str, Hiragana] = {}

@dataclass
class Katakana:
    """
    Représente un caractère katakana.
    
    Attributes:
        id (int): Identifiant unique
        kana (str): Caractère katakana
        romaji (str): Transcription en romaji
    """
    id: int
    kana: str
    romaji: str

katakanas: dict[int, str, Katakana] = {}

@dataclass
class User:
    """
    Représente un utilisateur du système.

    Attributes : 
        id (int): Identifiant unique
        username (str): Nom d'utilisateur
        password (str): Mot de passe hashé
    """
    id: int
    username: str
    password: str
    # favorites : list

@dataclass
class KanaItem(BaseModel):
    """
    Modèle Pydantic pour les items kana (hiragana/katakana/kanji).

    Attributes:
        id (str): Identifiant
        contenu (str) : Caractère japonais
        romaji (str, optional): Caractère kanji si applicable
    """
    id: str
    contenu: str
    romaji: str | None = None  # si c'est un hira ou kata
    kanji: str | None = None    #si c'est un kanji


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Route racine qui retourne la page d'accueil

    Args : 
        request (Request): Objet requête FastAPI
    
    Returns:
        TemplateResponse: Page index.html
    """
    #"""return server running"""

    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/hiragana", response_class=HTMLResponse)
async def read_hiragana(request: Request):
    """
    Retourne tous les hiraganas depuis la base de données.

    Args : 
        request (Request): Objet requête FastAPI
    
    Returns : 
        TemplateResponse: Page flashcard.html avec la liste des hiraganas
    """
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
    """
    Retourne tous les katakanas depuis la base de données

    Args : 
        request (Request): Objet requête FastAPI

    Returns:
        TemplateResponse: Page flashcard.html avec la liste de katakanas
    """
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
    """
    Retourne la page des kanjis (sans données)

    Args: 
        request (Request): Objet requête FastAPI
    
    Returns: 
        TemplateResponse: Page kanji.html
    """
    return templates.TemplateResponse("kanji.html", {"request": request})

@app.get("/kanji/{level}", response_class=HTMLResponse)
async def read_kanji_by_level(request: Request, level: str):
    """
    Retourne les kanjis filtrés par niveau JLPT.

    Args : 
        request (Request): Objet requête FastAPI
        level (str): Niveau JLPT (N1 à N5)

    Returns : 
        TemplateResponse : Pafe flashcard.html avec les kanjis du niveau
    Raises : 
        HTTPException: Si le niveau n'est pas valide
    """
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
    """
    Retourne toutes les données (hiragana, katakana, kanji) pour la page fe navigation.

    Args : 
        request(Resquest): Objet requête FastAPI
    
    Returns: 
        TemplateResponse: Page browse.html avec toutes les données
    """
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
    """
    Retourne la page d'apprentissage. 

    Args:
        request (Request): Objet requête FastAPI

    Returns: 
        TemplateResponse: Page learn.html
    """
    return templates.TemplateResponse("learn.html", {"request": request})

""" about html """
@app.get("/about", response_class=HTMLResponse)
async def learn_everything(request: Request):
    """
    Retourne la page 'À Propos'

    Args:
        request (Request): Objet requête FastAPI

    Returns:
        TemplateResponse: Page learn.html
    """
    return templates.TemplateResponse("about.html", {"request": request})

# Route GET : afficher le formulaire HTML
@app.get("/login", response_class=HTMLResponse)
async def get_login_form(request: Request):
    """
    Affiche le formulaire de connexion

    Args:
        request (Request): Objet requête FastAPI

    Returns:
        TemplateResponse: Page auth.html en mode login
    """
    return templates.TemplateResponse("auth.html", {"request": request, "form": "login"})
@app.post("/login")
async def post_login(request: Request, username: str = Form(...), password: str = Form(...)):
    """
    Traite la soumission du formulaire de connexion

    Args:
        request (Request): Objet requête FastAPI
        username (str, optional): Nom d'utilisateur
        password (str, optional): Mot de passe

    Returns:
        TemplateResponse: Page auth.html avec message d'erreur si échec
        RedirectResponse: Redirection vers l'accueil si susssèss
    """
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
    """
    Traite la soumission du formulaire d'inscription

    Args:
        request (Request): Objet requête FastAPI
        username (str, optional): Nom d'utilisateur souhaité
        password (str, optional): Mot de passe

    Returns:
        TemplateResponse: Page auth.html avec message de succès et d'erreur
    """
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
    """
    Affiche le profil d'utilisateur avec ses favoris

    Args:
        request (Request): Objet requête FastAPI
        user (str, optional): Nom d'utilisateur depuis les cookies

    Returns:
        TemplateResponse: Page profile.html avec les données utilisateur
        RedirectResponse: Redirection vers le login si pas connecté
    """
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
    """
    Déconnecte l'utilisateur et supprime le cookie.

    Returns: 
        RedirectResponse: Redirection vers la page de login
    """
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
    """
    Ajoute un élément aux favoris de l'utilisateur

    Args:
        request (Request): Objet requête contenant les données JSON

    Returns:
        JSONResponse: Message de confirmation ou d'erreur
    """
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