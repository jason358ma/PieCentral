import threading
import lcm

LCM_address = 'udpm://239.255.76.68:7667?ttl=2'
LCM_joiner = '|||'

def lcm_start_read(receive_channel, queue):
    '''
    Takes in receiving channel name (string), queue (Python queue object).
    Creates thread that receives any message to receiving channel and adds
    it to queue as tuple (header, dic).
    header: string
    dic: Python dictionary
    '''
    comm = lcm.LCM(LCM_address)

    def string_to_int(string):
        try:
            return int(string)
        except ValueError:
            return string

    def handler(_, item):
        msg = item.decode()
        msg_list = msg.split(LCM_joiner)
        dic = {}
        index = 1
        while index < len(msg_list) - 1:
            dic[string_to_int(msg_list[index])] = string_to_int(msg_list[index + 1])
            index += 2
        queue.put((msg_list[0], dic))

    comm.subscribe(receive_channel, handler)

    def run():
        while True:
            comm.handle()

    rec_thread = threading.Thread()
    rec_thread.run = run
    rec_thread.start()

def lcm_send(target_channel, header, dic):
    '''
    Send header (string) and dictionary to target channel (string)
    '''
    msg = str(header)
    for key, value in dic.items():
        msg = LCM_joiner.join([msg, str(key), str(value)])
    lcm.LCM(LCM_address).publish(target_channel, msg.encode())
