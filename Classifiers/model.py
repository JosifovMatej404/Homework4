import pandas as pd
import plotly.graph_objects as go
from Data.db_functions import get_company_data_by_code, get_last_update_for_all_companies
from datetime import datetime


# Helper function to check if the date is valid
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%d.%m.%Y')  # Validate the format
        return True
    except ValueError:
        return False


# Function to convert company data to a dictionary with valid dates
def company_data_to_dict(company_data_list):
    data_dict = []
    for company_data in company_data_list:
        if not is_valid_date(company_data.date):
            continue
        data_dict.append({
            'date': datetime.strptime(company_data.date, '%d.%m.%Y'),  # Convert string to datetime
            'last_trade_price': float(company_data.last_trade_price) if company_data.last_trade_price else None,
            'max_price': float(company_data.max_price) if company_data.max_price else None,
            'min_price': float(company_data.min_price) if company_data.min_price else None,
            'avg_price': float(company_data.avg_price) if company_data.avg_price else None,
            'percent_change': float(company_data.percent_change) if company_data.percent_change else None,
            'volume': float(company_data.volume) if company_data.volume else None,
            'turnover_best_denars': float(company_data.turnover_best_denars) if company_data.turnover_best_denars else None,
            'total_turnover_denars': float(company_data.total_turnover_denars) if company_data.total_turnover_denars else None
        })
    return data_dict


# Main data preparation function
def prepare_data(company_data_list):
    # Convert raw data into a dictionary
    data = company_data_to_dict(company_data_list)

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Ensure the 'date' column exists
    if 'date' not in df.columns:
        raise ValueError("The data does not contain a 'date' column.")

    # Set 'date' as the index
    df.set_index('date', inplace=True)

    # Resample data to daily, weekly, and monthly periods
    daily = df.copy()

    weekly = df.resample('W').agg({
        'last_trade_price': 'mean',
        'volume': 'sum',
        'percent_change': 'mean',
        'max_price': 'max',
        'min_price': 'min',
    }).ffill()

    monthly = df.resample('M').agg({
        'last_trade_price': 'mean',
        'volume': 'sum',
        'percent_change': 'mean',
        'max_price': 'max',
        'min_price': 'min',
    }).ffill()

    return daily, weekly, monthly


# Function to calculate SMA and EMA for price data
def calculate_sma_ema(df, window_sma=14, window_ema=14):
    # Calculate Simple Moving Average (SMA) and Exponential Moving Average (EMA)
    df['SMA'] = df['last_trade_price'].rolling(window=window_sma).mean()
    df['EMA'] = df['last_trade_price'].ewm(span=window_ema, adjust=False).mean()
    return df


# Function to plot the data using Plotly
def plot_data(df, title):
    # Create a Plotly figure with candlestick chart and SMA/EMA lines
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

    # Update layout with proper titles and axis labels
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark',
        xaxis_rangeslider_visible=False
    )

    return fig
