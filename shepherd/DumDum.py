import threading
import queue
import random as rand
from LCM import *
from Utils import *

def sender():
    while True:
        pass

def receiver():
    events = queue.Queue()
    lcm_start_read(LCM_TARGETS.SHEPHERD, events)
    while True:
        event = events.get(True)
        print("got event")
        if(event[0] == SHEPHERD_HEADER.GENERATE_RFID):
            x = {RFID: [4,5,6,7,8,9]}
            lcm_send(LCM_TARGETS.UI_HEADER, RFID_LIST, x);
            print("help")

if __name__ == "__main__":
    sender_thread = threading.Thread(target=sender, name="DummySensorSender")
    recv_thread = threading.Thread(target=receiver, name="DummySensorReceiver")
    sender_thread.start()
    recv_thread.start()
