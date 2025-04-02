import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Initialize the Dash app
app = dash.Dash(__name__, title="Spurious Ireland: Correlation ≠ Causation")

# Sample data - in real implementation, you'd load CSO data
# You would replace this with actual data from CSO
years = list(range(2010, 2024))

# Simulated data - replace with actual CSO data
data = {
    'Year': years,
    'Potato_Yield_Tonnes_per_Hectare': [32, 33, 30, 28, 35, 37, 31, 33, 29, 31, 36, 34, 32, 35],
    'Net_Migration_Thousands': [-27, -34, -25, -10, -1, 5, 16, 19, 28, 33, 30, 11, 14, 19],
    'Marriages': [21200, 20500, 22000, 21300, 22500, 23600, 24200, 22300, 21800, 23200, 16000, 18500, 21900, 22800],
    'GDP_Growth_Rate': [1.8, 0.2, 0.0, 1.6, 8.6, 25.2, 3.7, 9.1, 9.0, 5.7, -3.0, 13.6, 12.0, 2.5]
}

df = pd.DataFrame(data)

# Add correlation calculations
corr_potato_migration = round(np.corrcoef(df['Potato_Yield_Tonnes_per_Hectare'], df['Net_Migration_Thousands'])[0, 1], 2)
corr_marriages_gdp = round(np.corrcoef(df['Marriages'], df['GDP_Growth_Rate'])[0, 1], 2)

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("Spurious Ireland: When Correlation Doesn't Equal Causation", 
                style={'textAlign': 'center', 'color': '#2F4F4F', 'marginBottom': 20}),
        html.P("Exploring hilariously unrelated data relationships in Ireland", 
               style={'textAlign': 'center', 'color': '#708090'}),
    ], style={'backgroundColor': '#F0F8FF', 'padding': '20px', 'borderRadius': '10px'}),
    
    html.Div([
        html.Div([
            html.H3("Select a Spurious Correlation:"),
            dcc.Dropdown(
                id='correlation-selector',
                options=[
                    {'label': 'Potato Yield vs. Net Migration', 'value': 'potato_migration'},
                    {'label': 'Marriages vs. GDP Growth Rate', 'value': 'marriages_gdp'}
                ],
                value='potato_migration',
                style={'width': '100%'}
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '2%'}),
        
        html.Div([
            html.H3("Time Period:"),
            dcc.RangeSlider(
                id='year-slider',
                min=min(years),
                max=max(years),
                value=[min(years), max(years)],
                marks={year: str(year) for year in range(min(years), max(years)+1, 2)},
                step=1
            )
        ], style={'width': '65%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'margin': '20px 0'}),
    
    html.Div([
        dcc.Graph(id='correlation-graph')
    ]),
    
    html.Div(id='explanation-text', 
             style={'margin': '20px', 'padding': '15px', 'backgroundColor': '#F0FFF0', 'borderRadius': '10px'}),
    
    html.Div([
        html.H3("How This Works", style={'textAlign': 'center'}),
        html.P([
            "This dashboard demonstrates spurious correlations - statistical relationships between variables that have no causal connection. ",
            "Just because two trends appear similar doesn't mean one causes the other! ",
            "This is a humorous demonstration of how statistics can be misleading when not properly interpreted."
        ], style={'textAlign': 'justify'})
    ], style={'margin': '30px 0', 'padding': '20px', 'backgroundColor': '#FFFAF0', 'borderRadius': '10px'})
], style={'margin': '0 auto', 'maxWidth': '1200px', 'padding': '20px'})

# Callbacks
@app.callback(
    [Output('correlation-graph', 'figure'),
     Output('explanation-text', 'children')],
    [Input('correlation-selector', 'value'),
     Input('year-slider', 'value')]
)
def update_graph(selected_correlation, year_range):
    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    
    if selected_correlation == 'potato_migration':
        # Create subplot with two y-axes
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add potato yield line
        fig.add_trace(
            go.Scatter(
                x=filtered_df['Year'],
                y=filtered_df['Potato_Yield_Tonnes_per_Hectare'],
                name='Potato Yield (tonnes/hectare)',
                line=dict(color='#8B4513', width=3)
            ),
            secondary_y=False
        )
        
        # Add net migration line
        fig.add_trace(
            go.Scatter(
                x=filtered_df['Year'],
                y=filtered_df['Net_Migration_Thousands'],
                name='Net Migration (thousands)',
                line=dict(color='#2E8B57', width=3)
            ),
            secondary_y=True
        )
        
        # Update layout
        fig.update_layout(
            title='The Curious Relationship Between Potato Yields and Migration',
            xaxis_title='Year',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
            hovermode='x',
            plot_bgcolor='white',
            height=600
        )
        
        # Set y-axes titles
        fig.update_yaxes(title_text="Potato Yield (tonnes/hectare)", secondary_y=False)
        fig.update_yaxes(title_text="Net Migration (thousands)", secondary_y=True)
        
        # Calculate updated correlation
        filtered_corr = round(np.corrcoef(filtered_df['Potato_Yield_Tonnes_per_Hectare'], filtered_df['Net_Migration_Thousands'])[0, 1], 2)
        
        explanation = html.Div([
            html.H3(f"Potato Yields & Migration: r = {filtered_corr}", style={'textAlign': 'center', 'color': '#4B0082'}),
            html.P([
                "Who would have thought? As Ireland's potato yields fluctuate, so too does the migration pattern! ",
                f"With a correlation coefficient of {filtered_corr}, one might humorously suggest that Irish people are ",
                "making life decisions based on the health of the potato crop. Perhaps the collective memory of the ",
                "Great Famine still influences the national psyche? Or maybe people just really like potatoes?"
            ]),
            html.P([
                "Of course, this is purely coincidental. Migration is influenced by economic opportunities, housing costs, ",
                "and global conditions, while potato yields depend on agricultural practices, weather, and growing conditions."
            ], style={'fontStyle': 'italic'})
        ])
        
    else:  # marriages_gdp
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add marriages line
        fig.add_trace(
            go.Scatter(
                x=filtered_df['Year'],
                y=filtered_df['Marriages'],
                name='Number of Marriages',
                line=dict(color='#FF69B4', width=3)
            ),
            secondary_y=False
        )
        
        # Add GDP growth line
        fig.add_trace(
            go.Bar(
                x=filtered_df['Year'],
                y=filtered_df['GDP_Growth_Rate'],
                name='GDP Growth Rate (%)',
                marker_color='#4682B4',
                opacity=0.7
            ),
            secondary_y=True
        )
        
        # Update layout
        fig.update_layout(
            title='Marriage Rates and Economic Prosperity: A Love Story?',
            xaxis_title='Year',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
            hovermode='x',
            plot_bgcolor='white',
            height=600
        )
        
        # Set y-axes titles
        fig.update_yaxes(title_text="Number of Marriages", secondary_y=False)
        fig.update_yaxes(title_text="GDP Growth Rate (%)", secondary_y=True)
        
        # Calculate updated correlation
        filtered_corr = round(np.corrcoef(filtered_df['Marriages'], filtered_df['GDP_Growth_Rate'])[0, 1], 2)
        
        explanation = html.Div([
            html.H3(f"Marriages & GDP Growth: r = {filtered_corr}", style={'textAlign': 'center', 'color': '#4B0082'}),
            html.P([
                f"With a correlation coefficient of {filtered_corr}, one might be tempted to believe that economic prosperity ",
                "drives people to tie the knot! Or perhaps all those wedding expenses are boosting Ireland's GDP? ",
                "The wedding industry must be more powerful than we thought!"
            ]),
            html.P([
                "In reality, marriage rates are influenced by social trends, age demographics, and changing attitudes toward ",
                "relationships, while GDP growth depends on countless economic factors including global trade, investment, ",
                "productivity, and government policies."
            ], style={'fontStyle': 'italic'})
        ])
    
    return fig, explanation


if __name__ == '__main__':
    app.run(debug=True)