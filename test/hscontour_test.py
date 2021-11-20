from hs_mercenaries_bot.hscontour_match import HSContonurMatch
from hs_mercenaries_bot.hssetting import r19201080


class Test_Countor:

    def test_list_allow_move_cards(self):
        imgpath = 'test\\test_data\\test_list_allow_move_cards.png'
        r19201080.debug_img = True
        hsc = HSContonurMatch(r19201080)
        locations = hsc.list_allow_move_cards(imgpath)
        assert len(locations) == 6


    def test_list_allow_spell_cards(self):
        imgpath = 'test\\test_data\\test_list_allow_spell_cards.png'
        r19201080.debug_img = True
        hsc = HSContonurMatch(r19201080)
        locations = hsc.list_allow_spell_cards(imgpath)
        assert len(locations) == 2
        m_locs, c_locs = locations[0],locations[1]
        assert len(m_locs) == 2
        assert len(c_locs) == 3

        imgpath = 'test\\test_data\\divine_shield.png'
        r19201080.debug_img = True
        hsc = HSContonurMatch(r19201080)
        locations = hsc.list_allow_spell_cards(imgpath)
        assert len(locations) == 2
        m_locs, c_locs = locations[0],locations[1]
        assert len(m_locs) == 3
        assert len(c_locs) == 3


    def test_list_bounties(self):
        imgpath = 'test\\test_data\\test_list_bounties.png'
        r19201080.debug_img = True
        hsc = HSContonurMatch(r19201080)
        locations = hsc.list_bounties(imgpath)
        assert len(locations) == 6


    def test_list_mercenary_collections(self):
        imgpath = 'test\\test_data\\test_list_mercenary_collections.png'
        r19201080.debug_img = True
        hsc = HSContonurMatch(r19201080)
        locations = hsc.list_mercenary_collections(imgpath)
        assert len(locations) == 5

    def test_list_map_moves(self):
        imgpath = 'test\\test_data\\test_list_map_moves.png'
        r19201080.debug_img = True
        hsc = HSContonurMatch(r19201080)
        locations = hsc.list_map_moves(imgpath)
        assert len(locations) == 2
        imgpath = 'test\\test_data\\list_map_moves2.png'
        r19201080.debug_img = True
        hsc = HSContonurMatch(r19201080)
        locations = hsc.list_map_moves(imgpath)
        assert len(locations) == 2
        


    def test_list_spell(self):
        imgpath = 'test\\test_data\\list_spell.png'
        r19201080.debug_img = True
        hsc = HSContonurMatch(r19201080)
        locations = hsc.list_card_spells(imgpath)
        assert len(locations) == 2
        imgpath = 'test\\test_data\\list_spell2.png'
        r19201080.debug_img = True
        hsc = HSContonurMatch(r19201080)
        locations = hsc.list_card_spells(imgpath)
        assert len(locations) == 2

    def test_find_greenready(self):
        imgpath = 'test\\test_data\\ready.png'
        r19201080.debug_img = True
        hsc = HSContonurMatch(r19201080)
        locations = hsc.find_battle_green_ready(imgpath)
        assert len(locations) == 1

