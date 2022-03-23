#!/usr/bin/python3

# import libraries
from cgi import test
from numpy import tri
import api_requests as api
import os
from time import sleep
from flask import Flask, render_template, request

app = Flask(__name__)

# Variable declaration
meal_category = {1: 'Vegetarian', 2: 'Pasta',
                 3: 'Miscellaneous', 4: 'Goat'}

cocktail_dict = {1: 'Non-Alcoholic', 2: 'Champagne',
                 3: 'Vodka', 4: 'Scotch'}

genres_dict = {1: 'indie', 2: 'soul', 3: 'rock', 4: 'metal'}

trivia_dict = {1: 'soft', 2: 'romantic', 3: 'bold', 4: 'extra bold'}

movies_dict = {1: 'Comedy', 2: 'Romance', 3: 'Action', 4: 'Crime'}


def screen_clear():
    """Simple function to clear the console based on OS and add some new lines"""
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # for windows
        _ = os.system('cls')
    print('\n'*10)


@app.route('/')
def index():
    date_type = 0
    print('-'*32)
    print(f"| WELCOME TO DATIFY ! |")
    print('-'*32)
    while date_type not in [1, 2, 3, 4]:
        date_type = int(input(
            "\nEnter the type of date you want:\n\n[1] - Soft\n[2] - Romantic\n[3] - Bold\n[4] - Extra bold\n\nYour choice: "))
        sleep(1)
        screen_clear()

    meal = api.get_meal(meal_category[date_type])
    cocktail = api.get_cocktail(cocktail_dict[date_type])
    music = api.get_playlist(genres_dict[date_type])
    #music_list = [j['Song'] + ' by ' + j['Artist'] for _, j in music.iterrows()]
    chosen_artist = music[1]
    song_url = music[2].replace('/artist/', '/embed/artist/')
    trivia = api.get_trivia(trivia_dict[date_type])
    movie = api.get_movies(movies_dict[date_type])
    api.to_doc(cocktail, meal)
    # when a html request has been made return these values
    # use the dictionary {{ keys }} in the html
    templateData = {
        'meal_name': meal['Meal'][0],
        'meal_image': meal['Image'][0],
        'cocktail_name': cocktail['Cocktail'][0],
        'cocktail_image': cocktail['Image'][0],
        'chosen_artist': chosen_artist,
        'song_url': song_url,
        'trivia': trivia,
        'movie_name': movie['Movie'].values[0],
        'movie_poster': movie['Poster'].values[0],
    }
    return render_template('index.html', value=templateData)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8088, threaded=True)
