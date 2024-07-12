
# Run using `poetry install && poetry run flask run --reload`

from flask import Flask, render_template, jsonify
from typing import Any
from world import Maze, Bot
import postgresqlite

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = "th3y'11 n3v3r gu3ss th15"

db: Any = postgresqlite.connect()

maze = Maze('final/layout.json')
bot = Bot(maze, 'final/order.json')

@app.route("/")
def index():
    return render_template('maze.html', maze=maze, bot=bot)

@app.route("/bonk", methods=["GET"])
def bonk():
    return jsonify("bonk")

@app.route("/reached-crossing")
def reached_crossing():
    bot.reached_crossing()
    return jsonify(bot.get_next_instruction())

@app.route("/turned-left")
def mark_turn_left():
    bot.turned_left()
    return jsonify(bot.get_next_instruction())

@app.route("/turned-right")
def mark_turn_right():
    bot.turned_right()
    return jsonify(bot.get_next_instruction())
