import requests
import os
import boto3
import datetime
import base64
from io import StringIO
import csv


def get_all_players_data(api_key, season, date):
    datetime.datetime.today()
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket='bballreport-public-data', Key=f'{season}-player-data-{date}.csv')
        return {'status': 'Player data for this data already exists'}
    except Exception:
        data = get_msf_data(api_key, season)
        output = write_to_string(data)
        upload_to_s3(s3, season, date, output)
        return {'status': f'Created new entry for {season}:{date}'}


def get_msf_data(api_key, season):
    clean_player_data = []
    response = requests.get(
        url=f'https://api.mysportsfeeds.com/v2.1/pull/nba/{season}/player_stats_totals.json',
        headers={
            "Authorization": "Basic " + base64.b64encode(
                '{}:{}'.format(api_key, 'MYSPORTSFEEDS').encode('utf-8')).decode('ascii')
        }
    )

    raw_data = response.json()
    players = raw_data['playerStatsTotals']
    for entry in players:
        name = entry['player']['firstName'] + ' ' + entry['player']['lastName']
        position = entry['player']['primaryPosition']
        age = entry['player']['age']
        college = entry['player']['college']

        try:
            team = entry['team']['abbreviation']
        except Exception:
            team = 'FA'
        gp = entry['stats']['gamesPlayed']

        fg2m = entry['stats']['fieldGoals']['fg2PtMade']
        fg2a = entry['stats']['fieldGoals']['fg2PtAtt']
        fg2Pct = entry['stats']['fieldGoals']['fg2PtPct']
        fg2mPerGame = entry['stats']['fieldGoals']['fg2PtMadePerGame']
        fg2aPerGame = entry['stats']['fieldGoals']['fg2PtAttPerGame']

        fg3m = entry['stats']['fieldGoals']['fg3PtMade']
        fg3a = entry['stats']['fieldGoals']['fg3PtAtt']
        fg3Pct = entry['stats']['fieldGoals']['fg3PtPct']
        fg3mPerGame = entry['stats']['fieldGoals']['fg3PtMadePerGame']
        fg3aPerGame = entry['stats']['fieldGoals']['fg3PtAttPerGame']

        fgm = entry['stats']['fieldGoals']['fgMade']
        fga = entry['stats']['fieldGoals']['fgAtt']
        fgPct = entry['stats']['fieldGoals']['fgPct']
        fgmPerGame = entry['stats']['fieldGoals']['fgMadePerGame']
        fgaPerGame = entry['stats']['fieldGoals']['fgAttPerGame']

        ftm = entry['stats']['freeThrows']['ftMade']
        fta = entry['stats']['freeThrows']['ftAtt']
        ftPct = entry['stats']['freeThrows']['ftPct']
        ftmPerGame = entry['stats']['freeThrows']['ftMadePerGame']
        ftaPerGame = entry['stats']['freeThrows']['ftAttPerGame']

        trb = entry['stats']['rebounds']['reb']
        offReb = entry['stats']['rebounds']['offReb']
        defReb = entry['stats']['rebounds']['defReb']
        trbPerGame = entry['stats']['rebounds']['rebPerGame']
        offRebPerGame = entry['stats']['rebounds']['offRebPerGame']
        defRebPerGame = entry['stats']['rebounds']['defRebPerGame']

        ast = entry['stats']['offense']['ast']
        pts = entry['stats']['offense']['pts']
        astPerGame = entry['stats']['offense']['astPerGame']
        ptsPerGame = entry['stats']['offense']['ptsPerGame']

        tov = entry['stats']['defense']['tov']
        stl = entry['stats']['defense']['stl']
        blk = entry['stats']['defense']['blk']
        blka = entry['stats']['defense']['blkAgainst']
        tovPerGame = entry['stats']['defense']['tovPerGame']
        stlPerGame = entry['stats']['defense']['stlPerGame']
        blkPerGame = entry['stats']['defense']['blkPerGame']
        blkaPerGame = entry['stats']['defense']['blkAgainstPerGame']

        foulsPers = entry['stats']['miscellaneous']['foulPers']
        foulsPerGame = entry['stats']['miscellaneous']['foulPersPerGame']
        foulsPersDrawn = entry['stats']['miscellaneous']['foulPersDrawn']
        foulsPersDrawnPerGame = entry['stats']['miscellaneous']['foulPersDrawnPerGame']
        plusMinus = entry['stats']['miscellaneous']['plusMinus']
        plusMinusPerGame = entry['stats']['miscellaneous']['plusMinusPerGame']
        minSeconds = entry['stats']['miscellaneous']['minSeconds']
        minSecondsPerGame = entry['stats']['miscellaneous']['minSecondsPerGame']
        gamesStarted = entry['stats']['miscellaneous']['gamesStarted']

        clean_player_data.append([name, position, age, college, team, gp, fg2m, fg2a, fg2Pct, fg2mPerGame, fg2aPerGame,
                                 fg3m, fg3a, fg3Pct, fg3mPerGame, fg3aPerGame, fgm, fga, fgPct, fgmPerGame, fgaPerGame,
                                 ftm, fta, ftPct, ftmPerGame, ftaPerGame, trb, offReb, defReb, trbPerGame,
                                 offRebPerGame, defRebPerGame, ast, pts, astPerGame, ptsPerGame, tov, stl, blk, blka,
                                 tovPerGame, stlPerGame, blkPerGame, blkaPerGame, foulsPers, foulsPerGame,
                                 foulsPersDrawn, foulsPersDrawnPerGame, plusMinus, plusMinusPerGame, minSeconds,
                                 minSecondsPerGame, gamesStarted])

    return clean_player_data


def write_to_string(data):
    output = StringIO()
    writer = csv.writer(output)
    for entry in data:
        writer.writerow(entry)

    return output


def upload_to_s3(s3, season, date, information):
    s3.put_object(Bucket='bballreport-public-data', Key=f'{season}-player-data-{date}.csv', Body=information.getvalue())


def update_daily_player_season_stats_handler(event, context):
    api_key = os.getenv('api_key')
    get_all_players_data(api_key, event['season'], datetime.datetime.today().date())
