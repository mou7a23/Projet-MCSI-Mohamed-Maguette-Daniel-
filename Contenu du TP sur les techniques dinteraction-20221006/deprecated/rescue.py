from oscpy.server import OSCThreadServer
from time import sleep
##############
## Global libs
import socket
import sys
import select
from time import sleep

address = ('localhost', 6006)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def dump(address, *values):
    pass

def callback_touch(values):
    if values == True:
        print("RESCUE")
        data = b'P_RESCUE'
        client_socket.sendto(data, address)
        sleep(0.1)
        data = b'R_RESCUE'
        client_socket.sendto(data, address)
osc = OSCThreadServer(default_handler=dump)  # See sources for all the arguments

# You can also use an \*nix socket path here
sock = osc.listen(address='0.0.0.0', port=8000, default=True)

osc.bind(b'/multisense/pad/touchUP', callback_touch)

sleep(1000)
osc.stop()  # Stop the default socket