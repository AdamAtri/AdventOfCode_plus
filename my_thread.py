import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)

threads = [ ]
def send_message():
    print('Threads will begin momentarily...')
    time.sleep(1)
    start_threads()
    return

def start_threads():
    for t in threads:
        t.start();
        t.join();
    return;


class MyThread(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(MyThread, self).__init__(group, target, name, verbose)
        self.args = args
        self.kwargs = kwargs
        return

    def run(self):
        time.sleep(2)
        logging.debug('running with %s and %s. ', self.args, self.kwargs)
        return


if __name__ == '__main__':
    items = ['handkerchief', 'bell', '42 cents', 'a rooster', 'your mama', 'a billygoat']
    kwargs = dict(a=43, b=90, c='cat', d='doorbell')

    for i in range(3):
        t_num = i + 1
        min = i * 2
        max = min + 1

        args = (items[min], items[max])
        t = MyThread(args=args, kwargs=kwargs)
        threads.append(t);

    timer = threading.Timer(3.0, send_message)
    timer.start()
