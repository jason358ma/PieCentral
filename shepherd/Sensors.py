import queue
from LCM import *
from Utils import *
import serial

gold_serial = serial.Serial("COM4", timeout = 0)
blue_serial = serial.Serial("COM5", timeout = 0)

while True:
    lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.GOAL_SCORE, goal_letter, alliance)
    gold_serial.read().decode("utf-8")
    blue_serial.read().decode("utf-8")
