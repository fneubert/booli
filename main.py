import requests
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
from datetime import date
import plotly.graph_objs as go
import plotly
from plotly.offline import plot
plotly.tools.set_credentials_file(username='fneubert', api_key='mHBK7EcgD17bpZfWyvbt')
mapbox_access_token = 'pk.eyJ1IjoiZm5ldWJlcnQiLCJhIjoiY2p0OHZ3MTc0MGM0czRhbzc4eGUwc3RmciJ9.g8WKRZc7pgEQN0JocAeFqg'


def get_sales_data():
    today = str(date.today()).replace('-', '')
    URL = 'http://www.snittpris.se/backend/?id=MTQz&minSoldDate=20170310&maxSoldDate='+today+'&minFloor=&maxFloor=%27&minLivingArea=&maxLivingArea=&minRooms=&maxRooms=&objectType=VmlsbGEsTMOkZ2VuaGV0LEfDpXJkLFRvbXQtbWFyayxGcml0aWRzaHVzLFBhcmh1cyxLZWRqZWh1cw==&offset=0'

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
    sales_data = json_normalize(booli_data['sold'])

    return sales_data

def create_charts(df):

    df['rooms'].fillna(0, inplace=True)
    df['livingArea'].dropna(inplace=True)
    df['soldPrice'].dropna(inplace=True)
    df['text'] = df['location.address.streetAddress'] + ', rum:' + df['rooms'].round(0).astype(str) + ', boarea: ' + \
                 df['livingArea'].round(0).astype(str) + ', slutpris: ' + df['soldPrice'].round(0).astype(str)

    site_lat = df['location.position.latitude']
    site_lon = df['location.position.longitude']
    locations_name = df['text']

    data = go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=7,
            color='rgb(255, 0, 255)',
            opacity=0.7
        ),
        text=locations_name,
        hoverinfo='text'
    )

    trace1 = go.Scatter(
        x=[1, 2, 3],
        y=[4, 5, 6]
    )
    trace2 = go.Scatter(
        x=[20, 30, 40],
        y=[50, 60, 70],
        xaxis='x2',
        yaxis='y2'
    )

    layout = go.Layout(
        title='Sålda objekt i Stockholm',
        width=960,
        height=720,
        margin=dict(
            t=80,
            l=80,
            b=80,
            r=80,
            pad=2,
        ),
        #autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=59.329444,
                lon=18.068611
            ),
            domain=dict(
                x=[0,1],
                y=[0.24,1]
            ),
            pitch=0,
            zoom=10,
            style='light'
        ),
        xaxis = dict(
            range = ['2017', '2019'],
            domain = [0, 0.48],
            anchor = 'y2',
            title = 'Antal avslut',
        ),
        yaxis2 = dict(
            range = [0, 10],
            domain = [0, 0.2],
            anchor = 'x',
        ),
        xaxis2 = dict(
            range= ['2017', '2019'],
            domain = [0.53,1],
            anchor = 'y',
            title = 'Snittpriser'
        ),
        yaxis = dict(
            range = [0, 70],
            domain = [0, 0.2],
            anchor = 'x2'
        )
    )

    fig = go.Figure(data=[data,trace1,trace2], layout=layout)
    plot(fig, filename='snittpriser-stockholm.html', auto_open=True)

    return

def create_sales_chart():
    return

sales_data = get_sales_data()
create_charts(sales_data)