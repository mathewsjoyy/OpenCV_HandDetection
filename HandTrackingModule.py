"""
======================================================================================
This is just additionals/HandTracking.py but made into a python module for reuse in any
future projects.
"""

import cv2
import mediapipe as mp # A google made package for ready-to-use ML pipelines
import time


class HandDetector():
    def __init__(self, mode=False, maxHands=2, minDetectionConfidence=0.5, minTrackingConfidence=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.minDetectionConfidence = minDetectionConfidence
        self.minTrackingConfidence = minTrackingConfidence

        # Get the correct data from mediapipe for hands
        self.mpHands = mp.solutions.hands
        # By defalt detects 2 hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.minDetectionConfidence, self.minTrackingConfidence)
        # Helps to draw all points on the hand (WRIST, MIDDLE_FINGER_DIP, THUMB_TIP, etc...)
        self.mpDraw = mp.solutions.drawing_utils
        self.results = None

    # Finds hand(s) and draws it
    def findHands(self, img, draw=True):
        # We need to convert img to RGB as the hands object we made will need rgb images
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        
        # Checks hand(s) have actually been detected by the camera
        if self.results.multi_hand_landmarks:
            for handLandmark in self.results.multi_hand_landmarks: # Loop through all hands and draw out 21 landmark points
                if draw:
                    self.mpDraw.draw_landmarks(img, handLandmark, self.mpHands.HAND_CONNECTIONS)

        return img
    
    # Finds position of landmarks on a specific hand
    def findPosition(self, img, handNum=0, draw=True):
        
        landMarkList = []
        
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNum] #Get the specific hand we want
            for id, landMark in enumerate(myHand.landmark): # id is the landmark index e.g 0 = wrist and landMark is x,y,z values
                height, width, channel = img.shape
                channelX, channelY = int(landMark.x * width), int(landMark.y * height)
                
                landMarkList.append([id, channelX, channelY]) # Add the hand landmark id, and x and y position
                
                if draw:
                    cv2.circle(img, (channelX, channelY), 10 , (225,0,225), cv2.FILLED)
        
        return landMarkList
        