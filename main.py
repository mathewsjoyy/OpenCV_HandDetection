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

# Code to run webcam (and more)
while True:
    success, img = cap.read()
    
    # We need to convert img to RGB as the hands object we made will need rgb images
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    # Checks hand(s) have actually been detected by the camera
    if results.multi_hand_landmarks:
        for handLandmark in results.multi_hand_landmarks: # Loop through all hands and draw out 21 landmark points
            mpDraw.draw_landmarks(img, handLandmark, mpHands.HAND_CONNECTIONS)
        
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)

