import boto3
from boto3.dynamodb.conditions import Key


def setup_dynamodb():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('bballreport')

    return table


def get_game(table, game_id):
    response = table.query(
        KeyConditionExpression=Key('hashKey').eq('game{}'.format(game_id)) & Key('sortKey').eq('1')
    )
    return response['Items']


def get_season_games(table, season):
    response = table.query(
        IndexName='DailyGames',
        KeyConditionExpression=Key('hashKey').eq(season)
    )
    return response['Items']


def get_daily_games(table, season, date):
    response = table.query(
        IndexName='DailyGames',
        KeyConditionExpression=Key('hashKey').eq(season) & Key('sortKey').eq(date)
    )
    return response['Items']



def get_season_games_handler(event, context):
    table = setup_dynamodb()
    return get_season_games(table, event['season'])


# ToDo implement after adding GSI on season, date
def get_daily_games_handler(event, context):
    table = setup_dynamodb()
    return get_daily_games(table, event['season'], event['date'])


def get_game_handler(event, context):
    table = setup_dynamodb()
    return get_game(table, event['gameid'])
