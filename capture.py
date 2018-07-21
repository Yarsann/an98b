import cv2
import time

vc = cv2.VideoCapture(0)

time.sleep(2.0)

success, image = vc.read()
image_s = cv2.resize(image, (1280,720))

cv2.imwrite("before.png",image_s)

vc.release()
