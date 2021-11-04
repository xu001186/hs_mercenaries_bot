import time
import random

class HSMouseActions:

    def __init__(self,hssetting):
        self.hssetting = hssetting
        self.ahk = hssetting.ahk
        self.win = hssetting.win
        self.possibility = 0.6

    def click(self , x,y, x_margin=0,y_margin=0 ,sleep_time = 0):
        if sleep_time ==0:
            sleep_time = random.randint(3,6)
        move_speed = random.randint(20,40)
        self.ahk.mouse_move(x + x_margin, y +y_margin, speed=move_speed) 
        self.ahk.click()
        time.sleep(sleep_time)

    def right_click(self , x,y, x_margin=0,y_margin=0 ,sleep_time = 0):
        if sleep_time ==0:
            sleep_time = random.randint(3,6)
        move_speed = random.randint(20,40)
        self.ahk.mouse_move(x + x_margin, y +y_margin, speed=move_speed) 
        self.ahk.right_click()
        time.sleep(sleep_time)
                