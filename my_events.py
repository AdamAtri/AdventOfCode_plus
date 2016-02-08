import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - (%(threadName)-9s) %(message)s',
                    datefmt='%m-%d %H:%M:%S',)

def wait_for_event(e):
    logging.debug('wait_for_event starting')
    # this is a blocking call. until "wait" is satisfied, the current thread
    #  will wait right here
    event_is_set = e.wait()
    logging.debug('event set: %s', event_is_set)
    return

def wait_for_event_timeout(e, t):
    while not e.isSet():
        logging.debug('wait_for_event_timeout starting')
        # this wait times-out. Once time-out "t" is hit the thread continues
        #  with execution.
        event_is_set = e.wait(t)
        logging.debug('event set: %s', event_is_set)
        if event_is_set:
            logging.debug('processing event')
        else:
            logging.debug('doing other things')

def set_event(e):
    time.sleep(2)
    e.set()
    logging.debug('Event set')

if __name__ == '__main__':
    e = threading.Event()
    t1 = threading.Thread(name='blocking', target=wait_for_event, args=(e,))
    t1.start()

    t2 = threading.Thread(name='non-blocking',
                          target=wait_for_event_timeout,
                          args=(e, 2))
    t2.start()

    t3 = threading.Thread(name='setter', target=set_event, args=(e,))
    logging.debug('Waiting before calling Event.set()')
    t3.start()
