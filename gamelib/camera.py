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

class Camera(Rect):

    def __init__(self, sprite_to_follow):
        Rect.__init__(self, 0, 0, 800, 600)
        self.sprite_to_follow = sprite_to_follow
        self.level = None

    def set_init_pos(self):
        self.x = 0
        self.y = 0
        
    def update(self):
        self.centery = self.sprite_to_follow.rect.centery
        if self.top < 0:
            self.top = 0
        if self.bottom > self.level.height:
            self.bottom = self.level.height
