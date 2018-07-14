from imutils.video.pivideostream import PiVideoStream
import time
import datetime
import numpy as np
import cv2


class SimpleStreamer(object):
    def __init__(self, flip = False):
        try:
            self.vc = cv2.VideoCapture(0)
        except:
            print(self.vc)
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vc.release()

    def flip_if_needed(self, frame):
        if self.flip:
            return cv2.flip(frame, 0)
        return frame

    def get_frame(self):
        ret, frame = self.vc.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

