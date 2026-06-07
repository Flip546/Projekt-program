import requests

OMDB_API_KEY = "b57630c0" 

def fetch_movie_data(title):
    try:
        url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
        response = requests.get(url, timeout=5)
        response.raise_for_status() 
        
        data = response.json()

        if data.get("Response") == "False":
            return None, "Nie znaleziono filmu o takim tytule w bazie OMDb."

        movie_info = {
            "title": data.get("Title"),
            "year": data.get("Year"),
            "plot": data.get("Plot"),
            "poster": data.get("Poster") if data.get("Poster") != "N/A" else ""
        }
        return movie_info, None

    except requests.exceptions.RequestException:
        return None, "Błąd: Nie można połączyć się z serwerem OMDb API."