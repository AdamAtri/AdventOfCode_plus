import threading
import time
import logging
import random
import Queue

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - (%(threadName)-9s): %(message)s',
                    datefmt='%m-%d %I:%M:%S')

BUF_SIZE = 10
q = Queue.Queue(BUF_SIZE)

class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThread, self).__init__()
        self.target = target
        self.sleep_count = 0
        self.name = name

    def run(self):
        while True:
            if not q.full():
                item = random.randint(1, 10)
                q.put(item)
                logging.debug('Putting %s (%s items in queue).', str(item), str(q.qsize()))
                time.sleep(random.random())
            else:
                self.sleep_count += 1
                if self.sleep_count > 10:
                    logging.debug('good bye.')
                    return
                time.sleep(random.random())
        return

class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread, self).__init__()
        self.target = target
        self.name = name
        self.items = [ ]
        self.max = 10
        return

    def run(self):
        while True:
            if not q.empty() and len(self.items) <= self.max:
                item = q.get()
                self.items.append(item)
                logging.debug('Getting %s (%s items in queue).', str(item), str(q.qsize()))
                time.sleep(random.random())
            if len(self.items) == self.max:
                logging.debug('I\'m full: %s', self.items)
                return
        return

if __name__ == '__main__':
    p = ProducerThread(name='producer')
    p.setDaemon = True
    c = ConsumerThread(name='consumer1')
    c2 = ConsumerThread(name='consumer2')
    c3 = ConsumerThread(name='consumer3')

    p.start()
    time.sleep(2)
    c.start()
    c2.start()
    c3.start()
    c.join()
    c2.join()
    c3.join()
    time.sleep(2)
