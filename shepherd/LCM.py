import threading
import json
import lcm

LCM_address = 'udpm://239.255.76.68:7667?ttl=2'

def lcm_start_read(receive_channel, queue):
    '''
    Takes in receiving channel name (string), queue (Python queue object).
    Creates thread that receives any message to receiving channel and adds
    it to queue as tuple (header, dict).
    header: string
    dict: JSON dictionary
    '''
    comm = lcm.LCM(LCM_address)

    def handler(_, item):
        dic = json.loads(item.decode())
        header = dic.pop('header')
        queue.put((header, dic))

    comm.subscribe(receive_channel, handler)

    def run():
        while True:
            comm.handle()

    rec_thread = threading.Thread()
    rec_thread.run = run
    rec_thread.start()

def lcm_send(target_channel, header, dic):
    '''
    Send header and dictionary to target channel (string)
    '''
    dic['header'] = header
    json_str = json.dumps(dic)
    lcm.LCM(LCM_address).publish(target_channel, json_str.encode())
