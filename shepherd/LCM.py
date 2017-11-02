import lcm
import message.py
import threading

class LCM:


        def __init__(self, address):
            self.lc = lcm.LCM()
            self.thread
            self.queue = [] 
           	self.address = address;



        def add_to_queue(item):


        def run_queue(item):


        def receive_message(channel):
        	lc.subscribe(channel, handler)
        	while True:
        		lc.handle()

        def send_message(channel, item):
        	lc.publish(channel, item.encode())   

        def handler(channel, data):
            msg = message.decode(data)
            print(" message = '%s'" % msg.name)

lc = LCM();


