

#
#   Connects REQ socket to tcp://IP_OF_BASE-STATION:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq

context = zmq.Context()
print("Connecting to server…")
socket = context.socket(zmq.REQ)

# We need to connect to the local ip address of the base station at a chosen port.
socket.connect("tcp://10.248.149.97:5005")

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print("Sending request %s …" % request)
    socket.send(b"Hello, I'm the Raspberry PI!")
    message = socket.recv()
    print("Response %s [ %s ]" % (request, message))
