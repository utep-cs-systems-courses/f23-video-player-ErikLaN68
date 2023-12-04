from threading import Semaphore, Lock

class Storage:
    
    def __init__(self):
        self.queue = []
        self.full = Semaphore(0)
        self.empty = Semaphore(len(self.queue))
        self.storageLock = Lock
    
    def fullAcquire(self):
        self.full.acquire
    
    def fullRelease(self):
        self.full.release
        
    def emptyAcquire(self):
        self.empty.acquire
    
    def emptyRelease(self):
        self.empty.release
        
    def lockAcquire(self):
        self.storageLock.acquire
    
    def lockRelease(self):
        self.storageLock.release