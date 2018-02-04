import queue
from LCM import *
from Utils import *
import serial
import threading
import time
import sys

port_one = "/dev/ttyACM0" #change for correct port
port_two = "COM5" #change for correct port

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

def transfer_sensor_data(ser):
	print("starting sensor transfer", flush=True)
	while True:
		sensor_msg = ser.readline().decode("utf-8")
		if len(sensor_msg) != 7: #For Heartbeat
			continue
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

goal_serial_one = serial.Serial(port_one)
goal_serial_two = serial.Serial(port_two)

goal_thread_one = threading.Thread(
	target=transfer_sensor_data, name="transfer thread one", args=([goal_serial_one]))
goal_thread_two = threading.Thread(
	target=transfer_sensor_data, name="transfer thread two", args=([goal_serial_two]))
goal_thread_one.daemon = True
goal_thread_two.daemon = True

goal_thread_one.start()
goal_thread_two.start()

if __name__ == "__main__":
    while True:
        time.sleep(10)