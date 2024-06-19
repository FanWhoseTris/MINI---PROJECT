import cv2
camera = 0
cap = cv2.VideoCapture(camera)
while True:
    ret,frame = cap.read()
    cv2.imshow("door",frame)
    key = cv2.waitKey(1)
    if (key == ord('q')):
        break
cap.release()
cv2.destroyAllWindows()
