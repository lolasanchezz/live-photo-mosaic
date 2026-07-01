note: this was my official write up for this project as a school report. 
that's why it so formal.

the heart of the project/main script is photostream2.py. before running it for the first time,
run exportPhotos.py to get your local macos photos in a local directory.

exportPhotos.py, however, will only work on macos due to the fact that it uses
osxphotos, a util for getting photos out of the photo app. if you want to 
run the photostream2.py script on something other than a mac, you'll have to do
something else to get the photos in your local directory under /photos.



# *live-photo-mosaic*

## **Project Summary**

A program that composes a live video stream from local Photo App photos by color, effectively creating a ‘mosaic’ at the intersection of the original video stream and the Camera Roll photos attached to it. The goal is to create a visually interesting live video that argues our current circumstances are built from our memories and past experiences.  
	The first step is a Python script that loads photos from the past 30 weeks in the user’s camera roll via the terminal. Such a script is run only once, before everything else, to import all photos into a local directory as JPEGs. The number of photos imported can vary, but it averages around 1050\. The averages of their red, green, and blue values are collected into an array, which is then used to build a sorted K-d tree.  
	The organization of photos into a K-d tree is essential to the program's speed. As sorting multidimensional data in a linear fashion, like a table or an array, requires picking one key to sort by, it makes more sense to choose a non-linear data structure that doesn’t necessarily ‘prioritize’ reds, greens, or blues, or enforce an ‘order’ (ie. indexing, row number) on the images when an ‘order’ doesn’t mean anything. That’s why a K-d tree, a modification of the binary tree and a common data structure used for efficient searching and storage, was the best choice for storing image means. It stores images in a tree-like structure, allowing a search that takes in an array of red, green, and blue means and returns the image that is its nearest neighbor.  
	Once a K-d tree of the user’s photos has been built, the program iterates over frames from a webcam as they arrive. The Canny and findContours functions from CV are used to find bounding boxes of objects in the frame, which are then split into square sections and mapped to color-adjacent photos by querying the K-d tree with the means of the RGB of the square sections. The photos are then overlaid on the corresponding square sections, resulting in a pixelated mosaic effect on the webcam that visually composes the webcam's content with the user’s photos.

## 

## **Materials**

### Sources:

1. OSXphotos \- an essential library for exporting photos from macOS’s camera roll app. I initially thought this process would be extremely tedious and complicated, but using OSXphotos in the command line to export photos was very simple and allowed me to focus on the heart of the project.  
2. Visual Studio Code chatbot \- I used the local AI chatbot with auto mode to help debug code I had already written, fixing minor issues.

### Work:

1. Scripts [here](https://drive.google.com/drive/folders/1UocsTCAZfGkz8ZYuQTdgyY3Xhnwg27sm?usp=sharing)   
   1. exportPhotos.py runs a command to export photos from the user’s library. It should only be run once and before anything else.  
   2. photostream2.py runs all other functionality and is the ‘program’ its

Final Product:

### **![]["/example-photos/oli.png"]**



## [recorded demo](https://drive.google.com/file/d/1fpl46eLjtBFzIGn2gfm_UnHh_bumVIoV/preview)
 

## **Discussion**

This project has something interesting to say about the intersection of art and math. If the results of this project can be called art and say something interesting about the human condition, does my computer get to take any credit for the final product? While I provided the parameters for each photo to be inserted, I am not manually selecting each photo to be inserted into the video feed. While this is certainly not a piece of artwork created with generative AI, it is still a piece of art that has been computer-generated and pushes the definition of art. However, enough human work has gone into it to be c  
	While not all computer-aided artwork is artwork, live-photo-mosaic should count as human artwork. The thought behind the project's meaning and the placement of each photo is human and artistic in its own right. Each step the program takes was deliberately conceived by the artist (me), and, in all, the project produces a visually interesting piece that makes the viewer react.

## **Reflection**

I enjoyed making a project that became visually interesting through math. I think mathematics and art are perceived to be more different than they really are. Beautiful, sublime structures can come from math that says something, just as art does. I really liked the project's premise and building myself out of photos. It was a cool final visual that everyone, including me, could enjoy, even just at face value. In the future, I’d like to pursue more art that comes out of code \- I like how objective the result is, yet personalized and interesting. It was a fun project to iterate on, and I truly enjoyed seeing every step come to fruition. I also really enjoyed learning about K-d trees, which were an extremely fast data structure that could organize my photos extremely efficiently. If I ever run into another case requiring efficient sorting of multidimensional data, I’ll know which data structure to use.

