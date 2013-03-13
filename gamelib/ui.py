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

from pygame.surface import Surface
import pygame
import math
import media

class GameUI:
    def __init__(self, mainchar):
        self.bg = Surface((600, 1600))
        self.statusbar = Surface((200, 600))
        self.mainchar = mainchar
        self.widget = []
        self.create_bg()
    
    def create_bg(self):
        rbg = self.bg.get_rect()
        bgimg = media.load_image('bg.png').convert()
        rbgimg = bgimg.get_rect()
        columns = int(rbg.width / rbgimg.width) + 1
        rows = int(rbg.height / rbgimg.height) + 1
        
        for y in xrange(rows):
            for x in xrange(columns):
                if x == 0 and y > 0:
                    rbgimg = rbgimg.move([-(columns -1 ) * rbgimg.width, rbgimg.height])
                if x > 0:
                    rbgimg = rbgimg.move([rbgimg.width, 0])
                self.bg.blit(bgimg, rbgimg)
                        
    def update(self):
        r = pygame.rect.Rect(0, 0, 200, 100)
        
        for w in self.widget:
            w.update()
            self.statusbar.blit(w.image, r)
            r = r.move((0, 100))
            
class InfoWidget(pygame.sprite.Sprite):

    def __init__(self, bg, font):
        pygame.sprite.Sprite.__init__(self)
        self.title = ''
        self.data = ''
        self.bg = bg
        self.font = font
        self.image = Surface((200, 100))

    def update(self):
        self.image.blit(self.bg, (0,0))
        titleimg = self.font.render(self.title, True, (255,255,255))
        dataimg = self.font.render(self.data, True, (255,255,255))
        self.image.blit(titleimg, titleimg.get_rect().move(20, 20))
        self.image.blit(dataimg, dataimg.get_rect().move(60, 60))
    
class DepthInfoWidget(InfoWidget):

    def __init__(self, bg, font, mainchar):
        InfoWidget.__init__(self, bg, font)
        self.title = 'Depth:'
        self.level = None
        self.mainchar = mainchar
        
    def update(self):
        depth = int(self.mainchar.move.posy / 100) + 1
        depthTotal = int(self.level.height / 100)
        self.data = str(depth) + ' / ' + str(depthTotal) + ' m'
        InfoWidget.update(self)

class FuelInfoWidget(InfoWidget):

    def __init__(self, bg, font, mainchar):
        InfoWidget.__init__(self, bg, font)
        self.title = 'Fuel left:'
        self.mainchar = mainchar
        
    def update(self):
        self.data = str(self.mainchar.fuel)
        InfoWidget.update(self)

class FairyInfoWidget(InfoWidget):

    def __init__(self, bg, font, mainchar):
        InfoWidget.__init__(self, bg, font)
        self.title = 'Fairies left:'
        self.mainchar = mainchar
        
    def update(self):
        self.data = str(len(self.mainchar.fairies_to_catch))
        InfoWidget.update(self)

class LivesInfoWidget(InfoWidget):

    def __init__(self, bg, font, mainchar):
        InfoWidget.__init__(self, bg, font)
        self.title = 'Lives:'
        self.mainchar = mainchar
                        
    def update(self):
        self.data = str(self.mainchar.lives)
        InfoWidget.update(self)
        
class SpeedInfoWidget(InfoWidget):

    def __init__(self, bg, font, mainchar):
        InfoWidget.__init__(self, bg, font)
        self.title = 'Speed:'
        self.mainchar = mainchar
        self.nextupdate = 0
        
    def update(self):
        if self.nextupdate == 0:
            ms = int(self.mainchar.move.get_speed() / 100)
            kmh = ms / 1000.0 * 3600.0
            self.data = str(kmh) + ' km/h'
            InfoWidget.update(self)
            self.nextupdate = 10
        self.nextupdate -= 1

class LevelInfoWidget(InfoWidget):

    def __init__(self, bg, font):
        InfoWidget.__init__(self, bg, font)
        self.title = 'Level:'
        self.level = None
        
    def update(self):
        self.data = self.level.name
        InfoWidget.update(self)

    
