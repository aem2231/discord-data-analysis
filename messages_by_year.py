import json
import os
from pathlib import Path
from typing import Union
from tqdm import tqdm
import time
import matplotlib.pyplot as plt


def process_data(folders: list[Path]) -> dict:
    message_counts = {}

    for folder in tqdm(folders, desc="Processing Folders", unit="folder"):
        json_file = folder / "messages.json"
        
        if json_file.exists():
            try:
                with open(json_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
                
                for dict in data:
                    timestamp = dict.get("Timestamp", "")
                    if len(timestamp) >= 4:  # Ensure we can extract a year
                        year = timestamp[:4]
                        if int(year) not in message_counts:
                            message_counts[int(year)] = 0
                        message_counts[int(year)] += 1
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in {json_file}: {e}")
        else:
            print(f"No messages.json found in {folder}")
    
    return message_counts

def plot_graph(message_counts):
    # Sort the dictionary by year (keys) as integers
    sorted_counts = dict(sorted(message_counts.items(), key=lambda x: int(x[0])))

    # Extract sorted years and message counts
    years = list(sorted_counts.keys())
    messages_sent = list(sorted_counts.values())

    # Plot the data
    plt.bar(range(len(sorted_counts)), messages_sent, tick_label=years)
    plt.xlabel('Year')
    plt.ylabel('Messages Sent')
    plt.title('Messages Sent by Year')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()       # Adjust layout to fit labels
    plt.show()

def messages_by_year(use_test_data: bool = False):
    start_time = time.time()

    # Determine the root folder to use
    data_folder = "test_data" if use_test_data else "messages"
    rootdir = Path(os.getcwd()) / data_folder
    folders = [folder for folder in rootdir.iterdir() if folder.is_dir()]
    
    message_counts = process_data(folders)
    
    print(f"Message Counts by Year: {message_counts}")
    print(f"Processing completed in {time.time() - start_time:.2f} seconds.")
    plot_graph(message_counts)