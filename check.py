import cv2

def find_connected_cameras():
    num_cameras = 1  # Ganti dengan jumlah kamera yang ingin Anda cek
    for i in range(num_cameras):
        cap = cv2.VideoCapture(i)
        if not cap.read()[0]:
            break
        cap.release()
        print(f"Camera {i} is connected.")

find_connected_cameras()
