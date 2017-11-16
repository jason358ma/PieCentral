import lcm
import threading
import json

class LCMClass:
        def __init__(self, data_type, queue, receive_channel):
            self.receive_channel = receive_channel
            self.queue = queue
            self.lc = lcm.LCM()

        # def start_thread(self):
        #   self.thread = threading.Thread()
        #   self.thread.daemon = True
        #   self.thread.start() 

        # Receive messages
        def receive_message(self):
        	self.lc.subscribe(self.receive_channel, handler)
        	while True:
        		lc.handle()

        # Send a list into a target
        def send_message(self, target, item):
            msg = ''.join(str(e) for e in item)
        	self.lc.publish(target, msg.encode())   

        def handler(self, channel, item):
            msg = item.decode()
            self.queue.put(item)

       
