import cv2
cap = cv2.VideoCapture(0)
cascade_classifier = cv2.CascadeClassifier( 'haarcascades/haarcascade_frontalface_default.xml' )

while True:
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, 0)

    detectons = cascade_classifier.detectMultiScale(frame)

    if(len(detectons) > 1):
        cv2.imshow('frame', frame)
        cv2.waitKey(1)