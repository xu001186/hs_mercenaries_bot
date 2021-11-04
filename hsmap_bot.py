
import random
from textwrap import wrap
from hstemplate_match import HSTemplateMatch,MAPACTIONS
from hscontour_match import HSContonurMatch


class HSMapBot:
    def __init__(self,hssetting,hsmouse):
        self.hssetting = hssetting
        self.hsmouse = hsmouse
        self.ahk = hssetting.ahk
        self.win = hssetting.win
        self.hsmatch = HSTemplateMatch(self.hssetting.resolution)
        self.hscontonur = HSContonurMatch(self.hssetting.resolution)        

    def click_right_blank(self):
        self.hsmouse.click(self.win.width - 150 , int(self.win.height * 2 / 3 ),x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 0.5)

    # def map_scoll_up(self):
    #     locations = self.hsmatch.find_map_scoll(self.hssetting.screenshot())
    #     if locations == []:
    #         raise Exception("the map scoll can't be found")
    #     self.ahk.mouse_move(locations[0][0] + random.randint(1,10), locations[0][1] + random.randint(1,10) , speed=30) 
    #     self.ahk.mouse_drag(locations[0][0],locations[0][1]- self.hssetting.resolution.up_y_margin,speed=35) 

    def _move_action(self,move):
        self.hsmouse.click(move[0],move[1],random.randint(1,5),random.randint(1,5),sleep_time = 0.5)
        self.click_right_blank()
        location , action = self.hsmatch.find_map_action(self.hssetting.screenshot())
        if (location != []):
            print("noraml actions %s" % action)    
            self.hsmouse.click(location[0][0],location[0][1],random.randint(1,5),random.randint(1,5),sleep_time = 0.5)
                # leave the play to battle bot
            if action == MAPACTIONS.reveal:
                self.reveal()
            if action == MAPACTIONS.pickup:
                self.pickup()
            if action == MAPACTIONS.visit:
                self.visit()
            if action == MAPACTIONS.warp:
                self.warp()
            return action  
        return None      

    def move(self):
        imgpath = self.hssetting.screenshot()
        action = None
        mysterious_location  = self.hsmatch.find_mysterious(imgpath)
        if mysterious_location != []:
            print("mysterious action")
            action = self._move_action(mysterious_location)
        if action ==None:
            moves = self.hscontonur.list_map_moves(imgpath)
            for move in moves:
                print("noraml actions")
                action = self._move_action(move)
                if action != None:
                    return action
        return action

    def reveal(self):
        print("start reveal")

    def pickup(self):
        print("start pickup")  

    def warp(self):
        print("start warp")  


    def visit(self):
        print("start visit")            
        visitor_locations = self.hsmatch.find_vistors(self.hssetting.screenshot())
        if visitor_locations != []:
            self.hsmouse.click(visitor_locations[0][0], visitor_locations[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
            visitor_choose = self.hsmatch.find_vistor_choose(self.hssetting.screenshot())
            if visitor_choose != []:
                self.hsmouse.click(visitor_choose[0][0], visitor_choose[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
            else:
                raise Exception("fail to find the visitor choose button")    
        else:
            print("not mystery ")