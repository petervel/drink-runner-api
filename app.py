# Run using `poetry install && poetry run flask run --reload`

from flask import Flask, render_template, jsonify
from typing import Any
import postgresqlite

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = "th3y'11 n3v3r gu3ss th15"

with open('words.txt') as file:
    words = file.read().strip().split("\n")

db: Any = postgresqlite.connect()

@app.route("/", methods=["GET", "POST"])
def index():
    test = db.query_column("""
        select *
        from test
        """,
    )

    return render_template('guess.html', test=test)

@app.route("/bonk", methods=["GET"])
def bonk():
    return jsonify("bonk")

