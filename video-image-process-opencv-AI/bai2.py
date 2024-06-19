import cv2
import imutils
#xoay camera
rotate = 0
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if rotate != 0:
        frame = imutils.rotate(frame,rotate)
    cv2.imshow("show",frame)
    key = cv2.waitKey(1)
    if (key == ord('q')):
        break
    elif (key == ord('a')):
        rotate = 90
    elif (key == ord('s')):
        rotate = 0
    elif (key == ord('d')):
        rotate = -90
    elif (key == ord('w')):
        rotate = -180
cap.release()
cv2.destroyAllWindows()