import cv2
import time

cap = cv2.VideoCapture(0)
prev_time = time.time()

while true:
    ret, frame = cap.read()
    if not ret:
        break

    cur_time = time.time()
    fps = 1.0 / (cur_time - prev_time) if cur_time != prev_time else 0
    prev_time = cur_time

    cv2.putText(frame, f'FPS: {fps:.1f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Webcam Feed', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()