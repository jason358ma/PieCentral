import lcm
import threading

class LCMClass:
    '''
    Initialize with a queue (Python queue object), which should be processed separately within each process, and a receiving channel name (string).
    When lcm_start_read is run, a thread is created that receives any message to this receiving channel and adds it to the queue as a tuple (header, [*args]). 
    Header is a string and the list is variable length containing ints/strings.
    '''
    def __init__(self, queue, receive_channel):
        self.queue = queue
        self.receive_channel = receive_channel
        self.lc = lcm.LCM()

    def lcm_start_read(self):
        '''
        Starts thread that receives messages sent to channel and adds them to queue
        '''
        def string_to_int(string):
            try:
                return int(string)
            except ValueError:
                return string

        def handler(channel, item):
            msg = item.decode()
            msg_list = msg.split('|||')
            self.queue.put((msg_list[0], [string_to_int(x) for x in msg_list[1:]]))

        self.lc.subscribe(self.receive_channel, handler)

        def run():
            while True:
                self.lc.handle()

        rec_thread = threading.Thread()
        rec_thread.run = run
        rec_thread.start()

lc = lcm.LCM()

def lcm_send(target_channel, header, *args):
    '''
    Sends a header (string) and variable amount of arguments (string or int) to a target channel (string).
    '''
    msg = '|||'.join(str(a) for a in args)
    msg = '|||'.join([header, msg])
    lc.publish(target_channel, msg.encode())       

