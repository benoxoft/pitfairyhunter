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
from pygame.rect import Rect

from movement import Movement

import media

class Ghost(Sprite):

    def __init__(self, posx, posy):
        Sprite.__init__(self)
        self.move = Movement(self, thrust_strength = 1000,
                             accelx = 1000,
                             accely = 1000,
                             maxspeedx = 60,
                             maxspeedy = 60,
                             gravity = 0,
                             posx = posx,
                             posy = posy)
        self.ghost1 = media.load_image('ghost1.png')
        self.ghost2 = media.load_image('ghost2.png')
        self.image = self.ghost1
        self.rect = self.image.get_rect()
        self.currentframe = 1
        
    def update(self, tick):
        if self.currentframe >= 1 and self.currentframe <= 4:
            self.image = self.ghost2
        elif self.currentframe >= 5 and self.currentframe <= 8:
            self.image = self.ghost1
        self.currentframe += 1
        if self.currentframe == 9:
            self.currentframe = 1

        self.brain.update(tick)
        self.move.calculate_movement(tick)
        self.rect.x = self.move.posx
        self.rect.y = self.move.posy        
