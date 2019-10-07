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


def clean_response(data):
    games = []
    for game in data:
        games.append(game['schedule'])

    return games


def get_team_games_handler(event, context):
    api_key = os.getenv('api_key')

    team_games = get_team_games(api_key, event['season'], event['teamid'])
    return clean_response(team_games)
