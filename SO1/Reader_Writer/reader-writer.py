from time import sleep
from random import randint
from datetime import datetime
from threading import Thread
from threading import BoundedSemaphore


class Reader:
    def __init__(self, writing: BoundedSemaphore, mutex: BoundedSemaphore):
        self.writing = writing
        self.mutex = mutex
        self.reading = randint(1,20)
        
        self.active()
    
    def active(self):
        global message
        global readcount
        
        while self.reading:
            self.mutex.acquire()
            readcount += 1
            
            if readcount == 1:
                self.writing.acquire()
            
            self.mutex.release()
            
            # reading
            print(f"Loading time: {message}")
            
            self.mutex.acquire()
            readcount -= 1
            
            if readcount == 0:
                self.writing.release()
            
            self.mutex.release()
            
            sleep(0.5)
            self.reading -= 1
            
    def kill(self):
        self.reading = False
    
    
class Writer:
    def __init__(self, writing: BoundedSemaphore):
        self.writing = writing
        self.posting = randint(1,5)
        
        self.active()
        
        
    def active(self):
        global message
        
        while self.posting:
            self.writing.acquire()
            
            self.message = str(datetime.now())
            print(f"Saving time: {self.message}")
            message = self.message
            
            self.writing.release()
            
            sleep(1)
            self.posting -= 1
        
    
    
if __name__ == "__main__":
    writing = BoundedSemaphore(1)
    mutex = BoundedSemaphore(1)
    readcount = 0

    writers = dict()
    readers = dict()
    
    message = ''
  
    writers['w1'] = Thread(target=Writer, args=(writing, )).start()
    writers['w2'] = Thread(target=Writer, args=(writing, )).start()
    
    readers['r1'] = Thread(target=Reader, args=(writing, mutex, )).start()
    readers['r2'] = Thread(target=Reader, args=(writing, mutex, )).start()
    readers['r3'] = Thread(target=Reader, args=(writing, mutex, )).start()
    readers['r4'] = Thread(target=Reader, args=(writing, mutex, )).start()

    
