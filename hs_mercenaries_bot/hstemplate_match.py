import cv2
import numpy as np
import os
from datetime import datetime
from .hssetting import r19201080
from .hscontour_match import HSContonurMatch
import logging

class MAPACTIONS:
    play = "play"
    visit = "visit"
    reveal = "reveal"
    pickup = "pickup"
    warp = "warp"
class HSTemplateMatch:
   
    def __init__(self,resolution=r19201080):
        self.resolution = resolution
        self.debug = self.resolution.debug_img


    def find_reward(self,imgpath):
        img = cv2.imread(imgpath)
        location,_ = self._feature_match(img,"reward",folder="templates/map")
        if location != []:
            return [location ]
        return []

    def find_reward_done(self,imgpath):
        img = cv2.imread(imgpath)
        location,_ = self._feature_match(img,"done",folder="templates/map",min_match_nums=10)
        if location != []:
            return [location ]
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
        take =  self._three_choose_one_actions(imgpath,"take")
        keep = self._three_choose_one_actions(imgpath,"keep")
        if (take != []):
            return take
        if (keep != []):
            return keep

    def find_vistor_choose(self,imgpath):
        return self._three_choose_one_actions(imgpath,"vistor_choose")

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
            return [location ] 
        return [] 


    def find_mysterious_unreach(self,imgpath):
        img = cv2.imread(imgpath)
        location = self._feature_match(img,"mysterious_unreach",min_match_nums = 15, folder="templates/map" )[0]
        if location != []:
            return [location ] 
        return [] 

    def find_bounty_finish_ok(self,imgpath):
        img = cv2.imread(imgpath)
        location = self._feature_match(img,"ok",min_match_nums = 10, folder="templates/map" )[0]
        if location != []:
            return [location ] 
        return [] 

    def find_bounty_start_choose(self,imgpath):
        img = cv2.imread(imgpath)
        location = self._feature_match(img,"choose",min_match_nums = 25, folder="templates/map" )[0]
        if location != []:
            return [location ] 
        return [] 

    def is_party_start(self,imgpath):
        img = cv2.imread(imgpath)
        location = self._feature_match(img,"is_party",min_match_nums = 40, folder="templates/map" )[0]
        if location != []:
            return [location ] 
        return [] 

    def is_bounty(self,imgpath):
        img = cv2.imread(imgpath)
        location = self._feature_match(img,"boss_info",min_match_nums = 40, folder="templates/map" )[0]
        if location != []:
            return [location ] 
        return [] 


    def find_lock_in(self,imgpath):
        img = cv2.imread(imgpath)
        location = self._feature_match(img,"lock_in",min_match_nums = 13, folder="templates/map" )[0]
        if location != []:
            return [location ] 
        return [] 


    def is_gold_reward(self,imgpath):
        img = cv2.imread(imgpath)
        location = self._feature_match(img,"reward",min_match_nums = 30, folder="templates/ignore" )[0]
        if location != []:
            return [location ] 
        return [] 

    def find_battle_ready(self,imgpath):
        location = self.is_gold_reward(imgpath)
        if location != []:
            return []
        return self._right_side_button(imgpath,"ready",min_match_nums=15)[0]

    def find_battle_played(self,imgpath):
        location = self.is_gold_reward(imgpath)
        if location != []:
            return []        
        return self._right_side_button(imgpath,"played",min_match_nums=10)[0]

    def find_battle_ready_or_played(self,imgpath):
        ready = self.find_battle_ready(imgpath)
        if ready == []:
            return self.find_battle_played(imgpath)
        return ready

    def find_map_end(self,imgpath):
        img = cv2.imread(imgpath)
        location = self._feature_match(img,"map_end",min_match_nums = 30, folder="templates/map" )[0]
        if location != []:
            return [location ] 
        return [] 

    def find_map_begin(self,imgpath):
        img = cv2.imread(imgpath)
        location = self._feature_match(img,"map_begin",min_match_nums = 15, folder="templates/map" )[0]
        if location != []:
            return [location ] 
        return [] 

    def find_map_scoll(self,imgpath):
        return self._right_side_button(imgpath,"scoll","map",5)[0]

    def find_map_play(self,imgpath):
        return self._right_side_button(imgpath,MAPACTIONS.play,"map",30)[0]


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
            if self.debug:
                self._debug_img_with_text([[location[0] + int(w*left_x_cut_pect) , location[1] ] ],img)
                self.debug_img("%s_with_text" % action,img)
            return [[location[0] + int(w*left_x_cut_pect) , location[1] ] ] ,good_nums
        
        return [] ,good_nums

    


    def _feature_match(self,img,action,min_match_nums= 15, folder="templates"):
        train =  img
        sift = cv2.SIFT_create()

        try:
            query_path = os.path.join("files/", "{0}/{1}/{2}.png".format(self.resolution.path,folder,action) )
            query = cv2.imread( query_path ,  cv2.IMREAD_GRAYSCALE)  
            kp1, des1 = sift.detectAndCompute(query,None)
            kp2, des2 = sift.detectAndCompute(train,None)
            if kp1 == () or kp2 == ():
                logging.debug("Err - good %s for action %s , less than threshold %s" % (0,action,min_match_nums))
                return [],0
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

            ## re-group the pts .
            pts_groups = []
            pts = np.float32([kp2[m[0].trainIdx].pt for m in good])
            qh, qw = query.shape[:2]
            for pt in pts:
                in_group = False
                for pts_group in pts_groups:
                    if pt in pts_group:
                        in_group = True
                        break
                if not in_group:
                    approx_pts_rows = np.where(   (pts[:,1] >= pt[1] - qh)   &  (pts[:,1] <=   pt[1] + qh  ) & (pts[:,0] >= pt[0] - qw)   &  (pts[:,0] <=   pt[0] + qw  ) )
                    approx_pts = pts[approx_pts_rows] 
                    pts_groups.append(approx_pts)
            
            max_number_group = []
            for pts_group in pts_groups:
                if len(pts_group) > len(max_number_group):
                    max_number_group = pts_group

            if len(max_number_group) < min_match_nums:
                logging.debug("Err - good %s for action %s , less than threshold %s" % (len(max_number_group),action,min_match_nums))
                return [] , len(good)
            else:
                logging.debug(" good %s for action %s" % (len(max_number_group),action))


            x,y = np.mean(max_number_group, axis=0)
     
            return [int(x),int(y)] ,len(max_number_group)
        except Exception as e:
            print(e)
            return [],0

    def debug_img(self,img_name,img,save_to="files/debug/"):
        if (self.debug):
            filename = "{0}_{1}.png".format( datetime.now().strftime("%Y%m%d%H%M%S"),img_name)
            img_path = os.path.join(save_to, filename)
            cv2.imwrite(img_path,img)



    def _debug_img_with_text(self,locations,img):
        for idx in range(len(locations)): 
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, '%s' % (idx + 1), (locations[idx][0] , locations[idx][1]) , font, 1, (0, 255, 0), 2, cv2.LINE_AA)
