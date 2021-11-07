
import random
import time
from .hsbot import HSBot

class HSBountyBot(HSBot):
    def __init__(self,hssetting):
        super(HSBountyBot, self).__init__(hssetting)
    
    def start(self,bounty_no,mercenary_no):
        self._bounty(bounty_no)
        self._mercenary(mercenary_no)


    def _bounty(self,bounty_no):
        is_bounty =  self.retry_to_find_locations(self.hsmatch.is_bounty,5)
        if is_bounty == []:
            raise Exception("can't find the boss selection page" )
        locations =  self.retry_to_find_locations(self.hscontonur.list_bounties,5)
        if bounty_no > len(locations):
            raise Exception("The total bounties number is %s , less than the one you choosed %s  " % (len(locations),bounty_no) )
        bounty_loc = locations[bounty_no - 1]
        self.click(bounty_loc[0],bounty_loc[1],random.randint(1,5),random.randint(1,5),sleep_time = 0.5)
        start_loc =  self.retry_to_find_locations(self.hsmatch.find_bounty_start_choose,5)
        if start_loc == []:
            raise Exception("can't find the choose button for bounty" )
        self.click(start_loc[0][0],start_loc[0][1],random.randint(1,5),random.randint(1,5),sleep_time = 0.5)
        time.sleep(3)

        
    
    def _mercenary(self,mercenary_no):
        is_mercenary_selection =  self.retry_to_find_locations(self.hsmatch.is_party_start,5)
        if is_mercenary_selection == []:
            raise Exception("can't find the mercenary selection page" )        
        mercenary_collections_locations =  self.retry_to_find_locations(self.hscontonur.list_mercenary_collections,5)
        if  mercenary_collections_locations == []:
            raise Exception("can't find the mercenary collections" )
        if mercenary_no > len(mercenary_collections_locations):
            raise Exception("The total mercenary collections number is %s , less than the one you choosed %s  " % (len(mercenary_collections_locations),mercenary_no) )
        mercenary_loc = mercenary_collections_locations[mercenary_no - 1]
        self.click(mercenary_loc[0],mercenary_loc[1],random.randint(1,5),random.randint(1,5),sleep_time = 0.5)
        start_loc =  self.retry_to_find_locations(self.hsmatch.find_bounty_start_choose,5)
        if start_loc == []:
            raise Exception("can't find the choose button for mercenary  " )
        self.click(start_loc[0][0],start_loc[0][1],random.randint(1,5),random.randint(1,5),sleep_time = 0.5)
        time.sleep(2)
        button_location , next_step_action = self.retry_to_find_locations([self.hsmatch.find_lock_in , self.hsmatch.find_map_play] ,10)
        if next_step_action == "find_lock_in":
            self.click(button_location[0][0],button_location[0][1],random.randint(1,5),random.randint(1,5),sleep_time = 0.5)
            time.sleep(5)
            self.retry_to_find_locations(self.hsmatch.find_map_play ,10) # wait for the play comes out
            
        if next_step_action == "find_map_play":
            print("let the map bot to handle")
            # self.click(button_location[0][0],button_location[0][1],random.randint(1,5),random.randint(1,5),sleep_time = 0.5)
            time.sleep(5)
    