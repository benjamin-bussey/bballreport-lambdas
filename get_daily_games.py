import boto3
from boto3.dynamodb.conditions import Key


def query_dynamodb(date):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('bballreport')

    response = table.query(
        KeyConditionExpression=Key('season').eq(2019-2020) & Key('sortKey').begins_with('regular|{}'.format(date))
    )

    return response['Items']


def get_daily_games_handler(event, context):
    date = event['date']
    return query_dynamodb(date)
