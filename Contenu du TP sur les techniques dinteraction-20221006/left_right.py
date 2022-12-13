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
        
    return angle 


cap = cv2.VideoCapture(0)

# Curl counter variables
counter = 0
r_counter = 0
stage = None
r_stage = None

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
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            # 1- right hand
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            # Calculate angle
            left_angle = calculate_angle(left_wrist, left_shoulder, left_hip)
            right_angle = calculate_angle(right_wrist,right_shoulder, right_hip )
            angle = left_angle
            # Visualize angles
            cv2.putText(image, str(left_angle), 
                           tuple(np.multiply(left_shoulder, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            cv2.putText(image, str(right_angle), 
                           tuple(np.multiply(right_shoulder, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            ## 
            # Reculer            
            if left_angle >80:
                stage="gauche"
                if p_bra == False:
                    data = b'P_LEFT'
                    client_socket.sendto(data, address)
                    print("LEFT")
                    p_bra = True
                r_bra = False
            elif r_bra == False:
                # stage="up"
                data = b'R_LEFT'
                client_socket.sendto(data, address)
                print("R_LEFT")
                r_bra = True
            else:
                p_bra = False
            # Avancer
            if right_angle > 80:
                stage="droite"
                if p_bra == False:
                    data = b'P_RIGHT'
                    client_socket.sendto(data, address)
                    print("DROITE")
                    p_acc = True
                r_acc = False
            elif r_acc == False:
                # stage="up"
                data = b'R_RIGHT'
                client_socket.sendto(data, address)
                print("DROITE")
                r_acc = True
            else:
                p_acc = False
                     
            # if angle > 120: # and stage == "up":
            #     stage = "down"
            #     if p_acc == False:
            #         data = b'P_ACCELERATE'
            #         client_socket.sendto(data, address)
            #         print("P_ACCELERATE")
            #         p_acc == True
            #     r_acc = False
            # elif r_acc == False:
            #     data = b'R_ACCELERATE'
            #     client_socket.sendto(data, address)
            #     print("R_ACCELERATE")
            #     r_acc = True
            # else:
            #     p_acc = False
            
            
            # Curl counter logic right hand
            # if right_angle > 120 and stage == "up":
            #     r_stage = "down"
            #     data = b'P_ACCELERATE'
            #     client_socket.sendto(data, address)
            # if right_angle < 30 and stage =='down':
            #     r_stage="up"
            #     data = b'R_ACCELARATE'
            #     client_socket.sendto(data, address)
            #     r_counter +=1
            #     print("right counter:", r_counter)
                       
        except:
            pass
        
        # Render curl counter
        # Setup status box
        cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        cv2.rectangle(image, (500,0), (640,73), (16,117,245), -1)
        # Rep data
        cv2.putText(image, 'REPS', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), 
                    (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Stage data
        cv2.putText(image, 'STAGE', (65,12), 

                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, stage, 
                    (60,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        # Stage data
        cv2.putText(image, 'STAGE', (65,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, r_stage, 
                    (60,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
#############################################################

sleep(1000)
osc.stop()  # Stop tault socke