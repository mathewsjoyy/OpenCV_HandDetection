"""
========================
Main calling program
Python 3.9.0
"""

# Import the vital content from files
from handVolumeControl import *
from gui import *
import sys

# Call the main functionality 
if __name__ == "__main__":
    
    gui = Gui()
    gui.run_app()
    
    # Check if user closed gui or wanted to start the hand detection
    if gui.has_called_detection:
        handDetector = HandVolumeController()
        handDetector.handDetection()
    
    sys.exit()