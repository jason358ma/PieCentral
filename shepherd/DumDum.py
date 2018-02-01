import threading
import queue
import random as rand
from LCM import *
from Utils import *

def sender():
    while True:
        new_input = input_to_header.get(input("Command: score bid code "))
        if new_input == SHEPHERD_HEADER.GOAL_SCORE or new_input == SHEPHERD_HEADER.GOAL_BID:
            goal_letter = input_to_goal.get(input("Goal Letter: a b c d e blue gold "))
            alliance = input_to_alliance.get(input("Alliance: blue gold "))
            if goal_letter is None or alliance is None:
                print("Invalid input")
                continue
            lcm_send(LCM_TARGETS.SHEPHERD, new_input, goal_letter, alliance)
        else:
            print("Invalid input")

def receiver():
    events = queue.Queue()
    lcm_start_read(LCM_TARGETS.SENSORS, events)
    while True:
        event = events.get(True)
        if(event[0] == SHEPHERD_HEADER.GENERATE_RFID):
            val = rand.sample([1, 2, 3, 4, 5, 6], 6)
            send = str(val[0]) + "|" str(val[1]) + "|" str(val[2]) + "|" str(val[3]) + "|" str(val[4]) + "|" str(val[5])
            lcm_send(LCM_TARGETS.UI, "help", send)

if __name__ == "__main__":
    sender_thread = threading.Thread(target=sender, name="DummySensorSender")
    recv_thread = threading.Thread(target=receiver, name="DummySensorReceiver")
    sender_thread.start()
    recv_thread.start()