import cv2
import numpy as np
import time

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked_img = cv2.bitwise_and(img, mask)
    return masked_img

def draw_lines(img, lines, color=[255, 0, 0], thickness=3):
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def detect_lanes(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    edges = cv2.Canny(blur, 50, 150)

    # Define a region of interest
    height, width = edges.shape
    vertices = np.array([[(0, height), (width / 2, height / 2), (width, height)]], dtype=np.int32)
    masked_edges = region_of_interest(edges, vertices)

    # Detect lines using Hough transform
    lines = cv2.HoughLinesP(masked_edges, rho=2, theta=np.pi/180, threshold=100, minLineLength=50, maxLineGap=50)

    # Draw lines on the original image
    line_image = np.zeros_like(img)
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
        
        # Alert if lane deviation is detected
        if left_lane_count == 6:
            print("Watch out!")
        elif right_lane_count == 6:
            print("Watch out!")
            #print("Watch out! Vehicle crossing into the left lane")


    # Combine the line image with the original image
    result = cv2.addWeighted(img, 0.8, line_image, 1, 0)

    return result

# Read input video
cap = cv2.VideoCapture('Lane-Detection-Test-Video02.mp4')

while cap.isOpened():
    ret, frame = cap.read()

    if not ret or frame is None:
        break

    resize = cv2.resize(frame, (640,480))

    # Detect lanes
    result = detect_lanes(resize)

    # Display the resulting frame
    cv2.imshow('Lane Detection', result)

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    delay = int(200 / fps)
    if delay < 1: 
        delay = 1
    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()