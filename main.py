import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess
import numpy as np

# Open the device at the ID 0
# cap = cv2.VideoCapture(0)
# # Check whether user selected camera is opened successfully.
# if not (cap.isOpened()):
#     print("Could not open video device")

class CameraApp:
    def __init__(self, root, camera_index=0):
        self.root = root
        self.root.title("Brio 300")

        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
         # Check if the camera is opened successfully
        if not self.cap.isOpened():
            print(f"Error: Could not open camera with index {self.camera_index}")
            self.root.destroy()
            return

        self.label = ttk.Label(root)
        self.label.pack()

        # self.capture_button = ttk.Button(root, text="Capture", command=self.capture_image)
        # self.capture_button.pack()


        # Bind event handler to the root window for key press events
        self.root.bind('<Return>', self.capture_image_on_enter)
        self.root.bind('<KP_Enter>', self.capture_image_on_enter)  # KP_Enter represents the ENTER key on the numeric keypad
        self.root.bind('q', self.close_app)

        self.update()

    def update(self):
        _, frame = self.cap.read()
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image)

            self.label.config(image=photo)
            self.label.image = photo

        self.root.after(10, self.update)

    def capture_image(self, event=None):
        _, frame = self.cap.read()
        if frame is not None:
            cv2.imwrite("image.jpg", frame)
            print("Image captured!")

            subprocess.run(["py", "count-object.py"])

    def capture_image_on_enter(self, event):
        # Capture image only when the Enter key is pressed
        self.capture_image()

    def close_app(self, event):
      self.root.destroy()

if __name__ == "__main__":
    # Modify this line to pass the correct camera index
    camera_index = 0  # Change this to the correct camera index

    root = tk.Tk()
    app = CameraApp(root, camera_index)
    root.mainloop()
