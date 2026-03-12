import cv2
import time
import datetime

# Variables to track blinking frequency
blink_counter = 0
blink_start_time = None

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    frame = cv2.flip(frame,1)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    currentDate = str(datetime.datetime.now())
    
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in eyes:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Measure the time duration between consecutive blinks
    if len(eyes) == 0:
        if blink_start_time is None:
            blink_start_time = time.time()
        else:
            if time.time() - blink_start_time > 0.3:
                blink_counter += 1
                blink_start_time = None
    else:
        blink_start_time = None
    
    # In case of drowsiness, inform the driver.
    if blink_counter >= 5:
        blink_counter = 0
    
    # Display the frame with eye rectangles and blinking frequency
    cv2.putText(frame, f"Blinks: {blink_counter}", (10, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame,currentDate,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,0),1)
    cv2.imshow('Drowsiness Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()