import json
import hashlib
import base64
from dataclasses import dataclass
from flask import Flask, request, session, jsonify

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure secret key

# User class (only username and hashed password)
@dataclass
class User:
    username: str
    hashed_password: str

    def username_exists(self) -> bool:
        """Checks if username exists."""
        return self.username in users

    def login_user(self, password: str):
        """Checks if password matches hashed password."""
        if self.username_exists():
            if self.verify_password(password, users[self.username].hashed_password):
                session['username'] = self.username  # Store session data
                return users[self.username]
        return False

    def add(self, password: str):
        """Sign up, add new user with hashed password."""
        if self.username_exists():
            raise ValueError("Username already exists")
        if len(password) < 6:
            raise ValueError("Password too short")

        hashed_password = self.hash_password(password)
        users[self.username] = User(username=self.username, hashed_password=hashed_password)
        save_userDB()

    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes a password with SHA-256 and encodes it in base64."""
        hashed = hashlib.sha256(password.encode()).digest()
        return base64.b64encode(hashed).decode()

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verifies a password against a hashed password."""
        return User.hash_password(password) == hashed_password

users: dict[str, User] = {}

def load_userDB():
    """Load JSON and extract username and hashed password."""
    with open("db/user.json", encoding="utf8") as file:
        users_raw = json.load(file)
        for user_raw in users_raw:
            user = User(**user_raw)
            users[user.username] = user

def save_userDB():
    """Append to dict users and save to JSON."""
    users_list = [user.__dict__ for user in users.values()]
    with open("db/user.json", "w", encoding="utf8") as file:
        json.dump(users_list, file, indent=2)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = users.get(username)
    if user and user.login_user(password):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return jsonify({"message": "Logged out successfully"}), 200

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    try:
        user = User(username=username, hashed_password="")
        user.add(password)
        return jsonify({"message": "User created successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

load_userDB()

if __name__ == "__main__":
    app.run(debug=True)