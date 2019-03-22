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
        sales_data = pd.read_csv('booli_data ' + str(date.today())+'.csv', low_memory=True)
    except:
        sales_data = get_booli_data()

    return sales_data


def get_averages(df):

    df_averages = pd.DataFrame(columns=['months', 'averagePrices', 'deals'])
    df_averages['months'] = pd.date_range(start = df['soldDate'].min(), end=df['soldDate'].max(), freq='M')
    i = 0
    for month in df_averages['months']:
        #print(i)
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

    return df_averages

def create_charts(df):

    # pre-processing
    df['rooms'].fillna(0, inplace=True)
    df['livingArea'].dropna(inplace=True)
    df['soldPrice'].dropna(inplace=True)
    df['text'] = df['location.address.streetAddress'] + ', rum:' + df['rooms'].round(0).astype(str) + ', boarea: ' + \
                 df['livingArea'].round(0).astype(str) + ', slutpris: ' + df['soldPrice'].round(0).astype(str)

    site_lat = df['location.position.latitude']
    site_lon = df['location.position.longitude']
    locations_name = df['text']
    df['soldDate'] = pd.to_datetime(df['soldDate'])
    df['squareMeterPrice'] = df['soldPrice'].divide(df['livingArea'])

    # Create averages DFs

    df_2 = df[df['rooms'] == 2]
    df_3 = df[df['rooms'] == 3]
    df_averages_2 = get_averages(df_2)
    df_averages_3 = get_averages(df_3)
    df_averages_total = get_averages(df)

    # Create location-based averages DFs
    df_vasastan = df[df['location.namedAreas'].str.contains('Vasastan', na=False)]
    df_kungsholmen = df[df['location.namedAreas'].str.contains('Kungsholmen', na=False)]
    df_ostermalm = df[df['location.namedAreas'].str.contains('Östermalm', na=False)]
    df_sodermalm = df[df['location.namedAreas'].str.contains('Södermalm', na=False)]
    df_gardet = df[df['location.namedAreas'].str.contains('Gärdet', na=False)]

    df_averages_vasastan = get_averages(df_vasastan)
    df_averages_kungsholmen = get_averages(df_kungsholmen)
    df_averages_ostermalm = get_averages(df_ostermalm)
    df_averages_sodermalm = get_averages(df_sodermalm)
    df_averages_gardet = get_averages(df_gardet)


    # Create traces
    data = go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        name='Position för alla sålda bostadsrätter',
        marker=go.scattermapbox.Marker(
            size=7,
            color='rgb(255, 0, 255)',
            opacity=0.7
        ),
        text=locations_name,
        hoverinfo='text'
    )

    trace_prices_total = go.Scatter(
        x = df_averages_total['months'],
        y = df_averages_total['averagePrices'],
        mode='lines+markers',
        name='Snittpriser för alla bostadsrätter',
        hoverinfo='x+y',
        xaxis='x',
        yaxis='y2'
    )

    trace_prices_2 = go.Scatter(
        x=df_averages_2['months'],
        y=df_averages_2['averagePrices'],
        mode='lines+markers',
        name='Snittpriser för tvåor',
        hoverinfo='x+y',
        xaxis='x',
        yaxis='y2'
    )

    trace_prices_3= go.Scatter(
        x=df_averages_3['months'],
        y=df_averages_3['averagePrices'],
        mode='lines+markers',
        name='Snittpriser för treor',
        hoverinfo='x+y',
        xaxis='x',
        yaxis='y2'
    )

    trace_vasastan= go.Scatter(
        x=df_averages_vasastan['months'],
        y=df_averages_vasastan['averagePrices'],
        mode='lines+markers',
        name='Snittpriser i Vasastan',
        hoverinfo='x+y',
        xaxis='x3',
        yaxis='y3'
    )

    trace_kungsholmen= go.Scatter(
        x=df_averages_kungsholmen['months'],
        y=df_averages_kungsholmen['averagePrices'],
        mode='lines+markers',
        name='Snittpriser i Kungsholmen',
        hoverinfo='x+y',
        xaxis='x3',
        yaxis='y3'
    )

    trace_ostermalm= go.Scatter(
        x=df_averages_ostermalm['months'],
        y=df_averages_ostermalm['averagePrices'],
        mode='lines+markers',
        name='Snittpriser i Östermalm',
        hoverinfo='x+y',
        xaxis='x3',
        yaxis='y3'
    )

    trace_sodermalm= go.Scatter(
        x=df_averages_sodermalm['months'],
        y=df_averages_sodermalm['averagePrices'],
        mode='lines+markers',
        name='Snittpriser i Södermalm',
        hoverinfo='x+y',
        xaxis='x3',
        yaxis='y3'
    )

    trace_gardet= go.Scatter(
        x=df_averages_gardet['months'],
        y=df_averages_gardet['averagePrices'],
        mode='lines+markers',
        name='Snittpriser i Gärdet',
        hoverinfo='x+y',
        xaxis='x3',
        yaxis='y3'
    )

    trace_deals_total = go.Scatter(
        x = df_averages_total['months'],
        y=df_averages_total['deals'],
        mode='lines',
        name='Antal avslut för alla bostadsrätter',
        fill='tozeroy',
        hoverinfo='x+y',
        xaxis='x2',
        yaxis='y'
    )

    trace1 = go.Scatter(
        x=[1, 2, 3],
        y=[4, 5, 6],
        xaxis='x3',
        yaxis='y3'
    )

    # Create layout
    layout = go.Layout(
        title='Sålda objekt i Stockholm',
        #width=1200,
        #height=720,
        margin=dict(
            t=80,
            l=80,
            b=80,
            r=80,
            pad=2,
        ),
        autosize=True,
        hovermode='closest',
        showlegend=True,
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=59.329444,
                lon=18.068611
            ),
            domain=dict(
                x=[0,1],
                y=[0.35,1]
            ),
            pitch=0,
            zoom=10,
            style='light'
        ),
        xaxis = dict(
            #df_averages_total = df_averages['months'].astype(str).tolist(),
            #range=['2015', '2020'],
            domain = [0, 0.3],
            anchor = 'y2',
            title = 'Snittpriser per rum',
        ),
        yaxis2 = dict(
            range = [70000,120000],
            domain = [0, 0.3],
            anchor = 'x',
        ),
        xaxis2 = dict(
            #range= df_averages_total['months'].astype(str).tolist(),
            #range=['2015', '2020'],
            domain = [0.65, 1],
            anchor = 'y',
            title = 'Antal avslut'
        ),
        yaxis = dict(
            range = [0,df_averages_total['deals'].max()],
            domain = [0, 0.3],
            anchor = 'x2',
        ),
        xaxis3=dict(
            # df_averages_total = df_averages['months'].astype(str).tolist(),
            #range=['2015', '2020'],
            domain=[0.35, 0.6],
            anchor='y2',
            title='Snittpriser per stadsdel',
        ),
        yaxis3=dict(
            range=[70000, 120000],
            domain=[0, 0.3],
            anchor='x',
        )
    )

    fig = go.Figure(data=[data,trace_prices_total,trace_prices_2, trace_prices_3, trace_deals_total,
                          trace_vasastan, trace_kungsholmen, trace_ostermalm, trace_gardet,trace_sodermalm], layout=layout)
    plot(fig, filename='snittpriser-stockholm.html', auto_open=True)

    return

sales_data = get_sales_data()
create_charts(sales_data)

