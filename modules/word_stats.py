import json
from pathlib import Path
import re
from typing import Union
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import time
import itertools
from most_said_wordcloud import *
from better_profanity import profanity 

def count_messages() -> str:
    rootdir: Path = os.getcwd()
    data_folder: Path = "test_data"
    rootdir: Union[Path, str] = Path(os.getcwd()) / data_folder

    # Create a list of sibdirs by iterating over subdirs in the messages directory
    folders = [folder for folder in rootdir.iterdir() if folder.is_dir()]
    messages: list = []


    for folder in tqdm(folders, desc="Processing Folders", unit="folder"):
        json_file = folder / "messages.json"
        
        if json_file.exists():
            try:
                with open(json_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
                
                for dict in data:
                    message: str = dict['Contents']
                    if message not in messages:
                        messages.append(message)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in {json_file}: {e}")
        else:
            print(f"No messages.json found in {folder}")
    return messages
    
def count_words(use_test_data) -> dict:
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
    return dict(sorted(word_counts.items(), key=lambda x:x[1], reverse=True)) # I dont know why this works but it does 

def count_percentage_offensiveness(messages, message_count) -> int:
    offensive_message_count: int = 0
    for message in messages:
        censored_message: str = profanity.censor(message)
        if censored_message != message:
            offensive_message_count += 1
            print(censored_message)

    return (offensive_message_count/message_count) 

def word_use_over_time() -> dict:
    pass

def grammer_accuracry() -> int:
    pass

def word_stats() -> None:
    messages = count_messages()
    message_count = len(messages)
    word_counts = count_words(True)
    top5_words: dict[str: int] = dict(itertools.islice(word_counts.items(), 5))
    percententage_offensiveness: int = count_percentage_offensiveness(messages, message_count)
    print(percententage_offensiveness)

    



word_stats()

