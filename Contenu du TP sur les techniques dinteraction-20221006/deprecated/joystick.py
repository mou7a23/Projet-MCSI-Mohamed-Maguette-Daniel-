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
touch_up = True
X0 = 0
Y0 = 0
seuil = 0.2
def dump(address, *values):
    global X0, Y0, touch_up, seuil
    if(address == b'/multisense/pad/touchUP'):
        touch_up = True
        X0 = 0
        Y0 = 0
    else:
        touch_up = False
    if address == b'/multisense/pad/x' and X0 == 0 and touch_up == False:
        X0 = values[0]
    if address == b'/multisense/pad/y' and Y0 == 0 and touch_up == False:
        Y0 = values[0]

def callback_x(*values):
    global X0
    #print("X0 =", X0, "X =",values[0], "X - X0 =", values[0]-X0)
    dx = values[0]-X0
    if dx > seuil:
        data = b'R_RIGHT'
        client_socket.sendto(data, address)
        data = b'P_LEFT'
        client_socket.sendto(data, address)
        print("dx =", dx)
        print("TO THE RIGHT")
    elif dx < -1 * seuil:
        data = b'P_RIGHT'
        client_socket.sendto(data, address)
        data = b'R_LEFT'
        client_socket.sendto(data, address)
        print("dx =", dx)
        print("TO THE LEFT")
    
def callback_y(*values):
    global Y0
    #print("Y0 =", Y0, "Y =",values[0],"Y - Y0 = ", values[0]-Y0
    dy = values[0]-Y0
    if dy > seuil:
        data = b'P_ACCELERATE'
        client_socket.sendto(data, address)
        data = b'R_BRAKE'
        client_socket.sendto(data, address)
        print("dy =", dy)
        print("ACCELERATE")
    elif dy < -1 * seuil:
        data = b'R_ACCELERATE'
        client_socket.sendto(data, address)
        data = b'P_BRAKE'
        client_socket.sendto(data, address)
        print("dy =", dy)
        print("BRAKE")
    
def callback_touch(values):
    global X0, Y0
    if values == True:
        data = b'R_ACCELERATE'
        client_socket.sendto(data, address)
        data = b'R_BRAKE'
        client_socket.sendto(data, address)
        data = b'R_LEFT'
        client_socket.sendto(data, address)
        data = b'R_RIGHT'
        client_socket.sendto(data, address)
        X0 = 0
        Y0 = 0
       
osc = OSCThreadServer(default_handler=dump)  # See sources for all the arguments

# You can also use an \*nix socket path here
sock = osc.listen(address='0.0.0.0', port=8000, default=True)

osc.bind(b'/multisense/pad/x', callback_x)
osc.bind(b'/multisense/pad/y', callback_y)
osc.bind(b'/multisense/pad/touchUP', callback_touch)

sleep(1000)
osc.stop()  # Stop the default socket