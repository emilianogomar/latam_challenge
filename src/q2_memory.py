from typing import List, Tuple
from datetime import datetime
import pandas as pd
import gc
import regex
from collections import Counter
from pandas import json_normalize
from memory_profiler import profile

@profile
def q2_memory(file_path: str) -> List[Tuple[str, int]]:

    # read Json File
    df = pd.read_json(file_path, lines=True)

    columns_to_keep = ['content']
    df = df.drop(columns=[col for col in df.columns if col not in columns_to_keep])

    # Counter of emojis
    total_emojis = Counter()

    # identify emojis in twitter content and count them
    for tweet_text in df['content']:
        emojis = regex.findall(r'[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251\U0001f926-\U0001f937\U0001F1E0-\U0001F1FF]{1}', tweet_text)
        total_emojis.update(Counter(emojis))

    del df
    gc.collect()

    # Get top 10 emojis used
    top_10_emojis = total_emojis.most_common(10)

    emoji_list = [(emoji, count) for emoji, count in top_10_emojis]

    return emoji_list