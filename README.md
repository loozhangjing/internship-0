# These scripts are a work in progress!

## Installation
Prerequisites: [git](https://git-scm.com/) and [Python](https://www.python.org/) must be installed

Code blocks that look like ```this``` are commands to be run in a terminal.

1. ```git clone git@github.com:loozhangjing/webinarjam-scripts.git```
2. Create a file named `.env` inside the `webinarjam-scripts` folder that's just been cloned from GitHub.
3. Edit the `.env` file to add this: ```WEBINARJAM_API_KEY=[your api key]``` (replace `[your api key]` with your [WebinarJam API key](https://support.webinarjam.com/en/articles/15370143-apply-for-an-api-key-for-webinarjam-or-everwebinar)
4. ```python -m venv .venv```
5. ```source .venv/bin/activate``` (bash/zsh), or ```.venv\Scripts\Activate.ps1``` (Windows PowerShell)
6. ```pip install -r requirements.txt```
