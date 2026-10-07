"""
Fitness API — deliberately vulnerable Flask skeleton (Week 1).

This API is the TARGET for the 12-week API Security Assessment & Hardening
project. It intentionally contains common API vulnerabilities (OWASP API
Security Top 10) so they can be discovered, documented, and fixed in later
weeks. DO NOT deploy this to the public internet — run it locally only.

Intentional weaknesses (to be assessed/hardened in later weeks):
  - Broken Object Level Authorization / IDOR (API1)
  - Broken Authentication: plaintext passwords, no token expiry (API2)
  - Excessive Data Exposure: returns password hashes / all fields (API3)
  - No rate limiting (API4)
  - SQL Injection via string-formatted queries (Injection)
  - Hardcoded secret, debug mode on
"""

import sqlite3
import os
from flask import Flask, request, jsonify, g

app = Flask(__name__)

# VULN: hardcoded secret committed to source control
app.config["SECRET_KEY"] = "dev-secret-change-me"

DB_PATH = os.path.join(os.path.dirname(__file__), "fitness.db")


# --------------------------------------------------------------------------
# Database helpers
# --------------------------------------------------------------------------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create tables and seed sample data if the DB does not exist."""
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,          -- VULN: stored in plaintext
            email TEXT,
            role TEXT DEFAULT 'user'
        );
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            activity TEXT NOT NULL,
            duration_min INTEGER,
            calories INTEGER,
            notes TEXT
        );
        """
    )
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
            [
                ("alice", "password123", "alice@fit.local", "user"),
                ("bob", "qwerty", "bob@fit.local", "user"),
                ("admin", "admin", "admin@fit.local", "admin"),
            ],
        )
        cur.executemany(
            "INSERT INTO workouts (user_id, activity, duration_min, calories, notes) "
            "VALUES (?, ?, ?, ?, ?)",
            [
                (1, "Running", 30, 300, "Morning run"),
                (1, "Cycling", 45, 400, "Evening ride"),
                (2, "Yoga", 60, 200, "Private session notes"),
                (3, "Admin test", 10, 50, "Internal"),
            ],
        )
    db.commit()
    db.close()


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------
@app.route("/")
def index():
    return jsonify(
        {
            "service": "Fitness API (deliberately vulnerable)",
            "status": "ok",
            "endpoints": [
                "POST /api/register",
                "POST /api/login",
                "GET  /api/users/<id>",
                "GET  /api/workouts?user_id=<id>",
                "POST /api/workouts",
                "GET  /api/search?activity=<name>",
            ],
        }
    )


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")
    email = data.get("email", "")
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400
    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, password, email),  # VULN: plaintext password
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "username already exists"}), 409
    return jsonify({"message": "registered", "username": username}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")
    db = get_db()
    # VULN: SQL injection via string formatting
    query = (
        "SELECT * FROM users WHERE username = '%s' AND password = '%s'"
        % (username, password)
    )
    row = db.execute(query).fetchone()
    if row is None:
        return jsonify({"error": "invalid credentials"}), 401
    # VULN: predictable, non-expiring "token"
    token = "token-%d" % row["id"]
    return jsonify({"message": "login ok", "token": token, "user_id": row["id"]})


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if row is None:
        return jsonify({"error": "not found"}), 404
    # VULN: IDOR (no auth check) + excessive data exposure (returns password)
    return jsonify(dict(row))


@app.route("/api/workouts", methods=["GET", "POST"])
def workouts():
    db = get_db()
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        db.execute(
            "INSERT INTO workouts (user_id, activity, duration_min, calories, notes) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                data.get("user_id"),
                data.get("activity"),
                data.get("duration_min"),
                data.get("calories"),
                data.get("notes"),
            ),
        )
        db.commit()
        return jsonify({"message": "workout created"}), 201
    # VULN: IDOR — any user_id can be read without authorization
    user_id = request.args.get("user_id")
    if user_id:
        rows = db.execute(
            "SELECT * FROM workouts WHERE user_id = ?", (user_id,)
        ).fetchall()
    else:
        rows = db.execute("SELECT * FROM workouts").fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/search", methods=["GET"])
def search():
    activity = request.args.get("activity", "")
    db = get_db()
    # VULN: SQL injection via string formatting
    query = "SELECT * FROM workouts WHERE activity LIKE '%%%s%%'" % activity
    rows = db.execute(query).fetchall()
    return jsonify([dict(r) for r in rows])


if __name__ == "__main__":
    init_db()
    # VULN: debug=True and bound to all interfaces
    app.run(host="0.0.0.0", port=5000, debug=True)
