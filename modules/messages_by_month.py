import json
import os
from pathlib import Path
from typing import Union
from tqdm import tqdm
import time
import matplotlib.pyplot as plt

def process_data(folders: list[Path]) -> dict:
    message_counts = {
        "January": 0, "February": 0, "March": 0, "April": 0,
        "May": 0, "June": 0, "July": 0, "August": 0,
        "September": 0, "October": 0, "November": 0, "December": 0
    }

    month_names = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }

    for folder in tqdm(folders, desc="Processing Folders", unit="folder"):
        json_file = folder / "messages.json"

        if json_file.exists():
            try:
                with open(json_file, "r", encoding="utf-8") as file:
                    data = json.load(file)

                for message in data:
                    timestamp = message.get("Timestamp", "")
                    # Extract month and increment the count
                    month = int(timestamp.split("-")[1])
                    message_counts[month_names[month]] += 1
            except json.JSONDecodeError:
                print(f"Error decoding JSON in {json_file}")
        else:
            print(f"No messages.json found in {folder}")

    return message_counts


def plot_graph(message_counts: dict):
    output_dir: Path = Path.cwd() / "output"
    output_dir.mkdir(parents=True, exist_ok=True) # Create output directory if it does not exist
    file_path: Path = output_dir / "messages_by_month.png"
    
    # Extract sorted years and message counts
    months = list(message_counts.keys())
    messages_sent = list(message_counts.values())

    # Plot the data
    plt.bar(range(len(message_counts)), messages_sent, tick_label=months)
    plt.xlabel('Month')
    plt.ylabel('Messages Sent')
    plt.title('Messages Sent by Month')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()       # Adjust layout to fit labels
    plt.savefig(str(file_path))
    plt.show()

def messages_by_month(use_test_data: bool = False):
    start_time = time.time()

    # Determine the root folder to use
    data_folder = "test_data" if use_test_data else "messages"
    rootdir = Path(os.getcwd()) / data_folder
    folders = [folder for folder in rootdir.iterdir() if folder.is_dir()]
    
    message_counts = process_data(folders)

    # Plot the graph
    plot_graph(message_counts)