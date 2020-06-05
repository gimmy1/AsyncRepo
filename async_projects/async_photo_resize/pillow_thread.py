# FIRST MAKE SYNCRONOUS
# THEN MAKE THREADING
# THEN MAKE MULTIPROCESSING
# THEN MAKE ASYNCRONOUS
from threading import Thread, Lock

thread_lock = Lock()
class PilThread(Thread):
    def __init__(self, thread_id, _file, _func):
        Thread.__init__(self)
        self.thread_id = thread_id
        self._file = _file
        self._func = _func
    
    def run(self):
        thread_lock.acquire()
        self._func(self.file)
        thread_lock.release()


def resize_image(fi):

