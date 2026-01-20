from flask import Flask, request, jsonify, session
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "simple_secret_key"
CORS(app, supports_credentials=True)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sarita@1977",
    database="SCIENCE_DASHBOARD"
)

# ✅ API to get lessons
@app.route("/lessons", methods=["GET"])
def get_lessons():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM lessons")
    lessons = cursor.fetchall()
    return jsonify(lessons)
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (data["username"], data["password"])
    )

    user = cursor.fetchone()

    if user:
        session["user_id"] = user["id"]
        return jsonify({"message": "login success"})
    else:
        return jsonify({"message": "invalid credentials"}), 401

@app.route("/save-progress", methods=["POST"])
def save_progress():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    data = request.json
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO progress (user_id, lesson_id, completed)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE completed=%s
    """, (
        session["user_id"],
        data["lesson_id"],
        data["completed"],
        data["completed"]
    ))

    db.commit()
    return jsonify({"message": "progress saved"})

@app.route("/logout")
def logout():
    session.clear()
    return jsonify({"message": "logged out"})

# ✅ API to add lesson
@app.route("/add-lesson", methods=["POST"])
def add_lesson():
    data = request.json
    cursor = db.cursor()

    sql = """
    INSERT INTO lessons (subject, chapter, difficulty, pages)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        data["subject"],
        data["chapter"],
        data["difficulty"],
        data["pages"]
    )

    cursor.execute(sql, values)
    db.commit()

    return jsonify({"message": "Lesson added successfully"})

if __name__ == "__main__":
    app.run(debug=True)
@app.route("/save-progress", methods=["POST"])
def save_progress():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    data = request.json
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO user_progress (user_id, lesson_id, completed)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE completed=%s
    """, (
        session["user_id"],
        data["lesson_id"],
        data["completed"],
        data["completed"]
    ))

    db.commit()
    return jsonify({"message": "saved"})
@app.route("/get-progress")
def get_progress():
    if "user_id" not in session:
        return jsonify([])

    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT lesson_id, completed FROM user_progress WHERE user_id=%s",
        (session["user_id"],)
    )
    return jsonify(cursor.fetchall())
