from typing import List, Tuple
from datetime import datetime
import pandas as pd
from pandas import json_normalize
from memory_profiler import profile

@profile
def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:

    # read Json File
    df = pd.read_json(file_path, lines=True)

    # Normalize user field
    normalized_user = json_normalize(df['user'])

    #Add json prefix to all json columns
    normalized_user.columns = [f'json_{col}' for col in normalized_user.columns]

    # Combine normalized DataFrame with original DataFrame
    df_2 = pd.concat([df.drop(columns='user'), normalized_user], axis=1)

    # Get top 10 dates with more tweets
    top_dates = df_2['date'].value_counts().head(10)

    # Get users with more tweets for top 10 dates 
    users_top_dates = {}
    for fecha in top_dates.index:
        users_top_dates[fecha] = df_2[df_2['date'] == fecha]['json_username'].value_counts().idxmax()

    # Convert to proper output format
    date_list = [(fecha, valor) for fecha, valor in users_top_dates.items()]

    return date_list