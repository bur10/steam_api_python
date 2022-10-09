import requests
import re
from pprint import pprint


class SteamAPI:

    def __init__(self, api_key, url):
        self.api_key = api_key
        self.url = url

    def __get_steam_id(self, url: str):
        if(url[-1] == '/'):
            url = url[:-1]
        profile_identifier = url.split('/')[-1]

        if re.search('[a-zA-Z]', profile_identifier):
            # vanity
            response = requests.get(
                f'{self.url}ISteamUser/ResolveVanityURL/v0001/', params={
                    'key': self.api_key,
                    'vanityurl': profile_identifier
                })
            if response.status_code != 200:
                print("An error occured")
                return
            data = response.json()['response']['steamid']
            return data
        else:
            # id
            return profile_identifier

    def __get_user_games(self, user_id: str):
        response = requests.get(
            f'{self.url}IPlayerService/GetOwnedGames/v0001/', params={
                'key': self.api_key,
                'steamid': user_id,
                'include_played_free_games': True,
                'include_appinfo': True
            })
        return response.json()['response']['games']

    def get_players_summaries(self, user_ids):
        response = requests.get(f'{self.url}ISteamUser/GetPlayerSummaries/v0002/', params={
            'key': self.api_key,
            'steamids': ','.join(user_ids)
        })

        return response.json()['response']['players']

    def compare_user_games(self, user_url, friends_url):

        user_id = self.__get_steam_id(user_url)
        users_id = []
        users_id.append(user_id)

        for index, friend_url in enumerate(friends_url):
            friend_id = self.__get_steam_id(friend_url)
            users_id.append(friend_id)

            if index == 0:
                current_games = self.__get_user_games(user_id)
            friend_games = self.__get_user_games(friend_id)

            matched_games = [
                current_game for current_game in current_games for friend_game in friend_games if current_game['appid'] == friend_game['appid']]
            current_games = matched_games

        return {
            'users': users_id,
            'games': [{
                'appid': game['appid'],
                'name': game['name'],
                'img': f'http://media.steampowered.com/steamcommunity/public/images/apps/{game["appid"]}/{game["img_logo_url"]}.jpg'} for game in matched_games]
        }
