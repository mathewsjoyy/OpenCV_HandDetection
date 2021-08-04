import cv2
import mediapipe as mp # A google made package for ready-to-use ML pipelines
import time

import HandTrackingModule as htm # Importing module we made

def main():
    
    # Make video object
    cap = cv2.VideoCapture(0) # Change num for whatever webcam you using (if you have more then 1)

    # Make the object of handdetector
    detector = htm.HandDetector()

    prevTime = 0
    currTime = 0

    # Code to run webcam (and more)
    while True:
        success, img = cap.read()

        img = detector.findHands(img)
        landmarkList = detector.findPosition(img)
        
        if len(landmarkList) != 0:
            print(landmarkList[0]) # getting wrist position

        # fps counter
        currTime = time.time()
        fps = 1/(currTime - prevTime)
        prevTime = currTime
        
        # Display counter and set location, font, size, colour and thickness
        cv2.putText(img,str(int(fps)), (10,23), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255,0,255), 1)
        
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()