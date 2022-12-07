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
seuil = 10   
release_right_left = True  

def dump(address, *values):
    pass
    """print(u'{}: {}'.format(
        address.decode('utf8'),
        ', '.join(
            '{}'.format(
                v.decode(options.encoding or 'utf8')
                if isinstance(v, bytes)
                else v
            )
            for v in values if values
        )
    ))"""

osc = OSCThreadServer(default_handler=dump)  # See sources for all the arguments

# You can also use an \*nix socket path here
sock = osc.listen(address='0.0.0.0', port=8001, default=True)

######################" CV 2"################################
import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return np.round(angle, 2)

def avancer_reculer(angle):
    global p_acc, r_acc, p_bra, r_bra           
    if angle > 120:
        if p_acc == False:
            data = b'P_ACCELERATE'
            client_socket.sendto(data, address)
            print("P_ACCELERATE")
        p_acc = True
        r_acc = False
        
    elif r_acc == False:
        data = b'R_ACCELERATE'
        client_socket.sendto(data, address)
        print("R_ACCELERATE")
        r_acc = True
        p_acc = False
    else:
        r_acc = True
        p_acc = False
    # Reculer
    if angle < 20:
        if p_bra == False:
            data = b'P_BRAKE'
            client_socket.sendto(data, address)
            print("P_BRAKE")
        r_bra = False
        p_bra = True
    elif r_bra == False:
        data = b'R_BRAKE'
        client_socket.sendto(data, address)
        print("R_BRAKE")
        r_bra = True
        p_bra = False
    else:
        r_bra = True
        p_bra = False

cap = cv2.VideoCapture(1)

# make sure the button is not released
r_acc = False
r_bra = False
# make sure the button is not pressed
p_acc = False
p_bra = False


## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates 
            # 1- left hand
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            # 1- right hand
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            # Calculate angle
            left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            angle = left_angle
            # Visualize angles
            cv2.putText(image, str(left_angle), 
                           tuple(np.multiply(left_elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            cv2.putText(image, str(right_angle), 
                           tuple(np.multiply(right_elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            
            #avancer_reculer(angle)
                       
        except:
            pass
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)
        avancer_reculer(angle)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            data = b'R_BRAKE'
            client_socket.sendto(data, address)
            data = b'R_ACCELERATE'
            client_socket.sendto(data, address)
            break

    cap.release()
    cv2.destroyAllWindows()
    
#############################################################

sleep(1000)
osc.stop()  # Stop tault socke