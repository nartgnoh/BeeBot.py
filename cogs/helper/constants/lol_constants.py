# *********************************************************************************************************************
# lolconstants.py
# import cogs.helper.constants.lol_constants as lol_constants
# *********************************************************************************************************************

# *********************************************************************************************************************
# Riot Constants
# *********************************************************************************************************************

def riot_regions(): return ['br1', 'eun1', 'euw1',
                            'jp1', 'kr', 'la1', 'la2', 'na1', 'oc1', 'tr1', 'ru']


def riot_ranks(): return {1: {'tier': 'IRON', 'rank': 'I'},
                          2: {'tier': 'IRON', 'rank': 'II'},
                          3: {'tier': 'IRON', 'rank': 'III'},
                          4: {'tier': 'IRON', 'rank': 'IV'},
                          5: {'tier': 'BRONZE', 'rank': 'I'},
                          6: {'tier': 'BRONZE', 'rank': 'II'},
                          7: {'tier': 'BRONZE', 'rank': 'III'},
                          8: {'tier': 'BRONZE', 'rank': 'IV'},
                          9: {'tier': 'SILVER', 'rank': 'I'},
                          10: {'tier': 'SILVER', 'rank': 'II'},
                          11: {'tier': 'SILVER', 'rank': 'III'},
                          12: {'tier': 'SILVER', 'rank': 'IV'},
                          13: {'tier': 'GOLD', 'rank': 'I'},
                          14: {'tier': 'GOLD', 'rank': 'II'},
                          15: {'tier': 'GOLD', 'rank': 'III'},
                          16: {'tier': 'GOLD', 'rank': 'IV'},
                          17: {'tier': 'PLATINUM', 'rank': 'I'},
                          18: {'tier': 'PLATINUM', 'rank': 'II'},
                          19: {'tier': 'PLATINUM', 'rank': 'III'},
                          20: {'tier': 'PLATINUM', 'rank': 'IV'},
                          21: {'tier': 'DIAMOND', 'rank': 'I'},
                          22: {'tier': 'DIAMOND', 'rank': 'II'},
                          23: {'tier': 'DIAMOND', 'rank': 'III'},
                          24: {'tier': 'DIAMOND', 'rank': 'IV'},
                          25: {'tier': 'MASTER', 'rank': 'I'},
                          26: {'tier': 'MASTER', 'rank': 'II'},
                          27: {'tier': 'MASTER', 'rank': 'III'},
                          28: {'tier': 'MASTER', 'rank': 'IV'},
                          29: {'tier': 'GRANDMASTER', 'rank': 'I'},
                          30: {'tier': 'GRANDMASTER', 'rank': 'II'},
                          31: {'tier': 'GRANDMASTER', 'rank': 'III'},
                          32: {'tier': 'GRANDMASTER', 'rank': 'IV'},
                          33: {'tier': 'CHALLENGER', 'rank': 'I'},
                          34: {'tier': 'CHALLENGER', 'rank': 'II'},
                          35: {'tier': 'CHALLENGER', 'rank': 'III'},
                          36: {'tier': 'CHALLENGER', 'rank': 'IV'}
                          }


# *********************************************************************************************************************
# League of Legends Constants
# *********************************************************************************************************************

def lol_keys(): return ['Q', 'W', 'E', 'R']


def lol_roles(): return ['Top', 'Jung', 'Mid', 'Adc', 'Sup', 'Fill']


def lol_tags(): return ['Fighter', 'Tank', 'Mage',
                        'Assassin', 'Marksman', 'Support']
