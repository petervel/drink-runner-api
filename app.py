# Run using `poetry install && poetry run flask run --reload`

from flask import Flask, render_template, request, session, redirect
from random import randint
from typing import Any
import postgresqlite

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = "th3y'11 n3v3r gu3ss th15"

with open('words.txt') as file:
    words = file.read().strip().split("\n")

db: Any = postgresqlite.connect()


def load_game(user_id, force_new=False):
    if not force_new:
        game = db.query_row('''
            select *
            from games
            where user_id=:user_id
            order by id desc
            limit 1''',
            user_id=user_id
        )
        if game:
            return game

    secret = words[randint(0, len(words))]
    return db.query_row('''
        insert into games(user_id, secret)
        values(:user_id, :secret)
        returning *
        ''',
        user_id=user_id,
        secret=secret
    )


def guess_to_hint(guess, secret):
    """Given a guess as a string, it returns a list with one tuple for each letter in the
    string, where the first item is the letter, and the second item is one of the strings
    `correct`, `wrong` or `misplaced`, describing what applies for that letter."""
    result = []
    for idx, letter in enumerate(guess):
        actual = secret[idx]
        if actual == letter:
            result.append((letter, 'correct'))
        elif letter in secret:
            result.append((letter, 'misplaced'))
        else:
            result.append((letter, 'wrong'))
    return result


@app.route("/", methods=["GET", "POST"])
def index():
    message = None

    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']

    game = load_game(user_id)
    guesses = db.query_column("""
        select word
        from guesses
        where game_id=:game_id
        order by id
        """,
        game_id=game["id"]
    )

    if request.method == 'POST':
        if game["result"] is None:
            if "next" in request.form:
                game = load_game(user_id, True)
                message = "New word. Good luck!"
                guesses = []
        elif "guess" in request.form:
            word = request.form['word'].strip().lower()
            if len(word) != 5:
                message = f'"{word}" is not 5 letters...'
            elif word not in words:
                message = f'"{word}" is not a word...'
            elif word in guesses:
                message = f'"{word}" was already guessed...'
            else:
                message, game = check_guess(game, guesses, word)

    return render_template('guess.html',
        message=message,
        ready=(game["result"] is not None),
        guesses=[guess_to_hint(guess, game["secret"]) for guess in guesses]
    )

def check_guess(game, guesses, word):
    db.query("""insert into guesses(game_id, word) values(:game_id, :word)""", game_id=game["id"], word=word)
    guesses.append(word)
    guess_count = len(guesses)
    result = None
    message = ""
    if word == game["secret"]:
        message = "Congrats, you got it!"
        result = guess_count
    elif guess_count >= 15:
        message = f"Sorry, not good enough.. the word was: {game['secret']}"
        result = -1
        
    if result is not None:
        game = db.query("""update games set result=:result where id=:game_id returning * """,
                        result=result,
                        game_id=game["id"])
        
    return message, game

@app.route("/history")
def history():
    games = db.query("""
        select g.id, g.secret, g.result, u.name as user_name
        from games g
        join users u on g.user_id=u.id
        where g.result is not null
        order by g.time
        """
    )
    return render_template('history.html', games=games)

@app.route("/login", methods=["GET", "POST"])
def login():
    message = None
    if request.method == "POST":
        name = request.form['name'].strip().lower()
        user = db.query_row("select * from users where name=:name", name=name)
        if not user:
            user = db.query_row("""
                insert into users(name,password)
                values(:name, :password)
                returning *
                """,
                name=name,
                password=request.form['password']
            )

        if request.form['password'] == user["password"]:
            session['user_id'] = user['id']
            return redirect('/')
        message = "Invalid password."
    return render_template('login.html', message=message)

@app.route("/game/<int:game_id>")
def game_details(game_id):
    game = db.query_row("select * from games where id=:game_id", game_id=game_id)
    guesses = db.query_column("select word from guesses where game_id=:game_id order by id", game_id=game["id"])

    return render_template('guess.html',
        guesses=[guess_to_hint(guess, game["secret"]) for guess in guesses],
        review=True,
    )

@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect('/login')
