import json
from pathlib import Path
import re
from typing import Union
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from tqdm import tqdm
import os
import time

# Function to load blacklist from a file
def load_blacklist() -> set:
    with open("blacklist.txt", "r", encoding="utf-8") as file:
        blacklist = set(word.strip().lower() for word in file.readlines()) # Load blacklist into an array
    return blacklist

def extract_words(message: str, blacklist: set) -> list:
    url_regex = r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])" # Filter out URL's
    if re.search(url_regex, message):
        return []
    
    words = re.split(r"\s+", message) # Account for double spaces
    cleaned_words = [re.sub(r'[^a-zA-Z0-9]', '', word) for word in words] # Remove all punctuation
    return [word.lower() for word in cleaned_words if word and word.lower() not in blacklist] # Filter out words in the blacklist

# Function that processes all the data gathered
def process_folder(folder: Path, blacklist: set, word_counts: dict) -> None:
    json_file = folder / "messages.json"
    
    if json_file.exists():
        try:
            with open(json_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                
            for dict in data:
                message = dict.get("Contents", "")
                words = extract_words(message, blacklist) # Call extract words to filter messages

                for word in words:
                    if word not in word_counts:
                        word_counts[word] = 0 # Add key for dictionary if it is not already in there
                    word_counts[word] += 1 # Increment value of a word (key) whenever we come accorss it

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {json_file}: {e}")
    else:
        print(f"No messages.json found in {folder}")

def generate_word_cloud(word_counts: dict, start_time: float) -> None:
    output_dir: Path = Path.cwd() / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path: Path = output_dir / "wordcloud.png"
    

    end_time: float = time.time()
    execution_time: float = (end_time - start_time)*10**3
    print(f"Complete!\nGenerated in {execution_time:.03f} ms!")
    
    wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(word_counts)
    wordcloud.to_file(str(file_path))
    print("Word cloud saved as 'output.png'")

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def most_said_wordcloud(use_blacklist: bool, use_test_data: bool) -> None:
    start_time = time.time()

    if use_test_data:
        data_folder: str = "test_data"
    else:
        data_folder: str = "messages"
    if not use_blacklist:
        blacklist = set()
    
    word_counts: dict[str, int] = {}
    rootdir: Union[Path, str] = Path(os.getcwd()) / data_folder

    # Create a list of sibdirs by iterating over subdirs in the messages directory
    folders = [folder for folder in rootdir.iterdir() if folder.is_dir()] 

    if use_blacklist:
        blacklist = load_blacklist()
    else:
        blacklist = ()

    for folder in tqdm(folders, desc="Processing Folders", unit="folder"): # Then iterate through the subdirs and pass their names as a parameter
        process_folder(folder, blacklist, word_counts)

    generate_word_cloud(word_counts, start_time) # Finally, create and display the wordcloud