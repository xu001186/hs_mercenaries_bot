from hs_mercenaries_bot.hsbattle_bot import HSBattleBot
from hs_mercenaries_bot.hsmap_bot import HSMapBot
from hs_mercenaries_bot.hsbounty_bot import HSBountyBot
from hs_mercenaries_bot.hssetting import HSSetting
from hs_mercenaries_bot.hssetting import r19201080



r19201080.debug = False
hs = HSSetting(1,r19201080)
battle = HSBattleBot(hs)
map = HSMapBot(hs)
bounty = HSBountyBot(hs)
mercenaries = [1,2,3]
spells = [[1,1,1]]
bounty_no = 1
mercenary_collection = 1
bounty.start(bounty_no,mercenary_collection)
while True:
    time.sleep(1)
    action = map.move()
    if action == MAPACTIONS.play:
        print("start battle")
        battle.wait_battle_ready_or_played_action(20)
        print("start battle prepare")
        battle.battle_prepare(mercenaries)
        print("start round")
        battle.start_round(1,   spells =spells )
        if battle.battle_finished:
            print("it's end,start next turn")
            bounty.start(bounty_no,mercenary_collection)

