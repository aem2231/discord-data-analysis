import json
import os
from pathlib import Path
from typing import Union
from tqdm import tqdm
import time
import matplotlib.pyplot as plt
import pandas as pd

def process_data(folders: list[Path]) -> dict:
    message_counts = {}

    month_names = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }

    yearly_message_counts = {
        "January": 0, "February": 0, "March": 0, "April": 0,
        "May": 0, "June": 0, "July": 0, "August": 0, 
        "September": 0, "October": 0, "November": 0, "December": 0
        }

    for folder in tqdm(folders, desc="Processing Folders", unit="folder"):
        json_file = folder / "messages.json"
        
        if json_file.exists():
            try:
                with open(json_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    
                for dict in data:
                    timestamp = dict.get("Timestamp", "")
                    year = timestamp[:4]
                    month = int(timestamp.split("-")[1])
                    if year not in message_counts.keys():
                        message_counts[year] = yearly_message_counts.copy()
                    message_counts[year][month_names[month]] += 1
            except json.JSONDecodeError as e:
                print(f"Error processing folder {folder}: {e}")
        else:
            print(f"No messages.json found in {folder}")
    return message_counts

def plot_graph(message_counts):
    output_dir: Path = Path.cwd() / "output"
    output_dir.mkdir(parents=True, exist_ok=True) # Create output directory if it does not exist
    file_path: Path = output_dir / "monthy_messages_by_month.png"

    # Convert dictionary to DataFrame for easier plotting
    df = pd.DataFrame(message_counts)

    # Ensure years are sorted in ascending order
    df = pd.DataFrame(message_counts)
    df = df[sorted(df.columns)]  # Sort the columns (years) in ascending order

    df.transpose().plot.bar()
    plt.xlabel("Messages sent")
    plt.ylabel("Months by Years")
    plt.title("Messages Sent by Year and Month")
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()       # Adjust layout to fit labels
    plt.savefig(str(file_path))
    plt.show()

def monthly_messages_by_year(use_test_data: bool = False):
    start_time = time.time()

    # Determine the root folder to use
    data_folder = "test_data" if use_test_data else "messages"
    rootdir = Path(os.getcwd()) / data_folder
    folders = [folder for folder in rootdir.iterdir() if folder.is_dir()]
    
    message_counts = process_data(folders)
    
    print(f"Processing completed in {time.time() - start_time:.2f} seconds.")
    plot_graph(message_counts)