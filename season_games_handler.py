import requests
import base64
import boto3
import os


def execute_request(api_key, url):
    try:
        response = requests.get(
            url=url,
            headers={
                "Authorization": "Basic " + base64.b64encode(
                    '{}:{}'.format(api_key, 'MYSPORTSFEEDS').encode('utf-8')).decode('ascii')
            }
        )

        return response.json()

    except requests.exceptions.RequestException:
        print('HTTP Request Failed')


def clean_data(game_data):
    team_reference_info = game_data['references']['teamReferences']
    all_games_info = []

    for entry in game_data['games']:
        entry_info = entry['schedule']

        entry_info['hashKey'] = 'game{}'.format(entry_info['id'])
        entry_info['sortKey'] = '1'
        entry_info['season'] = '2019-2020-regular'
        entry_info['date'] = entry_info['startTime'].split('T')[0]
        entry_info.pop('id')

        entry_info['awayTeamid'] = entry_info['awayTeam']['id']
        entry_info['homeTeamid'] = entry_info['homeTeam']['id']

        away_team = list(filter(lambda team: team['id'] == entry_info['awayTeamid'], team_reference_info))[0]
        home_team = list(filter(lambda team: team['id'] == entry_info['homeTeamid'], team_reference_info))[0]

        entry_info['awayTeam'] = away_team
        entry_info['homeTeam'] = home_team

        entry_info['scores'] = {}

        all_games_info.append(entry_info)
    return all_games_info


def upload_to_dynamodb(games):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('bballreport')
    with table.batch_writer() as batch:
        for game in games:
            batch.put_item(
                Item=game
            )


def season_games_handler(event, context):
    response_game_data = execute_request(os.getenv('api_key'), 'https://api.mysportsfeeds.com/v2.1/pull/nba/2019-2020-regular/games.json')
    clean_game_data = clean_data(response_game_data)
    upload_to_dynamodb(clean_game_data)
