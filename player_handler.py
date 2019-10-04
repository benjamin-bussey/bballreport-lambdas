import requests
import base64
import boto3
import os


def execute_request(api_key):
    try:
        response = requests.get(
            url='https://api.mysportsfeeds.com/v2.1/pull/nba/players.json',
            headers={
                "Authorization": "Basic " + base64.b64encode(
                    '{}:{}'.format(api_key, 'MYSPORTSFEEDS').encode('utf-8')).decode('ascii')
            }
        )

        return response.json()['players']

    except requests.exceptions.RequestException:
        print('HTTP Request Failed')


def clean_response(players):
    all_players = []
    for player_entry in players:
        player = player_entry['player']

        current_team = 'None'
        if player['currentTeam'] is not None:
            current_team = player['currentTeam']['id']
            player['currentTeam'] = current_team
        else:
            player.pop('currentTeam')

        player['hashKey'] = 'player{}'.format(player['id'])
        player['sortKey'] = '2019-2020|{}'.format(current_team)

        player.pop('id')


        all_players.append(player)

    return all_players


def upload_to_dynamodb(players):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('bballreport')
    with table.batch_writer() as batch:
        for player in players:
            batch.put_item(
                Item=player
            )


def player_handler(event, context):
    api_key = os.getenv('api_key')
    raw_players = execute_request(api_key)
    all_players = clean_response(raw_players)
    upload_to_dynamodb(all_players)
