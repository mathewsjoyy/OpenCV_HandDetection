"""
A hand tracking script which can help to control the volume bar
Python 3.9.0
"""

# Import necessary libraries
import HandTrackingModule as htm
import mediapipe as mp
import cv2
import time
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


cap = cv2.VideoCapture(0)

# We will change default of detection confidence to 0.7 to reduce flickering,
# by ensuring the object we are looking hand is actually a hand
detector = htm.HandDetector(minDetectionConfidence=0.7)
    
# Set the size of the cam
CAM_WIDTH, CAM_HEIGHT = 640, 480
cap.set(3, CAM_WIDTH)
cap.set(4, CAM_HEIGHT)

# Fps counter vars
prevTime = 0
currTime = 0

# General code to access device speakers and be able to control volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# print(volume.GetVolumeRange()) # == (-96.0, 0.0, 0.125)
volRange = volume.GetVolumeRange()
minVolRange = volRange[0]
maxVolRange = volRange[1]


while True:
    success, img = cap.read()
    
    img = detector.findHands(img)
    landMarkList = detector.findPosition(img, draw=False)
    
    if len(landMarkList) != 0:
        #print(landMarkList[4], landMarkList[8])
        
        # Getting the central position of thumb and index finger 
        # e.g landMarkList (thumb) = [4,480,151] 480 = x val, 151 = y val similar case for index finger tip
        x1, y1 = landMarkList[4][1], landMarkList[4][2] # Thumb tip
        x2, y2 = landMarkList[8][1], landMarkList[8][2] # Index finger tip
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2 # Get the centre of the line between thumb and index
        
        cv2.circle(img, (x1,y1), 8, (0, 255, 255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 8, (0, 255, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 1) # Line between thumb and index
        cv2.circle(img, (cx,cy), 7, (255, 0 , 255))
        
        # The formula to find distance of a line between 2 points
        # You can also do math.hypot(x2 - x1, y2 - y1), but thats boring :(
        length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        if length <= 25: # Smallest volume point e.g 0 volume
            cv2.circle(img, (cx, cy), 7, (0, 255, 0), cv2.FILLED)
        elif length >= 250: # Largest volume point e.g 100 volume
            cv2.circle(img, (cx, cy), 7, (0, 0 , 255), cv2.FILLED)
        
        # Hand range 20 - 250 & Volume Range -96 - 0
        # This code helps convert our hand range to vol range so its universal
        vol = np.interp(length, [25, 250], [minVolRange, maxVolRange])
        
        volume.SetMasterVolumeLevel(vol, None)

        # Make a graphical volume bar, need to convert our hand range to vol bar
        cv2.rectangle(img, (50, 90), (85, 400), (0,255,0), 2)
        barVol = np.interp(length, [25, 250], [400, 90])
        cv2.rectangle(img, (50, int(barVol)), (85, 400), (255,0,255), cv2.FILLED)
        
        # Convert hand range to 0 - 100 for a percentage display
        percentageVol = np.interp(length, [25, 250], [0, 100])
        cv2.putText(img, f"{int(percentageVol)}%", (50, 420), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255,0,255), 1)
    

    # fps counter
    currTime = time.time()
    fps = 1/(currTime - prevTime)
    prevTime = currTime
    
    # Display counter and set location, font, size, colour and thickness
    cv2.putText(img, f"Frames Per Second (fps): {int(fps)}", (10,23), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255,0,255), 1)
    cv2.imshow("img", img)
    cv2.waitKey(1) # 1 millisecond delay
