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

class extract(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        clipFileName = 'clip.mp4'
        self.vidcap = cv2.VideoCapture(clipFileName)
        self.insert()
        
    def insert(self):
        print('in insert')
        success,image = self.vidcap.read()
        while True:
            # get a jpg encoded frame
            success, jpgImage = cv2.imencode('.jpg', image)

            #encode the frame as base 64 to make debugging easier
            # jpgAsText = base64.b64encode(jpgImage)
            print('Before sema empty')
            storage.emptyAcquire()
            print('after sema empty')
            storage.lockAcquire()
            # add the frame to the buffer
            storage.addToQueue(jpgImage)
            storage.lockRelease()
            storage.fullRelease()
        
            success,image = self.vidcap.read()
            
class display(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.display()
    
    def display():
        print('in display')
        while True:
            storage.fullAcquire()
            storage.lockAcquire()
            frame = storage.dequeue
            cv2.imshow('Video', frame)
            if cv2.waitKey(42) and 0xFF == ord("q"):
                break
            storage.lockRelease()
            storage.emptyRelease()
            time.sleep(1/30)

threadE = extract()
threadD = display()

threadE.start()
threadD.start()