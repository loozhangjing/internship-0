# These scripts are a work in progress!

## Installation
Prerequisites: [git](https://git-scm.com/) and [Python](https://www.python.org/) must be installed

Code blocks that look like
```
this
```
are commands to be run in a terminal.

### Steps
```
git clone git@github.com:loozhangjing/webinarjam-scripts.git
```
- Create a file named `.env` inside the `webinarjam-scripts` folder that's just been cloned from GitHub.
- Edit the `.env` file to add this: ```WEBINARJAM_API_KEY=[your api key]``` (replace `[your api key]` with your [WebinarJam API key](https://support.webinarjam.com/en/articles/15370143-apply-for-an-api-key-for-webinarjam-or-everwebinar)

```
python -m venv .venv
```
```
source .venv/bin/activate
```
(for bash/zsh), OR
```
.venv\Scripts\Activate.ps1
```
(for Windows PowerShell)

```
pip install -r requirements.txt
```
