import time
import random
import numpy as np
from hstemplate_match import HSTemplateMatch
from hscontour_match import HSContonurMatch


class HSBattleBot:
    def __init__(self,hssetting,hsmouse):
        self.hssetting = hssetting
        self.hsmouse = hsmouse
        self.ahk = hssetting.ahk
        self.win = hssetting.win
        self.battle_finished = False
        self.hsmatch = HSTemplateMatch(self.hssetting.resolution)
        self.hscontonur = HSContonurMatch(self.hssetting.resolution)        

    def _pickup_card(self,x,y,seq):
        self.ahk.mouse_move(x + random.randint(1,5)  , y + random.randint(1,5),speed=30)
        self.ahk.mouse_drag( int(self.win.width / 2) + self.hssetting.resolution.battle_drag_x_margin * (seq),  int(self.win.height / 2) , speed=40)

    def click_left_blank(self):
        self.hsmouse.click(self.hssetting.resolution.left_black_x_margin , int(self.win.height / 2) + 150,x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)

    def right_click_left_blank(self):
        self.hsmouse.right_click(self.hssetting.resolution.left_black_x_margin , int(self.win.height / 2) + 150,x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)


    def move_left_blank(self):
        self.ahk.mouse_move(self.hssetting.resolution.left_black_x_margin , int(self.win.height / 2) + 150,speed=30)


    def wait_battle_ready_or_played_action(self,max_retry_times):
        retry = 0 
        ready_location = self.hsmatch.find_battle_ready_or_played(self.hssetting.screenshot())
        while (len(ready_location) == 0 and retry <= max_retry_times ):
            self.click_left_blank()  
            time.sleep(3)
            retry +=1
            ready_location = self.hsmatch.find_battle_ready_or_played(self.hssetting.screenshot())
            print("retry to click ready or play %s  " % retry)
        if (retry >= max_retry_times):
            raise Exception("fail to click the ready or play button")        
        return ready_location


    def battle_prepare(self,cards_move):
        cards_move = np.sort(cards_move)
        for seq in range(len(cards_move)):
            locations = self.hscontonur.list_allow_move_cards(self.hssetting.screenshot())
            retry = 0 
            while (len(locations) == 0 and retry <= 5 ):
                self.click_left_blank()  
                time.sleep(3)
                retry +=1
                locations = self.hscontonur.list_allow_move_cards(self.hssetting.screenshot())
                print("retry to click ready or play %s  " % retry)
            if locations != []:
                card_position = locations[ cards_move[seq] - seq -1 ]
                self._pickup_card(card_position[0], card_position[1],seq)
                time.sleep(3)
            else:
                raise Exception("can't find the minions to move for the battle")
               

        locations = self.wait_battle_ready_or_played_action(5)
        if len(locations) != 0:
            self.hsmouse.click(locations[0][0], locations[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5), sleep_time = 2)
            self.wait_battle_ready_or_played_action(5) # wait until the played or ready button is there
        else:
            raise Exception("can't find the ready button for the battle")


    def start_round(self,round_nums):
        self.click_left_blank()  
        spells =[
            [1,1,1],
            [3,2,3]
            ]
        print("start round %s" % round_nums)
        
        spell_locations = self.hscontonur.list_card_spells(self.hssetting.screenshot()) # get spells
        if spell_locations != []:
            self.click_left_blank()  # make sure no spell is popped up before detecting the minions and cards
        minions_locations,cards_locations = self.hscontonur.list_allow_spell_cards(self.hssetting.screenshot())
        retry = 0
        while minions_locations == [] and retry >=3:
            minions_locations,cards_locations = self.hscontonur.list_allow_spell_cards(self.hssetting.screenshot())
            time.sleep(3)
            retry +=1
        
        if(minions_locations == []):
            raise Exception("can't find the minions")

        cards_nums = len(cards_locations)
        if cards_nums > 3:
            cards_nums = 3
        # drag the spell to the first minion
        for seq in range(cards_nums):
            self.click_left_blank()  
            self.hsmouse.click(cards_locations[seq][0], cards_locations[seq][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5) , sleep_time = 1) # click the card
            self.move_left_blank()
            spell_locations = self.hscontonur.list_card_spells(self.hssetting.screenshot()) # get spell
            if len(spell_locations) != None: 
                spell_set = spells[ (round_nums-1) % len(spells) ]
                spell_choose = spell_set[seq] - 1
                if (len(spell_locations)) < spell_choose:
                    spell_choose = len(spell_locations) - 1
                self.hsmouse.click(spell_locations[spell_choose][0], spell_locations[spell_choose][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 0.5) # move to spell and click
                self.hsmouse.click(minions_locations[0][0], minions_locations[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 0.5) # move to first minion and click
        
        ready_location = self.wait_battle_ready_or_played_action(5)
        self.hsmouse.click(ready_location[0][0], ready_location[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
        time.sleep(8) # wait 8 sec to finish the round
        self._battle_check(round_nums)


    def _battle_check(self,round_nums):
        retry = 0 
        # check whether the round is finished or the battle is finished.
        battle_img = self.hssetting.screenshot()
        ready_location = self.hsmatch.find_battle_ready(battle_img)
        treasure_location  = self.hsmatch.find_treasure(battle_img)
        is_reward = self.hsmatch.find_reward(battle_img)
        # print("wait for ready to come back %s %s" % [ready_location ,treasure_location])
        retry = 0 
        while len(ready_location) == 0 and len(treasure_location) ==0 and len(is_reward) ==0 and retry <= 10:
            print("retry %s  " % retry)
            self.click_left_blank()  
            time.sleep(3)
            battle_img = self.hssetting.screenshot()
            ready_location = self.hsmatch.find_battle_ready(battle_img)
            treasure_location  = self.hsmatch.find_treasure(battle_img)
            is_reward = self.hsmatch.find_reward(battle_img)
            retry +=1
            print("retry %s to find the ready or treasure button   " % retry)
        if (retry >= 10):
            raise Exception("fail to wait the round complete")  
        
        if len(ready_location) != 0 : # start next round
            self.start_round(round_nums+1)
        if len(treasure_location) !=0 : # the battle is finished , choose the first treasure
            self._pick_treasure(treasure_location)
        if len(is_reward) !=0: # start to pickup all the rewards
            self._pick_rewards()

    def _pick_rewards(self):
        rewards = self.hscontonur.list_rewards(self.hssetting.screenshot())
        for r in rewards:
            self.hsmouse.click(r[0], r[1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
        done_location = self.hsmatch.find_reward_done(self.hssetting.screenshot())
        if done_location != []:
            self.hsmouse.click(done_location[0][0], done_location[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
        else:
            print("fail to click the done rewards")                
        self.battle_finished = True

    def _pick_treasure(self,treasure_location):
        self.hsmouse.click(treasure_location[0][0], treasure_location[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
        treasure_take = self.hsmatch.find_treasure_take(self.hssetting.screenshot())
        if treasure_take != []:
            self.hsmouse.click(treasure_take[0][0], treasure_take[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
        else:
            raise Exception("fail to find the treasure take button")                  




            
        