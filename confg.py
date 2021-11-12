# the mercernaries pickup order, in this case, the card 1,2 and 3 are picked.
mercenaries = [1,2,3]
# the spell order , in this case ,the card1 ,card2 and card3 are using the spell1 in the first round ,
# in 2nd round the card1 is using the spell 3, and card 2 is using spell 2 and the card 3 is using the spell 2 . 
# in 3rd round , the card1 ,card2 and card3 are using the spell 1 , and so on.  
spells = [[1,1,1],[3,2,3]]
# the bounty selection order, in this case , the 5th bounty is selected.
bounty_no = 5
# the mercenary collection selection order, in this case , the 3rd collection is selected
mercenary_collection = 3
# whether the bot traverses the map to find the mysterious vistor
is_path_to_mysterious = True
# Is the bot starts from bounty selection
start_from_bounty = True


##Example to use two mercenaries to gain the coins from the map 1-1
# mercenaries = [1,2]
# spells = [[2,1],[2,3]]
# bounty_no = 1
# mercenary_collection = 4
# is_path_to_mysterious = False
# start_from_bounty = True