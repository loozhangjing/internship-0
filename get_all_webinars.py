from dotenv import load_dotenv
load_dotenv()

import os
API_KEY = os.environ["WEBINARJAM_API_KEY"]

print("WebinarJam API key:", API_KEY)
