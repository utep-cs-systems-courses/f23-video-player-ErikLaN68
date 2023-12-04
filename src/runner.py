#!/usr/bin/env python3

import threading
from typing import Any
import cv2
import base64
import time
import os
from ProducerConsumer import Storage

storage = Storage()
storageGray = Storage()

class extract():
    def __init__(self):
        clipFileName = 'clip.mp4'
        self.vidcap = cv2.VideoCapture(clipFileName)
        self.insert()
        
    def insert(self):
        while True:
            suc, image = self.vidcap.read()
            # get a jpg encoded frame
            if image is None:
                exit()
            suc, jpgImage = cv2.imencode('.jpg', image)
            #encode the frame as base 64 to make debugging easier
            # jpgAsText = base64.b64encode(jpgImage)
            storageGray.insert(image)

class gray():
    def __init__(self):
        self.togray()
    
    def togray(self):
        while True:
           colorFrame = storageGray.remove()
           grayFrame = cv2.cvtColor(colorFrame, cv2.COLOR_BGR2GRAY)
           storage.insert(grayFrame)

class display():
    def __init__(self):
        self.display()
    
    def display(self):
        while True:
            frame = storage.remove()
            cv2.imshow('Video', frame)
            key = cv2.waitKey(35)
            if(key == ord("q")):
                cv2.destroyAllWindows()
                exit()

threadE = threading.Thread(target=extract)
threadG = threading.Thread(target=gray)
threadD = threading.Thread(target=display)

threadE.start()
threadG.start()
threadD.start()