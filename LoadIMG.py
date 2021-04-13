from cmu_112_graphics_openCV import *
from tkinter import *
import cv2
import time
import numpy as np


def appStarted(app):
    pass
    
def cameraFired(app):
    """
    -In cameraFired, you can use app.frame 
    -app.frame is a numpy array
    -openCV images are all numpy arrays
    """
    # Example: You can blur the Camera!
    # app.frame = cv2.GaussianBlur(app.frame, (15,15), 0)

    # Example: You can flip the Camera: 
    # 0 means flipping around the x-axis and positive value (for example, 1) 
    # means flipping around y-axis. 
    # Negative value (for example, -1) means flipping around both axes.

    app.frame = cv2.flip(app.frame, 1)

    
def keyPressed(app, event):
    if event.key == "q":
        App._theRoot.app.quit()

def redrawAll(app, canvas):
    # making a frame
    canvas.create_rectangle(app.width/5, app.height/6 - 10, 
                            4*app.width/5, 5*app.height/6 + 10,
                            width = 5)

def timerFired(app):
    print("timer firing!")
        
if __name__ == "__main__":
    runApp(width=1080, height=720)
    os._exit(0)