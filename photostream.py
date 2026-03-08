import cv2 as cv
import numpy as np
import vars
from PIL import Image
import random
import os
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()


images = []
image_mean_colors = []  # Store precomputed mean RGB for each image

for i, path in enumerate(os.listdir('./photos')):
    img = Image.open('./photos/'+path).convert('RGB')
    numpy_rgb = np.array(img)
    bgr_image = numpy_rgb[:, :, ::-1].copy()
    images.append(bgr_image)
    
    # Precompute mean color (in BGR format to match OpenCV)
    mean_color = np.mean(bgr_image, axis=(0, 1))  # Shape: (3,) [B, G, R]
    image_mean_colors.append(mean_color)

print(f"Loaded {len(images)} images")
    


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(img_gray, 150, 255, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(image=thresh, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_SIMPLE)

    '''
    front_contours = []
    if hierarchy is not None:
        for i, contour in enumerate(contours):
            # hierarchy[0][i][3] is the parent index. -1 means no parent (top-level)
            if hierarchy[0][i][3] == -1:
                front_contours.append(contour)
    else:
        front_contours = contours

    #cv.drawContours(image=frame, contours=front_contours, contourIdx=-1, color=(255, 255, 0), thickness=2, lineType=cv.LINE_AA)
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    '''
    front_contours = contours
    
    lines = []
    #looping through each shape, drawing lines across
    for shapes in front_contours:
        
        shape_lines = []
        
        if len(shapes) < 2:
            continue
            
        #convert to (x,y)
        points = [(pt[0][0], pt[0][1]) for pt in shapes] # type: ignore
        
        #sort by x coordinate
        sorted_points = sorted(points, key=lambda p: p[0])
        
        #split into left and right halves of each shape
        mid_idx = len(sorted_points) // 2
        left_points = sorted_points[:mid_idx]
        right_points = sorted_points[mid_idx:]
        
        #for each point on the left, find the closest point on the right by y-coordinate
        for left_pt in left_points:
            #find the right point with the closest y-coordinate
            closest_right = list(min(right_points, key=lambda p: abs(p[1] - left_pt[1])))
            closest_right[1] = left_pt[1] # type: ignore
            #draw a line from left to right
            '''
            cv.line(frame, (int(left_pt[0]), int(left_pt[1])), 
                   (int(closest_right[0]), int(closest_right[1])), 
                   (0, 255, 0), 1)
            '''
            shape_lines.append([left_pt, closest_right])
        lines.append(shape_lines)
            

    # Filter lines to avoid vertical overlap - keep only lines with enough spacing
    MIN_VERTICAL_SPACING = 15  # minimum pixels between lines
    filtered_lines = []
    for shape in lines:
        shape_filtered = []
        for line in shape:
            y = line[0][1]
            # Check if this line is far enough from existing filtered lines
            too_close = False
            for existing_shape in filtered_lines:
                for existing_line in existing_shape:
                    if abs(y - existing_line[0][1]) < MIN_VERTICAL_SPACING:
                        too_close = True
                        break
                if too_close:
                    break
            if not too_close:
                shape_filtered.append(line)
        if shape_filtered:
            filtered_lines.append(shape_filtered)
    
    pts = []
    # Static width and height for all rectangles
    STATIC_WIDTH = 25
    STATIC_HEIGHT = 25
    
    # shape 
    for shape in filtered_lines:
        for line in shape:
            x_pos = line[0][0]
            y_pos = line[0][1]
            x_end = line[1][0]
            
            while x_pos + STATIC_WIDTH < x_end:  # ensure at least min width fits
                # store the point (x, y, width, height)
                pts.append([x_pos, y_pos, STATIC_WIDTH, STATIC_HEIGHT])
                
                # draw rectangle just cuz
                '''
                cv.rectangle(frame, (int(x_pos), int(y_pos - STATIC_HEIGHT // 2)), 
                            (int(x_pos + STATIC_WIDTH), int(y_pos + STATIC_HEIGHT // 2)), 
                            (0, 0, 255), 1)
                '''
                x_pos += STATIC_WIDTH
                
    THRESHOLD = 40
    
    for pt in pts:
        # Crop the region from frame
        y_start = max(0, pt[1] - pt[3] // 2)
        y_end = min(frame.shape[0], pt[1] + pt[3] // 2)
        x_start = max(0, pt[0])
        x_end = min(frame.shape[1], pt[0] + pt[2])
        
        cropped_bit = frame[y_start:y_end, x_start:x_end]
        
        if cropped_bit.size == 0:
            continue
        
        # Calculate mean color of the cropped region
        cropped_mean = np.mean(cropped_bit, axis=(0, 1))  # Shape: (3,) [B, G, R]
        
        # Fast color-based matching using precomputed means
        color_scores = []
        for i, img_mean in enumerate(image_mean_colors):
            # Calculate weighted color difference (emphasize green channel)
            color_diff = np.abs(cropped_mean - img_mean)
            color_score = float(color_diff[0] + 1.5 * color_diff[1] + color_diff[2])
            color_scores.append((color_score, i))
        
        # Sort by color score and only check top candidates
        color_scores.sort()
        TOP_CANDIDATES = 20  # Only do expensive pixel-wise comparison on best 20 color matches
        
        best_score = float('inf')
        best_image = None
        best_index = -1
        
        # Fine-grained matching on top candidates only
        for color_score, i in color_scores[:TOP_CANDIDATES]:
            im = images[i]
            res_im = cv.resize(im, (cropped_bit.shape[1], cropped_bit.shape[0]))
            
            # Calculate pixel-wise mean color difference
            diff = np.abs(cropped_bit.astype(np.float32) - res_im.astype(np.float32))
            score = float(np.mean(diff[:, :, 0] + 1.5 * diff[:, :, 1] + diff[:, :, 2]))
            
            if score < best_score:
                best_score = score
                best_image = res_im
                best_index = i
            
            if score < THRESHOLD:
                break  # Found a good enough match
            
            
            
        # Use the best match found
        if best_image is not None:
         #   print(f'Best match at index {best_index} with score {best_score:.2f}')
            frame[y_start:y_end, x_start:x_end] = best_image
            
           
       
           
                
        
        
        
       

    # Display the resulting frame
    
    cv.imshow('output', frame)
    


    # Press 'q' on the keyboard to exit the loop
    if cv.waitKey(1) == ord('q'):    
        break

# When everything done, release the capture and destroy windows


cap.release()
cv.destroyAllWindows()