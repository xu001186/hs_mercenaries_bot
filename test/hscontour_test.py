from hs_mercenaries_bot.hscontour_match import HSContonurMatch
from hs_mercenaries_bot.hssetting import r19201080


class Test_Countor():

    def test_list_allow_move_cards(self):
        imgpath = 'test\\test_data\\test_list_allow_move_cards.png'
        r19201080.debug = True
        hsc = HSContonurMatch(r19201080)
        locations = hsc.list_allow_move_cards(imgpath)
        assert len(locations) == 6
        assert 670 <= locations[0][0] <= 730
        assert 780  <= locations[1][0] <= 841
        assert 860 <= locations[2][0] <= 920
        assert 925 <= locations[3][0] <= 975
        assert 1000 <= locations[4][0] <= 1050
        assert 1080 <= locations[5][0] <= 1130
        
        assert 1030<= locations[0][1] <= 1080
        assert 1030<= locations[1][1] <= 1080
        assert 1030<= locations[2][1] <= 1080
        assert 1030<= locations[4][1] <= 1080
        assert 1030<= locations[5][1] <= 1080

    def test_list_allow_spell_cards(self):
        imgpath = 'test\\test_data\\test_list_allow_spell_cards.png'
        r19201080.debug = True
        hsc = HSContonurMatch(r19201080)
        locations = hsc.list_allow_spell_cards(imgpath)
        assert len(locations) == 2
        m_locs, c_locs = locations[0],locations[1]
        assert len(m_locs) == 2
        assert len(c_locs) == 3


    def test_list_bounties(self):
        imgpath = 'test\\test_data\\test_list_bounties.png'
        r19201080.debug = True
        hsc = HSContonurMatch(r19201080)
        locations = hsc.list_bounties(imgpath)
        assert len(locations) == 6


    def test_list_mercenary_collections(self):
        imgpath = 'test\\test_data\\test_list_mercenary_collections.png'
        r19201080.debug = True
        hsc = HSContonurMatch(r19201080)
        locations = hsc.list_mercenary_collections(imgpath)
        assert len(locations) == 5
        
t = Test_Countor()

t.test_list_allow_spell_cards()