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
# Repeated Closing operation to remove text from the document.
# kernel = np.ones((5,5),np.uint8)
# img = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations= 3)
# mask = np.zeros(img.shape[:2],np.uint8)
# bgdModel = np.zeros((1,65),np.float64)
# fgdModel = np.zeros((1,65),np.float64)
# rect = (20,20,img.shape[1]-20,img.shape[0]-20)
# cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
# mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
# img = img*mask2[:,:,np.newaxis]
# Blurring gambar untuk menghilangkan noise
img_blur = cv2.GaussianBlur(crop_image, (5, 5), 1)
# Smoothing gambar untuk menghilangkan noise
img_bil = cv2.bilateralFilter(img_blur, 30, 60, 80)
# Mengubah gambar menjadi grayscale
img_gray = cv2.cvtColor(img_bil, cv2.COLOR_BGR2GRAY)
# Mencari garis edge pada object
img_canny = cv2.Canny(img_gray, 95, 25)
# Otsu Filter
_, img_otsu = cv2.threshold(img_gray, 125, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
# Inverse otsu
img_otsu_inverse = cv2.bitwise_not(img_otsu)
# th, threshed = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

# cnts = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
# cnts = cv2.findContours(img_otsu_inverse, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
contours, hierarcy = cv2.findContours(img_otsu_inverse, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# s1= 100
# # s1= 310
# s2 = 255
# xcnts = []
# for cnt in cnts:
#   pprint(cnt)
#   if s1<cv2.contourArea(cnt)<s2:
#     xcnts.append(cnt)
cnt_area = []
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 70.0:
      print("Contours Area: {}".format(area))
      cnt_area.append(cnt)

# print("Dots number: {}".format(len(xcnts)))
print('Object in the image', len(cnt_area))
img_contour = crop_image.copy()

for cnt in cnt_area:
    cv2.drawContours(img_contour, cnt, -1, (255, 0, 255), 3)
    
# Displaying message box with tkinter
message = f'Total Part: {len(cnt_area)}'
root = tk.Tk()
# root.withdraw()  # Hide the main window
root.title("Confirmation")
root.geometry("1600x900")
# Create a Label with a larger font size
label = Label(root, text=message, fg="black", font=('Arial', 64))
label.pack(pady=20)
# Add a Frame
frame = Frame(root, bg="green3")
frame.pack(pady=10)
# Add labels based on conditions
if len(cnt_area) < 300:
    label_color = "red"
    label_text = "NO GOOD"
elif len(cnt_area) > 300:
    label_color = "yellow"
    label_text = "Check the detection object or call IT!"
else:
    label_color = "green"
    label_text = "GOOD"
    
status_label = Label(root, text=label_text, fg=label_color, font=('Arial', 52))
status_label.pack(pady=10)
# Add a Button for closing the window
close_button = Button(root, text="ENTER", command=root.destroy, font=('Arial', 24), padx=20, pady=10)
close_button.pack(pady=20)

# Add an event binding to trigger the close_button command when the Enter key is pressed
root.bind('<Return>', lambda event=None: close_button.invoke())

# Saving images as PDF
dt = datetime.now()
folder_name = dt.strftime("%B_%Y")
# Specify the main directory
main_directory = r'Output_Detection'
# Check if the main directory exists, if not, create it
if not os.path.exists(main_directory):
    os.makedirs(main_directory)
# Create a subdirectory for the current month and year
output_directory = os.path.join(main_directory, folder_name)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

pdf_filename = os.path.join(output_directory, dt.strftime("%d-%b-%Y %I.%M.%S %p") + ".pdf")
with PdfPages(pdf_filename) as pdf:
     # Create a single figure with two subplots
    fig, axes = plt.subplots(1, 3, figsize=(13, 12))

    # Plot the Original Image
    axes[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    axes[0].set_title('Original Image')

    # Plot the Detected Object Image
    axes[1].imshow(cv2.cvtColor(img_contour, cv2.COLOR_BGR2RGB))
    axes[1].set_title('Detected Object')
    # Add text to the PDF
    axes[1].text(10, img_contour.shape[0] - 10, f'Total part terdeteksi: {len(cnt_area)}', color='white', fontsize=12, ha='left', va='top', bbox=dict(facecolor='black', alpha=0.8))
    
    axes[2].imshow(img_otsu_inverse)
    axes[2].set_title('Image Inverse')
    
    # plt.figure(figsize=(8, 8))
    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.title('Original Image')
    # pdf.savefig()
    # plt.close()

    # plt.figure(figsize=(8, 8))
    # plt.imshow(cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB))
    # plt.title('Cropped Image')
    # pdf.savefig()
    # plt.close()

    # plt.figure(figsize=(8, 8))
    # plt.imshow(img_otsu_inverse, cmap='gray')
    # plt.title('Otsu Inverse')
    # pdf.savefig()
    # plt.close()
    
    # plt.figure(figsize=(8, 8))
    # plt.imshow(cv2.cvtColor(img_contour, cv2.COLOR_BGR2RGB))
    # plt.title('Detected Object')
    # Add text to the PDF
    # Add text to the PDF at the bottom left
    # plt.text(10, img_contour.shape[0] - 10, f'Object in the image: {len(cnt_area)}', color='white', fontsize=12, ha='left', va='top', bbox=dict(facecolor='black', alpha=0.8))
    pdf.savefig()
    plt.close()

print(f'PDF saved as {pdf_filename}')
# Run the tkinter main loop
root.mainloop()
# cv2.waitKey(0)
# cv2.destroyAllWindows()