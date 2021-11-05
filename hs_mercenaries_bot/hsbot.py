from .hstemplate_match import HSTemplateMatch
from .hscontour_match import HSContonurMatch
import time
import random

class HSBot:
    def __init__(self,hssetting,hsmouse):
        self.hssetting = hssetting
        self.hsmouse = hsmouse
        self.ahk = hssetting.ahk
        self.win = hssetting.win
        self.hsmatch = HSTemplateMatch(self.hssetting.resolution)
        self.hscontonur = HSContonurMatch(self.hssetting.resolution)        

    def click_left_blank(self):
        self.hsmouse.click(self.hssetting.resolution.left_black_x_margin , int(self.win.height / 2) + 150,x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)

    def right_click_left_blank(self):
        self.hsmouse.right_click(self.hssetting.resolution.left_black_x_margin , int(self.win.height / 2) + 150,x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)

    def move_left_blank(self):
        self.ahk.mouse_move(self.hssetting.resolution.left_black_x_margin , int(self.win.height / 2) + 150,speed=30)


    def retry_click(self, imgpath, action_call,max_rety ):
        locations = action_call(imgpath)
        retry = 1 
        while (len(locations) == 0 and retry <= max_rety ):
            self.click_left_blank()  
            time.sleep(3)
            locations = action_call(imgpath)
            print("retry to find the %s  %s  " % (action_call.__name__,retry))
            retry +=1
        if (retry >= max_rety):
            raise Exception("Failed to call %s  " % (action_call.__name__))   
        return locations  