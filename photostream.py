import cv2 as cv
import numpy as np
# Create a VideoCapture object. '0' refers to the first connected camera (webcam).
# Use '1' for the second camera, and so on.
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(img_gray, 150, 255, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(image=thresh, mode=cv.RETR_LIST, method=cv.CHAIN_APPROX_TC89_L1)

    cv.drawContours(image=frame, contours=contours, contourIdx=-1, color=(255, 255, 0), thickness=2, lineType=cv.LINE_AA)
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break


    #looping through each shape, finding points 50px apart that have space for photos
    lines = []
    for shapes in contours:
        #if shape is less than 50px wide/tall, skip it
        minX, minY, maxX, maxY = 0,0,0,0
        if len(shapes) < 25:
                continue
        sorted(shapes, key = lambda x: x[0][0])
        
        if len(shapes) % 2 == 0:
            rightY = shapes[:len(shapes)/2]
            leftY = shapes[len(shapes)/2:]
            odd = True
        else:
            rightY = shapes[:round(len(shapes)/2)]
            leftY = shapes[round(len(shapes)/2):len(shapes)-2]
        
        for coord in shapes:      
            x, y = coord[0][0], coord[0][1] #type: ignore

            
       
        


    



    # Display the resulting frame
    cv.imshow('camera', frame)
    #print(contours)
    



    # Press 'q' on the keyboard to exit the loop
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture and destroy windows


cap.release()
cv.destroyAllWindows()
