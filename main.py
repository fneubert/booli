import requests
import json
import numpy as np
import pandas as pd
import plotly


def get_booli_data():
    URL = 'http://www.snittpris.se/backend/?id=MTQz&minSoldDate=20170310&maxSoldDate=20190310&minFloor=&maxFloor=%27&minLivingArea=&maxLivingArea=&minRooms=&maxRooms=&objectType=VmlsbGEsTMOkZ2VuaGV0LEfDpXJkLFRvbXQtbWFyayxGcml0aWRzaHVzLFBhcmh1cyxLZWRqZWh1cw==&offset=0'

    session = requests.session()


    authentication_data = {
    'Accept': 'application / json, text / plain, * / *',
    'Accept - Encoding': 'gzip, deflate',
    'Accept - Language': 'sv - SE, sv; q = 0.9, en - US; q = 0.8, en; q = 0.7, de; q = 0.6',
    'Connection': 'keep - alive',
    'Cookie': '_ga = GA1.2.1935937918.1552236605;'
            'gid = GA1.2.1231589156.1552236605;_gat=1',
    'Host': 'www.snittpris.se',
    'Referer': 'http: // www.snittpris.se /',
    'User - Agent': 'Mozilla / 5.0(Macintosh;'
    'Intel Mac OS X 10_14_3) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 72.0.3626.96 Safari / 537.36'
        }

    req = session.get(URL, headers=authentication_data)

    if req.status_code != requests.codes.ok:
        print('fail')

    booli_data = req.json()

    print(booli_data)

    return booli_data

def create_charts():
    return

booli_data = get_booli_data()
