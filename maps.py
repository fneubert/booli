import plotly.graph_objs as go
import plotly
import plotly.plotly as py
from plotly.offline import plot
plotly.tools.set_credentials_file(username='fneubert', api_key='mHBK7EcgD17bpZfWyvbt')

header_table = go.Table(
    columnwidth=[1.55, 3, 3, 3, 3],
    header=dict(height=50,
                values=[' ', '<b>Prisutveckling, 6 mån</b>', '<b>Prisutveckling, 12 mån</b>',
                        '<b>Volatilitet, 6 mån</b>', '<b>Volatilitet, 12 mån</b>'],
                font=dict(size=12),
                # line = dict(color = '#000000'),
                fill=dict(color='rgb(255, 255, 2)'),
                align='center',
                ),
    domain=dict(x=[0.35, 1],
                y=[0.92, 1])
)

statistics_table = go.Table(
    columnwidth=[1.55,1,1,1,1,1,1,1,1,1,1,1,1,1],
    header=dict(height=45,
                values=['<b>Område</b>', '<b>Alla</b>', '<b>Två:or</b>', '<b>Tre:or</b>',
                        '<b>Alla</b>', '<b>Två:or</b>', '<b>Tre:or</b>', '<b>Alla</b>', '<b>Två:or</b>', '<b>Tre:or</b>',
                        '<b>Alla</b>', '<b>Två:or</b>', '<b>Tre:or</b>'],
                font=dict(size=11),
                # line=dict(color='#000000'),
                fill=dict(color='rgb(240, 240, 240)')
                ),
    cells=dict(height=40,
               values=[['Vasastan', 'Östermalm', 'Gärdet', 'Södermalm', 'Kungsholmen'],
                       [1, 2, 3, 4, 5],
                       [1, 2, 3, 4, 5],
                       [1, 2, 3, 4, 5],
                       [1, 2, 3, 4, 5],
                       [1, 2, 3, 4, 5],
                       [1, 2, 3, 4, 5],
                       [1, 2, 3, 4, 5],
                       [1, 2, 3, 4, 5],
                       [1, 2, 3, 4, 5],
                       [1, 2, 3, 4, 5],
                       [1, 2, 3, 4, 5],
                       [1, 2, 3, 4, 5]
                       ],
               font=dict(size=11),
               align=['left'] + ['right'] * 12,
               ),
    domain=dict(x=[0.35, 1],
                y=[0.3, 0.92])
)

data = [header_table, statistics_table]
plot(data, filename = 'basic_table',auto_open=True)

