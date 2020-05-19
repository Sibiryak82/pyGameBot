import numpy as np
from PIL import ImageGrab
import cv2
from pynput.keyboard import Key, Controller
import time
from random import randint
from time import sleep

keyboard = Controller()

while (True):
    # cap = np.array(ImageGrab.grab()) #capture full desktop
    cap = np.array(ImageGrab.grab(bbox=(0, 40, 800, 600)))  # Game Capture (window size)
    gray = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY) #Convert to gray

    template = cv2.imread('./images/fishing.png', 0) #define template
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(gray, template, cv2.TM_SQDIFF) #define type of template recognition
    threshold = 0.8 #set threshold
    loc = np.where(res >= threshold)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) #calculate values

    top_left = min_loc #define rectangle area
    bottom_right = (top_left[0] + w, top_left[1] + h)
    if min_val < 720000000.0: #this is to determine the threshold, I figured this out by adding print(min_val) in the loop and seeing what numbers it printed when it was recognized
        cv2.rectangle(cap, top_left, bottom_right, 255, 1) #draw rectangle
        cv2.putText(cap, 'Fish Hook', (top_left[0], top_left[1] - 10),
                    cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255))
        print("Hook Detected!")
        keyboard.press('e')
        keyboard.release('e')
        sleeptime = randint(1.0,5.0)
        print("Sleeping for " + str(sleeptime) + " seconds.")
        time.sleep(sleeptime)
        print("Recasting")
        keyboard.press('e')
        keyboard.release('e')
        #print(min_val)
    # cv2.rectangle(cap, top_left, bottom_right, 255, 1)
    # cv2.putText(cap, 'Fish Hook', (top_left[0], top_left[1] - 10),
    #     cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255))

    cv2.imshow('Test', cap) #show window

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()