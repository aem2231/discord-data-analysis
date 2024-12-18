import random
import json
import os
from pathlib import Path
from tqdm import tqdm
import shutil
import typing
from datetime import datetime, timedelta
from wonderwords import RandomWord
import time

def generate_messages() -> None:
    #initialize an instance of randomwords
    rw = RandomWord()

    #min and max used to generate a message id
    min: int = 1000000000000000 
    max: int = 9999999999999999

    #Creates a start and end date
    start: datetime = datetime.strptime("2015-05-13 00:00:00", "%Y-%m-%d %H:%M:%S")
    end: datetime = datetime.strptime("2025-05-13 00:00:00", "%Y-%m-%d %H:%M:%S")

    data: dict = {
        "ID": 0, 
        "Timestamp": "", 
        "Contents": "", 
        "Attachments": ""}

    id: int = random.randint(min,max)
    #creates a random time stamp by picking a number in the range of seconds between start and end
    delta: timedelta = end - start
    total_seconds: int = int(delta.total_seconds())
    random_seconds: int = random.randint(0, total_seconds)
    timestamp: str = str((start + timedelta(seconds=random_seconds)).strftime("%Y-%m-%d %H:%M:%S"))
    #generates random string of words to be used as a message,
    message: str = " ".join([rw.word() for i in range(15, 25)])

    data["ID"] = id
    data["Timestamp"] = timestamp
    data["Contents"] = message
    return data


def create_dirs() -> None:
    root_dir: Path = Path(os.getcwd())
    directory: Path = Path(root_dir / "test_data")
    json_file: Path = "messages.json" 
    sub_dirs: int = random.randint(25, 200)
    data: list  = []
    print(directory)
    time.sleep(1)

    #min and max used to generate a sub dir name
    min: int = 1000000000000000 
    max: int = 9999999999999999

    if os.path.exists(directory):
        shutil.rmtree(directory)
    directory.mkdir()

    for _ in tqdm(range(sub_dirs), desc = "Generating test data", unit = "files"):
        sub_dir_name = str(random.randint(min, max))
        (directory / sub_dir_name).mkdir() #Creates a new directry with a random name
        path = (directory / sub_dir_name / json_file)
        Path.touch(path) #Creates a messages.json in the newly created directory

        with open(path, "w") as f:
            for i in range(0, random.randint(5, 20)):
                data.append(generate_messages())
            json.dump(data, f)

def generate() -> None:
    create_dirs()
    print("Test data generated!")


