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
    # print(u'{}: {}'.format(
    #     address.decode('utf8'),
    #     ', '.join(
    #         '{}'.format(
    #             v.decode(options.encoding or 'utf8')
    #             if isinstance(v, bytes)
    #             else v
    #         )
    #         for v in values if values
    #     )
    # ))

seuil = 10   
    
def callback_y(*values):
    global seuil       
    if values[0] < -1 * seuil:
        data = b'P_RIGHT'
        client_socket.sendto(data, address)
        data = b'R_LEFT'
        client_socket.sendto(data, address)
    elif values[0] > seuil:
        data = b'R_RIGHT'
        client_socket.sendto(data, address)
        data = b'P_LEFT'
        client_socket.sendto(data, address)
    else:
        data = b'R_RIGHT'
        client_socket.sendto(data, address)
        data = b'R_LEFT'
        client_socket.sendto(data, address)

osc = OSCThreadServer(default_handler=dump)  # See sources for all the arguments

# You can also use an \*nix socket path here
sock = osc.listen(address='0.0.0.0', port=8000, default=True)

osc.bind(b'/multisense/orientation/pitch', callback_y)




sleep(1000)
osc.stop()  # Stop the default socket