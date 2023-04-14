# Author: Endri Dibra

# importing the required libraries
import math
import numpy as np
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector


# getting camera of the device
# and making some changes
camera = cv2.VideoCapture(0)
camera.set(3, 1280)
camera.set(4, 720)

# creating an object for hand detection operations
detector = HandDetector(detectionCon=0.8, maxHands=1)

# x is the raw distance
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]

# y is distance at cm
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

# creating a polynomial function
coeff = np.polyfit(x, y, 2)

while True:

    # reading the output of camera
    success, img = camera.read()

    # getting hand on the screen
    hand, img = detector.findHands(img)

    # working only if hand is detected
    if hand:

        lmlist = tuple(hand[0]['lmList'])
        x, y, w, h = hand[0]['bbox']

        # getting points from hands
        x1, y1 = lmlist[5]
        x2, y2 = lmlist[17]

        # calculating the distance
        distance = int(math.sqrt((y2-y1)**2 + (x2-x1)**2))

        # getting the coefficients and calculating distance in cm
        A, B, C = coeff
        distanceCM = A*distance**2 + B*distance + C

        # displaying output on screen
        cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x+80, y-10))

    cv2.imshow("Image", img)
    cv2.waitKey(1)