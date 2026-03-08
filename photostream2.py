import cv2 as cv
import numpy as np
import vars
from PIL import Image
import random
import os
import math
from scipy.spatial import KDTree
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()


images = []
image_mean_colors = []  # Store precomputed mean RGB for each image
WIDTH = 5
HEIGHT = 5
for i, path in enumerate(os.listdir('./photos')):
    if not path.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue
    img = Image.open('./photos/'+path).convert('RGB')
    numpy_rgb = np.array(img)
    bgr_image = numpy_rgb[:, :, ::-1].copy()
    res_im = cv.resize(bgr_image, (WIDTH, HEIGHT))
    images.append(res_im)
    
    # Precompute mean color (in BGR format to match OpenCV)
    mean_color = np.mean(res_im, axis=(0, 1))  #type: ignore
    image_mean_colors.append(mean_color)
working_images = images.copy()
working_image_mean_colors = image_mean_colors.copy()

# Build KD-tree for fast nearest-neighbor search
kdtree = KDTree(working_image_mean_colors)
print(f"Loaded {len(images)} images")



while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    
    # Convert to grayscale
    # Convert to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Blur to reduce noise
    blur = cv.GaussianBlur(gray, (5, 5), 0)

    # Edge detection
    edges = cv.Canny(blur, 50, 150)

    # Find contours
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        
        area = cv.contourArea(cnt)
        if area > 60:
            continue
        # Ignore tiny noise
       
        x, y, w, h = cv.boundingRect(cnt)
        if w < HEIGHT or h < WIDTH:
            continue
    
        
        frame_height, frame_width = frame.shape[:2]
        
        for ypos in range(y, y+h, HEIGHT):
            for xpos in range(x, x+w, WIDTH):
                # Clamp to frame boundaries
                y_end = min(ypos + HEIGHT, frame_height)
                x_end = min(xpos + WIDTH, frame_width)
                
                # Skip if the tile doesn't fit
                if y_end - ypos != HEIGHT or x_end - xpos != WIDTH:
                    continue
                
                cropped_bit = frame[ypos:y_end, xpos:x_end]
                cropped_mean = np.mean(cropped_bit, axis=(0, 1)) # type: ignore
                
                # Use KD-tree for fast nearest-neighbor search
                distance, index = kdtree.query(cropped_mean)
               
                frame[ypos:y_end, xpos:x_end] = working_images[index]
               
                
                if random.random() > 0.8:
                    working_images.pop(index)
                    working_image_mean_colors.pop(index)
                    # Rebuild KD-tree after removing an image
                    kdtree = KDTree(working_image_mean_colors)
                if len(working_images) < 300:
                    working_images = images.copy()
                    working_image_mean_colors = image_mean_colors.copy()
                    # Rebuild KD-tree when replenishing images
                    kdtree = KDTree(working_image_mean_colors)
                
    cv.imshow('art', frame)
    cv.waitKey(1)
                
                
                        
                
    
   
    
    
    
    
    


    # Press 'q' on the keyboard to exit the loop
    if cv.waitKey(1) == ord('q'):    
        break

# When everything done, release the capture and destroy windows


cap.release()
cv.destroyAllWindows()