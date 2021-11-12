from hs_mercenaries_bot.hsbattle_bot import HSBattleBot
from hs_mercenaries_bot.hsmap_bot import HSMapBot
from hs_mercenaries_bot.hsbounty_bot import HSBountyBot
from hs_mercenaries_bot.hssetting import HSSetting
from hs_mercenaries_bot.hssetting import r19201080
import time
from hs_mercenaries_bot.hstemplate_match import MAPACTIONS
from confg import *




r19201080.debug = False
hs = HSSetting(r19201080)
battle = HSBattleBot(hs,mercenaries,spells)
map = HSMapBot(hs,is_path_to_mysterious)
bounty = HSBountyBot(hs)

if start_from_bounty:
    bounty.start(bounty_no,mercenary_collection)
times = 1
while True:
    time.sleep(1)
    action = map.move()
    if action == MAPACTIONS.play:
        hs.debug_msg("start battle")
        battle.battle_prepare()
        hs.debug_msg("start round")
        battle.start_round(1 )
        if battle.battle_finished:
            battle.battle_finished = False
            print("it's end,start next turn %s" % times)
            hs.debug_msg("it's end,start next turn %s" % times)
            times +=1
            bounty.start(bounty_no,mercenary_collection)

