from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("calendar.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS availability (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            available INTEGER NOT NULL DEFAULT 0
        )
    """
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/availabilities")
def get_availabilities():
    conn = sqlite3.connect("calendar.db")
    c = conn.cursor()
    c.execute("SELECT date, available FROM availability")
    days = c.fetchall()
    conn.close()

    return jsonify(days)


@app.route("/set_availability", methods=["POST"])
def set_availability():
    date = request.form["date"]
    available = int(request.form["available"])

    conn = sqlite3.connect("calendar.db")
    c = conn.cursor()

    c.execute("SELECT * FROM availability WHERE date = ?", (date,))
    result = c.fetchone()

    if result:
        c.execute(
            "UPDATE availability SET available = ? WHERE date = ?", (available, date)
        )
    else:
        c.execute(
            "INSERT INTO availability (date, available) VALUES (?, ?)",
            (date, available),
        )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
