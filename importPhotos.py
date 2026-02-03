import osxphotos 
import datetime
import time
from datetime import date
from PIL import Image


photosdb = osxphotos.PhotosDB()
today = date.today()
start_date = date.today() - datetime.timedelta(days=70)

photos = photosdb.photos(
    images = True,
    movies = False,
    from_date= datetime.datetime(start_date.year, start_date.month, start_date.day)
    
)

print(f"Total photos found: {len(photos)}")

count = 0
for photo in photos:
    print(f"Processing photo {count}: {photo.filename}")
    print(f"  In iCloud: {photo.iscloudasset}, Downloaded: {not photo.iscloudasset or photo.path is not None}")
    try:
        result = photo.export(
            dest='/Users/lolasanchez/school/ds2/sem2proj/photos',
            overwrite=True,
            use_photos_export=True
        )
        if result:
            print(f'  ✓ Exported: {result}')
        else:
            print(f'  ✗ Export returned empty list - photo may not be available')
    except Exception as e:
        print(f'  ✗ Error: {e}')
    count+=1

