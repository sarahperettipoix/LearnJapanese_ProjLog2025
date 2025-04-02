# getting info for the frontend, heart of the backend
import json
from dataclasses import dataclass, field

# user class (name, password)
@dataclass
class User:
    username: str
    password: str = "" #default value
    # SophTries
    favorites: list = field(default_factory=list)

    def username_exists(self) -> bool:
        if self.username in users:
            return True
        return False

    def login_user(self):
        if self.username_exists():
            if self.password == users[self.username].password:
                return users[self.username]
        return False

    def add(self):
        if self.username_exists():
            raise ValueError("Username already exists")
        if len(self.password) < 6:
            raise ValueError("password too short")

        users[self.username] = self
        save_userDB()
    # SophTries
    def add_favorite(self, item: str):
        if item not in self.favorites:
            self.favorites.append(item)
            save_userDB()
    def remove_favorite(self, item: str):
        if item in self.favorites:
            self.favorites.remove(item)
            save_userDB
    def get_favorites(self) -> list[str]: #get all favorite items
        return self.favorites
    # Soph attempt with flashcard
    def add_to_favorites(self, flashcard_id: str):
        if flashcard_id not in self.favorites:
            self.favorites.append(flashcard_id)
        else:
            raise ValueError("Flashcard already in favorites")


users: dict[str, User] = {}

def load_userDB():
    with open("db/user.json", encoding="utf8") as file:
        users_raw = json.load(file)
        for user_raw in users_raw:
            user = User(**user_raw)
            users[user.username] = user

def save_userDB():
    users_list = []
    for user in users.values():
        users_list.append(user.__dict__)
    with open("db/user.json", "w", encoding="utf8") as file:
        json_object = json.dumps(users_list, indent=2)
        #Writing to user.json
        file.write(json_object)

load_userDB()

"""
@app.get("/login/{username}/{password}", response_model=User)
def read_user(username: str, password: str) -> User:
    if username not in users:
        raise HTTPException(status_code=404, detail="Username not found")
    if password != users[username].password:
        raise HTTPException(status_code=404, detail="Wrong password")
    return users[username]"""
""" test_user = User(username="sophie", password="123456")
test_user.add()
test_user.add_favorite("日") """

""" Soph notes 
if a name already exists - will not work
favorites works right now if manually put it in
--> must change so can add flashcards

source: https://chatgpt.com/share/67e934b3-8d1c-8000-a753-d046cbaebc30 
"""