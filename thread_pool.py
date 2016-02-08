import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - (%(threadName)-9s): %(message)s',
                    datefmt='%m-%d %I:%M:%S',)

class ThreadPool(object):
    def __init__(self):
        super(ThreadPool, self).__init__()
        self.active = [ ]
        self.lock = threading.Lock()

    def makeActive(self, name):
        with self.lock:
            self.active.append(name)
            logging.debug('Running: %s', str(self.active))

    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)
            logging.debug('Closing: %s; Active: %s', name, str(self.active))

def f(semaphore, pool):
    logging.debug('Waiting to join the pool')
    with semaphore:
        name = threading.currentThread().getName()
        pool.makeActive(name)
        time.sleep(5.0)
        pool.makeInactive(name)

if __name__ == '__main__':
    pool = ThreadPool()
    s = threading.Semaphore(10)
    for i in range(20):
        t = threading.Thread(target=f, name='Thread-%s' % i, args=(s, pool))
        t.start()
