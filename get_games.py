import boto3
from boto3.dynamodb.conditions import Key


def setup_dynamodb():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('bballreport')

    return table


def get_season_games(table, season, mode):
    response = table.query(
        KeyConditionExpression=Key('season').eq(season) & Key('sortKey').begins_with(mode)
    )
    return response['Items']


def get_daily_games(table, date):
    response = table.query(
        KeyConditionExpression=Key('season').eq(2019-2020) & Key('sortKey').begins_with('regular|{}'.format(date))
    )

    return response['Items']


# ToDo implement after adding GSI on gameID
def get_game(table, season, date, game_id):
    pass


def get_season_games_handler(event, context):
    table = setup_dynamodb()
    return get_season_games(table, event['season'], event['mode'])


def get_daily_games_handler(event, context):
    table = setup_dynamodb()
    return get_daily_games(table, event['date'])


# ToDo implement after adding GSI on gameID
def get_game_handler(event, context):
    pass
