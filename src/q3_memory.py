from typing import List, Tuple
from datetime import datetime
import pandas as pd
import gc
from memory_profiler import profile

@profile
def q3_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    
    # Read the json file
    df = pd.read_json(file_path, lines=True)

    # Discard the rows with no mencioned users
    df = df[df['mentionedUsers'].apply(lambda x: bool(x))]

    # flatten column mencionedUsers
    df = df.explode('mentionedUsers')

    # count for each username the amount of apperances
    username_counts = df['mentionedUsers'].apply(lambda x: x['username']).value_counts().head(10)

    del df
    gc.collect()

    mencioned_list = [(value, count) for value, count in username_counts.items()]

    return mencioned_list