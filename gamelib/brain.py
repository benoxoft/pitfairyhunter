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
from movement import Movement
import math
import random

class FairyBrain:

    def __init__(self, fairy, mainchar):
        self.fairy = fairy
        self.move = fairy.move
        self.mainchar = mainchar
        self.next_thrust = 0
        self.next_move = 0
        self.next_flee = 0
        self.dist_hunter = 0
        
    def update(self, tick):
        if self.detect_hunter() and self.next_flee <= 0:
            self.flee(tick)
            self.next_flee = -1
        else:
            self.live_life_peacefully(tick)
            if self.next_flee == -1:
                self.next_flee = random.randint(40, 300)
            elif self.next_flee > 0:
                self.next_flee -= 1
                
    def live_life_peacefully(self, tick):
        if self.next_move == 0:
            goleft = (self.move.maxspeedx + self.move.speedx)
            goright = self.move.maxspeedx - self.move.speedx
            xdir = random.randint(0, goleft + goright)
            if xdir < goleft:
                self.move.moveleft(tick)
            else:
                self.move.moveright(tick)
            self.next_move = random.randint(1,3)
        self.next_move -= 1
        
        goup = (self.move.maxspeedy + self.move.speedy)
        godown = self.move.maxspeedy - self.move.speedy
        ydir = random.randint(0, goup + godown)
        if ydir < goup:
            if self.next_thrust == 0:
                self.move.thrust(tick)
                self.next_thrust = random.randint(1,17)
            self.next_thrust -= 1

    def detect_hunter(self):
        fx = self.fairy.rect.centerx 
        fy = self.fairy.rect.centery
        hx = self.mainchar.rect.centerx
        hy = self.mainchar.rect.centery

        self.dist_hunter = math.sqrt((fx - hx)**2 + (fy - hy)**2)
        if self.dist_hunter > 120:
            return False
        
        if fx < hx:
            #fairy is on the left
            if fy > hy:
                #fairy is at bottom
                xpos = self.fairy.rect.right
                ypos = self.mainchar.rect.bottom
                width = self.mainchar.rect.x - self.fairy.rect.right
                height = self.fairy.rect.top - self.mainchar.rect.bottom
                detect_dir = 1                
            else:
                #hunter is at bottom
                xpos = self.fairy.rect.right
                ypos = self.fairy.rect.bottom
                width = self.mainchar.rect.x - self.fairy.rect.right
                height = self.mainchar.rect.top - self.fairy.rect.bottom
                detect_dir = -1
        else:
            #hunter is on the left
            if fy > hy:
                #fairy is at bottom
                xpos = self.mainchar.rect.right
                ypos = self.mainchar.rect.bottom
                width = self.fairy.rect.x - self.mainchar.rect.right
                height = self.fairy.rect.top - self.mainchar.rect.bottom
                detect_dir = -1
            else:
                #hunter is at bottom
                xpos = self.mainchar.rect.right
                ypos = self.fairy.rect.bottom
                width = self.fairy.rect.x - self.mainchar.rect.right
                height = self.mainchar.rect.top - self.fairy.rect.bottom
                detect_dir = 1
                
        view_rect = Rect(xpos, ypos, width, height)

        points = []
        hyp = int(math.sqrt(view_rect.width**2 + view_rect.height**2))
        if hyp == 0:
            return False
        
        x_angle = math.asin(float(view_rect.width) / hyp)
        y_angle = math.asin(float(view_rect.height) / hyp)
        checks = int(hyp / 20) + 1
        sinx = math.sin(x_angle)
        siny = math.sin(y_angle)
        can_see = True
        for i in range(0, checks):
            x_move = sinx * 20.0 * i
            y_move = siny * 20.0 * i
            if detect_dir == -1:
                x_point = view_rect.x + x_move
                y_point = view_rect.top + y_move
            else:
                x_point = view_rect.x + x_move
                y_point = view_rect.bottom - y_move

            for w in self.move.sprites():
                if w.rect.collidepoint(x_point, y_point):
                    can_see = False

        return can_see
    
    def flee(self, tick):
            
        if self.mainchar.move.posx > self.move.posx: #and len(self.move.bumping_walls) > 0:
            self.move.moveleft(tick)
        else:
            self.move.moveright(tick)

        if self.mainchar.move.posy > self.move.posy: #and len(self.move.bumping_walls) > 0:
            if self.next_thrust == 0:
                self.move.thrust(tick)
                self.next_thrust = random.randint(1,9)
            self.next_thrust -= 1
            
class GhostBrain:

    def __init__(self, ghost, mainchar):
        self.ghost = ghost
        self.move = ghost.move
        self.mainchar = mainchar
        self.nextaction = 0

        self.kill_event = None
        
    def update(self, tick):
        distance = math.sqrt(
            abs(self.ghost.rect.centerx - self.mainchar.rect.centerx)**2 +
            abs(self.ghost.rect.centery - self.mainchar.rect.centery)**2)
        if distance <= 160:
            if distance <= 12:
                self.kill_event()
            self.attack()
        else:
            self.nextaction -= tick
            if self.nextaction <= 0:
                self.patrol()
                self.nextaction = random.randint(200, 3000)
            
    def patrol(self):
        self.move.maxspeedx = 100
        self.move.maxspeedy = 100

        dist = []
        for w in self.move:
            dist.append((w, math.sqrt(w.rect.centerx**2 + w.rect.centery**2)))

        closest = dist[0]
        farthest = dist[1]
            
        for w, d in dist:
            if d < closest[1]:
                closest = (w, d)
            if d > farthest[1]:
                farthest = (w, d)

        direction = random.randint(1, 2)
        goup = True
        goleft = True
        
        if direction == 1: #move away from closest
            w = closest[0]
            if w.rect.centerx > self.ghost.rect.centerx:
                goleft = False
            elif w.rect.centerx < self.ghost.rect.centerx:
                goleft = False
            if w.rect.centery > self.ghost.rect.centery:
                goup = True
            elif w.rect.centery < self.ghost.rect.centery:
                goup = True
            
        elif direction == 2: #move to farthest
            w = farthest[0]
            if w.rect.centerx > self.ghost.rect.centerx:
                goleft = True
            elif w.rect.centerx < self.ghost.rect.centerx:
                goleft = True
            if w.rect.centery > self.ghost.rect.centery:
                goup = False
            elif w.rect.centery < self.ghost.rect.centery:
                goup = False
            
        direction = random.randint(1, 3)
        if direction == 1 or direction == 3: #move up or down
            if direction != 3:
                self.move.speedx = 0
            if goup:
                self.move.thrust(1000)
            else:
                self.move.movedown(1000)
        if direction == 2 or direction == 3: #move left or right
            if direction != 3:
                self.move.speedy = 0
            if goleft:
                self.move.moveleft(1000)
            else:
                self.move.moveright(1000)
        
    def attack(self):
        self.move.maxspeedx = 120
        self.move.maxspeedy = 120
        
        if self.ghost.rect.centerx - 3 > self.mainchar.rect.centerx:
            self.move.moveleft(1000) #goleft
        elif self.ghost.rect.centerx + 3 < self.mainchar.rect.centerx:
            self.move.moveright(1000) #goright
        else:
            self.move.speedx = 0
        if self.ghost.rect.centery - 3 > self.mainchar.rect.centery:
            self.move.thrust(1000) #goup
        elif self.ghost.rect.centery + 3 < self.mainchar.rect.centery:
            self.move.movedown(1000) #godown
        else:
            self.move.speedy = 0
    
