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
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from fairy import Fairy
from ghost import Ghost
from wall import Wall

class Levels:

    def __init__(self):
        self.levels = []
        self.level = None
        self.restore_all_levels()
        
    def get_next_level(self):
        lvl = self.levels.pop(0)
        self.level = lvl()
        return self.level

    def reload_level(self):
        self.level = type(self.level)()
        return self.level

    def restore_all_levels(self):
        self.levels = [Level1, Level2, Level3]
        
class BaseLevel(object):
    
    def __init__(self, height, levelname):
        self.height = height
        self.width = 600
        self.name = levelname
        self.walls = Group()
        self.boundaries = Group()
        self.create_walls()
        self.fairies = Group()
        self.ghosts = Group()
        self.fiends = Group()
        self.game_elements = Group()
        
    def create_walls(self):
        startPlatform = Wall(0, 110, 130, 60)
        wallTop = Wall(0, 0, self.width, 32)
        wallBottom = Wall(0, self.height - 32, self.width, 32)
        wallLeft = Wall(0, 0, 32, self.height)
        wallRight = Wall(self.width - 32, 0, 32, self.height)
        self.walls.add((startPlatform, wallTop, wallBottom, wallLeft, wallRight))
        self.boundaries.add((wallTop, wallBottom, wallLeft, wallRight))


    def pack(self):
        self.game_elements.add(self.fairies)
        self.game_elements.add(self.ghosts)
        self.game_elements.add(self.walls)
        self.game_elements.add(self.fiends)

class Level1(BaseLevel):

    def __init__(self):
        BaseLevel.__init__(self, 2400, '1')
        self.add_walls()
        self.add_fairies()
        self.add_ghosts()
        
    def add_walls(self):
        self.walls.add((Wall(0, 700, 400, 64),
                        Wall(300, 900, 300, 64),
                        Wall(100, 1100, 260, 260),
                        Wall(150, 1500, 300, 64),
                        Wall(300, 1900, 160, 300)
                        ))
        
    def add_fairies(self):
            self.fairies.add(Fairy(500, 2300))
            self.fairies.add(Fairy(200, 2300))
        
    def add_ghosts(self):
            self.ghosts.add(Ghost(100, 1000))
            self.ghosts.add(Ghost(500, 2300))

class Level2(BaseLevel):

    def __init__(self):
        BaseLevel.__init__(self, 5000, '2')
        self.add_walls()
        self.add_fairies()
        self.add_ghosts()
        
    def add_walls(self):
        self.walls.add((Wall(102, 300, 64, 1200),
                        Wall(268, 300, 64, 1200),
                        Wall(434, 300, 64, 1200),
                        Wall(100, 1800, 400, 64),
                        Wall(200, 2300, 200, 800),
                        Wall(200, 3100, 200, 800)
                        ))
        
    def add_fairies(self):
            self.fairies.add(Fairy(500, 2300))
            self.fairies.add(Fairy(200, 2300))
        
    def add_ghosts(self):
            self.ghosts.add(Ghost(300, 1000))
            self.ghosts.add(Ghost(300, 3000))
            self.ghosts.add(Ghost(300, 4200))
            self.ghosts.add(Ghost(200, 4800))

class Level3(BaseLevel):

    def __init__(self):
        BaseLevel.__init__(self, 4000, '3')
        self.add_walls()
        self.add_fairies()
        self.add_ghosts()
        
    def add_walls(self):
        w1 = Wall(0, 2800, 280, 160)
        w2 = Wall(320, 2800, 280, 160)
        w3 = Wall(100, 3900, 100, 100)
        w4 = Wall(400, 3900, 100, 100)
        self.walls.add((Wall(200, 1500, 200, 1000),
                        Wall(230, 2500, 140, 60),
                        Wall(260, 2560, 80, 60),
                        Wall(290, 2620, 20, 20),
                        Wall(170, 2440, 260, 60),
                        Wall(140, 2380, 320, 60),
                        Wall(110, 2320, 380, 60),
                        Wall(80, 2260, 440, 60),
                        Wall(200, 3200, 200, 200),
                        w1, w2, w3, w4
                        ))
        self.boundaries.add((w1, w2, w3, w4))
        
    def add_fairies(self):
            self.fairies.add(Fairy(500, 3400))
            self.fairies.add(Fairy(200, 3400))
        
    def add_ghosts(self):
            self.ghosts.add(Ghost(300, 3400))
            self.ghosts.add(Ghost(300, 3400))
        
class LevelTest(BaseLevel):
    def __init__(self):
        BaseLevel.__init__(self, 3000, 'Test')
        self.add_walls()
        self.add_fairies()
        self.add_ghosts()
        
    def add_walls(self):
        self.walls.add((Wall(200, 1150, 400, 64),
                        Wall(0, 1000, 200, 32),
                        Wall(100, 800, 130, 120)
                        ))
        
    def add_fairies(self):
        for i in range(1, 4):
            self.fairies.add(Fairy(300, 2500))
        
    def add_ghosts(self):
        for i in range(1,3):
            self.ghosts.add(Ghost(300, 2500))
            
    def add_fiends(self):
        pass
    
