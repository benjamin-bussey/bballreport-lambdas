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


def get_player(table, player_id):
    """
    Method for retrieving all entries for a player across multiple seasons and teams
    :param table: supplied table resource to query/scan
    :param player_id: the id of the player
    :return:
    """
    response = table.query(
        KeyConditionExpression=Key('hashKey').eq('player{}'.format(player_id))
    )
    return response['Items']


def get_player_team(table, player_id, season, team_id):
    """
    Gets information about a player for a specific season for a specific team
    :param table: supplied table resource to query/scan
    :param player_id: the id of the player
    :param team_id: the id of the team
    :return:
    """
    print(player_id)
    print(season)
    print(team_id)

    response = table.query(
        KeyConditionExpression=Key('hashKey').eq('player{}'.format(player_id)) & Key('sortKey').eq('{}|{}'.format(season, team_id))
    )
    return response['Items']


def get_team_players(table, team_id):
    """

    :param table: supplied table resource to query/scan
    :param team_id: the id of the team
    :return:
    """
    response = table.query(
        IndexName='TeamPlayers',
        KeyConditionExpression=Key('currentTeam').eq(team_id)
    )
    return response['Items']


def get_player_handler(event, context):
    table = setup_dynamodb()
    return get_player(table, event['playerid'])


def get_player_team_handler(event, context):
    table = setup_dynamodb()
    return get_player_team(table, event['playerid'], event['season'], event['teamid'])


def get_team_players_handler(event, context):
    table = setup_dynamodb()
    return get_team_players(table, event['teamid'])
