import requests
import boto3
import base64
import os


def setup_dynamodb():
    """
    Method for creating the dynamodb resource for querying/scanning
    :return:
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('bballreport')

    return table


def get_daily_standings(api_key):
    response = requests.get(
        url = 'https://api.mysportsfeeds.com/v2.1/pull/nba/2019-2020-regular/standings.json',
        headers={
            "Authorization": "Basic " + base64.b64encode(
                '{}:{}'.format(api_key, 'MYSPORTSFEEDS').encode('utf-8')).decode('ascii')
        }
    )

    return response.json()


def clean_response(standings):
    standings['hashKey'] = 'standings{}'.format(standings['lastUpdatedOn'].split('T')[0])
    for team in standings['teams']:
        team.pop('divisionRank', None)
        team['team'].pop('homeVenue', None)
    return standings


def add_to_dynamodb(table, standings):
    table.put_item(
        Item=standings
    )


def daily_standings_handler(event, context):
    api_key = os.getenv('api_key')
    table = setup_dynamodb()

    daily_standings = get_daily_standings(api_key)
    clean_standings = clean_response(daily_standings)
    add_to_dynamodb(table, clean_standings)
