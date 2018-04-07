# [LCM](https://lcm-proj.github.io/)

[LCM Build Instructions](https://lcm-proj.github.io/build_instructions.html) (Linux or Mac OS recommended)

Make sure to run setup.py (or the setup script for the language you are using).

LCM uses UDP multicast to exchange messages, and can be used for to send byte representations of various objects and user-defined data types. There are [tutorials](https://lcm-proj.github.io/tutorial_general.html) for defining these data types in various languages.


## Functions
This is a library of two functions for sending and receiving messages using the LCM communications protocol. 

<br>

`lcm_start_read(receive_channel, queue, put_json=False):`

Takes in receiving channel name (string), queue (Python queue object).
and whether to add received items to queue as JSON or Python dict.
Creates thread that receives any message to receiving channel and adds
it to queue as tuple (header, dict).
header: string
dict: Python dictionary

<br>

`lcm_send(target_channel, header, dic={}):`

Send header (any type) and dic (Python dictionary) to target channel (string).