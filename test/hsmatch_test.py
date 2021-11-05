from hs_mercenaries_bot.hstemplate_match import HSTemplateMatch
from hs_mercenaries_bot.hssetting import r19201080


class Test_Template():

    def test_find_bounty_start_choose(self):
        imgpath = 'test\\test_data\\b1.png'
        r19201080.debug = True
        hsc = HSTemplateMatch(r19201080)
        locations = hsc.find_bounty_start_choose(imgpath)
        assert len(locations) == 1

     
t = Test_Template()
t.test_find_bounty_start_choose()
      

