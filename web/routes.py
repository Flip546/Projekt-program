from flask import Blueprint, render_template, request, redirect, url_for, flash
from db.repository import get_all_movies, insert_movie, toggle_watched, delete_movie
from helpers import fetch_movie_data

web = Blueprint("web", __name__)

@web.route("/")
def index():
    movies = get_all_movies()
    return render_template("index.html", movies=movies)

@web.route("/add", methods=["GET", "POST"])
def add_movie_route():
    if request.method == "POST":
        title = request.form.get("title")
        
        movie_data, error = fetch_movie_data(title)
        
        if error:
            flash(error)
            return redirect(url_for('web.add_movie_route'))
        
        insert_movie(movie_data["title"], movie_data["year"], movie_data["plot"], movie_data["poster"])
        flash(f"Dodano film: {movie_data['title']} ({movie_data['year']})")
        return redirect(url_for('web.index'))

    return render_template("add_movie.html")

@web.route("/toggle/<int:movie_id>", methods=["POST"])
def toggle(movie_id):
    toggle_watched(movie_id)
    return redirect(url_for("web.index"))

@web.route("/delete/<int:movie_id>", methods=["POST"])
def delete(movie_id):
    delete_movie(movie_id)
    return redirect(url_for("web.index"))