
from flask import Flask, request, redirect, url_for, render_template
import sqlite3
from pathlib import Path

app = Flask(__name__)
DATABASE = Path(__file__).with_name("comments.db")


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL
            )
        """)

def clear_old_test_payloads():
    with get_db() as db:
        db.execute(
            "DELETE FROM comments WHERE message LIKE ?",
            ("%<script>%",)
        )


def clear_test_comments():
    with get_db() as db:
        db.execute("DELETE FROM comments")


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/submit", methods=["POST"])
def submit():
    message = request.form.get("message", "")

    if not message.strip():
        return "Comment cannot be empty.", 400

    if len(message) > 500:
        return "Comment must be 500 characters or fewer.", 400

    with get_db() as db:
        db.execute(
            "INSERT INTO comments (message) VALUES (?)",
            (message,)
        )

    # Return to the page where the form was submitted
    destination = request.form.get("return_to", "secure")

    if destination not in ("secure", "vulnerable"):
        destination = "secure"

    return redirect(url_for(destination))



@app.route("/vulnerable")
def vulnerable():
    with get_db() as db:
        comments = db.execute(
            "SELECT id, message FROM comments ORDER BY id DESC"
        ).fetchall()

    return render_template(
        "results.html",
        comments=comments,
        mode="vulnerable"
    )


@app.route("/secure")
def secure():
    with get_db() as db:
        comments = db.execute(
            "SELECT id, message FROM comments ORDER BY id DESC"
        ).fetchall()

    return render_template(
        "results.html",
        comments=comments,
        mode="secure"
    )



if __name__ == "__main__":
    initialize_db()
    clear_old_test_payloads()
    app.run(debug=False, host="127.0.0.1", port=5000)

