import json
from pathlib import Path
import re
from typing import Union
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from tqdm import tqdm

# Function to load stopwords from a file
def load_blacklist(file_path: str) -> set:
    with open(file_path, "r", encoding="utf-8") as file:
        stopwords = set(word.strip().lower() for word in file.readlines())
    return stopwords

word_counts: dict[str, int] = {}
rootdir: Union[Path, str] = Path("./messages")
url_regex = r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])"
folders = [folder for folder in rootdir.iterdir() if folder.is_dir()]

# Load stopwords from the external file
stopwords = load_blacklist("blacklist.txt")

for folder in tqdm(folders, desc="Processing Folders", unit="folder"):
    json_file = folder / "messages.json"
    
    if json_file.exists():
        try:
            with open(json_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                
            for dict in data:
                message = dict.get("Contents", "")
                if re.search(url_regex, message):
                    pass
                else:
                    words = re.split(r"\s+", message)
                    cleaned_words = [re.sub(r'[^a-zA-Z0-9]', '', word) for word in words]
                    
                    for word in cleaned_words:
                        if word and word.lower() not in stopwords:
                            word = word.lower()
                            if word not in word_counts:
                                word_counts[word] = 0
                            word_counts[word] += 1

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {json_file}: {e}")
    else:
        print(f"No messages.json found in {folder}")

wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(word_counts)

wordcloud.to_file("output.png")
print("Word cloud saved as 'output.png'")

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

print("Complete!")
