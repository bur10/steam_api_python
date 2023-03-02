from steamapi import SteamAPI
from flask import Flask, url_for, request, render_template

app = Flask(__name__)

API_KEY = "yourapikey"
URL = "http://api.steampowered.com/"


steam = SteamAPI(API_KEY, URL)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/games', methods=['POST'])
def games():
    if request.method == 'POST':
        limit = int(request.form["howMany"])
        user_url = request.form["user_url"]
        friends_url = [request.form[f"friend{i}_url"] for i in range(limit)]

        data = steam.compare_user_games(user_url, friends_url)
        users_data = [{
            'name': user_data['personaname'],
            'profileurl': user_data['profileurl'],
            'avatar': user_data['avatar'],

        } for user_data in steam.get_players_summaries(data['users'])]

        return render_template('games.html', games=data['games'], users=users_data)


if __name__ == '__main__':
    app.run(debug=True)
