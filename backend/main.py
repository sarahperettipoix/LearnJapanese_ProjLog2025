#getting info for the frontend, heart of the backend
""""why is **dict fucking up?"""
#import json
#from dataclasses import dataclass, field
from fastapi import Response, FastAPI, HTTPException, Query, Cookie
from user import *
from typing import Annotated
#from pydantic import BaseModel

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
    #uses line as separartion to iterate on text file (hiragana raws)
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
    """return server running"""
    return Response("The server is running.")


#what frontend will have to do
@app.get("/kanji/{kanji_id}", response_model=Kanji)
def read_kanji(kanji_id: int) -> Kanji:
    """return kanjis based on kanji id"""
    if kanji_id not in kanjis:
        raise HTTPException(status_code=404, detail="Kanji not found")
    return kanjis[kanji_id]

@app.get("/hiragana/{hiragana_id}", response_model=Hiragana)
def read_hiragana(hiragana_id: str) -> Hiragana:
    """return hiraganas based on hiragana id"""
    if hiragana_id not in hiraganas:
        raise HTTPException(status_code=404, detail="Hiragana not found")
    return hiraganas[hiragana_id]

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

"""@app.get("/favorites", response_model=str)
def read_favorites(favorites: str) ->Response:
    u = User(favorites=favorites)
    if u.favorites_exists():
        return Response("Favorites: " + favorites)
    raise HTTPException(status_code=404, detail="Favorite not found")"""

#post for user sending info
@app.post("/user/add", response_model=User)
def user_add(user: User) -> User:
    """add new user."""
    try:
        user.add()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}") #returns error message of ValueError of user.py
    return user

@app.put("/user/{username}/addFavorite")
def add_favorite(username: str, flashcard_id: str):
    # Simulate fetching the user (replace with DB logic)
    user = User(username=username, password="dummy", favorites=[])

    try:
        user.add_to_favorites(flashcard_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": f"Flashcard {flashcard_id} added to {username}'s favorites"}

@app.get("/user/{username}/favorites", response_model=str)
def read_favorites(favorites: list) ->Response:
    """return username if username exist."""
    u = User(favorites=favorites)
    if u.username_exists():
        return Response(favorites)
    raise HTTPException(status_code=404, detail="favorites not found")


"""class FavoriteRequest(BaseModel):
    username: str
    character: str

@app.post("/favorite")
def favorite(request: FavoriteRequest):
    if not request.username or not request.character:
        raise HTTPException(status_code=400, detail="Username and character are required.")
    add_favorite(request.username, request.character)
    return {"message": f"Added '{request.character}' to {request.username}'s favorites."}
"""
@app.get("/favorites")
def favorites(username: str = Query(..., description="Username to retrieve favorites for")):
    u = User(favorites=favorites)
    favorites_list = u.get_favorites()
    return {"username": username, "favorites": favorites_list}

#cookies
@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}

if __name__ == '__main__':
    app.run(debug=True)