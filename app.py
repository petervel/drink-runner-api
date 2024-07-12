
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

@app.route("/reached-crossing", methods=["GET"])
def reached_crossing():
    bot.reached_crossing()
    return jsonify(bot.current_node.name)

@app.route("/turned-left", methods=["GET"])
def mark_turn_left():
    bot.turned_left()
    return jsonify(bot.current_node.name)

@app.route("/turned-right", methods=["GET"])
def mark_turn_right():
    bot.turned_right()
    return jsonify(bot.current_node.name)
