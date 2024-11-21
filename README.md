# Discord Data Analysis Tools

## Overview
Basic tools to gather (maybe useful?) insights from your Discord data package.

## Requirements
- Python 3.8 or later
- Dependencies listed in `requirements.txt`
- A message folder from your Discord data package:
    - You can get this in the **Privacy and Safety** section of the Discord app. It can take up to 30 days to receive, but from my experience it takes less than 5 days.
    - Test data can be generated if you want to try the tools without your data.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/aem2231/discord-data-analysis.git
    ```

2. Install requirements:
    - **Nix users:**
        - If you have `direnv`, run:
          ```bash
          direnv allow
          ```
        - Otherwise, run:
          ```bash
          nix develop
          ```
        - Then, install Python requirements:
          ```bash
          pip install -r requirements.txt
          ```

    - **Non-Nix users:**
      Simply run:
      ```bash
      pip install -r requirements.txt
      ```

## Usage
1. Run the script:
    ```bash
    python main.py
    ```
    Make sure to run this in the directory where you cloned the repository.