import pandas as pd


def getKeys():
    creds = pd.read_csv('creds', index_col='id')
    key = creds.loc['key'][0]
    token = creds.loc['token'][0]
    return key, token
