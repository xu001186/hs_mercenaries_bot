import random 
import cv2
import numpy as np


from hssetting import r19201080


import os
from datetime import datetime

class HSContonurMatch:

    def __init__(self,resolution=r19201080,debug=False):
        self.resolution = resolution
        self.debug = debug




    def list_allow_move_cards(self,imgpath):
        img = cv2.imread(imgpath)
        left_x_cut_pect = 1/4
        right_x_cut_pect = 1/4
        top_y_cut_pect = 1/2 + 1/6
        bottom_y_cut_pect = 0
        crop_img = HSContonurMatch.crop_img(img, left_x_cut_pect,right_x_cut_pect,top_y_cut_pect, bottom_y_cut_pect)
        
        img_hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)  
        green_mask = cv2.inRange(img_hsv,(40,130,255),(90,255,255))
        kernel = np.ones((21, 21), 'uint8')
        dilate_img = cv2.dilate(green_mask, kernel)
        self.debug_img("list_allow_move_cards_dilate_img",img)
        h, w = img.shape[:2]
        ch,_ = crop_img.shape[:2]
        contours, _ = cv2.findContours(dilate_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        locations = []
        approx_locations = []
        for contour in contours:
            approx = cv2.approxPolyDP( contour, 0.01 * cv2.arcLength(contour, False), False) 
            area = cv2.contourArea(contour)
            arcLength = cv2.arcLength(contour, False)
            if (( arcLength >= 200) and (area >= 2000)):
                for p in approx:
                    approx_locations.append(p[0])
        if approx_locations ==[]:
            return locations
        approx_locations = np.array(approx_locations)
        approx_locationss_rows = np.where(  (approx_locations[:,1] >= ch - 100)   &  (approx_locations[:,1] <=  ch  ) )
        approx_locations = approx_locations[approx_locationss_rows] 
        approx_locations = HSContonurMatch.sort_2d_array(approx_locations)

        tmp_locations =[]
        for idx in range(len(approx_locations) - 1):
            x = approx_locations[idx][0]
            y = approx_locations[idx][1]
            if len(tmp_locations) != 0:
                tmp_max_x = np.max(tmp_locations,axis=0)[0]
                if x - tmp_max_x  > 30 or len(approx_locations)  == idx+1:
                    tmp_locations_a = np.array(tmp_locations)
                    max_point_row = np.where(  tmp_locations_a[:,1] == np.max(tmp_locations,axis=0)[1]) 
                    position = tmp_locations_a [max_point_row][0] 
                    locations.append([position[0] + int(w*left_x_cut_pect) + self.resolution.allow_move_card_x_margin, position[1]+int(h*top_y_cut_pect) + self.resolution.allow_move_card_y_margin])
                    tmp_locations = []
            tmp_locations.append([x,y])

        if self.debug:
            self._debug_img_with_text(locations,img)
            self.debug_img("list_allow_move_cards",img)

        return locations

    @staticmethod
    def crop_img(img,left_x_cut_pect,right_x_cut_pect,top_y_cut_pect,bottom_y_cut_pect ):
        h, w = img.shape[:2]
        cropped_image = img[int(h*top_y_cut_pect): h - int(h*bottom_y_cut_pect), int(w*left_x_cut_pect): w - int(w*right_x_cut_pect)]
        return cropped_image
    
    @staticmethod
    def sort_2d_array(array,by_x=True):
        if len(array)  == 0:
            return array
        array_a = np.array(array)
        
        if by_x:
            ind = np.lexsort((array_a[:,1],array_a[:,0]))    
        else:
            ind = np.lexsort((array_a[:,0],array_a[:,1]))    
        
        return array_a[ind]
   
    def list_allow_spell_cards(self,imgpath):
        img = cv2.imread(imgpath)

        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  
        green_mask = cv2.inRange(img_hsv,(2,0,150),(22,35,255))
        kernel = np.ones((5, 5), 'uint8')
        dilate_img = cv2.dilate(green_mask, kernel)
       
        self.debug_img("list_allow_move_cards_dilate_img",dilate_img)    
        contours, _ = cv2.findContours(dilate_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        cards_locations = []
        minion_locations = []
        h, w = img.shape[:2]
        for contour in contours:
            area = cv2.contourArea(contour)
            arcLength = cv2.arcLength(contour, False)
            if (( arcLength >= 100) and (area >= 100)):
                M = cv2.moments(contour)
                if M['m00'] != 0.0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                if (int(h/2) < cy): # the cards position
                    cards_locations.append([cx + self.resolution.allow_spell_card_x_margin , cy + self.resolution.allow_spell_card_y_margin ])
                else: # the minion position
                    minion_locations.append([cx + self.resolution.allow_spell_card_x_margin ,cy + self.resolution.allow_spell_card_y_margin ])
                if self.debug:
                    cv2.drawContours(img,[contour],0, (random.randint(0,256), random.randint(0,256), random.randint(0,256)),2  )
        self.debug_img("list_allow_move_cards_contour_img",img)

        if (cards_locations == [] or minion_locations ==[]):
            return [],[]
        
        cards_locations = np.array(cards_locations)
        cards_locations_rows = np.where(  ( h *8 / 15  + self.resolution.allow_spell_card_y_margin <= cards_locations[:,1]) 
         &  (cards_locations[:,1] <= h*10 / 15 + self.resolution.allow_spell_card_y_margin ) )
        cards_locations = cards_locations[cards_locations_rows] 
      
 
        minion_locations = np.array(minion_locations)
        minion_locations_row = np.where(   (  h *3 / 20  + self.resolution.allow_spell_card_y_margin <= minion_locations[:,1] )  
         &  (minion_locations[:,1] <= h*5/ 20  + self.resolution.allow_spell_card_y_margin)   )
        minion_locations = minion_locations[minion_locations_row]


        minion_locations = HSContonurMatch.sort_2d_array(minion_locations)
        cards_locations = HSContonurMatch.sort_2d_array(cards_locations)
        
        if self.debug:
            self._debug_img_with_text(minion_locations,img)
            self._debug_img_with_text(cards_locations,img)
            self.debug_img("list_allow_spell_cards",img)
        return minion_locations, cards_locations


    
   
    def list_card_spells(self,imgpath):
        return self._hsv_contour(imgpath,(40,130,255),(90,255,255),300,1000,0,30)

    def list_rewards(self,imgpath):
        return self._hsv_contour(imgpath,(90,110,130),(179,255,255),100,800)

    def _hsv_contour(self,imgpath,min_hsv ,max_hsv,min_arcLength ,min_area,  cx_margin=0,cy_margin=0, kernal=[5,5]):
        img = cv2.imread(imgpath)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  
        green_mask = cv2.inRange(img_hsv,min_hsv,max_hsv)
        kernel = np.ones(kernal, 'uint8')
        dilate_img = cv2.dilate(green_mask, kernel)
        self.debug_img("dilate_img_hsv_contour",dilate_img)
        contours, _ = cv2.findContours(dilate_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        locations = []
        for contour in contours:
            arcLength = cv2.arcLength(contour, False) 
            area = cv2.contourArea(contour)
            if  arcLength >= min_arcLength  and   area >= min_area:
                M = cv2.moments(contour)
                if M['m00'] != 0.0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    locations.append([cx + cx_margin,cy + cy_margin])
                if self.debug:
                    cv2.drawContours(img,[contour],0, (random.randint(0,256), random.randint(0,256), random.randint(0,256)),2  )
        locations = HSContonurMatch.sort_2d_array(locations)
        self.debug_img("dilate_img_hsv_contour_contour",img)
        locations = HSContonurMatch.sort_2d_array(locations)
        if self.debug:
            self._debug_img_with_text(locations,img)
            self.debug_img("_hsv_contour_final",img)
        return locations



    def is_spell_target(self,imgpath):
        img = cv2.imread(imgpath)
        
        # img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  
        red_mask = cv2.inRange(img,(0,0,190),(30,30,255))
        kernel = np.ones((11, 11), 'uint8')
        red_mask = cv2.dilate(red_mask, kernel)
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        self.debug_img("is_spell_target_mask",red_mask)
        locations = []
        for contour in contours:
            approx = cv2.approxPolyDP( contour, 0.01 * cv2.arcLength(contour, False), False) 
            area = cv2.contourArea(contour)
            arcLength = cv2.arcLength(contour, False)
                                                                 
            if ((  arcLength >= 200) and (  area >= 200) ):
                print(arcLength,area)
                M = cv2.moments(contour)
                if M['m00'] != 0.0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    locations.append([cx,cy-10])
                    if self.debug:
                        cv2.drawContours(img,[contour],0, (random.randint(0,256), random.randint(0,256), random.randint(0,256)),2  )
        self.debug_img("is_spell_target_contours",img)
        locations = HSContonurMatch.sort_2d_array(locations)
        if self.debug:
            self._debug_img_with_text(locations,img)
            self.debug_img("is_spell_target_final",img)
        return locations


    def list_map_moves(self,imgpath):
        img = cv2.imread(imgpath)
        cropped_img = HSContonurMatch.crop_img(img,0,7/24,0,1/10)    
        img_hsv = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)  
        gold_mask = cv2.inRange(img_hsv,(40,100,0),(179,255,255))
        kernel = np.ones((11, 11), 'uint8')
        gold_mask = cv2.dilate(gold_mask, kernel)
        contours, _ = cv2.findContours(gold_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        self.debug_img("list_map_moves_mask",gold_mask)
        locations = []
        for contour in contours:
            approx = cv2.approxPolyDP( contour, 0.01 * cv2.arcLength(contour, False), False) 
            area = cv2.contourArea(contour)
            arcLength = cv2.arcLength(contour, False)
                                                                  # exclude the hexagon "view party"
            if ((  arcLength >= 600) and (  area >= 1500) and len(approx) > 10):
                M = cv2.moments(contour)
                if M['m00'] != 0.0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    locations.append([cx,cy-10])
                    if self.debug:
                        cv2.drawContours(cropped_img,[contour],0, (random.randint(0,256), random.randint(0,256), random.randint(0,256)),2  )
        self.debug_img("list_map_moves_contours",cropped_img)
        locations = HSContonurMatch.sort_2d_array(locations)
        if self.debug:
            self._debug_img_with_text(locations,img)
            self.debug_img("list_map_moves_final",cropped_img)
        return locations


    def debug_img(self,img_name,img,save_to="files/debug/"):
        if (self.debug):
            filename = "{0}_{1}.png".format(img_name, datetime.now().strftime("%Y%m%d%H%M%S"))
            img_path = os.path.join(save_to, filename)
            print(img_path)
            cv2.imwrite(img_path,img)



    def _debug_img_with_text(self,locations,img):
        for idx in range(len(locations)): 
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, '%s' % (idx + 1), (locations[idx][0] , locations[idx][1]) , font, 1, (0, 255, 0), 2, cv2.LINE_AA)

