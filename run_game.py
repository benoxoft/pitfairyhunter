#! /usr/bin/env python

#    Copyright (C) 2010  Benoit <benoxoft> Paquet
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
import pygame

from gamelib.MainChar import MainChar
from gamelib.wall import Wall
from gamelib.camera import Camera
from gamelib.fairy import Fairy
from gamelib.level import *
from gamelib.ui import *
from gamelib.brain import *
from gamelib import media

class GameControl:

    def __init__(self):
        self.leftKeyDown = False
        self.rightKeyDown = False
        self.upKeyDown = False
        self.keepPlaying = True

    def reset(self):
        self.leftKeyDown = False
        self.rightKeyDown = False
        self.upKeyDown = False
        self.keepPlaying = True
        
def show_message(msg):
    draw(0)
    font = media.get_font(44)
    s = font.render(msg, True, (255,255,255))
    screen.blit(s, (300 - s.get_width() / 2, 200))
    pygame.display.update()
    pygame.time.delay(1500)
    clock.tick()

def show_intro():
    draw(1)
    w = Surface((640, 460))
    w.fill(pygame.color.Color('black'))
    w.blit(logo, (0,0))
    font = media.get_font(16)
    
    l1 = font.render('Use the arrow keys to move', True, (255,255,255))
    l2 = font.render('Press <spacebar> to activate your jetpack', True, (255,255,255))
    l3 = font.render('*** You need your jetpack to move in the air! ***', True, (255,255,255))
    l4 = font.render('Catch all fairies!' , True, (255,255,255))
    l5 = font.render('Avoid ghosts!', True, (255,255,255))

    lspace = font.render('Press <spacebar> to play', True, (255,255,255))
    lesc = font.render('Press <Esc> to quit', True, (255,255,255))
    lname = media.get_font(10).render('Everything by Benoit <benoxoft> Paquet', True, (255,255,255))

    x = 80
    w.blit(l1, (x, 180))
    w.blit(l2, (x, 210))
    w.blit(l3, (x, 240))
    w.blit(l4, (x, 290))
    w.blit(l5, (x, 320))
    
    w.blit(lspace, (30, 380))
    w.blit(lesc, (420, 380))
    w.blit(lname, (320 - lname.get_width() / 2, 440))
    
    screen.blit(w, (80, 80))    
    pygame.display.update()

    waiting = True    
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_SPACE:
                    waiting = False
                elif e.key == pygame.K_ESCAPE:
                    import sys
                    sys.exit(0)
        
    pygame.time.delay(100)
    clock.tick()
    
def ghost_kill():
    show_message('Oww...')
    mainchar.remove_life()
    kill_level(levels.level)
    load_level(levels.reload_level())
    
def out_of_fuel():
    show_message('Out of fuel!')
    mainchar.remove_life()
    kill_level(levels.level)
    load_level(levels.reload_level())

def no_more_life():
    show_message('Game Over!')
    pygame.time.delay(1500)
    
    kill_level(levels.level)
    levels.restore_all_levels()
    load_level(levels.get_next_level())
    mainchar.lives = 3
    show_intro()
    
def all_fairies_caught():
    show_message('Caught all fairies!')
    kill_level(levels.level)
    if len(levels.levels) == 0:
        show_message('You won the game!')
        pygame.time.delay(1500)
        levels.restore_all_levels()
        load_level(levels.get_next_level())
        mainchar.lives = 3
        show_intro()
    else:
        n = levels.get_next_level()
        load_level(n)

def load_level(level):
    cam.level = level
    levelWidget.level = level
    depthWidget.level = level
    mainchar.move.add(level.walls)
    mainchar.fairies_to_catch.add(level.fairies)
    mainchar.set_init_pos()
    mainchar.fuel = 10000
    cam.set_init_pos()
    for fairy in level.fairies:
        fairy.brain = FairyBrain(fairy, mainchar)
        fairy.move.add(level.walls)

    for ghost in level.ghosts:
        ghost.brain = GhostBrain(ghost, mainchar)
        ghost.brain.kill_event = ghost_kill
        ghost.move.add(level.boundaries)

    level.pack()

def kill_level(level):
    mainchar.move.empty()
    mainchar.fairies_to_catch.empty()
    mainchar.caught_fairies.empty()
    pygame.event.get()
    g.reset()
    
def draw(tick):
    level = levels.level
    
    if tick > 0:
        mainchar.update(tick)
        cam.update()
        ui.update()
        
    screen.blit(ui.bg, pygame.rect.Rect(0, -int(float(cam.y)/level.height*800), cam.w, cam.h))
    screen.blit(ui.statusbar, pygame.rect.Rect(600, 0, 200, 600))

    screen.blit(mainchar.image,
                    pygame.rect.Rect(mainchar.rect.x - cam.x,
                             mainchar.rect.y - cam.y,
                             mainchar.rect.w - cam.w,
                             mainchar.rect.h - cam.h))


    draw_elements(level.walls, tick)
    draw_elements(level.fairies, tick)
    draw_elements(level.ghosts, tick)
        
    pygame.display.update()
    pygame.time.delay(16)

def draw_elements(elements, tick):
    for element in elements:
        if tick > 0:
            element.update(tick)            
        screen.blit(element.image,
                        pygame.rect.Rect(element.rect.x - cam.x,
                                       element.rect.y - cam.y,
                                       element.rect.w - cam.w,
                                       element.rect.h - cam.h))


def main():
    
    while g.keepPlaying:
        tick = clock.tick()

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    g.leftKeyDown = True
                elif e.key == pygame.K_RIGHT:
                    g.rightKeyDown = True
                elif e.key == pygame.K_SPACE:
                    g.upKeyDown = True
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT:
                    g.leftKeyDown = False
                elif e.key == pygame.K_RIGHT:
                    g.rightKeyDown = False
                elif e.key == pygame.K_SPACE:
                    g.upKeyDown = False
                elif e.key == pygame.K_ESCAPE:
                  g.keepPlaying = False  

        if g.leftKeyDown:
            mainchar.moveleft(tick)
        if g.rightKeyDown:
            mainchar.moveright(tick)
        if g.upKeyDown:
            mainchar.thrust(tick)
        draw(tick)

if __name__ == '__main__':    
    pygame.init()

    #game objects
    #screen = pygame.display.set_mode((800, 600))
    screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN | pygame.HWSURFACE)

    pygame.display.set_caption('Pitfairy Hunter!')
    pygame.mouse.set_visible(False)
    
    g = GameControl()
    
    #main character
    mainchar = MainChar()
    mainchar.out_of_fuel_event = out_of_fuel
    mainchar.no_more_life_event = no_more_life
    mainchar.all_fairies_caught_event = all_fairies_caught

    logo = media.load_image('logo2.png')
    
    font = media.get_font(20)
    img = media.load_image('StatusBar.png').convert()
    rimg = img.get_rect()

    ui = GameUI(mainchar)
    cam = Camera(mainchar)

    depthWidget = DepthInfoWidget(img, font, mainchar)
    levelWidget = LevelInfoWidget(img, font)

    ui.widget.append(levelWidget)
    ui.widget.append(FuelInfoWidget(img, font, mainchar))
    ui.widget.append(depthWidget)
    ui.widget.append(SpeedInfoWidget(img, font, mainchar))
    ui.widget.append(FairyInfoWidget(img, font, mainchar))
    ui.widget.append(LivesInfoWidget(img, font, mainchar))

    levels = Levels()
    load_level(levels.get_next_level())

    clock = pygame.time.Clock()

    show_intro()
    main()
