import cv2
import numpy as np
import smbus
import RPi.GPIO as GPIO
import time
import datetime

# Initialize LCD
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1
lcd_address = 0x27
lcd_cols = 16

# Initialize buzzer
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
buzzer_pin = 11
GPIO.setup(buzzer_pin, GPIO.OUT)

# Variables to track blinking frequency
blink_counter = 0
blink_start_time = None

start_time = None
alert_duration = 3  # Alert if phone is held for 5 seconds

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
phone_cascade = cv2.CascadeClassifier('myhaar3.xml')

def lcd_init():
    lcd_byte(0x33, 0x00)
    lcd_byte(0x32, 0x00)
    lcd_byte(0x06, 0x00)
    lcd_byte(0x0C, 0x00)
    lcd_byte(0x28, 0x00)
    lcd_byte(0x01, 0x00)
    time.sleep(0.005)

def lcd_byte(bits, mode):
    # Send byte to data pins
    bits_high = mode | (bits & 0xF0) | 0x08
    bits_low = mode | ((bits << 4) & 0xF0) | 0x08
    # High bits
    bus.write_byte(lcd_address, bits_high)
    lcd_toggle_enable(bits_high)
    # Low bits
    bus.write_byte(lcd_address, bits_low)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    time.sleep(0.0005)
    bus.write_byte(lcd_address, (bits | 0x04))
    time.sleep(0.0005)
    bus.write_byte(lcd_address, (bits & ~0x04))
    time.sleep(0.0005)
    

def lcd_string(message, line):
    if line == 1:
        lcd_byte(0x80, 0)
    elif line == 2:
        lcd_byte(0xC0, 0)
    message = message.ljust(lcd_cols, " ")
    for i in range(lcd_cols):
        lcd_byte(ord(message[i]), 0x01)


#lane_lines_detection
def region_of_interest(frame2, vertices):
    mask = np.zeros_like(frame2)
    cv2.fillPoly(mask, vertices, 255)
    masked_img = cv2.bitwise_and(frame2, mask)
    return masked_img

def draw_lines(frame2, lines, color=[255, 0, 0], thickness=3):
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(frame2, (x1, y1), (x2, y2), color, thickness)

def detect_lanes(frame2):
    global left_lane_count, right_lane_count
    gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    edges = cv2.Canny(blur, 50, 150)

    # Define a region of interest
    height, width = edges.shape
    vertices = np.array([[(0, height), (width / 2, height / 2), (width, height)]], dtype=np.int32)
    masked_edges = region_of_interest(edges, vertices)

    # Detect lines using Hough transform
    lines = cv2.HoughLinesP(masked_edges, rho=3, theta=np.pi/180, threshold=100, minLineLength=50, maxLineGap=50)

    # Draw lines on the original image
    line_image = np.zeros_like(frame2)
    if lines is not None:
        draw_lines(line_image, lines)
        
        # Check for lane deviation
        left_lane_count = 0
        right_lane_count = 0
        for line in lines:
            for x1, y1, x2, y2 in line:
                slope = (y2 - y1) / (x2 - x1)
                if slope > 0.5:
                    right_lane_count += 1
                elif slope < -0.5:
                    left_lane_count += 1

    # Combine the line image with the original image
    result = cv2.addWeighted(frame2, 0.8, line_image, 1, 0)

    # Check for lane deviation
    if left_lane_count >= 3 and right_lane_count >= 3:
        deviation_detected = True
    else:
        deviation_detected = False
    
    return result, deviation_detected


def detect_eyes(frame):
    global blink_counter, blink_start_time
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect eyes in the frame
    eyes = eye_cascade.detectMultiScale(gray, 1.1, 5)
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
        return True

def detect_phone(frame):
    global start_time
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect phones in the frame
    phone = phone_cascade.detectMultiScale(gray,3.6,50)
    for (ex,ey,ew,eh) in phone:
        cv2.rectangle(frame,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)
    # If phones are detected, produce an alert
    if len(phone) !=0:
        if start_time is None:
            start_time = time.time()
        else:
            # Check if the duration exceeds the alert duration
            if time.time() - start_time >= alert_duration:
                start_time = None  # Reset the timer after alert
                return True
    else:
        # Reset the timer if no phones are detected
        start_time = None

def main():
    cap = cv2.VideoCapture('object2_2.mp4')
    cap2 = cv2.VideoCapture('lane1_3.mp4')

    while True:
        ret, frame = cap.read()
        ret2, frame2 = cap2.read()

        if not ret or ret2 is None:
            break

        # Detect lanes
        result, deviation_detected = detect_lanes(frame2)
        
        #frame = cv2.flip(frame,1)

        currentDate = str(datetime.datetime.now())
        
        conditions_met = 0

        # Detect eyes and phone usage on the first camera feed
        if detect_eyes(frame) or detect_phone(frame):
            conditions_met += 1

        # Detect lane departure on the second camera feed
        if deviation_detected:
            conditions_met += 1

        # If at least two conditions are met, trigger alert mechanism
        if conditions_met >= 2:
            lcd_init()
            lcd_string("Warning!!", 1)
            lcd_string("Condition Detect", 2)
            GPIO.output(buzzer_pin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(buzzer_pin, GPIO.LOW)
            print("Warning!!")
        
        # Display the frame with eye rectangles and blinking frequency
        cv2.putText(frame, f"Blinks: {blink_counter}", (10, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame,currentDate,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
        cv2.imshow('Eyes and Phone Detection', frame)
        # Display the resulting frame
        cv2.imshow('Lane Detection', result)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cap2.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()

if __name__ == "__main__":
    main()
