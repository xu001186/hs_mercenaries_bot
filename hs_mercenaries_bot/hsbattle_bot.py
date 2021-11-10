import time
import random
import numpy as np
from .hsbot import HSBot


class HSBattleBot(HSBot):
    def __init__(self,hssetting):
        super(HSBattleBot, self).__init__(hssetting)
        self.battle_finished = False
 
    def _pickup_card(self,x,y,seq):
        self.ahk.mouse_move(x , y ,speed=40)
        self.ahk.mouse_drag( int(self.win.width / 2) + self.hssetting.resolution.battle_drag_x_margin * (seq),  int(self.win.height / 2) , speed=40)



    def battle_prepare(self,cards_move):
        self.hssetting.debug_msg("Start to check the battle prepare",self)
        self.retry_to_find_locations(self.hsmatch.find_battle_played) #detect played button to ensure it's the right place
        self.hssetting.debug_msg("The battle is ready",self)
        self.click_left_blank() 
        cards_move = np.sort(cards_move)
        for seq in range(len(cards_move)):
            locations = self.retry_to_find_locations(self.hscontonur.list_allow_move_cards ) 
            if locations != []:
                card_position = locations[ cards_move[seq] - seq - 1 ]
                self.hssetting.debug_msg("Card moves nums %s , the seq is %s,location is %s " % (len(locations), seq,card_position) ,self)
                self._pickup_card(card_position[0], card_position[1],seq)
                time.sleep(3)
            # else:
            #     raise Exception("can't find the minions to move for the battle")
        locations = self.retry_to_find_locations(self.hsmatch.find_battle_ready_or_played)
        if len(locations) != 0:
            self.click(locations[0][0], locations[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5), sleep_time = 2)
            self.retry_to_find_locations(self.hsmatch.find_battle_ready_or_played) # wait until the played or ready button is there
        else:
            raise Exception("can't find the ready button for the battle")


    def start_round(self,round_nums,spells):
        self.hssetting.debug_msg("Start to check the start round",self)
        self.retry_to_find_locations(self.hsmatch.find_battle_ready_or_played ) #detect ready button to ensure it's the right place
        self.hssetting.debug_msg("The start round is ready",self)
        self.click_left_blank()  
        self.hssetting.debug_msg("start round %s" % round_nums,self)
        spell_locations = self.hscontonur.list_card_spells(self.hssetting.screenshot()) # get spells
        if spell_locations != []:
            self.click_left_blank()  # make sure no spell is popped up before detecting the minions and cards
        self.hssetting.debug_msg("Start to find the cards locations",self)
        locations = self.retry_to_find_locations(self.hscontonur.list_allow_spell_cards)
        minions_locations,cards_locations = locations[0],locations[1]
        cards_nums = len(cards_locations)
        if cards_nums > 3:
            cards_nums = 3
        # drag the spell to the first minion
        all_spell_found = True
        ready_location = []
        for seq in range(cards_nums):
            self.click_left_blank()  
            self.click(cards_locations[seq][0], cards_locations[seq][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5) , sleep_time = 1) # click the card
            self.move_bottm_blank()
            self.hssetting.debug_msg("Start to find the card spells locations",self)
            spell_locations = self.hscontonur.list_card_spells(self.hssetting.screenshot()) # get spell
            if spell_locations != []: 
                spell_set = spells[ (round_nums-1) % len(spells) ]
                spell_choose = spell_set[seq] - 1
                if (len(spell_locations)) <= spell_choose:
                    spell_choose = len(spell_locations) - 1
                self.click(spell_locations[spell_choose][0], spell_locations[spell_choose][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 0.5) # move to spell and click
                self.click(minions_locations[0][0], minions_locations[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 0.5) # move to first minion and click
            else:
                all_spell_found = False
        self.hssetting.debug_msg("Start to find the ready_location",self)
        ##Todo: refine
        if all_spell_found and cards_nums == len(cards_locations):
            ready_location = self.retry_to_find_locations(self.hscontonur.find_battle_green_ready,max_retry=5,err_if_not_found=False) 
            if ready_location == []:
                ready_location = self.retry_to_find_locations(self.hsmatch.find_battle_ready_or_played) 
            self.click(ready_location[0][0], ready_location[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
            time.sleep(4) # wait4 sec to finish the round
                
            retry = 0
            ready_location = self.hscontonur.find_battle_green_ready(self.hssetting.screenshot())
            while (ready_location != [] and retry < 5):
                self.hssetting.debug_msg("The ready button is still there ",self)
                self.click(ready_location[0][0], ready_location[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
                retry += 1
                time.sleep(4) # wait 4 sec to finish the round
        else:
            ready_location = self.retry_to_find_locations(self.hsmatch.find_battle_ready_or_played) 
            self.click(ready_location[0][0], ready_location[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
            time.sleep(4) # wait 4 sec to finish the round            

        


        self._battle_check(round_nums,spells)


    def _battle_check(self,round_nums,spells):
        self.hssetting.debug_msg("Start to check find_battle_ready,find_treasure or find_reward ",self)
        location,action = self.retry_to_find_locations([self.hsmatch.find_battle_ready, self.hsmatch.find_treasure,self.hsmatch.find_reward] ) 
        if action == "find_battle_ready" : # start next round
            self.hssetting.debug_msg("The ready location is found ",self)
            self.start_round(round_nums+1,spells)
        if action == "find_treasure" : # the battle is finished , choose the first treasure
            self.hssetting.debug_msg("The treasure location is found ",self)
            self._pick_treasure(location)
        if action == "find_reward":  # start to pickup all the rewards
            self.hssetting.debug_msg("The reward location is found ",self)
            self._pick_rewards()

    def _pick_rewards(self):
        self.hssetting.debug_msg("Start to pickup rewards ",self)
        rewards = self.retry_to_find_locations(self.hscontonur.list_rewards ) 
        for r in rewards:
            self.click(r[0], r[1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
        self.hssetting.debug_msg("Start to find the done location",self)     
        done_location = self.retry_to_find_locations(self.hsmatch.find_reward_done )        
        if done_location != []:
            self.click(done_location[0][0], done_location[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
        else:
            raise Exception("fail to click the done rewards")  
        time.sleep(5)
        self.hssetting.debug_msg("Start to find the ok location",self)     
        ok_location = self.retry_to_find_locations(self.hsmatch.find_bounty_finish_ok )        
        if ok_location != []:
            self.click(ok_location[0][0], ok_location[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
        else:
            raise Exception("fail to click ok")  
        self.battle_finished = True

    def _pick_treasure(self,treasure_location):
        self.hssetting.debug_msg("Start to pickup treasures",self)     
        self.click(treasure_location[0][0], treasure_location[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
        treasure_take = self.retry_to_find_locations(self.hsmatch.find_treasure_take )
        if treasure_take != []:
            self.click(treasure_take[0][0], treasure_take[0][1],x_margin=random.randint(1,5),y_margin=random.randint(1,5),sleep_time = 1)
        else:
            raise Exception("fail to find the treasure take button")                  




            
        