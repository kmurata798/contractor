from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27018/contractor')

client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
games = db.games
comments = db.comments

app = Flask(__name__)


# @app.route('/')
# def index():
#     """Return homepage."""
#     return render_template('home.html', msg='Flask is Cool!!')


# games = [
#     {'title': 'Cat Videos', 'description': 'Cats acting weird'},
#     {'title': '80\'s Music', 'description': 'Don\'t stop believing!'}
# ]


@app.route('/')
def index():
    """Show home"""
    return render_template('home.html', msg='WELCOME TO GAMEGO')


@app.route('/games')
def games_index():
    """show games"""
    return render_template("games_index.html", game=games.find())


@app.route('/games/new')
def games_new():
    """Create a new game."""
    return render_template('games_new.html', game={}, title='New game')


@app.route('/games/<game_id>/edit')
def games_edit(game_id):
    """Show the edit form for a game."""
    game = games.find_one({'_id': ObjectId(game_id)})
    return render_template('games_edit.html', game=game, title='Edit game')

# ^ BOTH USE THE PARTIALS IN THE HTML FILES! ^


@app.route('/games', methods=['POST'])
def games_submit():
    """Submit a new game."""
    game = {
        'title': request.form.get('title'),
        'price': request.form.get('price'),
        'images': request.form.get('images')
    }
    game_id = games.insert_one(game).inserted_id
    return redirect(url_for('game_show', game_id=game_id))


@app.route('/games/<game_id>')
def game_show(game_id):
    """Show a single game."""
    game = games.find_one({'_id': ObjectId(game_id)})
    game_comments = comments.find(
        {'game_id': ObjectId(game_id)})  # adds all comments display
    return render_template('games_show.html', game=game, comments=game_comments)


@app.route('/games/<game_id>', methods=['POST'])
def games_update(game_id):
    """Submit an edited game."""
    updated_game = {
        'title': request.form.get('title'),
        'price': request.form.get('price'),
        'images': request.form.get('images')
    }
    games.update_one(
        {'_id': ObjectId(game_id)},
        {'$set': updated_game})
    return redirect(url_for('game_show', game_id=game_id))


@app.route("/games/<game_id>/delete/", methods=["POST"])
def game_delete(game_id):
    games.delete_one({"_id": ObjectId(game_id)})
    return redirect(url_for("games_index"))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
