import requests
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
from datetime import date
import plotly.graph_objs as go
import plotly
from plotly.offline import plot
from data import get_booli_data

plotly.tools.set_credentials_file(username='fneubert', api_key='mHBK7EcgD17bpZfWyvbt')
mapbox_access_token = 'pk.eyJ1IjoiZm5ldWJlcnQiLCJhIjoiY2p0OHZ3MTc0MGM0czRhbzc4eGUwc3RmciJ9.g8WKRZc7pgEQN0JocAeFqg'


def get_sales_data():

    try:
        sales_data = pd.read_csv('booli_data ' + str(date.today())+'.csv', low_memory=False)
    except:
        sales_data = get_booli_data()

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

    df_averages = pd.DataFrame(columns = ['months', 'averagePrices', 'deals'])
    df['soldDate'] = pd.to_datetime(df['soldDate'])
    df_averages['months'] = pd.date_range(start = df['soldDate'].min(), end=df['soldDate'].max(), freq='M')
    df['squareMeterPrice'] = df['soldPrice'].divide(df['livingArea'])

    i=0
    for month in df_averages['months']:
        print(i)
        if i == 0:
            filtered_df = df[df['soldDate'] < month]
            filtered_df['squareMeterPrice'].dropna(inplace=True)
            df_averages.at[i,'averagePrices'] = filtered_df['squareMeterPrice'].mean()
            df_averages.at[i,'deals'] = len(filtered_df)
            last_month = month
            i = i + 1
            continue
        filtered_df = df[(df['soldDate'] >= last_month) & (df['soldDate'] < month)]
        filtered_df['squareMeterPrice'].dropna(inplace=True)
        df_averages.at[i,'averagePrices'] = filtered_df['squareMeterPrice'].mean()
        df_averages.at[i,'deals'] = len(filtered_df)
        last_month = month
        i = i + 1

    #print(df_averages)

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

    trace3 = go.Scatter(
        x = df_averages['months'],
        y = df_averages['averagePrices'],
        hoverinfo='x+y',
        xaxis='x',
        yaxis='y2'
    )
    trace4 = go.Scatter(
        x = df_averages['months'],
        y=df_averages['deals'],
        mode='lines',
        fill='tozeroy',
        hoverinfo='x+y',
        xaxis='x2',
        yaxis='y'

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
            #range = df_averages['months'].astype(str).tolist(),
            range=['2015', '2019'],
            domain = [0, 0.48],
            anchor = 'y2',
            title = 'Snittpriser',
        ),
        yaxis2 = dict(
            range = [0,df_averages['averagePrices'].max()],
            domain = [0, 0.2],
            anchor = 'x',
        ),
        xaxis2 = dict(
            #range= df_averages['months'].astype(str).tolist(),
            range=['2015', '2019'],
            domain = [0.53, 1],
            anchor = 'y',
            title = 'Antal avslut'
        ),
        yaxis = dict(
            range = [0,df_averages['deals'].max()],
            domain = [0, 0.2],
            anchor = 'x2'
        )
    )

    fig = go.Figure(data=[data,trace3,trace4], layout=layout)
    plot(fig, filename='snittpriser-stockholm.html', auto_open=True)

    return

sales_data = get_sales_data()
create_charts(sales_data)

