from hs_mercenaries_bot.hsbattle_bot import HSBattleBot
from hs_mercenaries_bot.hsmap_bot import HSMapBot
from hs_mercenaries_bot.hsbounty_bot import HSBountyBot
from hs_mercenaries_bot.hssetting import HSSetting
from hs_mercenaries_bot.hssetting import r19201080
import time
from hs_mercenaries_bot.hstemplate_match import MAPACTIONS

r19201080.debug = False
hs = HSSetting(r19201080)
battle = HSBattleBot(hs)
map = HSMapBot(hs)
bounty = HSBountyBot(hs)
mercenaries = [1,2,3]
spells = [[1,1,1],[3,2,2]]
bounty_no = 1
mercenary_collection = 1
# bounty.start(bounty_no,mercenary_collection)
times = 1
while True:
    time.sleep(1)
    action = map.move()
    if action == MAPACTIONS.play:
        hs.debug_msg("start battle")
        battle.battle_prepare(mercenaries)
        hs.debug_msg("start round")
        battle.start_round(1, spells =spells )
        if battle.battle_finished:
            battle.battle_finished = False
            hs.debug_msg("it's end,start next turn %s" % times)
            times +=1
            bounty.start(bounty_no,mercenary_collection)

