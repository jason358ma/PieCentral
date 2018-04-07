# LCM

[LCM Build Instructions](https://lcm-proj.github.io/build_instructions.html)

This is a library of two functions for sending and receiving messages using the LCM communications protocol.

`lcm_start_read(receive_channel, queue, put_json=False)`
Takes in receiving channel name (string), queue (Python queue object).
Takes whether to add received items to queue as JSON or Python dict.
Creates thread that receives any message to receiving channel and adds
it to queue as tuple (header, dict).
header: string
dict: Python dictionary

