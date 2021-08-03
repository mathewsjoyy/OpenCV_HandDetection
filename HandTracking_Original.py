"""
==============================================
This is the base code for the handing tracking.
"""

import cv2
import mediapipe as mp # A google made package for ready-to-use ML pipelines
import time

# Make video object
cap = cv2.VideoCapture(0) # Change num for whatever webcam you using (if you have more then 1)

# Get the correct data from mediapipe for hands
mpHands = mp.solutions.hands
# By defalt detects 2 hands
hands = mpHands.Hands()
# Helps to draw all points on the hand (WRIST, MIDDLE_FINGER_DIP, THUMB_TIP, etc...)
mpDraw = mp.solutions.drawing_utils

prevTime = 0
currTime = 0

# Code to run webcam (and more)
while True:
    success, img = cap.read()
    
    # We need to convert img to RGB as the hands object we made will need rgb images
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    # Checks hand(s) have actually been detected by the camera
    if results.multi_hand_landmarks:
        for handLandmark in results.multi_hand_landmarks: # Loop through all hands and draw out 21 landmark points
            for id, landMark in enumerate(handLandmark.landmark): # id is the landmark index e.g 0 = wrist and landMark is x,y,z values
                height, width, channel = img.shape
                channelX, channelY = int(landMark.x * width), int(landMark.y * height)
                
                #if id == 8:  # Now we can can do things, like identify certain points e.g my pointer finger
                    #cv2.circle(img, (channelX, channelY), 10, (225,0,225), cv2.FILLED)
            
            mpDraw.draw_landmarks(img, handLandmark, mpHands.HAND_CONNECTIONS)
    
    # fps counter
    currTime = time.time()
    fps = 1/(currTime - prevTime)
    prevTime = currTime
    
    # Display counter and set location, font, size, colour and thickness
    cv2.putText(img,str(int(fps)), (10,23), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255,0,255), 1)
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    


