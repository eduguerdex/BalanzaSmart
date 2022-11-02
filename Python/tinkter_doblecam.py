# Import required Libraries
from tkinter import *
from PIL import Image, ImageTk
import cv2

# Create an instance of TKinter Window or frame
win = Tk()

# Set the size of the window
win.geometry("1000x350")

# Create a Label to capture the Video frames
label =Label(win)
label.grid(row=0, column=0)
label2 =Label(win)
label2.grid(row=0, column=1)
cap= cv2.VideoCapture(0)
cap2= cv2.VideoCapture(2)
# Define function to show frame
def show_frames():
   # Get the latest frame and convert into Image
   cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   cv2image2= cv2.cvtColor(cap2.read()[1],cv2.COLOR_BGR2RGB)
   img = Image.fromarray(cv2image)
   img2 = Image.fromarray(cv2image2)
   # Convert image to PhotoImage
   imgtk = ImageTk.PhotoImage(image = img)
   imgtk2 = ImageTk.PhotoImage(image = img2)
   label.imgtk = imgtk
   label2.imgtk2 = imgtk2
   label.configure(image=imgtk)
   label2.configure(image=imgtk2)
   # Repeat after an interval to capture continiously
   label.after(19, show_frames)

show_frames()
win.mainloop()