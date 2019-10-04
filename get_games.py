import boto3
from boto3.dynamodb.conditions import Key


def setup_dynamodb():
    """
    Method for creating the dynamodb resource for querying/scanning
    :return:
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('bballreport')

    return table


def get_game(table, game_id):
    """
    Gets a single game with supplied gameid
    :param table: supplied table resource to query/scan
    :param game_id:
    :return:
    """
    response = table.query(
        KeyConditionExpression=Key('hashKey').eq('game{}'.format(game_id)) & Key('sortKey').eq('1')
    )
    return response['Items']


def get_season_games(table, season):
    """
    Gets all games for a particular season
    :param table: supplied table resource to query/scan
    :param season: the season to get games for
    :return:
    """
    response = table.query(
        IndexName='SeasonGames',
        KeyConditionExpression=Key('season').eq(season)
    )
    return response['Items']


def get_daily_games(table, season, date):
    """
    Gets all games for a particular day
    :param table: supplied table resource to query/scan
    :param season: the season to get games for
    :param date: the date to get games for
    :return:
    """
    response = table.query(
        IndexName='SeasonGames',
        KeyConditionExpression=Key('season').eq(season) & Key('date').eq(date)
    )
    return response['Items']


def get_season_games_handler(event, context):
    table = setup_dynamodb()
    return get_season_games(table, event['season'])


def get_daily_games_handler(event, context):
    table = setup_dynamodb()
    return get_daily_games(table, event['season'], event['date'])


def get_game_handler(event, context):
    table = setup_dynamodb()
    return get_game(table, event['gameid'])
