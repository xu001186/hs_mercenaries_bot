import cv2
import numpy as np
from hscontour_match import HSContonurMatch
import os
from hssetting import r19201080
from datetime import datetime

class MAPACTIONS:
    play = "play"
    visit = "visit"
    reveal = "reveal"
    pickup = "pickup"
    warp = "warp"
class HSTemplateMatch:
   
    def __init__(self,resolution=r19201080,debug = False):
        self.resolution = resolution
        self.debug = debug


    def find_reward(self,imgpath):
        img = cv2.imread(imgpath)
        location,_ = self._feature_match(img,"reward",folder="templates/map")
        if location != []:
            return [[location[0]  , location[1] ] ]
        return []

    def find_reward_done(self,imgpath):
        img = cv2.imread(imgpath)
        location,_ = self._feature_match(img,"done",folder="templates/map",min_match_nums=10)
        if location != []:
            return [[location[0]  , location[1] ] ]
        return []    

    def find_vistors(self,imgpath):
        return self._three_choose_one_items(imgpath,"visitor")


    def find_treasure(self,imgpath):
        return self._three_choose_one_items(imgpath,"treasure")
 
    def _three_choose_one_items(self,imgpath,type):
        left_x_cut_pect = 0
        right_x_cut_pect = 0
        top_y_cut_pect = 0
        bottom_y_cut_pect = 1/2
        img = cv2.imread(imgpath)
        cut_img = HSContonurMatch.crop_img(img, left_x_cut_pect, right_x_cut_pect,top_y_cut_pect,bottom_y_cut_pect)
        anchor_locations,_ = self._feature_match(cut_img,type,min_match_nums=30,folder="templates/map")

        if anchor_locations != []:
            treasure_1 = (anchor_locations[0] - self.resolution.treasure_x_margin, anchor_locations[1]  + self.resolution.treasure_y_margin)
            treasure_2 = (anchor_locations[0], anchor_locations[1] + self.resolution.treasure_y_margin)
            treasure_3 = (anchor_locations[0] + self.resolution.treasure_x_margin , anchor_locations[1] + self.resolution.treasure_y_margin)
            return [treasure_1,treasure_2,treasure_3]
        return anchor_locations        

    def find_treasure_take(self,imgpath):
        return self._three_choose_one_actions(imgpath,"take")
        
    def find_vistor_choose(self,imgpath):
        return self._three_choose_one_actions(imgpath,"choose")

    def _three_choose_one_actions(self,imgpath,type):
        left_x_cut_pect = 0
        right_x_cut_pect = 0
        top_y_cut_pect = 1/2
        bottom_y_cut_pect = 0
        img = cv2.imread(imgpath)
        cut_img = HSContonurMatch.crop_img(img, left_x_cut_pect, right_x_cut_pect,top_y_cut_pect,bottom_y_cut_pect)
        location,_ = self._feature_match(cut_img,type,folder="templates/map")
        h, w = img.shape[:2]
        if location != []:
            return [[location[0] + int(w*left_x_cut_pect) , location[1] + int(h*top_y_cut_pect)] ]
        return []

    def find_mysterious(self,imgpath):
        img = cv2.imread(imgpath)
        location = self._feature_match(img,"mysterious",min_match_nums = 15, folder="templates/map" )[0]
        if location != []:
            return [[location[0]  , location[1] ] ] 
        return [] 


    def find_battle_ready(self,imgpath):
        return self._right_side_button(imgpath,"ready",min_match_nums=10)[0]

    def find_battle_played(self,imgpath):
        return self._right_side_button(imgpath,"played",min_match_nums=10)[0]

    def find_battle_ready_or_played(self,imgpath):
        ready = self.find_battle_ready(imgpath)
        if ready == []:
            return self.find_battle_played(imgpath)
        return ready

    def find_map_scoll(self,imgpath):
        return self._right_side_button(imgpath,"scoll","map",10)[0]

    def find_map_action(self,imgpath,max_good_points= 50 ):
        play,play_nums = self._right_side_button(imgpath,MAPACTIONS.play,"map")
        if (play_nums >= max_good_points):
            return play,MAPACTIONS.play
        pickup,pickup_nums = self._right_side_button(imgpath,MAPACTIONS.pickup,"map")
        if (play_nums >= max_good_points):
            return pickup,MAPACTIONS.pickup
        reveal,reveal_nums = self._right_side_button(imgpath,MAPACTIONS.reveal,"map")     
        if (play_nums >= max_good_points):
            return reveal,MAPACTIONS.reveal
        visit,visit_nums = self._right_side_button(imgpath,MAPACTIONS.visit,"map")     
        if (play_nums >= max_good_points):
            return visit,MAPACTIONS.visit
        warp,warp_nums = self._right_side_button(imgpath,MAPACTIONS.warp,"map")     
        if (warp_nums >= max_good_points):
            return warp,MAPACTIONS.warp
            
        max_match, location, action = play_nums,play, MAPACTIONS.play 
        if(max_match < pickup_nums):
            max_match, location, action = pickup_nums,pickup, MAPACTIONS.pickup
        if(max_match < reveal_nums):
            max_match, location, action = reveal_nums,reveal, MAPACTIONS.reveal
        if(max_match < visit_nums):
            max_match, location, action = visit_nums,visit, MAPACTIONS.visit
        if(max_match < warp_nums):
            max_match, location, action = warp_nums,warp, MAPACTIONS.warp
            
        return location,action


    def _right_side_button(self,imgpath,action,img_type='battle',min_match_nums=15):
        left_x_cut_pect = 1/2
        img = cv2.imread(imgpath)
        cut_img = HSContonurMatch.crop_img(img, left_x_cut_pect, 0,0,0)
        location,good_nums = self._feature_match(cut_img,action,min_match_nums = min_match_nums, folder="templates/%s" % img_type)
        h, w = img.shape[:2]
        if location != []:
            return [[location[0] + int(w*left_x_cut_pect) , location[1] ] ] ,good_nums
        return [] ,good_nums

    def _feature_match(self,img,action,min_match_nums= 15, folder="templates"):
        train =  img
        sift = cv2.SIFT_create()
        query_path = os.path.join("files/", "{0}/{1}/{2}.png".format(self.resolution.path,folder,action) )
        query = cv2.imread( query_path ,  cv2.IMREAD_GRAYSCALE)  
        kp1, des1 = sift.detectAndCompute(query,None)
        kp2, des2 = sift.detectAndCompute(train,None)
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1,des2, k=2) 
        good = []
        ratio  = 0.7
        for m,n in matches:
            if m.distance < ratio *n.distance:
                good.append([m])

        if self.debug:
            img_match = np.empty(( img.shape[0] + 100, query.shape[1] + img.shape[1], 3), dtype=np.uint8)
            img_debug = cv2.drawMatchesKnn(query,kp1,img,kp2,good,flags=2,outImg=img_match)
            self.debug_img(action,img_debug)

        if len(good) <= min_match_nums:
            print("Err - good %s for action %s , less than threshold %s" % (len(good),action,min_match_nums))
            return [] , len(good)
        else:
            print(" good %s for action %s" % (len(good),action))
        pts2 = np.float32([kp2[m[0].trainIdx].pt for m in good])
        x,y = np.mean(pts2, axis=0)
        

        return [int(x),int(y)] ,len(good)


    def debug_img(self,img_name,img,save_to="files/debug/"):
        if (self.debug):
            filename = "{0}_{1}.png".format( datetime.now().strftime("%Y%m%d%H%M%S"),img_name)
            img_path = os.path.join(save_to, filename)
            print(img_path)
            cv2.imwrite(img_path,img)



    def _debug_img_with_text(self,locations,img):
        for idx in range(len(locations)): 
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, '%s' % (idx + 1), (locations[idx][0] , locations[idx][1]) , font, 1, (0, 255, 0), 2, cv2.LINE_AA)
