import json
from pathlib import Path
import re
from typing import Union
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from tqdm import tqdm
import os
from generate_test_data import generate

# Function to load blacklist from a file
def load_blacklist() -> set:
    with open("blacklist.txt", "r", encoding="utf-8") as file:
        blacklist = set(word.strip().lower() for word in file.readlines())
    return blacklist

def extract_words(message: str, blacklist: set) -> list:
    url_regex = r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])"
    if re.search(url_regex, message):
        return []
    
    words = re.split(r"\s+", message)
    cleaned_words = [re.sub(r'[^a-zA-Z0-9]', '', word) for word in words]
    return [word.lower() for word in cleaned_words if word and word.lower() not in blacklist]


def process_folder(folder: Path, blacklist: set, word_counts: dict) -> None:
    json_file = folder / "messages.json"
    
    if json_file.exists():
        try:
            with open(json_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                
            for dict in data:
                message = dict.get("Contents", "")
                words = extract_words(message, blacklist)

                for word in words:
                    if word not in word_counts:
                        word_counts[word] = 0
                    word_counts[word] += 1

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {json_file}: {e}")
    else:
        print(f"No messages.json found in {folder}")

def generate_word_cloud(word_counts: dict) -> None:
    wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(word_counts)
    wordcloud.to_file("output.png")
    print("Word cloud saved as 'output.png'")

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    print("Complete!")


def most_said_wordcloud(use_blacklist: bool, use_test_data: bool) -> None:
    if use_test_data:
        data_folder: str = "test_data"
    if not use_blacklist:
        blacklist = set()
    
    word_counts: dict[str, int] = {}
    rootdir: Union[Path, str] = Path(os.getcwd()) / data_folder
    folders = [folder for folder in rootdir.iterdir() if folder.is_dir()]

    if use_blacklist:
        blacklist = load_blacklist()
    else:
        blacklist = ()

    for folder in tqdm(folders, desc="Processing Folders", unit="folder"):
        process_folder(folder, blacklist, word_counts)

    generate_word_cloud(word_counts)
    print("Complete!")