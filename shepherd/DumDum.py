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
        if (event[0] == SHEPHERD_HEADER.GENERATE_RFID):
            s = []
            for i in range(6):
                s.append(rand.randrange(10))
            x = {"RFID_list": s}
            lcm_send(LCM_TARGETS.UI, UI_HEADER.RFID_LIST, x);
            print("Sent RFIDs")
        if (event[0] == SHEPHERD_HEADER.GET_SCORES):
            x = {"blue_score": rand.randrange(100), "gold_score": rand.randrange(100)}
            lcm_send(LCM_TARGETS.UI, UI_HEADER.SCORES, x);
            print("Sent scores")
        if (event[0] == SHEPHERD_HEADER.SCORE_ADJUST):
            print(event[1])

if __name__ == "__main__":
    sender_thread = threading.Thread(target=sender, name="DummySensorSender")
    recv_thread = threading.Thread(target=receiver, name="DummySensorReceiver")
    sender_thread.start()
    recv_thread.start()
