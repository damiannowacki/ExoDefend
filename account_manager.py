import json
import os
import hashlib

class Account_Manager:
    def __init__(self, file_name = "users.json"):
        self.file_name = file_name
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists(self.file_name):
            return {}
        
        try:
            with open(self.file_name, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}

    def save_users(self):
        with open(self.file_name, "w") as file:
            json.dump(self.users, file, indent = 4)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def sign_up(self, username, password):
        username = username.strip()
        if username == "":
            return False, "Username Cannot Be Empty!"
        if password == "":
            return False, "Password Cannot Be Empty!"
        if username in self.users:
            return False, "This Username Is Already In Use."
        
        self.users[username] = {
            "password": self.hash_password(password), 
            "highscore": 0
        }

        self.save_users()
        return True, "Account Created!"

    def login(self, username, password):
        if username in self.users:
            password_hash = self.hash_password(password)
            return self.users[username]["password"] == password_hash

    def get_highscore(self, username):
        return self.users[username]["highscore"]

    def save_highscore(self, username, score):
        if score > self.users[username]["highscore"]:
            self.users[username]["highscore"] = score
            self.save_users()
