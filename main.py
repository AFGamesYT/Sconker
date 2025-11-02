from random import choices

class Conker:
    def __init__(self):
        self.RARITIES = {"common": 80, "rare": 15, "ultra": 5}

        self.rarity = choices(list(self.RARITIES.keys()), weights=list(self.RARITIES.values()))[0]
