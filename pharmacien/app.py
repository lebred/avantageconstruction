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


def populate_dates(month, year):
    conn = sqlite3.connect("calendar.db")
    c = conn.cursor()

    first_day = datetime(year, month, 1)
    last_day = first_day.replace(day=28) + timedelta(days=4)
    last_day = last_day - timedelta(days=last_day.day)

    for i in range((last_day - first_day).days + 1):
        date_str = (first_day + timedelta(days=i)).strftime("%Y-%m-%d")
        c.execute(
            "INSERT OR IGNORE INTO availability (date, available) VALUES (?, 0)",
            (date_str,),
        )

    conn.commit()
    conn.close()


@app.route("/")
def index():
    month = request.args.get("month", default=datetime.now().month, type=int)
    year = request.args.get("year", default=datetime.now().year, type=int)

    populate_dates(month, year)

    conn = sqlite3.connect("calendar.db")
    c = conn.cursor()
    c.execute(
        'SELECT date, available FROM availability WHERE strftime("%m", date) = ? AND strftime("%Y", date) = ?',
        (f"{month:02d}", year),
    )
    days = c.fetchall()
    conn.close()

    return render_template("index.html", days=days, month=month, year=year)


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

    c.execute("UPDATE availability SET available = ? WHERE date = ?", (available, date))
    conn.commit()
    conn.close()

    return redirect(
        url_for("index", month=request.form["month"], year=request.form["year"])
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
