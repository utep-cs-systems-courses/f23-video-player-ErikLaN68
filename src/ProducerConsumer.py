from threading import Semaphore, Lock

class Storage:
    
    def __init__(self):
        print('Setting up Storage')
        self.queue = []
        self.full = Semaphore(0)
        self.empty = Semaphore(15)
        self.lock = Lock()
    
    def addToQueue(self, item):
        self.queue.append(item)
    
    def dequeue(self, item):
        head, *tail = self.queue
        self.queue = tail
        return head
    
    def fullAcquire(self):
        self.full.acquire()
    
    def fullRelease(self):
        self.full.release()
        
    def emptyAcquire(self):
        self.empty.acquire()
    
    def emptyRelease(self):
        self.empty.release()
        
    def lockAcquire(self):
        self.lock.acquire()
    
    def lockRelease(self):
        self.lock.release()