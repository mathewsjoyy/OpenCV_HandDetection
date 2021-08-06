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
from tkinter import *
from playsound import playsound


class App():
    def __init__(self, video_source=0):
        # Initialize tkinter gui attributes
        self.appName = "Hand Volume Controller"
        self.window = Tk()
        self.window.title(self.appName)
        self.window.resizable(0,0) # Setting window to not resizeable
        self.window.wm_iconbitmap("images-sounds/hand_icon.ico")
        self.window["bg"] = 'black'
        self.click_sound = "images-sounds/clicks.wav"
        
        self.vid = HandVolumeController(video_source)
        
        self.label = Label(self.window, text=self.appName, font=14, bg="blue", fg="white",).pack(side=TOP,fill=BOTH)
        
        # Button that lets user to see fps
        self.btn_fps = Button(self.window, text="Frames Per Second tracker", width=30, bg="goldenrod2", activebackground="red", command=self.__fps_tracker)
        self.btn_fps.pack(anchor=CENTER, expand=True)
    
    def __fps_tracker(self):
        playsound(self.click_sound)
        pass
    
    def __startDetection(self):
        self.vid.handDetection()
    
    # Method to run the tkinter main   
    def run_app(self):
        # Start the hand detection
        self.__startDetection()
        self.window.mainloop() # Keep window open
        return
            

class HandVolumeController():
    def __init__(self, video_source=0):
        
        # Open the video source and check its valid
        self.cap = cv2.VideoCapture(video_source)
        if not self.cap.isOpened():
            raise ValueError(f"> Unable to open your current video source {video_source}\n> Please try another")
        
        # Set the size of the cam
        CAM_WIDTH, CAM_HEIGHT = 640, 480
        self.cap.set(3, CAM_WIDTH)
        self.cap.set(4, CAM_HEIGHT)

        
        # We will change default of detection confidence to 0.7 to reduce flickering,
        # by ensuring the object we are looking hand is actually a hand
        self.detector = htm.HandDetector(minDetectionConfidence=0.7)
        
        # Fps counter vars
        self.prevTime = 0
        self.currTime = 0

        # General code to access device speakers and be able to control volume
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))

        # print(volume.GetVolumeRange()) # == (-96.0, 0.0, 0.125)
        self.volRange = self.volume.GetVolumeRange()
        self.minVolRange = self.volRange[0]
        self.maxVolRange =  self.volRange[1]


    def handDetection(self):
        
        counter = 0 # Muting tracker
        
        while True:
            success, img = self.cap.read()
            
            img = self.detector.findHands(img)
            landMarkList = self.detector.findPosition(img, draw=False)
            
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
                    counter+=1
                    if counter == 50: # Roughly a 4 second delay before muting
                        self.volume.SetMute(1, None)
                elif length >= 250: # Largest volume point e.g 100 volume
                    cv2.circle(img, (cx, cy), 7, (0, 0 , 255), cv2.FILLED)
                if self.detector.results.multi_hand_landmarks is not None: # Detects if there is 2 hands present
                    if len(self.detector.results.multi_hand_landmarks) == 2:
                        counter = 0
                        self.volume.SetMute(0, None)
                        
                
                # Hand range 20 - 250 & Volume Range -96 - 0
                # This code helps convert our hand range to vol range so its universal
                self.vol = np.interp(length, [25, 250], [self.minVolRange, self.maxVolRange])
                
                self.volume.SetMasterVolumeLevel(self.vol, None)

                # Make a graphical volume bar, need to convert our hand range to vol bar
                cv2.rectangle(img, (50, 90), (85, 400), (0,255,0), 2)
                barVol = np.interp(length, [25, 250], [400, 90])
                cv2.rectangle(img, (50, int(barVol)), (85, 400), (255,0,255), cv2.FILLED)
                
                # Convert hand range to 0 - 100 for a percentage display
                percentageVol = np.interp(length, [25, 250], [0, 100])
                cv2.putText(img, f"{int(percentageVol)}%", (50, 420), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255,0,255), 1)
            

            # fps counter
            self.currTime = time.time()
            fps = 1/(self.currTime - self.prevTime)
            self.prevTime = self.currTime
            
            # Display counter and set location, font, size, colour and thickness
            cv2.putText(img, f"Frames Per Second (fps): {int(fps)}", (10,23), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255,0,255), 1)
            cv2.imshow("img", img)
            cv2.waitKey(1) # 1 millisecond delay
    
    

if __name__ == "__main__":
    app = App()
    app.run_app() 
    

    


