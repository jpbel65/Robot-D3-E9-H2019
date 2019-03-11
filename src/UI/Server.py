

#
#   Binds REP socket to tcp://*:5005
#

import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5005")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)
    time.sleep(5)
    socket.send(b"World")
