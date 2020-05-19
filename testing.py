from tkinter import *
import numpy as np
from PIL import ImageGrab
import cv2
import time
import random
import keyboard


#ykeyboard = Controller()
print("Initial Listening")
img = ImageGrab.grab()
size = img.size
x1 = size[0] / 2 - 300;
y1 = size[1] / 2 - 300
x2 = x1 + 700;
y2 = y1 + 700  # these values needs to be double the values above to hit the center of screen. Offset using these
portion = img.crop((x1, y1, x2, y2))

class FishLoop():
    def __init__(self, root):
        self.running = True
        self.aboutToQuit = False
        self.root = root
        self.someVar = 0
        self.root.bind("<space>", self.switch)
        self.root.bind("<Escape>", self.exit)

        while not self.aboutToQuit:
            self.root.update() # always process new events

            if self.running:
                # cap = np.array(ImageGrab.grab()) #capture full desktop
                cap = np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2)))  # Game Capture (window size)
                gray = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)  # Convert to gray

                template = cv2.imread('./images/fishing.png', 0)  # define template
                w, h = template.shape[::-1]

                res = cv2.matchTemplate(gray, template, cv2.TM_SQDIFF_NORMED)  # define type of template recognition
                threshold = 0.675  # set threshold
                loc = np.where(res >= threshold)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # calculate values

                top_left = min_loc  # define rectangle area
                bottom_right = (top_left[0] + w, top_left[1] + h)
                if min_val < threshold:  # this is to determine the threshold, I figured this out by adding print(min_val) in the loop and seeing what numbers it printed when it was recognized
                    cv2.rectangle(cap, top_left, bottom_right, 255, 1)  # draw rectangle
                    cv2.putText(cap, 'Fish Hook', (top_left[0], top_left[1] - 10),
                                cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255))

                    print("Hook Detected! Threshold: " + str(min_val))
                    reelpause = round(random.uniform(0, 2), 3)
                    print("Reeling in " + str(reelpause) + " seconds")
                    time.sleep(reelpause)
                    keyboard.press('e')
                    keyboard.release('e')
                    sleeptime = round(random.uniform(1, 5), 3)
                    print("Sleeping for " + str(sleeptime) + " seconds.")
                    time.sleep(sleeptime)
                    print("Recasting")
                    print("Waiting for bite...")
                    keyboard.press('e')
                    keyboard.release('e')
                    # print(min_val)

                #cv2.imshow('Test', cap)  # show window

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                # cap.release()
                cv2.destroyAllWindows()
                    # self.someVar += 1
                    # print(self.someVar)
                    # time.sleep(.1)

            else: # If paused, don't do anything
                time.sleep(.1)

    def switch(self, event):
        print(['Unpausing','Pausing'][self.running])
        self.running = not(self.running)

    def exit(self, event):
        self.aboutToQuit = True
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    root.title("2020 Tax Automation")
    root.geometry("400x100")
    text = Label(root, text="Press Space in this Box to Pause/Play App\nThe app will appear to crash while it's in the process of pausing.")
    text.pack()
    #root.withdraw() # don't show the tkinter window
    FishLoop(root)
    root.mainloop()