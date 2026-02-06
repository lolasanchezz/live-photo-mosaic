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
    start_date = date.today() - datetime.timedelta(days=70)
    start_date_format = start_date.strftime("%Y-%m-%d")
    today_format = today.strftime("%Y-%m-%d")

    ##just clearing directory before running
    if os.path.isdir("./photos"):
        shutil.rmtree("./photos")
    os.mkdir("./photos")

    subprocess.run(["osxphotos", "export", "/Users/lolasanchez/school/ds2/sem2proj/photos", 
                    "--only-photos",
                    "--added-in-last",
                    "5w",
                    
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

    for photo in os.listdir("./photos"):
        if 'preview' not in photo:
            os.remove(os.path.abspath('./photos/' + photo))
        else:
            old_path = os.path.abspath('./photos/' + photo)
            new_path = old_path.replace('_preview', '') 
            im = Image.open(old_path)
            im = im.resize((50, 50), Image.Resampling.LANCZOS)
            im.save(new_path)
            os.remove(old_path)
    return 1





if __name__ == "__main__":
    export()
