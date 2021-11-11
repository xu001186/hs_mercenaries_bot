



# How to start?
1) Install the python 
2) Ensure the hearthstone is running in full screen.
3) Ensure the hearthstone is running in 1920*1080 resolution
![Capture](https://user-images.githubusercontent.com/39233649/140640534-f558dacc-2227-44fa-83b6-b63ae731b36d.PNG)
4) Pre-build your mercenary collection . 
5) Open the start.py , update the spells , bounty_no and mercenary_collection base on What the order number means section.
```python
# the mercernaries pickup order, in this case, the card 1,2 and 3 are picked.
mercenaries = [1,2,3] 
# the spell order , in this case ,the card1 ,card2 and card3 are using the spell1 in the first round ,
# in 2nd round the card1 is using the spell 3, and card 2 is using spell 2 and the card 3 is using the spell 2 . 
# in 3rd round , the card1 ,card2 and card3 are using the spell 1 , and so on.  
spells = [[1,1,1],[3,2,2]] 
# the first bounty is selected .
bounty_no = 1
# the firsrt mercenary is selected
mercenary_collection = 1 # refer to 
bounty.start(bounty_no,mercenary_collection)
while True:
    time.sleep(1)
    action = map.move()
    if action == MAPACTIONS.play:
        print("start battle")
        battle.battle_prepare(mercenaries)
        print("start round")
        battle.start_round(1, spells =spells )
        if battle.battle_finished:
            battle.battle_finished = False
            bounty.start(bounty_no,mercenary_collection)
            print("it's end,start next turn")

```
8) Click into the Bountries selection page.
9) Run python start.py

# What the order number means?
The bot numbers the mercenary collections , bountry , mercenaries and spells for the user to easily to use them 

- The mercenary collections are numbered from left to right , from top to bottom
![list_bounties_20211107205634](https://user-images.githubusercontent.com/39233649/140640409-6e99e1e4-71fa-4a40-8104-9cb7d50ba8a6.png)
- The Bountries are numbered from left to right , from top to bottom
![list_bounties_20211107205817](https://user-images.githubusercontent.com/39233649/140640450-f6ddc5cc-b26e-4609-aad3-449a83a0f97a.png)
- The mercenaries are numbered from left to right, but you need to find them position from the battle field , it can be changed sometimes .
![list_allow_move_cards_20211107210847](https://user-images.githubusercontent.com/39233649/140640748-c9edcccf-3c15-4b69-8240-2d6844e91db4.png)
- Check your mercenary spell order , they are numbered from left to right.
![hsv_contour_final_20211107211336](https://user-images.githubusercontent.com/39233649/140640857-bfad6172-fdf5-4aad-8b40-ca216046942b.png)

# How does auto-path mysterious work?
- The bot traverses the map to find the mysterious vistor  , and get its (x,y) location
- The bot reorder the moves location based on abs(its(x_axis) - mercenary(x_axis)) ascending order in each hsmap_bot moves.
- There is no guarantee that the mysterious vistor  will be reached, but it provides the greatest possibility


# Support 
- 1920 * 1080 FULL SCREEN

# KNOWN ISSUE
- The bot will stops working if the any of mercenary is died.  (FIXED)




# Todo:
 1) Pickup the "allow minion move" from power.log to get card names. ( None)
 2) Once the rewards are collected , re-choose the boss and start over . (Done)
 3) Refine the battle spell choose.
 4) Auto find the path to mysterious (DONE)

# Update History

## Update 2021/11/11.
- Update HSBattleBot to fix the known issue 1)
- Update HSMapBot to support the auto path to mysterious


## Update 2021/11/10.
- Fix bugs
- Update find_mysterious
- Update mysterious.PNG
- Update map begin ,end and scoll templates
- Add find_mysterious_position function to hsmap_bot

## Update 2021/11/9.
- Fix bugs
- Update list_allow_move_cards
- Update _hsv_contour



## Update 2021/11/7.
- Fix bugs
- Release alpha version

## Updated 2021/11/6
- Fix bugs
- code refactoring
- Added more unit test cases


## Updated 2021/11/5
- Added the bounties detection
- Added the mercenary collections detection
- Rewrite the list_allow_spell_cards method to make it's more accurate 
- Add unit test cases 
- code refactoring
