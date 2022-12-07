######################################################################################
# Determine the focal length of a webcam in pixels by displaying in front of the     #
# cameraa marker for which the size is known. The marker must be placed at a fix     #
# distance from the camera.                                                          #
#                                                                                    #
# date: December 2019                                                                #
# authors: Cedric Fleury                                                             #
# affiliation: Polytech Paris-Sud / LRI, Universite Paris-Saclay & Inria             #         
#                                                                                    #
# usage: python calibrate.py w h d                                                   #
#        where w is the width of the calibration marker in cm                        #
#              h is the height of the calibration marker in cm                       #
#              d is the distance between the calibration marker and the camera in cm #
#                                                                                    #
# Then, you need to press space to stop the video and select the marker in the       #
# image with the mouse, and press space again. Focal length values in pixels will be #
# displayed in the console. The process can be repeated several time.                #
# Hit ESC key to quit.                                                               #
######################################################################################

# import necessary modules
import sys

# import opencv for image processing
import cv2

marker_width = 0
marker_height = 0
marker_dist = 0

if len(sys.argv) >= 3:
	marker_width = float(sys.argv[1])
	marker_height = float(sys.argv[2])
	marker_dist = float(sys.argv[3])
else:
	print("ERROR: invalid parameters!")
	print("Usage: python calibrate.py w h d")
	print("       where w - width of the marker (cm)")
	print("             h - height of the marker (cm)")
	print("             d - distance between the marker and the camera (cm)")
	sys.exit()

print("Press space to stop the video, select the marker with the mouse and press space again.")
print("Focal length values in pixels will be displayed in the console.")
print("The process can be repeated several time.")
print("Hit ESC key to quit...\n")

# capture frames from a camera 
cap = cv2.VideoCapture(0) 

# infinite loop for processing the video stream
while True:

	# read one frame from a camera 
	ret, img = cap.read() 

	# Display an image in a window 
	cv2.imshow('img', img) 

	k = cv2.waitKey(30) & 0xff
	if k == 32: 
		marker = cv2.selectROI("img", img, fromCenter=False, showCrosshair=True)
		width_pix = marker[2]
		height_pix = marker[3]
		hf = (width_pix * marker_dist ) / marker_width
		vf = (height_pix * marker_dist ) / marker_height
		print("=> Horizontal focal length: " + "{:.2f}".format(hf) + " pixels - Vertical focal length: " + "{:.2f}".format(vf))

	if k == 27: 
		break

# release the video stream from the camera
cap.release()
	  
# close the associated window 
cv2.destroyAllWindows() 