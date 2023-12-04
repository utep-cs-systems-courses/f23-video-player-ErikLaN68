from threading import Semaphore, Lock

class Storage:
    
    def __init__(self):
        print('Setting up Storage')
        self.queue = []
        self.full = Semaphore(0)
        self.empty = Semaphore(30)
        self.lock = Lock()
    
    def insert(self,frame):
        self.emptyAcquire()
        self.lockAcquire()
        # Add frame to the queue
        self.addToQueue(frame)
        self.lockRelease()
        self.fullRelease()
        
    def remove(self):
        self.fullAcquire()
        self.lockAcquire()
        frame = self.dequeue()
        self.lockRelease()
        self.emptyRelease()
        return frame
        
    def addToQueue(self, item):
        self.queue.append(item)
    
    def dequeue(self):
        head = self.queue[0]
        self.queue = self.queue[1:]
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