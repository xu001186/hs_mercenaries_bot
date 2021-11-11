from hs_mercenaries_bot.hsbattle_bot import HSBattleBot
from hs_mercenaries_bot.hsmap_bot import HSMapBot
from hs_mercenaries_bot.hsbounty_bot import HSBountyBot
from hs_mercenaries_bot.hssetting import HSSetting
from hs_mercenaries_bot.hssetting import r19201080
import time
from hs_mercenaries_bot.hstemplate_match import MAPACTIONS


mercenaries = [1,3,4]
spells = [[1,1,1],[2,3,3]]
bounty_no = 6
mercenary_collection = 3
is_path_to_mysterious = True

# mercenaries = [1,2]
# spells = [[2,1],[2,3],[3,1]]
# bounty_no = 1
# mercenary_collection = 4
# is_path_to_mysterious = False


r19201080.debug = False
hs = HSSetting(r19201080)
battle = HSBattleBot(hs,mercenaries,spells)
map = HSMapBot(hs,is_path_to_mysterious)
bounty = HSBountyBot(hs)

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
            hs.debug_msg("it's end,start next turn %s" % times)
            times +=1
            bounty.start(bounty_no,mercenary_collection)

