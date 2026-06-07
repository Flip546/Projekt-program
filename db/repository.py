from db.init import get_db

def get_all_movies():
    db = get_db()
    return db.execute("SELECT * FROM movies ORDER BY created_at DESC").fetchall()

def insert_movie(title, year, plot, poster_url):
    db = get_db()
    db.execute(
        "INSERT INTO movies(title, year, plot, poster_url) VALUES (?, ?, ?, ?)", 
        [title, year, plot, poster_url]
    )
    db.commit()

def toggle_watched(movie_id):
    db = get_db()
    movie = db.execute("SELECT watched FROM movies WHERE id = ?", [movie_id]).fetchone()
    if movie:
        new_status = 0 if movie["watched"] == 1 else 1
        db.execute("UPDATE movies SET watched = ? WHERE id = ?", [new_status, movie_id])
        db.commit()

def delete_movie(movie_id):
    db = get_db()
    db.execute("DELETE FROM movies WHERE id = ?", [movie_id])
    db.commit()