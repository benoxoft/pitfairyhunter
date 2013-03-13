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

import pygame
import media

class Wall(Sprite):

    def __init__(self, x, y, h, w):
        Sprite.__init__(self)
        tile = media.load_image('tile_wall.png').convert()
        rtile = tile.get_rect()
        self.rect = pygame.rect.Rect(x, y, h, w)
        self.image = pygame.surface.Surface((self.rect.width, self.rect.height))
                        
        columns = int(self.rect.width / rtile.width) + 1
        rows = int(self.rect.height / rtile.height) + 1
        
        for y in xrange(rows):
            for x in xrange(columns):
                if x == 0 and y > 0:
                    rtile = rtile.move([-(columns -1 ) * rtile.width, rtile.height])
                if x > 0:
                    rtile = rtile.move([rtile.width, 0])
                self.image.blit(tile, rtile)

    def update(self, tick):
        pass
    
