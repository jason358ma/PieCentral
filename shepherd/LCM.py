import threading
import lcm

class LCMClass:
    '''
    __init__: receiving channel name (string), queue (Python queue object)
    lcm_start_read: creates thread that receives any message to receiving
    channel and adds it to queue as a tuple (header, [*args]).
    header: string
    [*args]: variable length containing ints/strings.
    '''
    def __init__(self, receive_channel, queue):
        self.receive_channel = receive_channel
        self.queue = queue
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

        def handler(_, item):
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
    Send header (string) and variable number of arguments (string or int) to target channel (string)
    '''
    msg = '|||'.join(str(a) for a in args)
    msg = '|||'.join([header, msg])
    lc.publish(target_channel, msg.encode())
