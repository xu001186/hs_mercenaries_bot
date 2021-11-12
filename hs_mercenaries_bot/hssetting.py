from ahk import AHK

import pyautogui

class CONSTANT:
    GAME_NAME = "Hearthstone"

#magic numbers for the different resolutions
class r19201080:
    debug_img = False
    # pickup treasure and vistor margin
    treasure_x_margin = 300
    treasure_y_margin = 200

    # allow move card margin
    allow_move_card_y_margin = -30

    # _allow_spell_cards margin
    allow_spell_card_x_margin = -40
    allow_spell_card_y_margin = 60
    
    #battle drag
    battle_drag_x_margin = 140

    left_black_x_margin =70
    bottom_black_y_margin = 200

    path="1920x1080"

from datetime import datetime
import logging

class HSSetting:
  
    def __init__(self,  resolution):
        logging.basicConfig(filename='files\\debug\\hs_bot.log', level=logging.INFO)
        self.resolution = resolution
        self.possibility = 0.6
        self.screenshot_id = 1
        self.ahk = AHK()
        self.win =self.ahk.win_get(title=CONSTANT.GAME_NAME)
        self.bring_game()

    
    def screenshot(self):
        #filename = "{0}.png".format( datetime.now().strftime("%Y%m%d%H%M%S"))
        self.screenshot_id = int(self.screenshot_id % 50)
        filename = "screenshot_%s.png" % self.screenshot_id
        imgpath = 'files/debug/' + filename
        pyautogui.screenshot(imgpath)
        self.screenshot_id +=1
        return imgpath

    def bring_game(self):
        self.win.show()
        self.win.restore()
        self.win.maximize()
        self.win.to_top()      
        self.win.activate()
    
    def debug_msg(self,msg,ci=None):
        if ci == None:
            logging.info("%s - [None]: %s - with screenshot id : %s" % (datetime.now().strftime("%Y%m%d-%H:%M:%S") , msg, self.screenshot_id))
        else:
            logging.info("%s - [%s] : %s - with screenshot id : %s" % (datetime.now().strftime("%Y%m%d-%H:%M:%S"),ci.__class__.__name__,msg, self.screenshot_id))



