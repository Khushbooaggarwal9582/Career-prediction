import json
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from mongodb_roadmaps import HAS_MONGO, MONGO_URI, MONGO_DB
from pymongo import MongoClient

class DBHandler:
    def __init__(self):
        self.has_mongo = HAS_MONGO
        if self.has_mongo:
            try:
                self.client = MongoClient(MONGO_URI)
                self.db = self.client[MONGO_DB]
                self.users_col = self.db["users"]
            except Exception:
                self.has_mongo = False
                self._init_sqlite()
        else:
            self._init_sqlite()

    def _init_sqlite(self):
        self.sqlite_file = "career_compass.db"
        conn = sqlite3.connect(self.sqlite_file)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                predictions TEXT DEFAULT '[]',
                progress TEXT DEFAULT '{}'
            )
        """)
        conn.commit()
        conn.close()

    def _get_sqlite_conn(self):
        return sqlite3.connect(self.sqlite_file)

    def register_user(self, email, password):
        hashed_password = generate_password_hash(password)
        if self.has_mongo:
            if self.users_col.find_one({"email": email}):
                return False
            self.users_col.insert_one({
                "email": email,
                "password": hashed_password,
                "predictions": [],
                "progress": {}
            })
            return True
        else:
            conn = self._get_sqlite_conn()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users (email, password, predictions, progress) VALUES (?, ?, '[]', '{}')",
                    (email, hashed_password)
                )
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False
            finally:
                conn.close()

    def verify_user(self, email, password):
        if self.has_mongo:
            user = self.users_col.find_one({"email": email})
            if user and check_password_hash(user["password"], password):
                return {
                    "email": user["email"],
                    "predictions": user.get("predictions", []),
                    "progress": user.get("progress", {})
                }
            return None
        else:
            conn = self._get_sqlite_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT password, predictions, progress FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            conn.close()
            if row and check_password_hash(row[0], password):
                return {
                    "email": email,
                    "predictions": json.loads(row[1]),
                    "progress": json.loads(row[2])
                }
            return None

    def get_user_profile(self, email):
        if self.has_mongo:
            user = self.users_col.find_one({"email": email})
            if user:
                return {
                    "email": user["email"],
                    "predictions": user.get("predictions", []),
                    "progress": user.get("progress", {})
                }
            return None
        else:
            conn = self._get_sqlite_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT predictions, progress FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return {
                    "email": email,
                    "predictions": json.loads(row[0]),
                    "progress": json.loads(row[1])
                }
            return None

    def save_prediction(self, email, prediction):
        # prediction is a dict: {"career": str, "category": str, "timestamp": str}
        if self.has_mongo:
            self.users_col.update_one(
                {"email": email},
                {"$addToSet": {"predictions": prediction}}
            )
            return True
        else:
            conn = self._get_sqlite_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT predictions FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                predictions = json.loads(row[0])
                # avoid duplicates
                if prediction not in predictions:
                    predictions.append(prediction)
                cursor.execute(
                    "UPDATE users SET predictions = ? WHERE email = ?",
                    (json.dumps(predictions), email)
                )
                conn.commit()
            conn.close()
            return True

    def save_progress(self, email, career, checked_steps):
        # checked_steps is a dict of step_num -> boolean
        if self.has_mongo:
            # Update nested field progress.career
            self.users_col.update_one(
                {"email": email},
                {"$set": {f"progress.{career}": checked_steps}}
            )
            return True
        else:
            conn = self._get_sqlite_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT progress FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                progress = json.loads(row[0])
                progress[career] = checked_steps
                cursor.execute(
                    "UPDATE users SET progress = ? WHERE email = ?",
                    (json.dumps(progress), email)
                )
                conn.commit()
            conn.close()
            return True

db_handler = DBHandler()
