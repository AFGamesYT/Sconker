from time import sleep
from threading import Thread

import pygame

from math import pi, sqrt, sin, cos
from random import choices, uniform, random, randint

from playsound3 import playsound

class ConkerModifier:
    def __init__(self, name, mod_type, chance, multiplier):
        self.name = name
        self.type = mod_type
        self.chance = chance
        self.multiplier = multiplier


common = ConkerModifier("common", "rarity", 80, 1)
rare = ConkerModifier("rare", "rarity", 15, 1.5)
ultra = ConkerModifier("ultra", "rarity", 5, 2.5)

single = ConkerModifier("single", "amount", 80, 1)
double = ConkerModifier("double", "amount", 15, 2)
triple = ConkerModifier("triple", "amount", 5, 3)


RARITIES = {"common": common.chance, "rare": rare.chance, "ultra": ultra.chance}
MULTIPLIERS = {"single": single.chance, "double": double.chance, "triple": triple.chance}

class Tree:
    def __init__(self):
        self.growth_time = 5
        self.max_tree_conker_amount = 17
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
        radius = 0.53 * HEIGHT / 2
        r = radius * sqrt(random())
        x = r * cos(angle)
        y = r * sin(angle)

        self.position = (WIDTH/2 + x, HEIGHT*2/5 + y)

        self.size = randint(60, 75)  # TODO: (later) upgrade: "Make the conkers smaller. Makes more fit on the tree"
        self.actual_size = 0
        # self.rotation = randint(0, 359)
        self.rotation = 0  # TODO: looks weird when rotated, because of the shadow. change this

        self.surface = pygame.transform.rotate(pygame.transform.scale(conker_t, (self.size, self.size)), self.rotation)
        self.surface_pos = [self.position[0]-self.actual_size/2, self.position[1]-self.actual_size/2]

        self.growing = True
        self.grow_time = tree.growth_time + randint(0, 2)
        self.spawn_time = pygame.time.get_ticks()

    def update_surface_pos(self):
        self.surface_pos = [self.position[0]-self.actual_size/2, self.position[1]-self.actual_size/2]

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


    sleep(new_conker.grow_time)
    playsound("sounds/conker_grow.mp3", block=False)
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
        ticks = pygame.time.get_ticks()

        if conker.growing:
            grown_percent = (ticks - conker.spawn_time) / (conker.grow_time * 1000)
        else:
            grown_percent = 1
        
        shadow_size = conker.size*1.7*grown_percent
        
        screen.blit(pygame.transform.scale(
                shadow_t, (shadow_size, shadow_size)
            ), (conker.position[0]-shadow_size/2, conker.position[1]-shadow_size/2))


        # the conker
        if conker.growing:
            conker.actual_size = conker.size*grown_percent
            conker.update_surface_pos()

            # print(f"target size: {conker.size} | grown percent: {grown_percent*100}% | ticks since conker spawned: {ticks-conker.spawn_time} | conker size: {conker.size*grown_percent}")

            # time passed since the conker spawned / milliseconds per 1 growth step

            screen.blit(pygame.transform.rotate(
                pygame.transform.scale(conker_t, (

                    conker.actual_size,
                    conker.actual_size)

                ), conker.rotation), conker.surface_pos)
        else:
            screen.blit(conker.surface, conker.surface_pos)


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
