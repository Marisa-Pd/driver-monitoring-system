#phone detector
import cv2
import time

cap = cv2.VideoCapture(0)

phone_cascade = cv2.CascadeClassifier('myhaar.xml')

start_time = None
alert_duration = 5  # Alert if phone is held for 10 seconds

while True:
    ret, frame = cap.read()

    frame = cv2.flip(frame,1)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    phone = phone_cascade.detectMultiScale(gray,2.3,30)

    for (ex,ey,ew,eh) in phone:
        cv2.rectangle(frame,(ex,ey),(ex+ew,ey+eh),(255,0,0),thickness=5)


    # If phones are detected, produce an alert
    if len(phone) !=0:
        if start_time is None:
            start_time = time.time()
        else:
            # Check if the duration exceeds the alert duration
            if time.time() - start_time >= alert_duration:
                print("Phone has been held for 5 seconds! Alert!")
                # Reset the timer after alert
                start_time = None
    else:
        # Reset the timer if no phones are detected
        start_time = None

    cv2.imshow("Output",frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
