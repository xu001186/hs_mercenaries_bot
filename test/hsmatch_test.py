from hs_mercenaries_bot.hstemplate_match import HSTemplateMatch
from hs_mercenaries_bot.hssetting import r19201080


class Test_Template():

    def test_find_bounty_start_choose(self):
        imgpath = 'test\\test_data\\test_list_bounties.png'
        r19201080.debug = True
        hsc = HSTemplateMatch(r19201080)
        locations = hsc.find_bounty_start_choose(imgpath)
        assert len(locations) == 1

    def test_is_party_start(self):
        imgpath = 'test\\test_data\\test_list_mercenary_collections.png'
        r19201080.debug = True
        hsc = HSTemplateMatch(r19201080)
        locations = hsc.is_party_start(imgpath)
        assert len(locations) == 1
        imgpath = 'test\\test_data\\test_list_bounties.png'
        locations = hsc.is_party_start(imgpath)
        assert len(locations) == 0
     
    def test_is_boss(self):
        imgpath = 'test\\test_data\\test_list_bounties.png'
        r19201080.debug = True
        hsc = HSTemplateMatch(r19201080)
        locations = hsc.is_bounty(imgpath)
        assert len(locations) == 1
        imgpath = 'test\\test_data\\m5.png'
        locations = hsc.is_bounty(imgpath)
        assert len(locations) == 0

    def test_find_choose(self):
        imgpath = 'test\\test_data\\vistorchoose.png'
        r19201080.debug = True
        hsc = HSTemplateMatch(r19201080)
        locations = hsc.find_vistor_choose(imgpath)
        assert len(locations) == 1
