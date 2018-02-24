import sys
import time
import threading
import serial
from LCM import *
from Utils import *


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

IDENTIFY_TIMEOUT = 1

def get_working_serial_ports(excludes: set):
    """Get a list of working serial ports, excluding some.
    
    Returns a list of `serial.Serial` object.
    """
    import glob
    maybe_ports = set(glob.glob("/dev/ttyACM*"))
    maybe_ports.difference_update(excludes)

    working = []
    for p in maybe_ports:
        try:
            working.append(serial.Serial(p))
        except serial.SerialException:
            pass

    return working


def identify_linebreak_sensors(working_ports):
    """ Check which ports have linebreak sensors on them.

    Returns a list of serial ports.
    """
    def maybe_identify_sensor(serial_port, timeout, flag):
        """Check whether a serial port contains a sensor.

        Parameters:
            serial_port -- the port to check
            timeout -- quit reading from the serial port after this
            amount of time
            flag -- a flag to set if a device is successfully identified
        """
        prev_timeout = serial_port.timeout
        serial_port.timeout = timeout
        try:
            msg = serial_port.readline().decode("utf-8")
            if is_linebreak_sensor(msg):
                flag.set()
        except serial.SerialTimeoutException:
            pass
        serial_port.timeout = prev_timeout

    flags = [threading.Event() for _ in working_ports]
    threads = [threading.Thread(target=maybe_identify_sensor,
                                args=(port,
                                      IDENTIFY_TIMEOUT,
                                      flag)) for (flag, port) in zip(flags, working_ports)]
    for thread in threads:
        thread.start()

    time.sleep(IDENTIFY_TIMEOUT)
    sensor_ports = [port for (flag, port) in zip(flags, working_ports) if flag.is_set()]
    for thread in threads:
        thread.join()
    return sensor_ports


def is_linebreak_sensor(sensor_msg):
    """Check whether a message is sent from a linebreak sensor."""
    # TODO: fill this in
    pass


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
    working_ports = get_working_serial_ports(set())
    linebreak_ports = identify_linebreak_sensors(working_ports)
    for port in linebreak_ports:
        sensor_thread = threading.Thread(target=transfer_linebreak_data, args=(port, ), daemon=True)
        sensor_thread.start()
    while True:
        time.sleep(100)

if __name__ == "__main__":
    main()
