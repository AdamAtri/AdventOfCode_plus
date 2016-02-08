import threading
import time
import logging
import random

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)

def n():
    logging.debug('Starting')
    logging.debug('Exiting')

def d():
    logging.debug('Starting')
    time.sleep(5)
    logging.debug('Exiting')

def f():
    t = threading.currentThread()
    r = random.randint(1, 10)
    logging.debug('sleeping %s', r)
    time.sleep(r)
    logging.debug('ending')
    return

if __name__ == '__main__' :
    t = threading.Thread(name='non-daemon', target=n)
    t2 = threading.Thread(name='daemon', target=d)
    t2.setDaemon(True)

    t2.start()
    t.start()

    # to verify that the daemon thread completes, join the threads to the main thread
    # a timeout can be added so that we're not waiting a ridiculous amount of time
    timeout = 5.1
    t2.join(timeout)
    t.join()


    for i in range(3):
        nt = threading.Thread(target=f)
        nt.setDaemon(True)
        nt.start()
    main_thread = threading.current_thread()
    for nt in threading.enumerate():
        if nt is main_thread:
            continue
        logging.debug('joining %s', nt.getName())
        nt.join(timeout)
