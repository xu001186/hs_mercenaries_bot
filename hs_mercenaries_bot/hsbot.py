from .hstemplate_match import HSTemplateMatch
from .hscontour_match import HSContonurMatch
import time
import random

class HSBot:
    def __init__(self,hssetting):
        self.hssetting = hssetting

        self.ahk = hssetting.ahk
        self.win = hssetting.win
        self.hsmatch = HSTemplateMatch(self.hssetting.resolution)
        self.hscontonur = HSContonurMatch(self.hssetting.resolution)        

    def click_left_blank(self):
        self.click(self.hssetting.resolution.left_black_x_margin , int(self.win.height / 2) + 150,x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 0.1)

    def click_right_blank(self):
        self.click(self.win.width - 150 , int(self.win.height * 2 / 3 ),x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 0.1)

    def right_click_left_blank(self):
        self.right_click(self.hssetting.resolution.left_black_x_margin , int(self.win.height / 2) + 150,x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)

    def move_left_blank(self):
        self.ahk.mouse_move(self.hssetting.resolution.left_black_x_margin , int(self.win.height / 2) + 150,speed=10)

    def move_bottm_blank(self):
        self.ahk.mouse_move(0,self.hssetting.resolution.bottom_black_y_margin,speed=10,relative=True)

    def click(self , x,y, x_margin=0,y_margin=0 ,sleep_time = 0):
        if sleep_time ==0:
            sleep_time = random.randint(1,2)
        move_speed = random.randint(5,10)
        self.ahk.mouse_move(x + x_margin, y +y_margin, speed=move_speed) 
        self.ahk.click()
        time.sleep(sleep_time)

    def right_click(self , x,y, x_margin=0,y_margin=0 ,sleep_time = 0):
        if sleep_time ==0:
            sleep_time = random.randint(1,2)
        move_speed = random.randint(5,10)
        self.ahk.mouse_move(x + x_margin, y +y_margin, speed=move_speed) 
        self.ahk.right_click()
        time.sleep(sleep_time)
                

    def retry_to_find_locations(self, location_calls,max_retry=30 ,err_if_not_found = True ):
      
        retry = 0
        location = []
        action_calls = location_calls
        if not isinstance(action_calls,list):
            action_calls = [location_calls]
        while (len(location) == 0 and retry < max_retry):
            if retry != 0:
                self.click_left_blank()
                time.sleep(2)
                self.hssetting.debug_msg("retry to find the %s  %s  " % (action_call.__name__,retry))
            retry +=1
            for action_call in action_calls:
                location = (action_call(self.hssetting.screenshot()))
                if (len(location) == 0 and retry <= max_retry ):
                    continue
                else:
                    if isinstance(location_calls,list): 
                        return location  , action_call.__name__
                    return location
        if err_if_not_found:
            raise Exception("Failed to call %s  " % (action_call.__name__))   
        else:
            if isinstance(location_calls,list): 
                return location  , action_call.__name__
            return location

