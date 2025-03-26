# getting info for the frontend, heart of the backend
import json
from dataclasses import dataclass, field

# user class (name password)
@dataclass
class User:
    username: str
    password: str


users: dict[str, User] = {}

with open("db/user.json", encoding="utf8") as file:
    users_raw = json.load(file)  # kanjis_raw = structure JSON
    for user_raw in users_raw:
        user = User(**user_raw)
        users[user.username] = user

"""
@app.get("/login/{username}/{password}", response_model=User)
def read_user(username: str, password: str) -> User:
    if username not in users:
        raise HTTPException(status_code=404, detail="Username not found")
    if password != users[username].password:
        raise HTTPException(status_code=404, detail="Wrong password")
    return users[username]"""

def username_exists(username: str) -> bool:
    if username in users:
        return True
    return False

def login_user(username: str, password: str):
    if username_exists(username):
        if password == users[username].password:
            return users[username]
    return False

def signup_user(username: str, password: str):
    if not username_exists(username):
        users[username] = User(username=username, password=password)
        json_object = json.dumps(users, indent=2)

        # Writing to sample.json
        with open("user.json", "w") as outfile:
            outfile.write(json_object)
