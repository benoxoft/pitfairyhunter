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

#Main Character of the game.

from pygame.sprite import Sprite, Group
from movement import Movement

import pygame
import math
import media

class MainChar(Sprite):

    def __init__(self):
        self.move = Movement(self, thrust_strength = 1800,
                             accelx = 900,
                             maxspeedx = 1000,
                             maxspeedy = 1000,
                             posx=50,
                             posy=50)
        self.hunter = media.load_image('hunter.png').convert_alpha()
        self.hunter_boost = media.load_image('hunter_boost.png').convert_alpha()
        self.firstupdate = False
        self.image = self.hunter
        self.rect = self.image.get_rect()
        self.imgflip = False
        self.dir = 1

        self.fuel = 10000
        self.lives = 3
        
        self.caught_fairies = Group()
        self.fairies_to_catch = Group()

        self.out_of_fuel_event = None
        self.no_more_life_event = None
        self.all_fairies_caught_event = None

    def set_init_pos(self):
        self.move.posx = 33
        self.move.posy = 50
        self.move.speedx = 0
        self.move.speedy = 0
        self.dir = 1
        self.flip()
        
    def flip(self):
        if not self.imgflip and self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.imgflip = True
        elif self.imgflip and self.dir == 1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.imgflip = False
        
    def moveleft(self, tick):
        self.dir = -1
        self.flip()

        if self.move.speedy == 0:
            self.move.moveleft(tick)
        
    def moveright(self, tick):
        self.dir = 1
        self.flip()
        if self.move.speedy == 0:
            self.move.moveright(tick)
        
    def thrust(self, tick):
        if self.fuel > 0:
            self.image = self.hunter_boost
            self.imgflip = False
            self.flip()
            self.firstupdate = True
            if self.imgflip:
                self.move.moveleft(tick / 2)
            else:
                self.move.moveright(tick / 2)
            self.move.thrust(tick)
            self.fuel -= tick / 8
        else:
            self.fuel = 0
            self.out_of_fuel_event()
        
    def update(self, tick):
        if not self.firstupdate:
            self.image = self.hunter
            self.imgflip = False
            self.flip()
        self.firstupdate = False
        
        self.move.calculate_movement(tick)

        if self.move.speedx > 0:
            self.move.speedx -= 1
        elif self.move.speedx < 0:
            self.move.speedx += 1
            
        self.rect.x = self.move.posx
        self.rect.y = self.move.posy

        self.catch_fairies()
        
    def raise_out_of_fuel_event(self):
        self.out_of_fuel_event()

    def raise_no_more_life_event(self):
        self.no_more_life_event()

    def raise_all_fairies_caught_event(self):
        self.all_fairies_caught_event()

    def remove_life(self):
        self.lives -= 1
        if self.lives == 0:
            self.raise_no_more_life_event()
        
    def catch_fairies(self):
        for f in self.fairies_to_catch:
            dist = math.sqrt((f.rect.centerx - self.rect.centerx)**2 + (f.rect.centery - self.rect.centery)**2)
            if dist < 20:
                f.kill()
                self.caught_fairies.add(f)
        if len(self.fairies_to_catch) == 0:
            self.raise_all_fairies_caught_event()
            
