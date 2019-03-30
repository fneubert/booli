import requests
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
from datetime import date
import plotly.graph_objs as go
import plotly.plotly as py
import plotly
from plotly.offline import plot
from data import get_booli_data
import datedelta

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


def create_statistics_table(df):


    statistics_list = ['price_six_months', 'price_twelve_months','price_twntyfour']
    room_type = ['all', 2, 3]
    areas = ['Vasastan', 'Östermalm', 'Gärdet', 'Södermalm', 'Kungsholmen', 'Stockholms innerstad']

    table = []
    for statistic_type in statistics_list:
        for room in room_type:
            col = []
            if room == 'all':
                df_room = df
            else:
                df_room = df[df['rooms'] == int(room)]
            for area in areas:
                if not area == 'Stockholms innerstad':
                    df_statistics = df_room[df_room['location.namedAreas'].str.contains(area, na=False)]
                else:
                    df_statistics = df_room
                #print(area)
                df_averages = get_averages(df_statistics)
                if statistic_type == 'price_six_months':
                    statistic = str(round(((df_averages['averagePrices'].iloc[-1] / df_averages['averagePrices'].iloc[-7]-1)*100), 2)) + '%'
                elif statistic_type == 'price_twelve_months':
                    statistic = str(round(((df_averages['averagePrices'].iloc[-1] / df_averages['averagePrices'].iloc[-13] - 1) * 100), 2)) + '%'
                elif statistic_type == 'price_twntyfour':
                    statistic = str(round(((df_averages['averagePrices'].iloc[-1] / df_averages['averagePrices'].iloc[-25] - 1) * 100),2)) + '%'
                col.append(statistic)
            table.append(col)
            #print(table)

    header_table = go.Table(
        columnwidth=[1.55, 3, 3, 3],
        header=dict(height=50,
                    values=[' ', '<b>Prisutveckling, 6 mån</b>', '<b>Prisutveckling, 12 mån</b>', '<b>Prisutveckling, 24mån</b>'],
                    font=dict(size=12),
                    # line = dict(color = '#000000'),
                    fill=dict(color='rgb(255, 255, 2)'),
                    align='center',
                    ),
        domain=dict(x=[0.51, 1],
                    y=[0.94, 1])
    )

    statistics_table = go.Table(
        columnwidth=[1.55, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        header=dict(height=45,
                    values=['<b>Område</b>', '<b>Alla</b>', '<b>Två:or</b>', '<b>Tre:or</b>',
                            '<b>Alla</b>', '<b>Två:or</b>', '<b>Tre:or</b>', '<b>Alla</b>', '<b>Två:or</b>', '<b>Tre:or</b>'],
                    font=dict(size=11),
                    # line=dict(color='#000000'),
                    fill=dict(color='rgb(240, 240, 240)')
                    ),
        cells=dict(height=45,
                   values=[['Vasastan', 'Östermalm', 'Gärdet', 'Södermalm', 'Kungsholmen', 'Stockholms innerstad'],
                           table[0],
                           table[1],
                           table[2],
                           table[3],
                           table[4],
                           table[5],
                           table[6],
                           table[7],
                           table[8],
                           ],
                   font=dict(size=11),
                   align=['left'] + ['right'] * 9,
                   ),
        domain=dict(x=[0.51, 1],
                    y=[0.52, 0.94])
    )

    return header_table,statistics_table

def create_charts(df):

    # pre-processing
    df['rooms'].fillna(0, inplace=True)
    df['livingArea'].dropna(inplace=True)
    df['soldPrice'].dropna(inplace=True)

    site_lat = df['location.position.latitude']
    site_lon = df['location.position.longitude']
    df['soldDate'] = pd.to_datetime(df['soldDate'])
    df['squareMeterPrice'] = df['soldPrice'].divide(df['livingArea'])
    df['text'] = df['location.address.streetAddress'] + ', rum:' + df['rooms'].round(0).astype(str) + ', boarea: ' + \
                 df['livingArea'].round(0).astype(str) + ', <br />slutpris: ' + df['soldPrice'].round(0).astype(str) + ', kvadratmeterpris: ' + df['squareMeterPrice'].round(0).astype(str)
    locations_name = df['text']

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
        name='Position för <br />alla objekt',
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
        name='Snittpriser för <br />alla objekt',
        hoverinfo='x+y',
        xaxis='x',
        yaxis='y2'
    )

    trace_prices_2 = go.Scatter(
        x=df_averages_2['months'],
        y=df_averages_2['averagePrices'],
        mode='lines+markers',
        name='Snittpriser <br />för tvåor',
        hoverinfo='x+y',
        xaxis='x',
        yaxis='y2'
    )

    trace_prices_3= go.Scatter(
        x=df_averages_3['months'],
        y=df_averages_3['averagePrices'],
        mode='lines+markers',
        name='Snittpriser <br />för treor',
        hoverinfo='x+y',
        xaxis='x',
        yaxis='y2'
    )

    trace_vasastan= go.Scatter(
        x=df_averages_vasastan['months'],
        y=df_averages_vasastan['averagePrices'],
        mode='lines+markers',
        name='Snittpriser i <br />Vasastan',
        hoverinfo='x+y',
        xaxis='x3',
        yaxis='y2'
    )

    trace_kungsholmen= go.Scatter(
        x=df_averages_kungsholmen['months'],
        y=df_averages_kungsholmen['averagePrices'],
        mode='lines+markers',
        name='Snittpriser i <br />Kungsholmen',
        hoverinfo='x+y',
        xaxis='x3',
        yaxis='y2'
    )

    trace_ostermalm= go.Scatter(
        x=df_averages_ostermalm['months'],
        y=df_averages_ostermalm['averagePrices'],
        mode='lines+markers',
        name='Snittpriser i <br />Östermalm',
        hoverinfo='x+y',
        xaxis='x3',
        yaxis='y2'
    )

    trace_sodermalm= go.Scatter(
        x=df_averages_sodermalm['months'],
        y=df_averages_sodermalm['averagePrices'],
        mode='lines+markers',
        name='Snittpriser i <br />Södermalm',
        hoverinfo='x+y',
        xaxis='x3',
        yaxis='y2'
    )

    trace_gardet= go.Scatter(
        x=df_averages_gardet['months'],
        y=df_averages_gardet['averagePrices'],
        mode='lines+markers',
        name='Snittpriser i <br />Gärdet',
        hoverinfo='x+y',
        xaxis='x3',
        yaxis='y2'
    )
    
    df_averages_other  = pd.DataFrame(columns=['months', 'deals'])
    df_averages_other['deals'] = df_averages_total['deals'] - df_averages_sodermalm['deals']- df_averages_kungsholmen['deals']\
                        - df_averages_ostermalm['deals']-df_averages_vasastan['deals']

    df_averages_other['months'] = df_averages_total['months']

    trace_deals_total = go.Scatter(
        x = df_averages_other['months'],
        y=df_averages_other['deals'],
        mode='lines',
        name='Antal avslut, övriga',
        text=', övriga',
        stackgroup='one',
        hoverinfo='x+y+text',
        xaxis='x2',
        yaxis='y'
    )

    trace_deals_vasastan= go.Scatter(
        x = df_averages_vasastan['months'],
        y=df_averages_vasastan['deals'],
        mode='lines',
        name='Antal avslut i <br />Vasastan',
        text=', Vasastan',
        stackgroup='one',
        hoverinfo='x+y+text',
        xaxis='x2',
        yaxis='y'
    )

    trace_deals_ostermalm = go.Scatter(
        x = df_averages_ostermalm['months'],
        y=df_averages_ostermalm['deals'],
        mode='lines',
        name='Antal avslut i <br />Östermalm',
        text=', Östermalm',
        stackgroup='one',
        hoverinfo='x+y+text',
        xaxis='x2',
        yaxis='y'
    )

    trace_deals_kungsholmen= go.Scatter(
        x = df_averages_kungsholmen['months'],
        y=df_averages_kungsholmen['deals'],
        mode='lines',
        name='Antal avslut i <br />Kungsholmen',
        text=', Kungsholmen',
        stackgroup='one',
        hoverinfo='x+y+text',
        xaxis='x2',
        yaxis='y'
    )


    trace_deals_sodermalm= go.Scatter(
        x = df_averages_sodermalm['months'],
        y=df_averages_sodermalm['deals'],
        mode='lines',
        name='Antal avslut i <br />Södermalm',
        text=', Södermalm',
        stackgroup='one',
        hoverinfo='x+y+text',
        xaxis='x2',
        yaxis='y'
    )

    trace_deals_gardet= go.Scatter(
        x = df_averages_gardet['months'],
        y=df_averages_gardet['deals'],
        mode='lines',
        name='Antal avslut i <br />Gärdet',
        text=', Gärdet',
        stackgroup='one',
        hoverinfo='x+y+text',
        xaxis='x2',
        yaxis='y'
    )

    header_table, statistics_table = create_statistics_table(df)

    # Create layout
    layout = go.Layout(
        title='Sålda objekt i Stockholms innerstad',
        #width=1200,
        #height=1200,
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
                x=[0, 0.49],
                y=[0.52, 1]
            ),
            pitch=0,
            zoom=10,
            style='light'
        ),
        xaxis = dict(
            #df_averages_total = df_averages['months'].astype(str).tolist(),
            #range=['2015', '2020'],
            domain = [0, 0.32],
            anchor = 'y2',
            title = 'Snittpriser per rum',
            rangeselector=dict(
                buttons=list([
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                         label='YTD',
                         step='year',
                         stepmode='todate'),
                    dict(count=1,
                         label='1y',
                         step='year',
                         stepmode='backward'),
                    dict(count=2,
                         label='2y',
                         step='year',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            type='date'
        ),
        yaxis2 = dict(
            range = [70000,120000],
            domain = [0, 0.46],
            anchor = 'x',
        ),
        xaxis2 = dict(
            #range= df_averages_total['months'].astype(str).tolist(),
            #range=['2015', '2020'],
            domain = [0.68, 1],
            anchor = 'y',
            title = 'Antal avslut',
            rangeselector=dict(
                buttons=list([
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                         label='YTD',
                         step='year',
                         stepmode='todate'),
                    dict(count=1,
                         label='1y',
                         step='year',
                         stepmode='backward'),
                    dict(count=2,
                         label='2y',
                         step='year',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            type='date'
        ),
        yaxis = dict(
            domain = [0, 0.46],
            anchor = 'x2',
        ),
        xaxis3=dict(
            # df_averages_total = df_averages['months'].astype(str).tolist(),
            #range=['2015', '2020'],
            domain=[0.33, 0.65],
            anchor='y2',
            title='Snittpriser per stadsdel',
            rangeselector=dict(
                buttons=list([
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                         label='YTD',
                         step='year',
                         stepmode='todate'),
                    dict(count=1,
                         label='1y',
                         step='year',
                         stepmode='backward'),
                    dict(count=2,
                         label='2y',
                         step='year',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            type='date'
        ),
        yaxis3=dict(
            range=[70000, 120000],
            domain=[0, 0.46],
            anchor='x',
        )
    )

    fig = go.Figure(data=[data,trace_prices_total,trace_prices_2, trace_prices_3, trace_deals_total,
                          trace_vasastan, trace_kungsholmen, trace_ostermalm, trace_gardet,trace_sodermalm,
                          trace_deals_vasastan, trace_deals_sodermalm, trace_deals_ostermalm, trace_deals_gardet, trace_deals_kungsholmen,
                          header_table, statistics_table], layout=layout)
    #plot(fig, filename='snittpriser-stockholm.html', auto_open=True)
    py.plot(fig, filename='snittpriser-stockholm.html', auto_open=True)

    return

sales_data = get_sales_data()
create_charts(sales_data)

