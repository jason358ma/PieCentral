import sys
import time
import threading
import serial
from LCM import *
from Utils import *

sensor_port_one = "/dev/ttyACM0" # change to correct port
sensor_port_two = "/dev/ttyACM1" # change to correct port
bidding_port_one = "/dev/ttyACM2"
bidding_port_two = "/dev/ttyACM3"

alliance_mapping = {
    "gold": ALLIANCE_COLOR.GOLD,
    "blue": ALLIANCE_COLOR.BLUE
}

goal_mapping = {
    "a": GOAL.A,
    "b": GOAL.B,
    "c": GOAL.C,
    "d": GOAL.D,
    "e": GOAL.E,
    "bg": GOAL.BLUE,
    "gg": GOAL.GOLD
}

def transfer_linebreak_data(ser):
    print("<1> Starting Linebreak Process", flush=True)
    while True:
        sensor_msg = ser.readline().decode("utf-8")
        if len(sensor_msg) != 7: #For Heartbeat
            continue
        print("<2> Message Received: ", sensor_msg, flush=True)
        alliance = sensor_msg[0:4].lower()
        alliance_enum = alliance_mapping[alliance]
        goal_letter = sensor_msg[4].lower()
        if goal_letter == "g":
            alliance_letter = alliance[0] # 'b' or 'g'
            goal_enum = goal_mapping[alliance_letter + "g"]
        else:
            goal_enum = goal_mapping[goal_letter]
        lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.GOAL_SCORE, goal_enum, alliance_enum)
        time.sleep(0.01)

def transfer_bid_data(ser):
    print("<3> Starting Bidding Process", flush=True)
    while True:
        bid_msg = ser.readline().decode("utf-8")
        time.sleep(0.01)

def main():
    goal_serial_one = serial.Serial(sensor_port_one)
    goal_serial_two = serial.Serial(sensor_port_two)

    goal_thread_one = threading.Thread(
        target=transfer_linebreak_data, name="sensor transfer thread one", args=([goal_serial_one]))
    goal_thread_two = threading.Thread(
        target=transfer_linebreak_data, name="sensor transfer thread two", args=([goal_serial_two]))
    goal_thread_one.daemon = True
    goal_thread_two.daemon = True

    goal_thread_one.start()
    goal_thread_two.start()

    bidding_serial_one = serial.Serial(bidding_port_one)
    bidding_serial_two = serial.Serial(bidding_port_two)

    bidding_thread_one = threading.Thread(
        target=transfer_bid_data, name="bidding transfer thread one", args=([bidding_serial_one]))
    bidding_thread_two = threading.Thread(
        target=transfer_bid_data, name="bidding transfer thread two", args=([bidding_serial_two]))
    bidding_thread_one.daemon = True
    bidding_thread_two.daemon = True

    bidding_thread_one.start()
    bidding_thread_two.start()

    while True:
        time.sleep(100)

if __name__ == "__main__":
    main()
