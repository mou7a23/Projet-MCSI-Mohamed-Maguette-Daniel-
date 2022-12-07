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
seuil = 20   
release_right_left = True  

def dump(address, *values):
    pass  
    # print(u'{}: {}'.format(
    #     address.decode('utf8'),
    #      ', '.join(
    #         '{}'.format(
    #             v.decode(options.encoding or 'utf8')
    #             if isinstance(v, bytes)
    #             else v
    #         )
    #         for v in values if values
    #     )
    # )) 

 
def right_left_pitch(*values): # pour aller à droite et à gauche
    global seuil
    global release_right_left     
    if values[0] < -1 * seuil:# and values[0] > -3 * seuil:
        data = b'P_RIGHT'
        client_socket.sendto(data, address)
        release_right_left = False
        print("RIGHT")
        # wait = -0.01 * values[0] / 90
        # sleep(wait)
        # data = b'R_RIGHT'
        # client_socket.sendto(data, address)
        # release_right_left = True
        # print("RELEASE", wait)
        # sleep(0.01 - wait)
        
    elif values[0] > seuil:# and values[0] < 3 * seuil: 
        data = b'P_LEFT'
        client_socket.sendto(data, address)
        release_right_left = False
        print("LEFT")
        # wait = 0.01 * values[0] / 90
        # sleep(wait)
        # data = b'R_LEFT'
        # client_socket.sendto(data, address)
        # release_right_left = True
        # print("RELEASE", wait)
        # sleep(0.01 - wait)
    else:
        if release_right_left == False:
            data = b'R_RIGHT'
            client_socket.sendto(data, address)
            data = b'R_LEFT'
            client_socket.sendto(data, address)
            print("RELEASE")
            release_right_left = True

def rescue_touch(values):
    if values == True:
        print("RESCUE")
        data = b'P_RESCUE'
        client_socket.sendto(data, address)
        sleep(0.1)
        data = b'R_RESCUE'
        client_socket.sendto(data, address)

def fire(values):
    if values == 0.0:
        data = b'P_NITRO'
        client_socket.sendto(data, address)
        sleep(0.1)
        data = b'R_NITRO'
        client_socket.sendto(data, address)
        print("NITRO")
osc = OSCThreadServer(default_handler=dump)  # See sources for all the arguments

osc = OSCThreadServer(default_handler=dump)  # See sources for all the arguments

# You can also use an \*nix socket path here
sock = osc.listen(address='0.0.0.0', port=8000, default=True)

osc.bind(b'/multisense/orientation/yaw', right_left_pitch)
osc.bind(b'/multisense/pad/touchUP', rescue_touch)
osc.bind(b'/multisense/proximity/x', fire )



sleep(1000)
osc.stop()  # Stop tault socke