
# Run using `poetry install && poetry run flask run --reload`

from flask import Flask, render_template, jsonify
from typing import Any
from world import Maze, Bot
import postgresqlite

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = "th3y'11 n3v3r gu3ss th15"

db: Any = postgresqlite.connect()

world = Maze('layout.json')
bot = Bot(world)

@app.route("/", methods=["GET", "POST"])
def index():
    db.execute("""
        create table IF NOT EXISTS test(
               test text NOT NULL PRIMARY KEY
        );
    """)

    test = db.query_column("""
        select *
        from test
        """,
    )

    return render_template('guess.html', test=test)

@app.route("/bonk", methods=["GET"])
def bonk():
    return jsonify("bonk")

@app.route("/crossing", methods=["GET"])
def mark_crossing():
    pass
    # expected = world.bot.next_expected_node()
    # if expected == None:
    #     world.bot.add_crossing()
