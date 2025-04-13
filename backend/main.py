""" Soph problems: had to change with open file path """
# Soph: backend built using FastAPI
#getting info for the frontend, heart of the backend
import json
# Soph: define objects hiragana, kata, kanji
from dataclasses import dataclass, field
# Soph: Response + HTTP - send responses and handle errors
from fastapi import Response, FastAPI, HTTPException
# Soph: imports everything from user.py
from user import *

# Soph: FastAPI
# Soph: provides API that allows frontend app to access data on kanji, hiragana, kata
# and user info
# initialise
app = FastAPI()

# Soph: loading kanji data from json
@dataclass
class Kanji:
    id: int
    kanji: str
    onyomi: list[str]
    kunyomi: list[str]
    meaning: str
    JLPT: str

# Get the current file's directory
""" base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "db", "kanjis.json") """

# Soph: dict to store kanji data
kanjis: dict[int, Kanji] = {}

""" with open(file_path, encoding="utf8") as file:
    kanjis_raw = json.load(file)
    for kanji_raw in kanjis_raw:
        kanji = Kanji(**kanji_raw)
        kanjis[kanji.id] = kanji
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Could not find kanjis.json at: {file_path}") """

#put in file path to JSON
with open("backend/db/kanjis.json", encoding="utf8") as file:
    kanjis_raw = json.load(file) #kanjis_raw = structure JSON
    for kanji_raw in kanjis_raw:
        kanji = Kanji(**kanji_raw)
        kanjis[kanji.id] = kanji

@dataclass
class Hiragana:
    id: str
    romaji: str

# Get the current file's directory
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "db", "hiragana.json")

# Soph: dict to store hiragana data
hiraganas: dict[str, Hiragana] = {}

with open(file_path, encoding="utf8") as file:
    hiraganas_raw = json.load(file)
    #uses line as separartion to iterate on text file (hiragana raws)
    for hiragana_raw in hiraganas_raw:
        hiragana = Hiragana(**hiragana_raw)
        hiraganas[hiragana.id] = hiragana 

#put in file path to JSON
""" with open("/Users/sophieward/Desktop/ProjetLogiciel2025-main/backend/db/hiragana.json", encoding="utf8") as file:
    hiraganas_raw = json.load(file)
    #uses line as separartion to iterate on text file (hiragana raws)
    for hiragana_raw in hiraganas_raw:
        hiragana = Hiragana(**hiragana_raw)
        hiraganas[hiragana.id] = hiragana """

@dataclass
class Katakana:
    id: str
    romaji: str

# Get the current file's directory
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "db", "katakana.json")

# Soph: dict to store katakana data
katakanas: dict[str, Katakana] = {}

with open(file_path, encoding="utf8") as file:
    katakanas_raw = json.load(file)
    for katakana_raw in katakanas_raw:
        katakana = Katakana(**katakana_raw)
        katakanas[katakana.id] = katakana

#put in file path to JSON
""" with open("/Users/sophieward/Desktop/ProjetLogiciel2025-main/backend/db/katakana.json", encoding="utf8") as file:
    katakanas_raw = json.load(file)
    for katakana_raw in katakanas_raw:
        katakana = Katakana(**katakana_raw)
        katakanas[katakana.id] = katakana """

# Soph: basic server check
# when user visits /, server responds with "The server is running"
# this confirms API is active
@app.get("/") #ask server to get sthg for u
def read_root() ->Response:
    return Response("The server is running.")

# Soph: retrieves kanji details by id
# if id not found, 404 error
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

# Soph: check if a username exists
@app.get("/exists/{username}", response_model=str)
def read_username(username: str) ->Response:
    u = User(username=username)
    if u.username_exists():
        return Response("valid username: " + username)
    raise HTTPException(status_code=404, detail="Username not found")

# Soph: adding a new user
#post for user sending info
@app.post("/user/add", response_model=User)
def user_add(user: User) -> User:
    try:
        user.add()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}") #returns error message of ValueError of user.py
    return user

"""@app.get("/hello/{name}")
def read_hello(name: str) ->Response:
    return Response("hello " + name)

@app.get("/hello")
def read_hello() ->Response:
    return Response("hello world")"""