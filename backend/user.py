# getting info for the frontend, heart of the backend
import json
from dataclasses import dataclass, field

# user class (name, password)
@dataclass
class User:
    username: str
    password: str = "" #default value

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