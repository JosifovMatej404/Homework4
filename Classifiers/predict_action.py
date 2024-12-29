import pandas as pd
from Data.db_functions import get_company_data_by_code
from datetime import datetime

def company_data_to_dict(company_data_list):
    """
    Converts a list of CompanyData objects into a list of dictionaries, with all attributes.
    """
    data_dict = []
    for company_data in company_data_list:
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
    """
    Takes raw company data and prepares 1-day, 1-week, and 1-month transformations.
    """
    df = pd.DataFrame(data)  # Convert data into a DataFrame
    df['date'] = pd.to_datetime(df['date'])  # Ensure date column is datetime
    df.set_index('date', inplace=True)  # Set date as the index

    # Resample for each period
    daily = df.copy()  # 1-day data remains the same
    weekly = df.resample('W').agg({
        'last_trade_price': 'mean',
        'volume': 'sum',
        'percent_change': 'mean',
        'max_price': 'max',
        'min_price': 'min',
    }).ffill().infer_objects(copy=False)  # Forward fill and fix dtypes

    monthly = df.resample('ME').agg({
        'last_trade_price': 'mean',
        'volume': 'sum',
        'percent_change': 'mean',
        'max_price': 'max',
        'min_price': 'min',
    }).ffill().infer_objects(copy=False)  # Forward fill and fix dtypes

    return daily, weekly, monthly

def calculate_sma_ema(df, window_sma=14, window_ema=14):
    """
    Calculates SMA and EMA for the DataFrame.
    """
    # Calculate SMA and EMA
    df['SMA'] = df['last_trade_price'].rolling(window=window_sma).mean()
    df['EMA'] = df['last_trade_price'].ewm(span=window_ema, adjust=False).mean()

    return df


def predict_action(df):
    """
    Predicts 'BUY', 'SELL', or 'HOLD' based on the crossover of SMA and EMA.
    """
    predictions = []
    for i in range(1, len(df)):
        if df['SMA'].iloc[i] > df['EMA'].iloc[i] and df['SMA'].iloc[i - 1] <= df['EMA'].iloc[i - 1]:
            predictions.append('BUY')
        elif df['SMA'].iloc[i] < df['EMA'].iloc[i] and df['SMA'].iloc[i - 1] >= df['EMA'].iloc[i - 1]:
            predictions.append('SELL')
        else:
            predictions.append('HOLD')

    # Add the first prediction as 'HOLD' (since there's no prior data to compare for the first record)
    predictions.insert(0, 'HOLD')

    df['Action'] = predictions
    return df



if __name__ == '__main__':


    data_alk = get_company_data_by_code("ALKB")



    data_dict = company_data_to_dict(data_alk)

    prepared_data_daily,prepared_data_weekly,prepared_data_monthly = prepare_data(data_dict)


    prediction_data_daily = calculate_sma_ema(prepared_data_daily)
    final_action_daily = predict_action(prediction_data_daily)
    print("Daily data prediction: " + final_action_daily['Action'])

    prediction_data_weekly = calculate_sma_ema(prepared_data_weekly)
    final_action_weekly = predict_action(prediction_data_weekly)
    print("Weekly data prediction: " + final_action_weekly['Action'])

    prediction_data_monthly = calculate_sma_ema(prepared_data_monthly)
    final_action_monthly = predict_action(prediction_data_monthly)
    print("Monthly data prediction: " + final_action_monthly['Action'])

