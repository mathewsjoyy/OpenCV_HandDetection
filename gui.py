"""
===============================================================
This is the Gui to show the user how the program works
Python 3.9.0
"""

from tkinter.constants import CENTER
import tkinter as tk
from tkinter import *
from playsound import playsound

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 350
WINDOW_TITLE = "Hand Volume Controller"
BUTTON_CLICK_SOUND = "additionals/clicks.wav" # Make sure its in .wav format

class Gui:
           
    def __init__(self):
        # Define the format of the GUI
        self.window = tk.Tk()
        self.window.geometry("{}x{}".format(WINDOW_WIDTH,WINDOW_HEIGHT))
        self.window.configure(bg="mintcream")
        self.window.title(WINDOW_TITLE)
        self.window.iconbitmap("images/icon.ico")
        self.window.resizable(width=0, height=0)
        
        # Create text
        text = Text(self.window)
        text.insert(INSERT, """ \t        > The Hand Volume Controller <\n
Instructions:\n
> Press 'P' / 'O' on your keyboard to show/not show FPS.\n
> Press 'X' to close the program.\n
> Keep your hand about 10 inches from the webcam.\n
> Palm of your hand should be facing clearly to the webcam.\n
> Move your index + thumb to control the volume.\n
> Mute = keep your thumb + index pinched for 4 seconds.\n
> Un-Mute = just show your other hand to the camera.\n
> Press the button below to start the hand detection.\n
""")
        text.pack()
        text.tag_add("here", "1.10", "1.40")
        text.tag_config("here", background="yellow", foreground="blue")

        # Create Download Button 
        self.download_button = tk.Button(self.window, text = "Start Detection", fg="white", bg="black", height=1, width=24, command = self.close_gui)
        self.download_button.place(relx=0.5, rely=0.95,anchor=CENTER)
        
        # This is to see if user closes the program or pressed start to start the detection
        self.has_called_detection = False
        
    # Method to run the tkinter main   
    def run_app(self):
        self.window.mainloop()
        return
    
    def close_gui(self):
        playsound(BUTTON_CLICK_SOUND)
        self.has_called_detection = True
        self.window.destroy() 
        return

        