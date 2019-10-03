import boto3
from boto3.dynamodb.conditions import Key


def setup_dynamodb():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('bballreport')

    return table


def query_dynamodb_all_players(table):
    """

    :param table: DynamoDB table being operated on
    :return: dictionary of all players
    """
    response = table.query(
        KeyConditionExpression=Key('season').eq('2019-2020') & Key('sortKey').begins_with('player|')
    )

    return response['Items']


def query_dynamodb_player_all_teams(table, player_id):
    """

    :param table: DynamoDB table being operated on
    :param player_id: the numeric integer for the player
    :return:
    """
    response = table.query(
        KeyConditionExpression=Key('season').eq('2019-2020') & Key('sortKey').begins_with('player|{}'
                                                                                          .format(player_id))
    )

    return response['Items']


def query_dynamodb_player_team(table, player_id, team_id):
    """

    :param table: DynamoDB table being operated on
    :param player_id: the numeric integer for the player
    :param team_id: the specific team you're looking for the player's stats on
    :return:
    """
    response = table.query(
        KeyConditionExpression=Key('season').eq('2019-2020') & Key('sortKey').begins_with('player|{}|{}'
                                                                                          .format(player_id, team_id))
    )

    return response['Items']


def get_players_handler(event, context):
    table = setup_dynamodb()
    return query_dynamodb_all_players(table)


def get_player_all_teams_handler(event, context):
    table = setup_dynamodb()
    return query_dynamodb_player_all_teams(table, event['playerid'])


def get_player_specific_team_handler(event, context):
    table = setup_dynamodb()
    return query_dynamodb_player_team(table, event['playerid'], event['teamid'])
