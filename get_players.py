import boto3
from boto3.dynamodb.conditions import Key


def setup_dynamodb():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('bballreport')

    return table


def get_player(table, player_id):
    response = table.query(
        KeyConditionExpression=Key('hashKey').eq('player{}'.format(player_id))
    )
    return response['Items']


def get_player_team(table, player_id, team_id):
    response = table.query(
        KeyConditionExpression=Key('hashKey').eq('player{}'.format(player_id)) & Key('sortKey').eq('2019-2020|{}'.format(team_id))
    )
    return response['Items']


def get_team_players(table, team_id):
    response = table.query(
        IndexName='TeamPlayers',
        KeyConditionExpression=Key('hashKey').eq(team_id)
    )
    return response['Items']


def get_player_handler(event, context):
    table = setup_dynamodb()
    return get_player(table, event['playerid'])


def get_player_team_handler(event, context)
    table = setup_dynamodb()
    return get_player_team(table, event['playerid'], event['teamid'])

def get_team_players_handler(event, context):
    table = setup_dynamodb()
    return get_team_players(table, event['teamid'])

