import queue
from LCM import *
from Utils import *
import serial
import threading
import time

port_one = "COM4"
# port_two = "COM5"

def transfer_sensor_data(ser):
	while True:
		sensor_msg = ser.readline().decode("utf-8")
		print(sensor_msg)
		alliance = sensor_msg[0:4].lower()
		goal_letter = sensor_msg[4].lower()
		lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.GOAL_SCORE, goal_letter, alliance)
		time.sleep(0.01)

goal_serial_one = serial.Serial(port_one)
# goal_serial_two = serial.Serial(port_two)

goal_thread_one = threading.Thread(
	target=transfer_sensor_data, name="transfer thread one", args=([goal_serial_one]))
# goal_thread_two = threading.Thread(
	# target=transfer_sensor_data, name="transfer thread two", args=([goal_serial_two]))
goal_thread_one.daemon = True
# goal_thread_two.daemon = True

goal_thread_one.start()
# goal_thread_two.start()

if __name__ == "__main__":
    while True:
        time.sleep(10)
