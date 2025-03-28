#getting info for the frontend, heart of the backend
import json
from dataclasses import dataclass, field
from fastapi import Response, FastAPI, HTTPException
from user import *

app = FastAPI()

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
    id: str
    romaji: str

hiraganas: dict[str, Hiragana] = {}

#put in file path to JSON
with open("db/hiragana.json", encoding="utf8") as file:
    hiraganas_raw = json.load(file)
    for hiragana_raw in hiraganas_raw:
        hiragana = Hiragana(**hiragana_raw)
        hiraganas[hiragana.id] = hiragana

@dataclass
class Katakana:
    id: str
    romaji: str

katakanas: dict[str, Katakana] = {}

#put in file path to JSON
with open("db/katakana.json", encoding="utf8") as file:
    katakanas_raw = json.load(file)
    for katakana_raw in katakanas_raw:
        katakana = Katakana(**katakana_raw)
        katakanas[katakana.id] = katakana

@app.get("/") #ask server to get sthg for u
def read_root() ->Response:
    return Response("The server is running.")


#what frontend will have to do
@app.get("/kanji/{kanji_id}", response_model=Kanji)
def read_kanji(kanji_id: int) -> Kanji:
    if kanji_id not in kanjis:
        raise HTTPException(status_code=404, detail="Kanji not found")
    return kanjis[kanji_id]

@app.get("/hiragana/{hiragana_id}", response_model=Hiragana)
def read_hiragana(hiragana_id: str) -> Hiragana:
    if hiragana_id not in hiraganas:
        raise HTTPException(status_code=404, detail="Hiragana not found")
    return hiraganas[hiragana_id]

@app.get("/katakana/{katakana_id}", response_model=Katakana)
def read_katakana(katakana_id: str) -> Katakana:
    if katakana_id not in katakanas:
        raise HTTPException(status_code=404, detail="Katakana not found")
    return katakanas[katakana_id]


@app.get("/exists/{username}", response_model=str)
def read_username(username: str):
    u = User()
    if u.username_exists(username):
        return "valid username", username
    raise HTTPException(status_code=404, detail="Username not found")


"""@app.get("/hello/{name}")
def read_hello(name: str) ->Response:
    return Response("hello " + name)

@app.get("/hello")
def read_hello() ->Response:
    return Response("hello world")"""
