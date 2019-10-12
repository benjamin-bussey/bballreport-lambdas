import os
import requests
import base64


def get_team_games(api_key, season, team_id):
    response = requests.get(
        url='https://api.mysportsfeeds.com/v2.1/pull/nba/{}/games.json?team={}'.format(season, team_id),
        headers={
            "Authorization": "Basic " + base64.b64encode(
                '{}:{}'.format(api_key, 'MYSPORTSFEEDS').encode('utf-8')).decode('ascii')
        }
    )

    return response.json()['games']


def get_game(api_key, season, game_id):
    response = requests.get(
        url=' https://api.mysportsfeeds.com/v2.1/pull/nba/{}/games/{}/boxscore.json'.format(season, game_id),
        headers={
            "Authorization": "Basic " + base64.b64encode(
                '{}:{}'.format(api_key, 'MYSPORTSFEEDS').encode('utf-8')).decode('ascii')
        }
    )

    return response.json()


def get_team_games_handler(event, context):
    api_key = os.getenv('api_key')

    return get_team_games(api_key, event['season'], event['teamid'])


def get_game_handler(event, context):
    api_key = '84b4b9ad-90dc-4cad-abd3-eb6e2f' or os.getenv('api_key')

    return get_game(api_key, event['season'], event['gameid'])


if __name__ == '__main__':
    response = requests.get(
        url='https://api.mysportsfeeds.com/v2.1/pull/nba/2019-2020-regular/games/20191116-TOR-DAL/boxscore.json',
        headers={
            "Authorization": "Basic " + base64.b64encode(
                '{}:{}'.format('84b4b9ad-90dc-4cad-abd3-eb6e2f', 'MYSPORTSFEEDS').encode('utf-8')).decode('ascii')
        }
    )

    print(response)

