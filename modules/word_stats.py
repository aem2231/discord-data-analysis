import json
from pathlib import Path
import re
from typing import Union
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from tqdm import tqdm
import os
import time
from operator import itemgetter
from most_said_wordcloud import *

def word_counts(use_test_data) -> dict:
    start_time = time.time()

    if use_test_data:
        data_folder: str = "test_data"
    else:
        data_folder: str = "messages"
    
    word_counts: dict[str, int] = {}
    rootdir: Union[Path, str] = Path(os.getcwd()) / data_folder

    # Create a list of sibdirs by iterating over subdirs in the messages directory
    folders = [folder for folder in rootdir.iterdir() if folder.is_dir()] 
    blacklist = set()

    for folder in tqdm(folders, desc="Processing Folders", unit="folder"):
        process_folder(folder, blacklist, word_counts)
    ""
    return sorted(word_counts, key=itemgetter(1))

def percentage_swearing() -> int:
    pass

def word_use_over_time() -> dict:
    pass

print(word_counts(True))

