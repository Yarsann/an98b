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

    def get_output_image(self, frame):
        if self.flip:
            flipped_frame = cv2.flip(frame, 0)
            return cv2.imencode('.jpg', flipped_frame)
        return cv2.imencode('.jpg', frame)

    def get_frame(self):
        ret, frame = self.vc.read()
        ret, image = self.get_output_image(frame)
        return image.tobytes()

