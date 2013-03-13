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

from pygame.sprite import Sprite
from movement import Movement

import media

class Fairy(Sprite):

    def __init__(self, posx, posy):
        Sprite.__init__(self)
        self.move = Movement(self, thrust_strength = 15000,
                             accelx = 3800,
                             maxspeedx = 2000,
                             maxspeedy = 2500,
                             posx=posx,
                             posy=posy)
        self.brain = None
        self.fairy_wingup = media.load_image('fairy_wingup.png')
        self.fairy_wingmid = media.load_image('fairy_wingmid.png')
        self.fairy_wingdown = media.load_image('fairy_wingdown.png')
        self.image = self.fairy_wingup
        self.rect = self.image.get_rect()
        self.currentframe = 1
        
    def update(self, tick):
        if self.currentframe == 1:
            self.image = self.fairy_wingup
        elif self.currentframe == 2:
            self.image = self.fairy_wingmid
        elif self.currentframe == 3:
            self.image = self.fairy_wingdown
        self.currentframe += 1
        if self.currentframe == 4:
            self.currentframe = 1
            
        self.brain.update(tick)
        self.move.calculate_movement(tick)
        self.rect.x = self.move.posx
        self.rect.y = self.move.posy
                
