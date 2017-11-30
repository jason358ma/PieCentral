import time
import queue
import LCM

q = queue.Queue()
dummy = LCM.LCMClass(q, 'Channel')

# start receiving thread
dummy.lcm_start_read()

# testing LCMClass.send_message
LCM.lcm_send('Channel', 'header', 'List', 'of', 'items', 2, 3, 4)
LCM.lcm_send('Channel', 'header1', 'a', 'b', 'c', 1, 5)
LCM.lcm_send('Channel', 'header2', 3, [1, 2])
LCM.lcm_send('Channel', 'header3', 'testing_delay', 1)

while True:
    item = q.get()
    if item is None:
        pass
    else:
        print(item)
        time.sleep(5)