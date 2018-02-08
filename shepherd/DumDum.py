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
            val = rand.sample([1, 2, 3, 4, 5, 6], 6)
            send = str(val[0]) + "|" +str(val[1]) + "|" +str(val[2]) + "|" +str(val[3]) + "|" +str(val[4]) + "|" +str(val[5])
            lcm_send(LCM_TARGETS.UI, UI_HEADER.RFID_LIST, send);
            print("help")

if __name__ == "__main__":
    sender_thread = threading.Thread(target=sender, name="DummySensorSender")
    recv_thread = threading.Thread(target=receiver, name="DummySensorReceiver")
    sender_thread.start()
    recv_thread.start()
