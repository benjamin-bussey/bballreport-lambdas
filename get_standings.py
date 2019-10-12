import requests
import base64
import os


def get_standings(api_key, season):
    response = requests.get(
        url='https://api.mysportsfeeds.com/v2.1/pull/nba/{}/standings.json?stats=none'.format(season),
        headers={
            "Authorization": "Basic " + base64.b64encode(
                '{}:{}'.format(api_key, 'MYSPORTSFEEDS').encode('utf-8')).decode('ascii')
        }
    )

    return response.json()


def sort_teams(teams):
    east_teams = []
    west_teams = []

    for team in teams:
        if team['conferenceRank']['conferenceName'] == 'Eastern':
            east_teams.append(team)
        else:
            west_teams.append(team)

    east_sorted = sorted(east_teams, key=lambda team_entry: team_entry['conferenceRank']['rank'])
    west_sorted = sorted(west_teams, key=lambda team_entry: team_entry['conferenceRank']['rank'])

    return {
        "east": east_sorted,
        "west": west_sorted
    }


def standings_handler(event, context):
    api_key = os.getenv('api_key')
    team_data = get_standings(api_key, event['season'])
    return sort_teams(team_data)
