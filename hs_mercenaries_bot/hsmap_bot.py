
import random

from hs_mercenaries_bot.hscontour_match import HSContonurMatch
from .hstemplate_match import MAPACTIONS
from .hsbot import HSBot

class HSMapBot(HSBot):
    def __init__(self, hssetting, is_path_to_mysterious=True):
        super(HSMapBot, self).__init__(hssetting)
        self.mysterious_loc = []
        self.is_path_to_mysterious = is_path_to_mysterious
     
    def find_mysterious_position(self):
        ss = self.hssetting.screenshot() 
        is_start = self.hsmatch.find_map_begin(ss)
        if is_start == []:
            return []
        is_map_end = []
        mysterious_loc = [] 
        while is_map_end == [] and mysterious_loc == []:
            ss = self.hssetting.screenshot()
            mysterious_loc = self.hsmatch.find_mysterious_unreach(ss)
            if mysterious_loc == []:
                is_map_end = self.hsmatch.find_map_end(ss)
                if is_map_end == []:
                    locations = self.hsmatch.find_map_scoll(ss)
                    if (locations != []):
                        self.ahk.mouse_move(locations[0][0] , locations[0][1] , speed=30) 
                        self.ahk.mouse_drag(locations[0][0],locations[0][1]-200,speed=35) 
        is_map_begin = []
        while is_map_begin == []:
            ss = self.hssetting.screenshot()
            is_map_begin = self.hsmatch.find_map_begin(ss)
            if is_map_begin == []:
                locations = self.hsmatch.find_map_scoll(ss)
                if (locations != []):
                    self.ahk.mouse_move(locations[0][0] , locations[0][1] , speed=30) 
                    self.ahk.mouse_drag(locations[0][0],locations[0][1]+200,speed=35)   
        return mysterious_loc
  

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

    def path_to_mysterious(self,moves):
        move_checks = []
        new_move = []
        if moves == [] or self.mysterious_loc == []:
            return moves
        if self.mysterious_loc != []:
            mx = self.mysterious_loc[0][0]
            for idx in range(len(moves)):
                move_checks.append( [ abs(moves[idx][0] - mx),idx] )

        move_checks = HSContonurMatch.sort_2d_array(move_checks)
        for move_check in move_checks:   
            new_move.append(moves[move_check[1]])
        return new_move  
       

    def move(self):
        imgpath = self.hssetting.screenshot()
        action = None
        mysterious_location  = self.hsmatch.find_mysterious(imgpath)
        if mysterious_location != []:
            self.hssetting.debug_msg("mysterious action",self)
            action = self._move_action(mysterious_location[0])
        if action == None:
            moves = self.hscontonur.list_map_moves(imgpath)
            if moves != []:
                print("start to find the find_mysterious_position1")
                if self.is_path_to_mysterious and self.mysterious_loc == []:
                    print("start to find the find_mysterious_position2")
                    self.mysterious_loc = self.find_mysterious_position()
                moves = self.path_to_mysterious(moves)
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