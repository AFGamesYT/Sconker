from time import sleep
from threading import Thread

import pygame

from math import pi, sqrt, sin, cos
from random import choices, uniform, random, randint

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


        angle = uniform(0, 2 * pi)
        radius = 0.42 * HEIGHT / 2
        r = radius * sqrt(random())
        x = r * cos(angle)
        y = r * sin(angle)

        self.position = (WIDTH/2 + x, HEIGHT/3 + y)

        self.size = randint(60, 75)  # TODO: (later) upgrade: "Make the conkers smaller. Makes more fit on the tree"
        # self.rotation = randint(0, 359)
        self.rotation = 0  # TODO: looks weird when rotated, because of the shadow. change this

        self.surface = pygame.transform.rotate(pygame.transform.scale(conker_t, (self.size, self.size)), self.rotation)
        self.surface_pos = (self.position[0]-self.size/2, self.position[1]-self.size/2)

        self.growing = True

    def __str__(self):
        return f"Conker: rarity={self.rarity}, multiplier={self.multiplier}, growing={self.growing}."

def spawn_conker(v=False):
    if not len(tree.conkers_on_tree) < tree.max_tree_conker_amount:  # check if there is space on the tree to grow
        if v: print("Not enough space on the tree")
        return

    if v: print("Waiting for conker to grow.")

    wiggle_room = 15

    new_conker = Conker()
    new_conker_rect = pygame.Rect(
        new_conker.surface_pos[0]-wiggle_room,
        new_conker.surface_pos[1]-wiggle_room,
        new_conker.surface.get_width()+wiggle_room,
        new_conker.surface.get_height()+wiggle_room)  # this sucks, but works


    found_spot = False
    while not found_spot and not tree.conkers_on_tree == []:  # genuinely what the fuck. TODO: fix it when the tree is full
        for c in tree.conkers_on_tree:
            c_rect = pygame.Rect(c.surface_pos[0],
                                 c.surface_pos[1],
                                 c.surface.get_width(),
                                 c.surface.get_height())  # this sucks, but works

            if new_conker_rect.colliderect(c_rect):
                new_conker = Conker()
                new_conker_rect = pygame.Rect(
                    new_conker.surface_pos[0]-wiggle_room,
                    new_conker.surface_pos[1]-wiggle_room,
                    new_conker.surface.get_width()+wiggle_room,
                    new_conker.surface.get_height()+wiggle_room)  # this sucks, but works

                break
        else:
            found_spot = True

    tree.conkers_on_tree.append(new_conker)

    sleep(tree.growth_time+randint(0, 3))  # TODO: think of a smarter way to vary the conker growth time
    if v: print("Conker finished growing.")

    new_conker.growing = False
    if v: print(new_conker)


def update():  # function to update variables and other things.
    global RARITIES, MULTIPLIERS
    RARITIES = {"common": common.chance, "rare": rare.chance, "ultra": ultra.chance}
    MULTIPLIERS = {"single": single.chance, "double": double.chance, "triple": triple.chance}


# for i in range(20):
#     spawn_conker_thread = Thread(target=spawn_conker, args=[True], daemon=True)
#     spawn_conker_thread.start()
#     sleep(tree.new_conker_appear_time)


pygame.init()


# textures
background_day_t = pygame.image.load("images/background_day.png")
sun_t = pygame.image.load("images/sun.png")
tree_ground_t = pygame.image.load("images/tree_ground.png")
shadow_t = pygame.image.load("images/shadow.png")
conker_t = pygame.image.load("images/conker.png")


# resolution
WIDTH = 1600
HEIGHT = 900

FPS = 120

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
no_frame_toggle = True  # TODO: remove this later

pygame.display.set_caption("Sconker")

clock = pygame.time.Clock()
run = True
fullscreen = True

while run:
    spawn_conker_thread = Thread(target=lambda: spawn_conker(), daemon=True)


    bg = screen.blit(pygame.transform.scale(
        background_day_t, (WIDTH, HEIGHT)), (0, 0))  # TODO: replace with day/night cycle

    sun_size = 150
    sun_pos = (WIDTH/4*3, HEIGHT/5*1)  # TODO: make sun move on an arc, change it to moon when it's nighttime

    sun = screen.blit(pygame.transform.scale(
        sun_t, (sun_size, sun_size)), sun_pos)


    tree_ground = screen.blit(pygame.transform.scale(
        tree_ground_t, (WIDTH, HEIGHT)), (0, 0))

    for conker in tree.conkers_on_tree:
        # shadow for the conker to see better
        screen.blit(pygame.transform.scale(
                shadow_t, (conker.size*1.7, conker.size*1.7)
            ), (conker.position[0]-conker.size*1.7/2, conker.position[1]-conker.size*1.7/2))

        # the conker
        screen.blit(conker.surface, conker.surface_pos)

        # print(f"drawing a conker on {conker.position}, with size {conker.size} and rotation {conker.rotation}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:  # TODO: remove this later
                if no_frame_toggle:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
                no_frame_toggle = not no_frame_toggle

            if event.key == pygame.K_r:
                spawn_conker_thread.start()


    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
