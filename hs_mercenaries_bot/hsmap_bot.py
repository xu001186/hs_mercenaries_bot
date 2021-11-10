
import random
from .hstemplate_match import MAPACTIONS
from .hsbot import HSBot

class HSMapBot(HSBot):
    def __init__(self,hssetting):
        super(HSMapBot, self).__init__(hssetting)
     

    def _move_action(self,move):
        self.click(move[0],move[1],random.randint(1,5),random.randint(1,5),sleep_time = 0.5)
        self.click_right_blank()
        location , action = self.hsmatch.find_map_action(self.hssetting.screenshot())
        if (location != []):
            self.hssetting.debug_msg("noraml actions %s" % action , self)    
            self.click(location[0][0],location[0][1],random.randint(1,5),random.randint(1,5),sleep_time = 0.5)
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
            self.hssetting.debug_msg("mysterious action",self)
            action = self._move_action(mysterious_location[0])
        if action == None:
            moves = self.hscontonur.list_map_moves(imgpath)
            for move in moves:
                action = self._move_action(move)
                if action != None:
                    return action
        return action

    def reveal(self):
        self.hssetting.debug_msg("start reveal",self)

    def pickup(self):
        self.hssetting.debug_msg("start pickup",self)

    def warp(self):
        self.hssetting.debug_msg("start warp",self)


    def visit(self):
        self.hssetting.debug_msg("start visit",self)  
        visitor_locations = self.retry_to_find_locations(self.hsmatch.find_vistors , max_retry= 5, err_if_not_found = False)          
        # visitor_locations = self.hsmatch.find_vistors(self.hssetting.screenshot())
        if visitor_locations != []:
            self.click(visitor_locations[0][0], visitor_locations[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
            visitor_choose = self.hsmatch.find_vistor_choose(self.hssetting.screenshot())
            if visitor_choose != []:
                self.click(visitor_choose[0][0], visitor_choose[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
            else:
                raise Exception("fail to find the visitor choose button")    
        else:
            self.hssetting.debug_msg("not mystery ",self)