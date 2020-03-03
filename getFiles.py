import json

import pandas as pd
import requests


def processData(url, key, token, fields, filter=None, dataframe=True):
    querystring = {"key": key, "token": token, 'fields': fields}
    if filter:
        querystring['filter'] = filter
    response = requests.request("GET", url, params=querystring)
    parsed = json.loads(response.text)
    if dataframe:
        return pd.DataFrame(parsed)
    else:
        return parsed


def cards(board, key, token):
    url = f"https://api.trello.com/1/boards/{board}/cards"
    fields = ['id', 'name', 'dateLastActivity', 'desc', 'idBoard', 'idList', 'idShort', 'idLabels', 'due',
              'idChecklists', 'shortUrl']
    df = processData(url, key, token, fields)
    df.to_csv('stage/cards.csv', index=False)


def lists(board, key, token):
    url = f"https://api.trello.com/1/boards/{board}/lists"
    fields = ['id', 'name']
    df = processData(url, key, token, fields)
    df.to_csv('stage/lists.csv', index=False)


def labels(board, key, token):
    url = f"https://api.trello.com/1/boards/{board}/labels"
    fields = ['id', 'name', 'color']
    df = processData(url, key, token, fields)
    df.to_csv('stage/labels.csv', index=False)


def actions(board, key, token):
    cards = pd.read_csv('stage/cards.csv')
    cards = cards['id']
    dflist = []

    for id in cards:
        url = f"https://api.trello.com/1/cards/{id}/actions"
        fields = ['all']
        data = processData(url, key, token, fields, dataframe=False)

        for entry in data:
            entry['cardid'] = id
            if entry['type'] == 'updateCard':
                entry['listBefore'] = entry['data']['listBefore']['id']
                entry['listCurrent'] = entry['data']['listAfter']['id']
                entry['commentText'] = None
            elif entry['type'] == 'commentCard':
                entry['listBefore'] = None
                entry['listCurrent'] = entry['data']['list']['id']
                entry['commentText'] = entry['data']['text']

            for k in ['memberCreator', 'data', 'limits']:
                entry.pop(k, None)

            dflist.append(entry)
    newDf = pd.DataFrame(dflist)
    newDf.to_csv('stage/actions.csv', index=False)


def run(board, key, token):
    for func in [cards, labels, lists, actions]:
        func(board, key, token)
