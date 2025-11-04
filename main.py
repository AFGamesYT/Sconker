from random import choices

class Common:
    def __init__(self):
        self.chance = 80
        self.multiplier = 1

common = Common()

class Rare:
    def __init__(self):
        self.chance = 15
        self.multiplier = 1.5

rare = Rare()

class Ultra:
    def __init__(self):
        self.chance = 5
        self.multiplier = 7

ultra = Ultra()

class Conker:
    def __init__(self):
        self.RARITIES = {"common": common.chance, "rare": rare.chance, "ultra": ultra.chance}

        self.rarity = choices(
            list(self.RARITIES.keys()),
            weights=list(self.RARITIES.values())
        )[0]

