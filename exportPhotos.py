import osxphotos 
import os
import datetime
import time
import shutil
import subprocess
from datetime import date
from PIL import Image

def export():
    ## ONLY works in terminal. vscode doesn't request permissions
    today = date.today()
    start_date = date.today() - datetime.timedelta(days=900)
    start_date_format = start_date.strftime("%Y-%m-%d")
    today_format = today.strftime("%Y-%m-%d")

    ##just clearing directory before running
    if os.path.isdir("./photos-tmp"):
        shutil.rmtree("./photos-tmp")
    os.mkdir("./photos-tmp")

    subprocess.run(["osxphotos", "export", "/Users/lolasanchez/school/ds2/live-photo-mosaic/photos-tmp", 
                    "--only-photos",
                    "--added-in-last",
                    "30w",
                    
                    "--verbose",
                 "--use-photokit",
                 "--download-missing",
                    "--convert-to-jpeg",
    "--jpeg-ext",
    "jpeg",
    "--jpeg-quality", 
    "0.4",
                
                    "--preview",
                    "--report",
                    "./photos-exported.json",
                    "--filename",
                    "{counter}"
                    ])

    for photo in os.listdir("./photos-tmp"):
        if 'preview' not in photo:
            os.remove(os.path.abspath('./photos-tmp/' + photo))
    
    if os.path.isdir("./photos"):
        shutil.rmtree("./photos")
    os.rename('./photos-tmp', './photos')
    return 1





if __name__ == "__main__":
    export()
