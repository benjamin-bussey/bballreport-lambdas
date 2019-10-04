import requests
import json
import base64
import boto3
import os
from datetime import date


def get_daily_games(api_key, date):
    url = 'https://api.mysportsfeeds.com/v2.1/pull/nba/2019-2020-regular/date/{}/games.json'.format(date)

    try:
        response = requests.get(
            url=url,
            headers={
                "Authorization": "Basic " + base64.b64encode(
                    '{}:{}'.format(api_key, 'MYSPORTSFEEDS').encode('utf-8')).decode('ascii')
            }
        )

        daily_games = json.loads(response.content.decode('utf-8'))['games']

        game_ids = []
        for game in daily_games:
            game_ids.append(game['schedule']['id'])

        return game_ids

    except requests.exceptions.RequestException:
        print('HTTP Request Failed')


def execute_request(api_key, game_ids):
    games = []
    for game in game_ids:
        url = 'https://api.mysportsfeeds.com/v2.1/pull/nba/2019-2020-regular/games/{}/boxscore.json'.format(game)

        try:
            response = requests.get(
                url=url,
                headers={
                    "Authorization": "Basic " + base64.b64encode(
                        '{}:{}'.format(api_key, 'MYSPORTSFEEDS').encode('utf-8')).decode('ascii')
                }
            )

            game_data = json.loads(response.content.decode('utf-8'))

            for quarter in game_data['scoring']['quarters']:
                quarter.pop('scoringPlays', None)

            game_id = game_data['game']['id']
            stats = game_data['stats']
            summary_stats = game_data['scoring']

            games.append((game_id, stats, summary_stats))
        except requests.exceptions.RequestException:
            print('HTTP Request Failed')

    return games


def update_dynamodb(game_boxscores, date):
    client = boto3.client('dynamodb')

    for game_id, stats, summary_stats in game_boxscores:
        client.update_item(
            TableName='bballreport',
            Key={
                'season': '2019-2020',
                'sortKey': 'regular|{}|{}'.format(date, game_id)
            },
            UpdateExpression='set scores.stats = :b, scores.summaryStats = :s',
            ExpressionAttributeValues={
                ':b': stats,
                ':s': summary_stats
            }
        )


def daily_games_handler(event, context):
    api_key = os.getenv('api_key')
    today = date.today().strftime('%Y%m%d')

    game_ids = get_daily_games(api_key, today)
    game_boxscores = execute_request(api_key, game_ids)
    update_dynamodb(game_boxscores, today)
