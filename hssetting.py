import cv2
from ahk import AHK
import mss


class CONSTANT:
    MODE_NORMAL = "normal"
    MODE_HEROIC = "heroic"
    GAME_NAME  = 'Hearthstone'

#magic numbers for the different resolutions
class r19201080:
    debug = False
    # pickup treasure and vistor margin
    treasure_x_margin = 300
    treasure_y_margin = 200

    # allow move card margin
    allow_move_card_x_margin = 20
    allow_move_card_y_margin = -2

    # _allow_spell_cards margin
    allow_spell_card_x_margin = -40
    allow_spell_card_y_margin = 60
    

    
    #battle drag
    battle_drag_x_margin = 130

    #left blank click
    left_black_x_margin =70

    #map scoll up 
    up_y_margin = 100

    path="1920x1080"

from datetime import datetime
class HSSetting:
  
    def __init__(self, monitor , resolution):
        self.resolution = resolution
        self.possibility = 0.6
        self.monitor = monitor
        self.ahk = AHK()
        self.win =self.ahk.win_get(title=CONSTANT.GAME_NAME)
        self.bring_game()
        # self.ahk.show_info_traytip("Starting", "loading files", slient=False, blocking=True)
        # self.ahk.show_info_traytip("started", "all files loaded successfully", slient=False, blocking=False)
        
    
    def screenshot(self):
        filename = "{0}.png".format( datetime.now().strftime("%Y%m%d%H%M%S"))
        imgpath = 'files/debug/' + filename
        sct = mss.mss()
        sct.shot(mon=self.monitor, output=imgpath)
        return imgpath

    def bring_game(self):
        self.win.show()
        self.win.restore()
        self.win.maximize()
        self.win.to_top()      
        self.win.activate()
    



