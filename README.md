# Discord Data Analysis Tools

## Overview
Basic tools to gather (maybe useful?) insights from your discord data package

## Requirements
- Python 3.8 or later
- Dependencies listsed in requirements.txt
- Message folder from discord data package
    - You can find this in the privacy and safety section of the app, however it can take up to 30 days to receive it. From my experience, it takes no more than 5.
    - Test data can be generated if you would like to try it out.

## Installation
1. Clone the repository:
    ```bash
   git clone https://github.com/aem2231/discord-data-analysis.git
   ```
2. Install requirements:
    2a. Nix Only:
    If you have direnv, just run `direnv allow`. Otherwise run `nix develop`.

    Then install requirements.
    ```bash
    pip install -r requirements.txt
    ```

    2b. Everyone else:
    ```bash
    pip install -r requirements.txt
    ```
## Usage
1. Run `python main.py` in the directory that you cloned the repo too.


