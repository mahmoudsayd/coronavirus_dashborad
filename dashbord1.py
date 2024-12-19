
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv(r'C:\\Users\\Administrator\\Desktop\\Sales-scorecard-in-plotly-dash-main\\country_wise_latest.csv')

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Corona Dashboard'),

    html.Div([
        html.Label("Select Metric:"),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[
                {'label': 'Confirmed', 'value': 'Confirmed'},
                {'label': 'Deaths', 'value': 'Deaths'},
                {'label': 'Recovered', 'value': 'Recovered'},
                {'label': 'Active', 'value': 'Active'},
                {'label': 'New cases', 'value': 'New cases'},
                {'label': 'New deaths', 'value': 'New deaths'}
            ],
            value='Deaths'
        )
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': i, 'value': i} for i in df['WHO Region'].unique()],
            value=df['WHO Region'].unique()[0]
        )
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

     html.Div([
        dcc.Graph(id='country-bar-chart', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='country-pie-chart', style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ], style={'width': '95%', 'display': 'inline-block'}),

    html.Div([
      dcc.Graph(id='country-scatter-chart', style={'width': '48%', 'display': 'inline-block'}),
      dcc.Graph(id='country-line-chart', style={'width': '48%', 'float': 'right', 'display': 'inline-block'})

    ], style={'width': '95%', 'display': 'inline-block'}),

     html.Div([
      dcc.Graph(id='country-bubble-chart', style={'width': '48%', 'display': 'inline-block'}),
      dcc.Graph(id='country-histogram-chart', style={'width': '48%', 'float': 'right', 'display': 'inline-block'})

    ], style={'width': '95%', 'display': 'inline-block'})


])

@app.callback(
    Output(component_id='country-bar-chart', component_property='figure'),
    [Input(component_id='metric-dropdown', component_property='value'),
     Input(component_id='region-dropdown', component_property='value')]
)
def update_bar_chart(selected_metric, selected_region):
    filtered_df = df[df['WHO Region'] == selected_region]

    fig = px.bar(filtered_df.sort_values(selected_metric).tail(15),
                 x=selected_metric, y="Country/Region", color='WHO Region',
                 text=selected_metric, orientation='h', width=600,
                 color_discrete_sequence = px.colors.qualitative.Dark2)

    fig.update_layout(title=f'{selected_metric} by Country in {selected_region}',
                      xaxis_title="", yaxis_title="",
                      yaxis_categoryorder = 'total ascending',
                      uniformtext_minsize=8, uniformtext_mode='hide')
    return fig


@app.callback(
    Output(component_id='country-pie-chart', component_property='figure'),
    [Input(component_id='metric-dropdown', component_property='value'),
     Input(component_id='region-dropdown', component_property='value')]
)
def update_pie_chart(selected_metric, selected_region):
    filtered_df = df[df['WHO Region'] == selected_region]

    fig = px.pie(filtered_df, values=selected_metric, names='Country/Region',
                 title=f'{selected_metric} Distribution in {selected_region}',
                 color_discrete_sequence = px.colors.qualitative.Dark2)
    return fig


@app.callback(
    Output(component_id='country-scatter-chart', component_property='figure'),
    [Input(component_id='metric-dropdown', component_property='value'),
     Input(component_id='region-dropdown', component_property='value')]
)
def update_scatter_chart(selected_metric, selected_region):
    filtered_df = df[df['WHO Region'] == selected_region]

    fig = px.scatter(filtered_df, x="Confirmed", y=selected_metric,
                     title=f'Confirmed vs {selected_metric} in {selected_region}',
                    color='Country/Region',
                    color_discrete_sequence = px.colors.qualitative.Dark2)
    return fig

@app.callback(
    Output(component_id='country-line-chart', component_property='figure'),
    [Input(component_id='metric-dropdown', component_property='value'),
     Input(component_id='region-dropdown', component_property='value')]
)
def update_line_chart(selected_metric, selected_region):
    filtered_df = df[df['WHO Region'] == selected_region]

    fig = px.line(filtered_df.sort_values(selected_metric).tail(15),
                   x="Country/Region", y=selected_metric,
                     title=f'{selected_metric} trend in {selected_region}',
                    color='Country/Region',
                    color_discrete_sequence = px.colors.qualitative.Dark2)
    return fig


@app.callback(
    Output(component_id='country-bubble-chart', component_property='figure'),
    [Input(component_id='metric-dropdown', component_property='value'),
     Input(component_id='region-dropdown', component_property='value')]
)
def update_bubble_chart(selected_metric, selected_region):
    filtered_df = df[df['WHO Region'] == selected_region]

    fig = px.scatter(filtered_df, x="Confirmed", y=selected_metric,
                     size=selected_metric, color="Country/Region",
                     hover_name="Country/Region", size_max=60,
                     title=f'Bubble Chart of Confirmed vs {selected_metric} in {selected_region}',
                    color_discrete_sequence = px.colors.qualitative.Dark2)
    return fig


@app.callback(
    Output(component_id='country-histogram-chart', component_property='figure'),
    [Input(component_id='metric-dropdown', component_property='value'),
     Input(component_id='region-dropdown', component_property='value')]
)
def update_histogram_chart(selected_metric, selected_region):
  filtered_df = df[df['WHO Region'] == selected_region]
  fig = px.histogram(filtered_df, x=selected_metric,
                       title=f'Distribution of {selected_metric} in {selected_region}',
                    color_discrete_sequence = px.colors.qualitative.Dark2)
  return fig

if __name__ == '__main__':
    app.run_server(debug=True)