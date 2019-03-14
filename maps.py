from plotly import tools
import plotly as py
import plotly.graph_objs as go
from plotly.offline import plot
py.tools.set_credentials_file(username='fneubert', api_key='mHBK7EcgD17bpZfWyvbt')

trace0 = go.Scatter(
    x=[1, 2],
    y=[1, 2]
)
trace1 = go.Scatter(
    x=[1, 2],
    y=[1, 2]
)
trace2 = go.Scatter(
    x=[1, 2, 3],
    y=[2, 1, 2]
)
fig = tools.make_subplots(rows=2, cols=2, specs=[[{}, {}], [{'colspan': 2}, None]],
                          subplot_titles=('First Subplot','Second Subplot', 'Third Subplot'))

fig.append_trace(trace0, 1, 1)
fig.append_trace(trace1, 1, 2)
fig.append_trace(trace2, 2, 1)

fig['layout'].update(showlegend=False, title='Specs with Subplot Title')
plot(fig, filename='custom-sized-subplot-with-subplot-titles')
