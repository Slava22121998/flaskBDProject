from flask import Flask, render_template

from utils import get_film_by_name, get_films_by_time_period, get_films_by_rating, get_films_by_genre

app = Flask(__name__)


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/movie/<title>/')
def show_movie(title):
    film = get_film_by_name(title)
    return (film, 200, {'Content-Type': 'application/json'})


@app.route('/movie/<year_1>/to/<year_2>/')
def show_movies_by_period(year_1, year_2):
    films = get_films_by_time_period(year_1, year_2)
    return (films, 200, {'Content-Type': 'application/json'})


@app.route('/rating/<rating>/')
def show_movies_by_rating(rating):
    films = get_films_by_rating(rating)
    return (films, 200, {'Content-Type': 'application/json'})


@app.route('/genre/<genre>/')
def show_movies_by_genre(genre):
    films = get_films_by_genre(genre)
    return (films, 200, {'Content-Type': 'application/json'})


if __name__ == '__main__':
    app.run()
