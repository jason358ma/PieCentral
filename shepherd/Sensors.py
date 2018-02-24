import sys
import time
import threading
import serial
from LCM import *
from Utils import *

linebreak_port_one = "/dev/ttyACM0" # change to correct port
linebreak_port_two = "/dev/ttyACM1" # change to correct port
bidding_port_blue = "/dev/ttyACM2" # change to correct port
bidding_port_gold = "/dev/ttyACM3" # change to correct port

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

def recv_from_bid(ser, alliance_enum):
    print("<3> Starting Linebreak Process", flush=True)
    while True:
        sensor_msg = ser.readline().decode("utf-8")
        if len(sensor_msg) != 7: #For Heartbeat
            continue
        print("<4> Message Received: ", sensor_msg)
        sensor_msg.lower()
        payload_list = sensor_msg.split(";")
        if payload_list[0] == "bg":
            goal_enum = goal_mapping[payload_list[1]]
            send_dictionary = {"goal": goal_enum, "alliance": alliance_enum}
            lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.GOAL_BID, send_dictionary)
        
        send_dictionary = {"alliance" : alliance_enum, "goal" : goal_enum}
        lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.GOAL_SCORE, send_dictionary)
        time.sleep(0.01)

def send_to_bid(ser, alliance_enum):
    recv_q = queue.Queue()
    lcm_start_read(LCM_TARGETS.SENSORS, recv_q)
    while True:
        msg = recv_q.get()
        payload_dict = msg[1]
        send_str = ""
        if (msg[0] == SENSOR_HEADERS.BID_PRICE):
            send_str = "bp;"
            goal_list = payload_dict["price"]
            if alliance_enum == ALLIANCE_COLOR.BLUE:
                goal_list = goal_list[::-1]
            for price in goal_list:
                send_str += str(price) + ";"
            send_str += '\n'
        elif (msg[0] == SENSOR_HEADERS.TEAM_SCORE):
            send_str = "ts;"
            score = str(payload_dict["score"][alliance_enum])
            send_str += score + ";\n"
        elif (msg[0] == SENSOR_HEADERS.CODE_RESULT):
            send_str = "cstatus;"
            send_str += str(payload_dict["result"]) + ";\n"
        elif (msg[0] == SENSOR_HEADERS.GOAL_OWNERS):
            send_str = "go;"
            owners_list = payload_dict["owners"]
            bidders_list = payload_dict["bidders"]
            if alliance_enum == ALLIANCE_COLOR.BLUE:
                owners_list = owners_list[::-1]
                bidders_list = bidders_list[::-1]
            for i in range(len(owners_list)):
                owner = owners_list[i]
                owner_color = ""
                if owner == None:
                    owner_color = "n"
                elif owner == ALLIANCE_COLOR.BLUE:
                    owner_color = "b"
                else:
                    owner_color = "g"
                send_str += owner_color + ";"
                bidder = bidders_list[i]
                if bidder == None and owner == alliance_enum:
                    send_str += owner_color
                elif bidder == None and owner != alliance_enum:
                    send_str += "n"
                elif bidder == alliance_enum:
                    send_str += "n"
                else:
                    send_str += "e"
                send_str += ";\n" 
        ser.write(send_str.encode("utf-8"))

def transfer_linebreak_data(ser):
    print("<1> Starting Linebreak Process", flush=True)
    while True:
        sensor_msg = ser.readline().decode("utf-8")
        if len(sensor_msg) != 7: #For Heartbeat
            continue
        print("<2> Message Received: ", sensor_msg)
        alliance = sensor_msg[0:4].lower()
        alliance_enum = alliance_mapping[alliance]
        goal_letter = sensor_msg[4].lower()
        if goal_letter == "g":
            alliance_letter = alliance[0] # 'b' or 'g'
            goal_enum = goal_mapping[alliance_letter + "g"]
        else:
            goal_enum = goal_mapping[goal_letter]
        send_dictionary = {"alliance" : alliance_enum, "goal" : goal_enum}
        lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.GOAL_SCORE, send_dictionary)
        time.sleep(0.01)

def main():
    goal_serial_one = serial.Serial(linebreak_port_one)
    goal_serial_two = serial.Serial(linebreak_port_two)
    bid_serial_blue = serial.Serial(bidding_port_blue)
    bid_serial_gold = serial.Serial(bidding_port_gold)

    goal_thread_one = threading.Thread(
        target=transfer_linebreak_data, name="transfer thread one", args=([goal_serial_one]))
    goal_thread_two = threading.Thread(
        target=transfer_linebreak_data, name="transfer thread two", args=([goal_serial_two]))
    goal_thread_one.daemon = True
    goal_thread_two.daemon = True

    goal_thread_one.start()
    goal_thread_two.start()

    recv_thread_blue = threading.Thread(
        target=recv_from_bid, name="receive thread blue", args=([bid_serial_blue, ALLIANCE_COLOR.BLUE]))
    send_thread_blue = threading.Thread(
        target=send_to_bid, name="send thread blue", args=([bid_serial_blue, ALLIANCE_COLOR.BLUE]))

    recv_thread_gold = threading.Thread(
        target=recv_from_bid, name="receive thread gold", args=([bid_serial_gold, ALLIANCE_COLOR.GOLD]))
    send_thread_gold = threading.Thread(
        target=send_to_bid, name="send thread gold", args=([bid_serial_gold, ALLIANCE_COLOR.GOLD]))

    recv_thread_blue.daemon = True
    send_thread_blue.daemon = True
    recv_thread_gold.daemon = True
    send_thread_gold.daemon = True

    recv_thread_blue.start()
    send_thread_blue.start()
    recv_thread_gold.start()
    send_thread_gold.start()

    while True:
        time.sleep(100)

if __name__ == "__main__":
    main()
