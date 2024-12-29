import pandas as pd
import plotly.graph_objects as go
from Data.db_functions import get_company_data_by_code, get_last_update_for_all_companies
from datetime import datetime
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import os

# Helper functions (same as before)
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except ValueError:
        return False

def company_data_to_dict(company_data_list):
    data_dict = []
    for company_data in company_data_list:
        if not is_valid_date(company_data.date): continue
        data_dict.append({
            'date': datetime.strptime(company_data.date.replace(".","-"), '%d-%m-%Y'),
            'last_trade_price': company_data.last_trade_price,
            'max_price': company_data.max_price,
            'min_price': company_data.min_price,
            'avg_price': company_data.avg_price,
            'percent_change': company_data.percent_change,
            'volume': company_data.volume,
            'turnover_best_denars': company_data.turnover_best_denars,
            'total_turnover_denars': company_data.total_turnover_denars
        })
    return data_dict

def prepare_data(data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    daily = df.copy()
    weekly = df.resample('W').agg({
        'last_trade_price': 'mean',
        'volume': 'sum',
        'percent_change': 'mean',
        'max_price': 'max',
        'min_price': 'min',
    }).ffill()
    monthly = df.resample('ME').agg({
        'last_trade_price': 'mean',
        'volume': 'sum',
        'percent_change': 'mean',
        'max_price': 'max',
        'min_price': 'min',
    }).ffill()
    return daily, weekly, monthly

def calculate_sma_ema(df, window_sma=14, window_ema=14):
    df['SMA'] = df['last_trade_price'].rolling(window=window_sma).mean()
    df['EMA'] = df['last_trade_price'].ewm(span=window_ema, adjust=False).mean()
    return df

def plot_data(df, title):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['last_trade_price'],
        high=df['max_price'],
        low=df['min_price'],
        close=df['last_trade_price'],
        name='Stock Price',
        increasing_line_color='green',
        decreasing_line_color='red'
    ))
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA'], mode='lines', name='SMA', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA'], mode='lines', name='EMA', line=dict(color='orange')))
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark',
        xaxis_rangeslider_visible=False
    )
    return fig

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    # Dropdown for selecting company code
    html.Div([
        html.Label("Select Company Code:"),
        dcc.Dropdown(id='company-dropdown',
                     options=[{'label': company.code, 'value': company.code} for company in get_last_update_for_all_companies()],
                     value='ALKB',  # Default value
                     style={'width': '50%'}),
    ], style={'padding': '20px'}),

    # Tabs for daily, weekly, and monthly data
    dcc.Tabs(id='tabs', value='daily', children=[
        dcc.Tab(label='Daily Data', value='daily'),
        dcc.Tab(label='Weekly Data', value='weekly'),
        dcc.Tab(label='Monthly Data', value='monthly')
    ]),

    # Graphs will be displayed here
    html.Div([
        dcc.Graph(id='graph', style={'height': '70vh'})
    ])
])

@app.callback(
    Output('graph', 'figure'),
    [Input('company-dropdown', 'value'),
     Input('tabs', 'value')]
)
def update_graph(company_code, time_period):
    # Fetch company data based on selected code
    data = get_company_data_by_code(company_code)
    data_dict = company_data_to_dict(data)

    # Prepare data for each time period
    prepared_data_daily, prepared_data_weekly, prepared_data_monthly = prepare_data(data_dict)

    # Calculate SMA and EMA for the selected time period
    if time_period == 'daily':
        data_to_plot = calculate_sma_ema(prepared_data_daily)
        title = f"Daily Data for {company_code} with SMA & EMA"
    elif time_period == 'weekly':
        data_to_plot = calculate_sma_ema(prepared_data_weekly)
        title = f"Weekly Data for {company_code} with SMA & EMA"
    elif time_period == 'monthly':
        data_to_plot = calculate_sma_ema(prepared_data_monthly)
        title = f"Monthly Data for {company_code} with SMA & EMA"

    # Plot and return figure
    return plot_data(data_to_plot, title)

if __name__ == '__main__':
    app.run_server(debug=True)
