from hs_mercenaries_bot.hstemplate_match import HSTemplateMatch
from hs_mercenaries_bot.hssetting import r19201080


class Test_Template:

    def test_find_bounty_start_choose(self):
        imgpath = 'test\\test_data\\test_list_bounties.png'
        r19201080.debug_img = True
        hsc = HSTemplateMatch(r19201080)
        locations = hsc.find_bounty_start_choose(imgpath)
        assert len(locations) == 1

    def test_is_party_start(self):
        imgpath = 'test\\test_data\\test_list_mercenary_collections.png'
        r19201080.debug_img = True
        hsc = HSTemplateMatch(r19201080)
        locations = hsc.is_party_start(imgpath)
        assert len(locations) == 1
        imgpath = 'test\\test_data\\test_list_bounties.png'
        locations = hsc.is_party_start(imgpath)
        assert len(locations) == 0
     
    def test_is_boss(self):
        imgpath = 'test\\test_data\\test_list_bounties.png'
        r19201080.debug_img = True
        hsc = HSTemplateMatch(r19201080)
        locations = hsc.is_bounty(imgpath)
        assert len(locations) == 1
        imgpath = 'test\\test_data\\m5.png'
        locations = hsc.is_bounty(imgpath)
        assert len(locations) == 0

    def test_find_choose(self):
        imgpath = 'test\\test_data\\vistorchoose.png'
        r19201080.debug_img = True
        hsc = HSTemplateMatch(r19201080)
        locations = hsc.find_vistor_choose(imgpath)
        assert len(locations) == 1

    def test_find_mysterious(self):
        imgpath = 'test\\test_data\\find_mysterious.png'
        r19201080.debug_img = True
        hsc = HSTemplateMatch(r19201080)
        locations = hsc.find_mysterious(imgpath)
        assert len(locations) == 1

    def test_find_mysterious_unreach(self):
        imgpath = 'test\\test_data\\find_mysterious_unreach.png'
        r19201080.debug_img = True
        hsc = HSTemplateMatch(r19201080)
        locations = hsc.find_mysterious_unreach(imgpath)
        assert len(locations) == 1

    def test_find_scoll(self):
        imgpath = 'test\\test_data\\find_mysterious.png'
        r19201080.debug_img = True
        hsc = HSTemplateMatch(r19201080)
        locations = hsc.find_map_scoll(imgpath)
        assert len(locations) == 1

    def test_find_map_end(self):
        imgpath = 'test\\test_data\\map_end.png'
        r19201080.debug_img = True
        hsc = HSTemplateMatch(r19201080)
        locations = hsc.find_map_end(imgpath)
        assert len(locations) == 1
        imgpath = 'test\\test_data\\find_mysterious.png'
        r19201080.debug_img = True
        hsc = HSTemplateMatch(r19201080)
        locations = hsc.find_map_end(imgpath)
        assert len(locations) == 0

    def test_find_map_begin(self):
        imgpath = 'test\\test_data\\map_begin.png'
        r19201080.debug_img = True
        hsc = HSTemplateMatch(r19201080)
        locations = hsc.find_map_begin(imgpath)
        assert len(locations) == 1
        imgpath = 'test\\test_data\\find_mysterious.png'
        r19201080.debug_img = True
        hsc = HSTemplateMatch(r19201080)
        locations = hsc.find_map_begin(imgpath)
        assert len(locations) == 0

