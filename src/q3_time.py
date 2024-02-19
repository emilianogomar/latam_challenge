from typing import List, Tuple
from datetime import datetime
import pandas as pd
import gc
from memory_profiler import profile

@profile
def q3_time(file_path: str) -> List[Tuple[str, int]]:

    # Read the json file
    df = pd.read_json(file_path, lines=True)

    # Discard the rows with no mencioned users
    df_filtered = df[df['mentionedUsers'].apply(lambda x: bool(x))]

    # flatten column mencionedUsers
    df_flattened = df_filtered.explode('mentionedUsers')

    # count for each username the amount of apperances
    username_counts = df_flattened['mentionedUsers'].apply(lambda x: x['username']).value_counts().head(10)

    mencioned_list = [(value, count) for value, count in username_counts.items()]

    return mencioned_list