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

from gamelib import media

from Tkinter import *
from tkMessageBox import *
import os

class LevelEditor(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.init_widgets()

    def init_widgets(self):
        self.title('Level Editor')
        self.menu = Menu(self)
        self.file_menu = Menu(self.menu)

        self.menu.add_cascade(label='File', menu=self.file_menu, accelerator='Alt+F', underline=0)
        self.file_menu.add_command(label='New Level', command=self.new_level_click, accelerator='Ctrl+N', underline=0)
        self.file_menu.add_command(label='Open', command=self.open_level_click, accelerator='Ctrl+O', underline=0)
        self.file_menu.add_command(label='Quit', command=self.quit_editor_click, accelerator='Ctrl+Q', underline=0)

        self.root_pane = PanedWindow(self, orient=HORIZONTAL)
        self.root_pane.pack(expand='yes', fill='both')

        self.button_frame = Frame(self.root_pane)

        self.wall_img = PhotoImage(file=media.get_wall_tile_path())
        self.wall_button = Button(self.button_frame, compound=CENTER, image=self.wall_img, command=self.wall_button_click)
        self.wall_button.pack()
        
        self.canvas = Canvas(self.root_pane, width=400, height=400)
        self.canvas.create_rectangle((10, 10, 50, 50), fill='black')
        self.canvas.pack()


        self.root_pane.add(self.canvas)
        self.root_pane.add(self.button_frame)
        
        self.config(menu=self.menu)

    def new_level_click(self):
        pass

    def open_level_click(self):
        pass

    def quit_editor_click(self):
        if askquestion('Level Editor', 'Really quit?') == 'yes':
            self.quit()

    def wall_button_click(self):
        pass
    
if __name__ == '__main__':
    app = LevelEditor()
    app.mainloop()

        


