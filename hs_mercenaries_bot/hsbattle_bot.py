import time
import random
import numpy as np
from .hsbot import HSBot

class HSBattleBot(HSBot):
    def __init__(self,hssetting):
        super(HSBattleBot, self).__init__(hssetting)
        self.battle_finished = False
 
    def _pickup_card(self,x,y,seq):
        self.ahk.mouse_move(x + random.randint(1,5)  , y + random.randint(1,5),speed=30)
        self.ahk.mouse_drag( int(self.win.width / 2) + self.hssetting.resolution.battle_drag_x_margin * (seq),  int(self.win.height / 2) , speed=40)



    def battle_prepare(self,cards_move):
        self.retry_to_find_locations(self.hsmatch.find_battle_played ,5)  #detect played button to ensure it's the right place
        self.click_left_blank() 
        cards_move = np.sort(cards_move)
        for seq in range(len(cards_move)):
            locations = self.retry_to_find_locations(self.hscontonur.list_allow_move_cards ,10) 
            if locations != []:
                card_position = locations[ cards_move[seq] - seq -1 ]
                self._pickup_card(card_position[0], card_position[1],seq)
                time.sleep(3)
            else:
                raise Exception("can't find the minions to move for the battle")
        locations = self.retry_to_find_locations(self.hsmatch.find_battle_ready_or_played ,5) 
        if len(locations) != 0:
            self.click(locations[0][0], locations[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5), sleep_time = 2)
            self.retry_to_find_locations(self.hsmatch.find_battle_ready_or_played ,5)  # wait until the played or ready button is there
        else:
            raise Exception("can't find the ready button for the battle")


    def start_round(self,round_nums,spells):
        self.retry_to_find_locations(self.hsmatch.find_battle_ready ,5) #detect ready button to ensure it's the right place
        self.click_left_blank()  
        print("start round %s" % round_nums)
        spell_locations = self.hscontonur.list_card_spells(self.hssetting.screenshot()) # get spells
        if spell_locations != []:
            self.click_left_blank()  # make sure no spell is popped up before detecting the minions and cards
        locations = self.retry_to_find_locations(self.hscontonur.list_allow_spell_cards ,5) 
        minions_locations,cards_locations = locations[0],locations[1]
        cards_nums = len(cards_locations)
        if cards_nums > 3:
            cards_nums = 3
        # drag the spell to the first minion
        for seq in range(cards_nums):
            self.click_left_blank()  
            self.click(cards_locations[seq][0], cards_locations[seq][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5) , sleep_time = 1) # click the card
            self.move_bottm_blank()
            spell_locations = self.hscontonur.list_card_spells(self.hssetting.screenshot()) # get spell
            if spell_locations != []: 
                spell_set = spells[ (round_nums-1) % len(spells) ]
                spell_choose = spell_set[seq] - 1
                if (len(spell_locations)) <= spell_choose:
                    spell_choose = len(spell_locations) - 1
                print(spell_choose,len(spell_locations))
                self.click(spell_locations[spell_choose][0], spell_locations[spell_choose][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 0.5) # move to spell and click
                self.click(minions_locations[0][0], minions_locations[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 0.5) # move to first minion and click
        
        ready_location = self.retry_to_find_locations(self.hsmatch.find_battle_ready_or_played ,5) 
        self.click(ready_location[0][0], ready_location[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
        time.sleep(8) # wait 8 sec to finish the round
        self._battle_check(round_nums,spells)


    def _battle_check(self,round_nums,spells):
        location,action = self.retry_to_find_locations([self.hsmatch.find_battle_ready, self.hsmatch.find_treasure,self.hsmatch.find_reward] ,10) 
        if action == "find_battle_ready" : # start next round
            self.start_round(round_nums+1,spells)
        if action == "find_treasure" : # the battle is finished , choose the first treasure
            self._pick_treasure(location)
        if action == "find_reward":  # start to pickup all the rewards
            self._pick_rewards()

    def _pick_rewards(self):
        rewards = self.hscontonur.list_rewards(self.hssetting.screenshot())
        for r in rewards:
            self.click(r[0], r[1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
        done_location = self.hsmatch.find_reward_done(self.hssetting.screenshot())
        if done_location != []:
            self.click(done_location[0][0], done_location[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
        else:
            raise Exception("fail to click the done rewards")  
        time.sleep(5)
        ok_location = self.hsmatch.find_bounty_finish_ok(self.hssetting.screenshot())
        if ok_location != []:
            self.click(ok_location[0][0], ok_location[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
        else:
            raise Exception("fail to click ok")  
        self.battle_finished = True

    def _pick_treasure(self,treasure_location):
        self.click(treasure_location[0][0], treasure_location[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
        treasure_take = self.hsmatch.find_treasure_take(self.hssetting.screenshot())
        if treasure_take != []:
            self.click(treasure_take[0][0], treasure_take[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
        else:
            raise Exception("fail to find the treasure take button")                  




            
        