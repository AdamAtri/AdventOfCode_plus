import threading
import time
import logging
import random

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - (%(threadName)-9s) %(message)s',
                    datefmt='%m-%d %H:%M:%S',)

class Counter(object):
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.value = start

    def increment(self):
        logging.debug('Waiting for a lock')
        self._get_lock()
        try:
            logging.debug('Acquired a lock')
            self.value += 1
        finally:
            logging.debug('Release the lock')
            self.lock.release()

    def _get_lock(self):
        while True:
            if self.lock.acquire(1):
                return
            logging.debug('Still waiting....')
            time.sleep(1)

def consumer(condition):
    logging.debug('Consumer thread started...')
    with condition:
        logging.debug('Consumer waiting...')
        # blocking wait call
        condition.wait()
        logging.debug('Consumer consumed the resource.')

def producer(condition):
    logging.debug('Producer thread started...')
    with condition:
        logging.debug('Making resource available')
        for i in range(5):
            print 'This is where some work could be done'
            time.sleep(2)
        logging.debug('Notifying all consumers')
        condition.notifyAll()


def locker(lock):
    logging.debug('Starting load simulation')
    while True:
        with lock:
            logging.debug('Locking (using with context)')
            time.sleep(3.0)
            logging.debug('Not locking')
        time.sleep(0.1)
    return

def worker(c):
    logging.debug('Start')
    for i in range(2):
        r = random.random()
        logging.debug('Sleeping %0.02f', r)
        time.sleep(r)
        c.increment()
    logging.debug('Done')

if __name__ == '__main__':
    counter = Counter()
    lock_thread = threading.Thread(name='Locker',
                                   target=locker,
                                   args=(counter.lock,))
    lock_thread.setDaemon(True)
    lock_thread.start()

    for i in range(2):
        t = threading.Thread(name='T%s' % i,
                             target=worker,
                             args=(counter,))
        t.start()

    # # Worker threads demonstrate how to have threads work independently
    # #  on shared objects
    # logging.debug('Waiting for worker threads to complete')
    # main_thread = threading.currentThread()
    # for t in threading.enumerate():
    #     # Make sure that the main thread won't die before
    #     #  the worker threads have finished
    #     if t is not main_thread and t is not lock_thread:
    #         t.join()
    # logging.debug('Counter: %d', counter.value)

    # Working with conditionals illustrates the fundamentals of
    # the producer/consumer pattern
    print "\nProducer / Consumer pattern"
    condition = threading.Condition()
    cs1 = threading.Thread(name='consumer1', target=consumer, args=(condition,))
    cs2 = threading.Thread(name='consumer2', target=consumer, args=(condition,))
    prod = threading.Thread(name='producer', target=producer, args=(condition,))

    cs1.start()
    time.sleep(2)
    cs2.start()
    prod.start()
