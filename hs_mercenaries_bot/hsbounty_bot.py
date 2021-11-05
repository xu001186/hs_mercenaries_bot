
import random
import time
from .hsbot import HSBot

class HSBountyBot(HSBot):
    def __init__(self,hssetting,hsmouse):
        super(HSBountyBot, self).__init__(hssetting,hsmouse)

  
    
    def bounty(self,no):
        locations =  self.retry_click(self.hssetting.screenshot(),self.hscontonur.list_bounties,5)
        if no > len(locations):
            raise Exception("The total bounties is only %s , less than the one you choosed %s  " % (locations,no) )
        bounty_loc = locations[no - 1]
        self.hsmouse.click(bounty_loc[0],bounty_loc[1],random.randint(1,5),random.randint(1,5),sleep_time = 0.5)
        start_loc = self.hsmatch.find_bounty_start_choose(self.hssetting.screenshot())
        if start_loc == []:
            raise Exception("can't find the choose button  " )
        self.hsmouse.click(start_loc[0],start_loc[1],random.randint(1,5),random.randint(1,5),sleep_time = 0.5)
        time.sleep(5)
        self.retry_click(self.hssetting.screenshot(),self.hsmatch.find_battle_played,5)
      
    