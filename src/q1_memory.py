from typing import List, Tuple
from datetime import datetime
import pandas as pd
from pandas import json_normalize

def q1_memory1(file_path: str) -> List[Tuple[datetime.date, str]]:
    
    # read Json File
    df = pd.read_json(file_path, lines=True)

    # Normalize user field
    normalized_user = json_normalize(df['user'])

    #Add json prefix to all json columns
    normalized_user.columns = [f'json_{col}' for col in normalized_user.columns]

    # Combine normalized DataFrame with original DataFrame
    df = pd.concat([df.drop(columns='user'), normalized_user], axis=1)

    # Drop all columns except username and date
    columnas_a_mantener = ['date', 'json_username']
    df = df.drop(columns=[col for col in df.columns if col not in columnas_a_mantener])

    # Change columns types
    df['date'] = df['date'].dt.date
    df['json_username'] = df['json_username'].astype(str)

    # Get top 10 dates with more tweets
    top_dates = df['date'].value_counts().head(10)

    # Get users with more tweets for top 10 dates 
    users_top_dates = {}
    for fecha in top_dates.index:
        users_top_dates[fecha] = df[df['date'] == fecha]['json_username'].value_counts().idxmax()

    # Convert to proper output format
    date_list = [(fecha, valor) for fecha, valor in users_top_dates.items()]

    return date_list