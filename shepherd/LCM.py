import lcm
import threading

class LCMClass:
        def __init__(self, queue, receive_channel):
            self.queue = queue
            self.receive_channel = receive_channel
            self.lc = lcm.LCM()

        # Receive messages
        def lcm_start_read(self):
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

# Send a list into a target
def lcm_send(target_channel, header, *args):
    msg = '|||'.join(str(a) for a in args)
    msg = '|||'.join([header, msg])
    lc.publish(target_channel, msg.encode())       
