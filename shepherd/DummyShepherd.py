import queue
import time
from LCM import *
from Utils import *

if __name__ == '__main__':
    lcm_send(LCM_TARGETS.DAWN, DAWN_HEADER.CODES, {"rfids" : [1,2,3,4,5,6],
                                                   "codes" : [1,2,3,4,5,6],
                                                   "solutions" : [1,2,3,4,5,6]})

    msg = {"autonomous": True, "enabled": True}
    lcm_send(LCM_TARGETS.DAWN, DAWN_HEADER.ROBOT_STATE, msg)

    time.sleep(10)
    msg2 = {"autonomous": False, "enabled": False}
    lcm_send(LCM_TARGETS.DAWN, DAWN_HEADER.ROBOT_STATE, msg)


    """
    events = queue.Queue()
    lcm_start_read(str.encode(#lcm_TARGETS.SHEPHERD), events)
    while True:
        event = events.get()
        print("RECEIVED:", event)
    """
