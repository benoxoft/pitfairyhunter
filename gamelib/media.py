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
import os

def load_image(img):
    return pygame.image.load(os.path.join('.', 'media', img))

def get_font(size):
    return pygame.font.Font(os.path.join('.', 'media', 'Purisa-BoldOblique.ttf'), size)

def get_media_path():
    return os.path.join(os.path.abspath(os.path.curdir), 'media')

def get_full_path(f):
    return os.path.join(get_media_path(), f)

def get_wall_tile_path():
    return get_full_path('tile_wall_32.gif')
