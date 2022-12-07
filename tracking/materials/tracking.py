######################################################################################
# This python script implements a 3D face tracking which uses a webcam               #
# to achieve face detection. This face detection is done with the opencv             #
# face detection algorithm based on Haar Feature-based Cascade Classifiers:          #
# https://docs.opencv.org/master/db/d28/tutorial_cascade_classifier.html             #
# https://docs.opencv.org/2.4.13.7/modules/objdetect/doc/cascade_classification.html #
#                                                                                    #
# The script then streams the 3D position through OSC and can be used to do          #
# adptative viewing with motion parallax in Unity.                                   #
#                                                                                    #
# date: December 2019                                                                #
# authors: Cedric Fleury                                                             #
# affiliation: Polytech Paris-Sud / LRI, Universite Paris-Saclay & Inria             #         
#                                                                                    #
# usage: python tracking.py x                                                        #
# where x is an optional value to tune the interpupillary distance of the            #
# tracked subject (by default, the interpupillary distance is set at 6cm).           #                                                                      #
######################################################################################

# import necessary modules
import sys
import time
from math import *

# import opencv for image processing
import cv2

# import oscpy for OSC streaming (https://pypi.org/project/ocspy/)
from oscpy.client import OSCClient

### Part 1 ###
# load the trained XML classifiers for face and eyes
# these XML files can be downloaded at the following address:
# https://github.com/opencv/opencv/tree/master/data
face_cascade = cv2.CascadeClassifier( 'haarcascades/haarcascade_frontalface_default.xml' )

### Part 2 ###
#eye_cascade = cv2.CascadeClassifier( ... )

### Part 3 ###
# define the camera focal length in pixels
# Use the calbirate.py script to determine it!
fl = 0

### Part 4 ###
# define the default interpupillary distance
user_ipd = 0

### Part 4 ###
# define the height of the screen
screen_heigth = 0


# Set interpupillary distance from the command parameter
if len(sys.argv) >= 2:
	user_ipd = sys.argv[1]

print("Tracking initialized with an interpupillary distance of " + str(user_ipd) + " cm")

# capture frames from a camera
cap = cv2.VideoCapture(0) 

# get image size
frame_width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print("Video size: " + str(frame_width) + " x " + str(frame_height))

# define address and port for streaming
address = "127.0.0.1"
port = 7000

clientOSC = OSCClient(address, port)
print("OSC connection established to " + address + " on port " + str(port) + "!")


################################## Exceptions #################################

class TrackingFailedException(Exception):
	"""Tracking Failed!"""
	pass


############################# Tracking fonction ###############################

# return the position in-between the two eyes 
# and the interpupillary distance in pixels
def trackBiggestFace(img):

	# Initialize the position in-between the two eyes
	ibe_x = 0
	ibe_y = 0
	ipd = 0
	
	### Part 1 ###
	# detect the faces of different sizes in the frame
	faces = ...

	# if we detect at least one face
	if len(faces) > 0:
		# keep the biggest face
	  
	 	### Part 2 ###
		# detects the eyes in the biggest face
		# eyes = ... 			

		# if we detect at least two eyes
		# if len(eyes) >= 2:

			# keep the two largest eyes
			
			# compute the position between the two eyes
			# compute the interpupillary distance (in pixels)

		# else:

			### Part 1 ###
			# estimate the position between the two eyes
			# estimate the interpupillary distance (in pixels)


	else: raise TrackingFailedException

	return (ibe_x, ibe_y, ipd)

########################## 3D computation fonction ##########################

# convert the 2 position in pixels in the image to 
# a 3D position in cm in the camera reference frame
def compute3DPos(ibe_x, ibe_y, ipd):
	
	### Part 4 ###
	# compute the distance z between the head and the camera
	z = 0

	# compute the x and y coordinate in a Yup reference frame
	x = 0
	y = 0

	# center the reference frame on the center of the screen
	# (and not on the camera)
	
	return (x, y, z)



################################ main fonction ##############################
	
def runtracking():

	print ("\nTracking started !!!")
	print ("Hit ESC key to quit...")
	
	# infinite loop for processing the video stream
	while True:
		
		# add to delay to avoid that the loop run too fast
		time.sleep(0.02)

		# read one frame from a camera 
		ret, img = cap.read()  
		
		# get the position of the biggest face
		try:
			x, y, d = trackBiggestFace(img)

			# draw the point between the two eyes and the interpupillar distance
			# cv2.circle(img, (x,y), 5, (0,0,255), -1)
			# cv2.line(img, (int(x-d/2),y), (int(x+d/2),y), (0,255,0), 2)

			# compute the 3D position in the camera reference frame
			# pos_x, pos_y, pos_z = compute3DPos(x, y, d)

			# Stream the values on OCS
			# clientOSC.send_message(b'/tracker/head/pos_xyz', [... , ... , ...])

		except TrackingFailedException:
			print(TrackingFailedException.__doc__)
  
		# Display an image in a window 
		cv2.imshow('img', img) 
  
		# Wait for Esc key to stop 
		k = cv2.waitKey(30) & 0xff
		if k == 27: 
	   		break
  
	# release the video stream from the camera
	cap.release()
	  
	# close the associated window 
	cv2.destroyAllWindows() 


############################ program execution #############################
			
runtracking()
 
