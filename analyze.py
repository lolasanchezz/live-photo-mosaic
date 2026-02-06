import os
import exportPhotos
import pandas as pd
from PIL import Image, ImageStat


def getAvgVals():
    df = pd.DataFrame(columns=['avgRed', 'avgGrn', 'avgBlu'])

    for photo in os.listdir("./photos"):
        path = os.path.abspath('./photos/' + photo)
        im = Image.open(path)
        index = int(photo.replace('.jpeg', ''))
        stats = ImageStat.Stat(im)
        df.loc[index] = [stats.mean[0], stats.mean[1], stats.mean[2]]
    df.sort_index(inplace=True)    
    print(df)

if __name__ == "__main__":
    if not os.path.isdir("./photos"):
        exportPhotos.export()
    getAvgVals()