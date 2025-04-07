# getting info for the frontend, heart of the backend
import json
from dataclasses import dataclass, field


"""def load_users():
    with open(USER_DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)"""

"""def save_users(users):
    with open(USER_DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4)"""


# user class (name, password)
@dataclass
class User:
    username: str
    password: str = "" #default value
    favorites: list[str] = field(default_factory=list)

    def username_exists(self) -> bool:
        """checks if username exists."""
        if self.username in users:
            return True
        return False

    def favorites_exists(self) -> bool:
        """checks if username exists."""
        if self.favorites is not None:
            return True
        return False

    def login_user(self):
        """checks if password matches username."""
        if self.username_exists():
            if self.password == users[self.username].password:
                return users[self.username]
        return False

    def add(self):
        """sign up, add new user."""
        if self.username_exists():
            raise ValueError("Username already exists")
        if len(self.password) < 6:
            raise ValueError("password too short")

        users[self.username] = self
        save_userDB()

users: dict[str, User] = {}

def load_userDB():
    """load json and extract username and password."""
    with open("db/user.json", encoding="utf8") as file:
        users_raw = json.load(file)
        for user_raw in users_raw:
            user = User(**user_raw)
            users[user.username] = user

def save_userDB():
    """append to dict users and save to json."""
    users_list = []
    for user in users.values():
        users_list.append(user.__dict__)
    with open("db/user.json", "w", encoding="utf8") as file:
        json_object = json.dumps(users_list, indent=2)
        #Writing to user.json
        file.write(json_object)

def add_favorite(username, character):
    usersDB = load_userDB()
    for user in users:
        if user['username'] == username:
            if 'favorites' not in user:
                user['favorites'] = []
            if character not in user['favorites']:
                user['favorites'].append(character)
            break
    save_userDB(usersDB)

def get_favorites(username):
    usersDB = load_userDB()
    for user in usersDB:
        if user['username'] == username:
            return user.get('favorites', [])
    return []

load_userDB()

"""
@app.get("/login/{username}/{password}", response_model=User)
def read_user(username: str, password: str) -> User:
    if username not in users:
        raise HTTPException(status_code=404, detail="Username not found")
    if password != users[username].password:
        raise HTTPException(status_code=404, detail="Wrong password")
    return users[username]"""