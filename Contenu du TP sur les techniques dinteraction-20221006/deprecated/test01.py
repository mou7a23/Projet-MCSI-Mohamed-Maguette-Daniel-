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
    print(u'{}: {}'.format(
        address.decode('utf8'),
        ', '.join(
            '{}'.format(
                v.decode(options.encoding or 'utf8')
                if isinstance(v, bytes)
                else v
            )
            for v in values if values
        )
    ))

# seuil = 0.3
def callback_x(*values):
    if values[0] < -0.3:
        data = b'P_LEFT'
        client_socket.sendto(data, address)
        data = b'R_RIGHT'
        client_socket.sendto(data, address)
    elif values[0] > 0.3:
        data = b'P_RIGHT'
        client_socket.sendto(data, address)
        data = b'R_LEFT'
        client_socket.sendto(data, address)
    else:
        data = b'R_LEFT'
        client_socket.sendto(data, address)
        data = b'R_RIGHT'
        client_socket.sendto(data, address)
    
def callback_y(*values):       
    if values[0] < - 0.3:
        data = b'P_ACCELERATE'
        client_socket.sendto(data, address)
        data = b'R_BRAKE'
        client_socket.sendto(data, address)
    elif values[0] > 0.3:
        data = b'R_ACCELERATE'
        client_socket.sendto(data, address)
        data = b'P_BRAKE'
        client_socket.sendto(data, address)
    else:
        data = b'R_ACCELERATE'
        client_socket.sendto(data, address)
        data = b'R_BRAKE'
        client_socket.sendto(data, address)

def callback_touch(values):
    if values == True:
        data = b'R_ACCELERATE'
        client_socket.sendto(data, address)
        data = b'R_BRAKE'
        client_socket.sendto(data, address)
        data = b'R_LEFT'
        client_socket.sendto(data, address)
        data = b'R_RIGHT'
        client_socket.sendto(data, address)

osc = OSCThreadServer(default_handler=dump)  # See sources for all the arguments

# You can also use an \*nix socket path here
sock = osc.listen(address='0.0.0.0', port=8000, default=True)

osc.bind(b'/multisense/pad/x', callback_x)
osc.bind(b'/multisense/pad/y', callback_y)
osc.bind(b'/multisense/pad/touchUP', callback_touch)




sleep(1000)
osc.stop()  # Stop the default socket