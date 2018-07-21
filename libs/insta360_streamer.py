import numpy as np
import matplotlib.pyplot as plt
import random
%matplotlib inline
import itertools
import math
import cv2
import itertools

def cv_imshow(image_bgr):
    image_rgb = cv2.cvtColor(image_bgr,cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    plt.show()

vc = cv2.VideoCapture(0)
image = vc.read()
image_s = cv2.resize(image, (1280,720))
cv_imshow(image_s)

vertex = 640
dst_map = np.array(list(itertools.product(range(vertex),range(vertex*2))))
print(dst_map)

src_cx = 319
src_cy = 319
src_r = 283
src_cx2 = 1280 - src_cx


map_x = np.zeros((vertex,vertex*2))
map_y = np.zeros((vertex,vertex*2))
for y in range(vertex):
    for x in range(vertex*2):
        phi1 = math.pi * x / vertex
        theta1 = math.pi * y / vertex

        X = math.sin(theta1) * math.cos(phi1)
        Y = math.sin(theta1) * math.sin(phi1)
        Z = math.cos(theta1)
        
        phi2 = math.acos(-X)
        theta2 = np.sign(Y)*math.acos(-Z/math.sqrt(Y*Y + Z*Z))
      
        #0 等距離射影
        #1 立体射影
        #2 立体射影逆変換
        #3 正射影
        #4 正射影逆変換
        method = 0
        
        if(phi2 < math.pi / 2):
            #等距離射影
            if method == 0:
                r_ = phi2 / math.pi * 2
            #立体射影
            elif method == 1:
                r_ =  math.tan((phi2) / 2)
            #立体射影逆変換
            elif method == 2:
                r_ =  1 - math.tan((math.pi / 2 - phi2) / 2)
            #正射影
            elif method == 3:
                r_ = math.sin(phi2)
            #正射影逆変換
            elif method == 4:
                r_ = 1 - math.sin(math.pi / 2 - phi2)
            map_x[y,x] = src_r * r_ * math.cos(theta2) + src_cx
            map_y[y,x] = src_r * r_ * math.sin(theta2) + src_cy
        else:
            #等距離射影
            if method == 0:
                r_ = (math.pi - phi2) / math.pi * 2
            #立体射影
            elif method == 1:
                r_ =  math.tan((math.pi - phi2) / 2)
            #立体射影逆変換
            elif method == 2:
                r_ =  1 - math.tan((-math.pi/2 + phi2) / 2)
            #正射影
            elif method == 3:
                r_ = math.sin(math.pi - phi2)
            #正射影逆変換
            elif method == 4:
                r_ = 1 - math.sin(- math.pi / 2 + phi2)
            map_x[y,x] = src_r * r_ * math.cos(math.pi - theta2) + src_cx2
            map_y[y,x] = src_r * r_ * math.sin(math.pi - theta2) + src_cy         
            
map_x = map_x.astype('float32')
map_y = map_y.astype('float32')

image2 = cv2.remap( image_s, map_x, map_y, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT);

cv_imshow(image2)
cv2.imwrite("Equirectangular.png",image2)