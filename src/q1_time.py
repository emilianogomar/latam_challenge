from typing import List, Tuple
from datetime import datetime
import pandas as pd
from pandas import json_normalize
from memory_profiler import profile

@profile
def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:

    df = pd.read_json(file_path, lines=True)

    # Normalize the DataFrame
    normalized_user = json_normalize(df['user'])

    #Add json prefix to all json columns
    normalized_user.columns = [f'json_{col}' for col in normalized_user.columns]

    # Combine normalized DataFrame with original DataFrame
    df = pd.concat([df.drop(columns='user'), normalized_user], axis=1)

    # Convertir la columna de fecha a tipo datetime si no está en ese formato
    df['date'] = df['date'].dt.date

    # Agrupar por fecha y usuario, y contar el número de tweets por usuario en cada día
    user_tweets_per_day = df.groupby('date')['json_username'].agg(lambda x: x.value_counts().idxmax()).reset_index()

    # Obtener el top 10 de días con más tweets
    top_10_days = df.groupby('date').size().reset_index(name='count').nlargest(10,'count')

    # Para cada día en el top 10, obtener el usuario con más tweets
    top_user_per_day = top_10_days.merge(user_tweets_per_day, on='date', how='left')

    return_list = list(zip(top_user_per_day['date'], top_user_per_day['json_username']))

    return return_list