from flask import Flask, render_template, request, redirect, url_for
import requests
import random

app = Flask(__name__)

def get_random_anime():
    """Fetches a random anime using Jikan API."""
    random_page = random.randint(1, 100)  # Get random anime from page 1-100
    url = f"https://api.jikan.moe/v4/anime?page={random_page}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        anime_list = data.get("data", [])
        if anime_list:
            anime = random.choice(anime_list)  # Select a random anime from the page
            return {
                "title": anime["title"],
                "rank": anime.get("rank", 9999),  # Fallback rank if not ranked
                "image_url": anime["images"]["jpg"]["image_url"],
            }
    return None

@app.route("/")
def index():
    """Homepage that displays two random anime."""
    anime1 = get_random_anime()
    anime2 = get_random_anime()

    # Ensure two different anime
    while anime1["title"] == anime2["title"]:
        anime2 = get_random_anime()

    return render_template("index.html", anime1=anime1, anime2=anime2)

@app.route("/result", methods=["POST"])
def result():
    """Handles the user's selection and determines win/loss."""
    anime1_rank = int(request.form["anime1_rank"])
    anime2_rank = int(request.form["anime2_rank"])
    selected = request.form["selected"]

    # Determine if the selection is correct
    if selected == "anime1" and anime1_rank < anime2_rank:
        result = "win"
    elif selected == "anime2" and anime2_rank < anime1_rank:
        result = "win"
    else:
        result = "lose"

    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)

