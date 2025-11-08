from random import choices
from time import sleep
from threading import Thread

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
        self.multiplier = 2.5

ultra = Ultra()

class Single:
    def __init__(self):
        self.chance = 80
        self.multiplier = 1

single = Single()

class Double:
    def __init__(self):
        self.chance = 15
        self.multiplier = 2

double = Double()

class Triple:
    def __init__(self):
        self.chance = 5
        self.multiplier = 3

triple = Triple()


RARITIES = {"common": common.chance, "rare": rare.chance, "ultra": ultra.chance}
MULTIPLIERS = {"single": single.chance, "double": double.chance, "triple": triple.chance}


class Tree:
    def __init__(self):
        self.growth_time = 5
        self.max_tree_conker_amount = 10
        self.new_conker_appear_time = 1

        self.conkers_on_tree: list[Conker] = []

tree = Tree()

class Conker:
    def __init__(self):
        self.rarity = choices(
            list(RARITIES.keys()),
            weights=list(RARITIES.values())
        )[0]

        self.multiplier = choices(
            list(MULTIPLIERS.keys()),
            weights=list(MULTIPLIERS.values())
        )[0]

        self.growing = True

    def __str__(self):
        return f"Conker: rarity={self.rarity}, multiplier={self.multiplier}, growing={self.growing}."

def spawn_conker(v=False):
    if not len(tree.conkers_on_tree) < tree.max_tree_conker_amount:  # check if there is space on the tree to grow
        if v: print("Not enough space on the tree")
        return


    if v: print("Waiting for conker to grow.")
    conker = Conker()
    tree.conkers_on_tree.append(conker)

    sleep(tree.growth_time)
    if v: print("Conker finished growing.")

    conker.growing = False
    if v: print(conker)



for i in range(20):
    spawn_conker_thread = Thread(target=spawn_conker, args=[True], daemon=True)
    spawn_conker_thread.start()
    sleep(tree.new_conker_appear_time)
