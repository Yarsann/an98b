from imutils.video.pivideostream import PiVideoStream
import time
import datetime
import numpy as np
import cv2


class SimpleStreamer(object):
    def __init__(self, flip = False):
        try:
            self.vs = cv2.VideoCapture(0)
        except:
            print(self.vs)
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vs.release()

    def flip_if_needed(self, frame):
#        if self.flip:
#            return np.flip(frame, 1)
        return frame

    def get_frame(self):
        ret, frame = self.vs.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

