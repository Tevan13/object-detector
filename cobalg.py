import cv2
from matplotlib import pyplot as plt
import imutils
import numpy as np
from datetime import datetime
import pyautogui
from matplotlib.backends.backend_pdf import PdfPages
import os
import tkinter as tk
from tkinter import messagebox, Label, Frame, Button

image = cv2.imread('gambar-ori.jpeg', cv2.IMREAD_COLOR)
# Resize gambar
image = imutils.resize(image, 400)
#crop image
y=30
x=75
h=320
w=500
crop_image = image[x:w, y:h]
crop_image2 = crop_image.copy()
img_blur = cv2.GaussianBlur(crop_image, (7, 7), 1.5)
# Smoothing gambar untuk menghilangkan noise
img_bil = cv2.bilateralFilter(img_blur, 30, 60, 80)
# Mengubah gambar menjadi grayscale
img_gray = cv2.cvtColor(img_bil, cv2.COLOR_BGR2GRAY)
img_canny = cv2.Canny(img_gray, 50, 120)

h, w = img_gray.shape[:]


circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 2, int(w / 30), param1=50, param2=20, minRadius=int(w / 40), maxRadius=int(w / 20))

if circles is not None:
    circles = np.uint16(np.around(circles))
    count_objects = 0

    for c in circles[0, :]:
        print(c)
        cv2.circle(crop_image, (c[0], c[1]), c[2], (0, 255, 0), 2)
        cv2.circle(crop_image, (c[0], c[1]), 1, (0, 0, 255), 1)
        count_objects += 1

    print(f"Number of detected objects: {count_objects}")

    cv2.imshow('Detected object', crop_image)
    cv2.imshow('Original', crop_image2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No objects detected.")
