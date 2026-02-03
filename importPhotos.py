import osxphotos 
import datetime
import time
import subprocess
from datetime import date
from PIL import Image

## ONLY works in terminal. vscode doesn't request permissions
today = date.today()
start_date = date.today() - datetime.timedelta(days=70)
start_date_format = start_date.strftime("%Y-%m-%d")
today_format = today.strftime("%Y-%m-%d")
subprocess.run(["osxphotos", "export", "/Users/lolasanchez/school/ds2/sem2proj/photos", 
                "--only-photos",
                "--added-in-last",
                "3w",
                "--verbose",
                "--use-photokit",
                "--download-missing",
                "--only-photos"
                ])