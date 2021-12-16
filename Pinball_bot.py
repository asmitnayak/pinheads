import subprocess
import threading
import time
from mss import mss
import cv2
from PIL import Image
import numpy as np
import pydirectinput
import pyautogui
import pygetwindow as gw


# mon = {'top': 0, 'left':0, 'width':1920, 'height':1080}
class PinBallBot:
    def __init__(self, window_inst):

        self.cnt = [0]
        self.my_window = None
        try:
            # my_window = gw.getWindowsithTitle("3D Pinball for Windows - Space Cadet")[0]
            self.my_window = window_inst
            self.title = self.my_window.title
        except:
            try:
                print("starting pinball")
                subprocess.Popen("Pinball.lnk")
                print("pinball started")
                time.sleep(1)
                self.my_window = gw.getWindowsWithTitle("3D Pinball for Windows - Space Cadet")[0]
            except:
                print(
                    "please install Pinball on C drive\nthe installation file is in https://github.com/TRTR5TRTR/python-Pinball-bot")
                quit()

        self.sct = mss()
        self.l_contours = []
        self.r_contours = []

    def screen_left(self):
        while 1:
            mon = {'top': self.my_window.topleft[1] + 10, 'left': self.my_window.topleft[0] + 10,
                   'width': self.my_window.size[0] - 10,
                   'height': self.my_window.size[1] - 10}
            # mon = {'top': my_window.topleft[1], 'left': my_window.topleft[0], 'width': my_window.size[0],'height': my_window.size[1]}
            sct_img = self.sct.grab(mon)
            frame = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
            frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
            sct_img1 = self.sct.grab(mon)
            frame1 = Image.frombytes('RGB', (sct_img1.size.width, sct_img1.size.height), sct_img1.rgb)
            frame1 = cv2.cvtColor(np.array(frame1), cv2.COLOR_RGB2BGR)
            diff = cv2.absdiff(frame1, frame)
            gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
            cv2.imshow("screen_left", frame1)
            self.l_contours = contours
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def screen_right(self):
        while 1:
            mon = {'top': self.my_window.topleft[1] + 10, 'left': self.my_window.topleft[0] + 10,
                   'width': self.my_window.size[0] - 10,
                   'height': self.my_window.size[1] - 10}
            # mon = {'top': my_window.topleft[1], 'left': my_window.topleft[0], 'width': my_window.size[0],'height': my_window.size[1]}
            sct_img = self.sct.grab(mon)
            frame = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
            frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
            sct_img1 = self.sct.grab(mon)
            frame1 = Image.frombytes('RGB', (sct_img1.size.width, sct_img1.size.height), sct_img1.rgb)
            frame1 = cv2.cvtColor(np.array(frame1), cv2.COLOR_RGB2BGR)
            diff = cv2.absdiff(frame1, frame)
            gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
            cv2.imshow("screen_right", frame1)
            self.r_contours = contours
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def l_click(self):
        while 1:
            start = time.time()
            flag = False
            if gw.getActiveWindowTitle() == self.title:
                for c in self.l_contours:
                    pydirectinput.keyDown("z")
                    pyautogui.sleep(0.02)
                    pydirectinput.keyUp("z")
                    time.sleep(0.1)
                if self.l_contours:
                    flag = True
                    current = time.time()
            if flag and current - start < 0.28:
                time.sleep(0.5)

    def r_click(self):
        while 1:
            start = time.time()
            flag = False
            if gw.getActiveWindowTitle() == self.title:
                for c in self.r_contours:
                    pydirectinput.keyDown("/")
                    pyautogui.sleep(0.02)
                    pydirectinput.keyUp("/")
                    time.sleep(0.1)
                if self.r_contours:
                    flag = True
                    current = time.time()
            if flag and current - start < 0.255:
                time.sleep(0.5)

    def check_start(self):
        while 1:
            mon = {'top': self.my_window.topleft[1], 'left': self.my_window.topleft[0], 'width': self.my_window.size[0],
                   'height': self.my_window.size[1]}
            sct_img = self.sct.grab(mon)
            if sct_img.pixel(0, 0) == (56, 56, 56):
                print("starting")
                pydirectinput.keyDown(" ")
                pyautogui.sleep(1)
                pydirectinput.keyUp(" ")

    def main(self):
        t1 = threading.Thread(target=self.screen_left)
        t2 = threading.Thread(target=self.screen_right)
        t3 = threading.Thread(target=self.l_click)
        t4 = threading.Thread(target=self.check_start)
        t5 = threading.Thread(target=self.r_click)

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        time.sleep(0.2)
        self.my_window.activate()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
