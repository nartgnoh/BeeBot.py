# *********************************************************************************************************************
# lol_constants.py
# import cogs.helper.constants.lol_constants as lol_constants
# *********************************************************************************************************************

# *********************************************************************************************************************
# Riot Constants
# *********************************************************************************************************************

def riot_regions(): return ['br1', 'eun1', 'euw1',
                            'jp1', 'kr', 'la1', 'la2', 'na1', 'oc1', 'tr1', 'ru']


def riot_ranks(): return {1: {'tier': 'IRON', 'rank': 'IV'},
                          2: {'tier': 'IRON', 'rank': 'III'},
                          3: {'tier': 'IRON', 'rank': 'II'},
                          4: {'tier': 'IRON', 'rank': 'I'},
                          5: {'tier': 'BRONZE', 'rank': 'IV'},
                          6: {'tier': 'BRONZE', 'rank': 'III'},
                          7: {'tier': 'BRONZE', 'rank': 'II'},
                          8: {'tier': 'BRONZE', 'rank': 'I'},
                          9: {'tier': 'SILVER', 'rank': 'IV'},
                          10: {'tier': 'SILVER', 'rank': 'III'},
                          11: {'tier': 'SILVER', 'rank': 'II'},
                          12: {'tier': 'SILVER', 'rank': 'I'},
                          13: {'tier': 'GOLD', 'rank': 'IV'},
                          14: {'tier': 'GOLD', 'rank': 'III'},
                          15: {'tier': 'GOLD', 'rank': 'II'},
                          16: {'tier': 'GOLD', 'rank': 'I'},
                          17: {'tier': 'PLATINUM', 'rank': 'IV'},
                          18: {'tier': 'PLATINUM', 'rank': 'III'},
                          19: {'tier': 'PLATINUM', 'rank': 'II'},
                          20: {'tier': 'PLATINUM', 'rank': 'I'},
                          21: {'tier': 'DIAMOND', 'rank': 'IV'},
                          22: {'tier': 'DIAMOND', 'rank': 'III'},
                          23: {'tier': 'DIAMOND', 'rank': 'II'},
                          24: {'tier': 'DIAMOND', 'rank': 'I'},
                          25: {'tier': 'MASTER', 'rank': 'IV'},
                          26: {'tier': 'MASTER', 'rank': 'III'},
                          27: {'tier': 'MASTER', 'rank': 'II'},
                          28: {'tier': 'MASTER', 'rank': 'I'},
                          29: {'tier': 'GRANDMASTER', 'rank': 'IV'},
                          30: {'tier': 'GRANDMASTER', 'rank': 'III'},
                          31: {'tier': 'GRANDMASTER', 'rank': 'II'},
                          32: {'tier': 'GRANDMASTER', 'rank': 'I'},
                          33: {'tier': 'CHALLENGER', 'rank': 'IV'},
                          34: {'tier': 'CHALLENGER', 'rank': 'III'},
                          35: {'tier': 'CHALLENGER', 'rank': 'II'},
                          36: {'tier': 'CHALLENGER', 'rank': 'I'}
                          }


# *********************************************************************************************************************
# League of Legends Constants
# *********************************************************************************************************************

def lol_keys(): return ['Q', 'W', 'E', 'R']


def lol_roles(include_fill=True):
    if include_fill:
        return ['Top', 'Jung', 'Mid', 'Adc', 'Sup', 'Fill']
    else:
        return ['Top', 'Jung', 'Mid', 'Adc', 'Sup']


def lol_tags(): return ['Fighter', 'Tank', 'Mage', 'Assassin', 'Marksman', 'Support']
