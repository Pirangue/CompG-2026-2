import cv2
#Função VideoCapture

cap = cv2.VideoCapture("videos\dog.mp4")

while (True):
    ret, frame =  cap.read()

    cv2.imshow("Video do dog", frame)

    # waitkey para videos
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
    #215 assercion failed

cap.release()
cv2.destroyAllWindows()