from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("calendar.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS availability (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL UNIQUE,
            available INTEGER NOT NULL DEFAULT 0
        )
    """
    )
    conn.commit()
    conn.close()


def populate_dates():
    conn = sqlite3.connect("calendar.db")
    c = conn.cursor()

    today = datetime.today()
    first_day = today.replace(day=1)
    num_days = (
        first_day.replace(month=today.month % 12 + 1, day=1) - timedelta(days=1)
    ).day
    for i in range(num_days):
        date_str = (first_day + timedelta(days=i)).strftime("%Y-%m-%d")
        c.execute(
            "INSERT OR IGNORE INTO availability (date, available) VALUES (?, 0)",
            (date_str,),
        )

    conn.commit()
    conn.close()


@app.route("/")
def index():
    populate_dates()
    conn = sqlite3.connect("calendar.db")
    c = conn.cursor()
    c.execute("SELECT date, available FROM availability")
    days = c.fetchall()
    conn.close()
    return render_template("index.html", days=days)


@app.route("/calendar")
def calendar():
    return render_template("calendar.html")


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
