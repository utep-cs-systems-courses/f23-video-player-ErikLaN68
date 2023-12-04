#!/usr/bin/env python3

import threading
from typing import Any
import cv2
import base64
import time
import os
from ProducerConsumer import Storage

storage = Storage()

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
            storage.emptyAcquire()
            storage.lockAcquire()
            # Add frame to the queue
            print('Inserting frame')
            storage.addToQueue(image)
            storage.lockRelease()
            storage.fullRelease()
            
class display():
    def __init__(self):
        self.display()
    
    def display(self):
        while True:
            storage.fullAcquire()
            storage.lockAcquire()
            frame = storage.dequeue()
            print("Displaying frame")
            cv2.imshow('Video', frame)
            key = cv2.waitKey(35)
            if(key == ord("q")):
                cv2.destroyAllWindows()
                exit()
            storage.lockRelease()
            storage.emptyRelease()

threadE = threading.Thread(target=extract)
threadD = threading.Thread(target=display)

threadE.start()
threadD.start()