#getting info for the frontend, heart of the backend
import json
from dataclasses import dataclass, field
from fastapi import Response, FastAPI, HTTPException
from user import *
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import random

app = FastAPI()
templates = Jinja2Templates(directory="../frontend")
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

@dataclass
class Kanji:
    id: int
    kanji: str
    onyomi: list[str]
    kunyomi: list[str]
    meaning: str
    JLPT: str

kanjis: dict[int, Kanji] = {}

#put in file path to JSON
with open("db/kanjis.json", encoding="utf8") as file:
    kanjis_raw = json.load(file) #kanjis_raw = structure JSON
    for kanji_raw in kanjis_raw:
        kanji = Kanji(**kanji_raw)
        kanjis[kanji.id] = kanji

@dataclass
class Hiragana:
    id: int
    kana: str
    romaji: str

hiraganas: dict[int, str, Hiragana] = {}

#put in file path to JSON
with open("db/hiragana.json", encoding="utf8") as file:
    hiraganas_raw = json.load(file)
    #uses line as separartion to iterate on text file (hiragana raws)
    for hiragana_raw in hiraganas_raw:
        hiragana = Hiragana(**hiragana_raw)
        hiraganas[hiragana.id] = hiragana

@dataclass
class Katakana:
    id: int
    kana: str
    romaji: str

katakanas: dict[int, str, Katakana] = {}

#put in file path to JSON
with open("db/katakana.json", encoding="utf8") as file:
    katakanas_raw = json.load(file)
    for katakana_raw in katakanas_raw:
        katakana = Katakana(**katakana_raw)
        katakanas[katakana.id] = katakana

@app.get("/", response_class=HTMLResponse) #ask server to get sthg for u
async def home(request: Request):
    """return server running"""
    message = "Bienvenue sur ma page avec FastAPI et Jinja2!"
    return templates.TemplateResponse("index.html", {"request": request, "message": message})


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

    random_list = []
    for ninin in len(hiraganas):
        random_list[ninin].append(random.randint(1,len(hiraganas)))
    print(random_list)

    message = "Bienvenue sur ma page avec FastAPI et Jinja2!"
    return templates.TemplateResponse("flashcard.html", {"request": request, "message": message})



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
