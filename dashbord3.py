import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Load Data
data = pd.read_csv(r'C:\\Users\\Administrator\\Desktop\\Sales-scorecard-in-plotly-dash-main\\country_wise_latest.csv')

# Initialize Dash App
app = dash.Dash(__name__)
app.title = "COVID-19 Dashboard"

# App Layout
app.layout = html.Div([
    html.H1("COVID-19 Dashboard", style={'textAlign': 'center', 'marginBottom': '20px'}),

    # Summary Section
    html.Div([
        html.Div([
            html.H4("Global Confirmed"),
            html.P(f"{data['Confirmed'].sum():,}")
        ], className='summary-card'),
        html.Div([
            html.H4("Global Deaths"),
            html.P(f"{data['Deaths'].sum():,}")
        ], className='summary-card'),
        html.Div([
            html.H4("Global Recovered"),
            html.P(f"{data['Recovered'].sum():,}")
        ], className='summary-card')
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '30px'}),

    # Dropdowns for Filtering
    html.Div([
        html.Div([
            html.Label("Select Metric:"),
            dcc.Dropdown(
                id='metric-dropdown',
                options=[{'label': col, 'value': col} for col in ['Confirmed', 'Deaths', 'Recovered', 'Active', 'New cases', 'New deaths']],
                value='Confirmed',
                style={'width': '100%'}
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Select Region:"),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': region, 'value': region} for region in data['WHO Region'].unique()],
                value='Global',
                style={'width': '100%'}
            )
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ], style={'marginBottom': '30px'}),

    # Visualizations
    html.Div([
        html.Div([
            dcc.Graph(id='bar-chart'),
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='pie-chart'),
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ], style={'marginBottom': '30px'}),

    html.Div([
        html.Div([
            dcc.Graph(id='line-chart'),
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='map-chart'),
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ], style={'marginBottom': '30px'}),

    html.Div([
        html.Div([
            dcc.Graph(id='scatter-chart'),
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='histogram-chart'),
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ])
])

# Callbacks
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('metric-dropdown', 'value'), Input('region-dropdown', 'value')]
)
def update_bar_chart(metric, region):
    if region == 'Global':
        filtered_df = data
    else:
        filtered_df = data[data['WHO Region'] == region]
    fig = px.bar(
        filtered_df.sort_values(metric).tail(15),
        x=metric, y='Country/Region',
        color='WHO Region',
        text=metric, orientation='h',
        title=f"Top 15 Countries by {metric} ({region})"
    )
    fig.update_layout(yaxis=dict(categoryorder='total ascending'))
    return fig

@app.callback(
    Output('pie-chart', 'figure'),
    [Input('metric-dropdown', 'value'), Input('region-dropdown', 'value')]
)
def update_pie_chart(metric, region):
    if region == 'Global':
        filtered_df = data
    else:
        filtered_df = data[data['WHO Region'] == region]
    fig = px.pie(
        filtered_df,
        values=metric,
        names='Country/Region',
        title=f"Proportion of {metric} ({region})"
    )
    return fig

@app.callback(
    Output('line-chart', 'figure'),
    [Input('metric-dropdown', 'value'), Input('region-dropdown', 'value')]
)
def update_line_chart(metric, region):
    if region == 'Global':
        filtered_df = data
    else:
        filtered_df = data[data['WHO Region'] == region]
    fig = px.line(
        filtered_df.sort_values(metric),
        x='Country/Region', y=metric,
        title=f"Trend of {metric} ({region})"
    )
    return fig

@app.callback(
    Output('map-chart', 'figure'),
    [Input('metric-dropdown', 'value'), Input('region-dropdown', 'value')]
)
def update_map_chart(metric, region):
    if region == 'Global':
        filtered_df = data
    else:
        filtered_df = data[data['WHO Region'] == region]
    fig = px.scatter_geo(
        filtered_df,
        locations="Country/Region",
        locationmode="country names",
        size=metric,
        color=metric,
        hover_name="Country/Region",
        title=f"Geographic Distribution of {metric} ({region})",
        projection="natural earth"
    )
    return fig

@app.callback(
    Output('scatter-chart', 'figure'),
    [Input('metric-dropdown', 'value'), Input('region-dropdown', 'value')]
)
def update_scatter_chart(metric, region):
    if region == 'Global':
        filtered_df = data
    else:
        filtered_df = data[data['WHO Region'] == region]
    fig = px.scatter(
        filtered_df,
        x='Confirmed', y=metric,
        size=metric, color='WHO Region',
        hover_name='Country/Region',
        title=f"Scatter Plot: Confirmed vs {metric} ({region})"
    )
    return fig

@app.callback(
    Output('histogram-chart', 'figure'),
    [Input('metric-dropdown', 'value'), Input('region-dropdown', 'value')]
)
def update_histogram_chart(metric, region):
    if region == 'Global':
        filtered_df = data
    else:
        filtered_df = data[data['WHO Region'] == region]
    fig = px.histogram(
        filtered_df,
        x=metric, color='WHO Region',
        title=f"Histogram of {metric} ({region})"
    )
    return fig

# Run App
if __name__ == '__main__':
    app.run_server(debug=True)
