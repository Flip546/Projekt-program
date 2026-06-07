from flask import Blueprint, request, jsonify, abort
from db.repository import get_all_movies, insert_movie, delete_movie
from helpers import fetch_movie_data

api = Blueprint("api", __name__)

@api.route("/movies", methods=["GET"])
def api_movies_list():
    rows = get_all_movies()
    
    def t(row):
        return row["year"]
        
    sorted_rows = sorted([dict(row) for row in rows], key=t, reverse=True)
    return jsonify(sorted_rows)

@api.route("/movies", methods=["POST"])
def api_movies_add():
    data = request.get_json(silent=True)

    if not data or "title" not in data:
        abort(400, description="Missing JSON or title")

    title = data["title"]
    movie_data, error = fetch_movie_data(title)

    if error:
        abort(400, description=error)

    insert_movie(movie_data["title"], movie_data["year"], movie_data["plot"], movie_data["poster"])
    return jsonify({"message": "Pomyślnie dodano film", "movie": movie_data}), 201

@api.route("/movies/<int:movie_id>", methods=["DELETE"])
def api_movies_delete(movie_id):
    delete_movie(movie_id)
    return "", 204