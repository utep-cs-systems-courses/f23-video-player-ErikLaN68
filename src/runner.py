#!/usr/bin/env python3

from collections.abc import Callable, Iterable, Mapping
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
        #threading.Thread.__init__(self)
        clipFileName = 'clip.mp4'
        self.vidcap = cv2.VideoCapture(clipFileName)
        self.insert()
        
    def insert(self):
        print('in insert')
        while True:
            suc, image = self.vidcap.read()
            # get a jpg encoded frame
            if image is None:
                exit()
            suc, jpgImage = cv2.imencode('.jpg', image)
            #encode the frame as base 64 to make debugging easier
            # jpgAsText = base64.b64encode(jpgImage)
            storage.emptyAcquire()
            print('after sema empty')
            storage.lockAcquire()
            # add the frame to the buffer
            storage.addToQueue(jpgImage)
            print('Image stored')
            storage.lockRelease()
            storage.fullRelease()
            
class display():
    def __init__(self):
        #threading.Thread.__init__(self)
        print('setting up display')
        self.display()
    
    def display(self):
        print('in display')
        while True:
            storage.fullAcquire()
            print('Past sema in display')
            storage.lockAcquire()
            frame = storage.dequeue()
            cv2.imshow('Video', frame)
            storage.lockRelease()
            storage.emptyRelease()
            time.sleep(1/30)

threadE = threading.Thread(target=extract)
threadD = threading.Thread(target=display)

threadE.start()
threadD.start()