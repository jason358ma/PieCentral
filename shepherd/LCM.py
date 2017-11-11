import lcm
import message.py
import threading

class LCMClass:
        def __init__(self, lc, queue, send_channel, receive_channel):
            self.thread = threading.Thread()
            self.thread.start()
            self.receive_channel = receive_channel
            self.send_channel = send_channel
            self.main_queue = queue
            self.queue = []
                
        def add_to_queue():
            while True:
                self.main_queue.append(self.queue.pop(0))

        def receive_message():
        	lc.subscribe(self.receive_channel, handler)
        	while True:
        		lc.handle()

        def send_message(item):
        	lc.publish(self.send_channel, item.encode())   

        def handler(channel, data):
            msg = message.decode(data)
            self.queue.append(msg)

