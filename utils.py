import json
import sqlite3
from collections import Counter


def get_films_by_rating_execute_query(query):
    film_json = list()
    try:
        with sqlite3.connect('netflix.db') as connection:
            cursor = connection.cursor()
            search = cursor.execute(query).fetchall()
            col_names = [description[0] for description in cursor.description]
            for film in search:
                film_json.append(dict(zip(col_names, film)))
            for item in film_json:
                item['description'] = item['description'].strip('\n')
            return json.dumps(film_json, indent=2, ensure_ascii=False)
    except Exception as ex:
        return f'Ошибка подключения к бд: {ex}'


def get_film_by_name(film_name):
    query = """
        SELECT title, country, MAX(release_year) AS release_year ,listed_in AS genre, description
        FROM netflix
        WHERE title = ?
        GROUP BY release_year

    """
    try:
        with sqlite3.connect('netflix.db') as connection:
            cursor = connection.cursor()
            search = cursor.execute(query, (film_name,)).fetchall()
            col_names = [description[0] for description in cursor.description]  # Получаем имена колонок
            film_json = dict(zip(col_names, list(search[0])))  # Создаем словарь имя колонки БД - результат запроса
            film_json['description'] = film_json['description'].strip('\n')  # Удаляем символы переноса строки
            return json.dumps(film_json, indent=2, ensure_ascii=False)

    except Exception as ex:
        return f'Ошибка подключения к бд: {ex}'


def get_films_by_time_period(year_1, year_2):
    film_json = list()
    query = """
        SELECT title, release_year
        FROM netflix
        WHERE release_year BETWEEN ? AND ?
        LIMIT 100
    """
    try:
        with sqlite3.connect('netflix.db') as connection:
            cursor = connection.cursor()
            search = cursor.execute(query, (year_1, year_2,)).fetchall()
            col_names = [description[0] for description in cursor.description]
            for film in search:
                film_json.append(dict(zip(col_names, film)))
            return json.dumps(film_json, indent=2, ensure_ascii=False)

    except Exception as ex:
        return f'Ошибка подключения к бд: {ex}'


def get_films_by_rating(rating: str):
    if rating == 'children':
        query = """
                        SELECT title, rating, description
                        FROM netflix
                        WHERE rating in ('G')
                        ORDER BY rating DESC
                    """
        get_films_by_rating_execute_query(query)

    elif rating == 'family':
        query = """
                        SELECT title, rating, description
                        FROM netflix
                        WHERE rating in ('G', 'PG', 'PG-13')
                        ORDER BY rating DESC
                    """
        get_films_by_rating_execute_query(query)

    elif rating == 'adult':
        query = """
                        SELECT title, rating, description
                        FROM netflix
                        WHERE rating in ('R', 'NC-17')
                        ORDER BY rating DESC
                    """
        get_films_by_rating_execute_query(query)


def get_films_by_genre(genre: str):
    film_json = list()
    # Попробовал с f-строкой сформировать запрос
    query = f"SELECT title, description FROM netflix WHERE listed_in LIKE '%{genre}%' AND release_year BETWEEN 2019 AND 2021 LIMIT 10"
    try:
        with sqlite3.connect("netflix.db") as connection:
            cursor = connection.cursor()
            search = cursor.execute(query).fetchall()
            col_names = [description[0] for description in cursor.description]
            for film in search:
                film_json.append(dict(zip(col_names, film)))
            for item in film_json:
                item['description'] = item['description'].strip('\n')
            return json.dumps(film_json, indent=2, ensure_ascii=False)

    except Exception as ex:
        return f'Ошибка подключения к бд: {ex}'


# 5 задание
def get_cast_info(name_1, name_2):
    query = f"SELECT netflix.cast FROM netflix WHERE netflix.cast LIKE '%{name_1}%' AND netflix.cast LIKE '%{name_2}%'"
    try:
        with sqlite3.connect("netflix.db") as connection:
            cursor = connection.cursor()
            names_list = list()
            cast_list = list()
            cast = cursor.execute(query).fetchall()
            for item in cast:
                for name in item[0].split(', '):
                    if name != name_1 and name != name_2:
                        names_list.append(name)

            for item in Counter(names_list):
                if Counter(names_list)[item] > 2:
                    cast_list.append(item)
        return cast_list
    except Exception as ex:
        return f'Ошибка подключения к бд: {ex}'


# 6 задание
def get_info_about_picture(type, date, genre):
    query = f"SELECT title, description FROM netflix WHERE type = '{type}' AND release_year = '{date}' AND listed_in LIKE '%{genre}%'"
    try:
        film_json = list()
        with sqlite3.connect("netflix.db") as connection:
            cursor = connection.cursor()
            res = cursor.execute(query).fetchall()
        col_names = [description[0] for description in cursor.description]
        for film in res:
            film_json.append(dict(zip(col_names, film)))
        for item in film_json:
            item['description'] = item['description'].strip('\n')
        return json.dumps(film_json, indent=2)

    except Exception as ex:
        return f'Ошибка подключения к бд: {ex}'


# print(get_info_about_picture('TV Show', '1925', 'TV Shows'))
