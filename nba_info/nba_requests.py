__author__ = 'Sumbhav'

import requests

def make_request(url):
    #BORROWED FROM seemsthere's nba_py
    headers = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/45.0.2454.101 Safari/537.36'),
               'referer': 'http://stats.nba.com/scores/'
            }
    return requests.get(url, headers=headers)