import numpy as np
import random
import math
import cv2

class SimpleStreamer(object):
    def __init__(self, flip = False):
        # Define the codec and create VideoWriter object
        #fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #self.out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
        # Video Capture
        try:
            self.vc = cv2.VideoCapture(0)
            self.map_x = np.load("/var/isaax/project/libs/map_x.npy")
            self.map_y = np.load("/var/isaax/project/libs/map_y.npy")
        except:
            print(self.vc)
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        #self.out.release()
        self.vc.release()

    def get_output_image(self, frame):
        # if self.flip:
        #     flipped_frame = cv2.flip(frame, 0)
        #     return cv2.imencode('.jpg', flipped_frame)
        return cv2.imencode('.jpg', frame)

    def save_frame(self):
        return False

    def get_frame(self):
        ret, frame = self.vc.read()
        resized = cv2.resize(frame, (1280,720))
        remaped = cv2.remap(resized, self.map_x, self.map_y, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)
        ret, image = self.get_output_image(remaped)
        return image.tobytes()

    def generate_map(self):
        image = cv2.imread("before1.png")

        image_s = cv2.resize(image, (1280,720))

        cv2.imwrite("before.png",image_s)

        vertex = 640
        dst_map = np.array(list(itertools.product(range(vertex),range(vertex*2))))
        #print(dst_map)

        src_cx = 319
        src_cy = 329
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
                method = 2
                
                if(phi2 < math.pi):
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

                np.save("map_x.npy", map_x)
                np.save("map_y.npy", map_y)

                image2 = cv2.remap( image_s, np.load("map_x.npy"), np.load("map_y.npy"), cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)
                cv2.imwrite("after.png",image2)
