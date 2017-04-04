#!/usr/bin/env python

# For compatibility with Python 2.7
# A future statement is a directive to the compiler that a particular module 
# should be compiled using syntax or semantics that will be available in a 
# specified future release of Python.
# The future statement is intended to ease migration to future versions of 
# Python that introduce incompatible changes to the language. It allows use 
# of the new features on a per-module basis before the release in which the 
# feature becomes standard.
from __future__ import print_function
from __future__ import division


try:
    import Tkinter as tk
    from tkFileDialog import askopenfilename
except ImportError:
    import tkinter as tk
    from tkinter.filedialog import askopenfilename
    
import os

from sokoban import Warehouse

# Written by f.maire@qut.edu.au using icon images from Risto Stevcev.
# Last modified on 2015/03/16

# todo: documentation!!
#       stepping function?


__author__ = "Frederic Maire"
__version__ = "1.2"

#if not __package__:
#    __package__ = "CAB320_sokoban"

# Directory where this file is located
_ROOT = os.path.abspath(os.path.dirname(__file__))


class Menu(object):
    def __init__(self, app):
        self.app = app
    def OpenFile(self):
        self.app.grid_forget()
        self.app.level_file_name = askopenfilename(initialdir=os.path.join(_ROOT, 'warehouses'))
        print ('\n self.app.level_file_name ', self.app.level_file_name, '\n')
        self.app.start_level()
    def About(self):
        AboutDialog()


class AboutDialog(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self = tk.Toplevel()
        self.title("About")

        info = tk.Label(self, text="Sokoban v%s - by %s" % ( __version__, __author__))
        info.grid(row=0)

        self.ok_button = tk.Button(self, text="OK", command=self.destroy)
        self.ok_button.grid(row=1)


class CompleteDialog(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self = tk.Toplevel()
        self.title("Puzzle solved")

        info = tk.Label(self, text=("Congratulations, you have solved the puzzle!"))
        info.grid(row=0)

        self.ok_button = tk.Button(self, text="OK", command=self.destroy)
        self.ok_button.grid(row=1)

# hole is a synonym  for target
# crate is a synonym  for box

##image_dict={} # 'wall':tk.PhotoImage(file=os.path.join(_ROOT, 'images/wall.gif'))}


##    self.level[row][column - 1] is not warehouse_symbol['wall']

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.configure(background="black")
        self.master.title("Sokoban v%s" % (__version__))
        self.master.resizable(0,0)
        self.image_dict={'wall':tk.PhotoImage(file=os.path.join(_ROOT, 'images/wall.gif')),
                         'target':tk.PhotoImage(file=os.path.join(_ROOT, 'images/hole.gif')),
                         'box_on_target':tk.PhotoImage(file=os.path.join(_ROOT, 'images/crate-in-hole.gif')),
                         'box':tk.PhotoImage(file=os.path.join(_ROOT, 'images/crate.gif')),
                         'worker':tk.PhotoImage(file=os.path.join(_ROOT, 'images/player.gif')),
                         'smiley':tk.PhotoImage(file=os.path.join(_ROOT, 'images/smiley.gif')),
                         'worker_on_target':tk.PhotoImage(file=os.path.join(_ROOT, 'images/player-in-hole.gif')),
                         }
        icon = self.image_dict['box']
        self.warehouse_symbol =  { 'wall':'#' , 'target':'.' , 'box_on_target': '*' , 'box':'$'
                                   , 'worker':'@', 'worker_on_target': '!', 'floor' : ' '}
        self.direction_offset = {'Left' :(-1,0), 'Right':(1,0) , 'Up':(0,-1), 'Down':(0,1)} # (x,y) = (column,row)
     
        self.master.tk.call('wm', 'iconphoto', self.master._w, icon)
        self.create_menu()

        self.DEFAULT_SIZE = 200
        self.frame = tk.Frame(self, height=self.DEFAULT_SIZE, width=self.DEFAULT_SIZE)
        self.frame.grid()
        self.default_frame()
        self.cells={} # dict with key (x,y) and value Label widget to keep track of the Labels in the grid
        self.level_file_name = None 
        self.warehouse = Warehouse()


        
    def key(self, event):
        if event.keysym in ('Left', 'Right', 'Up', 'Down'): 
            self.move_player(event.keysym)
        if event.keysym in ('r','R'):
            self.restart_level()

    def create_menu(self):
        root = self.master
        menu = tk.Menu(root)
        user_menu = Menu(self)
        root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Restart", command=self.restart_level)
        file_menu.add_command(label="Open...", command=user_menu.OpenFile)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=menu.quit)

        help_menu = tk.Menu(menu)
        menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=user_menu.About)

    def default_frame(self):
        start_width = 50
        start_label = tk.Label(self.frame, text="\n *** Welcome to Sokoban! ***\n", width=start_width)
        start_label.grid(row=0, column=0)

        start_label2 = tk.Label(self.frame, text="To play: File -> Open\n", width=start_width)
        start_label2.grid(row=1, column=0)

        start_label3 = tk.Label(self.frame, text="To reset current warehouse: press the 'r' key \n", width=start_width)
        start_label3.grid(row=3, column=0)

    def clear_level(self):
        self.frame.destroy()
        self.frame = tk.Frame(self)
        self.frame.grid()
        self.warehouse = Warehouse() # warehouse
        self.cells = {}

    def start_level(self):
        self.clear_level()
        self.warehouse.read_warehouse_file(self.level_file_name)
        self.master.title("Sokoban v%s - %s" % ( __version__, self.level_file_name.split("/")[-1]))
        self.fresh_display()
        
 
    def restart_level(self):
        if self.level_file_name: 
            self.start_level()
 
    def fresh_display(self):
        '''
        First display of the warehouse
        Setup the self.cells dictionary
        '''
        for x,y in self.warehouse.walls:
            w = tk.Label(self.frame, image=self.image_dict['wall'])
            w.grid(row=y,column=x)
            self.cells[(x,y)] = w
        for x,y in self.warehouse.targets:
            w = tk.Label(self.frame, image=self.image_dict['target'])
            w.grid(row=y,column=x)
            self.cells[(x,y)] = w
        for x,y in self.warehouse.boxes:
            if (x,y) in self.warehouse.targets:
                w = self.cells[(x,y)]
                w['image'] = self.image_dict['box_on_target']
            else:
                w = tk.Label(self.frame, image=self.image_dict['box'])
                w.grid(row=y,column=x)
            self.cells[(x,y)] = w
        x,y = self.warehouse.worker
        if (x,y) in self.warehouse.targets:
            w = self.cells[(x,y)]
            w['image'] = self.image_dict['worker_on_target']
        else:
            w = tk.Label(self.frame, image=self.image_dict['worker'])
            w.grid(row=y,column=x)
            self.cells[(x,y)] = w
        self.pack()

    def move_player(self, direction):
        '''
        direction in ['Left', 'Right', 'Up', 'Down']:
        Check whether the worker is pushing a box
        '''
        x,y = self.warehouse.worker
##        print 'worker x,y = ',x,y
        xy_offset = self.direction_offset[direction]
##        print 'xy_offset = ', xy_offset
        next_x , next_y = x+xy_offset[0] , y+xy_offset[1] # where the player will go if possible
##        print 'next_x , next_y = ', next_x , next_y
        # Let's find out if it is possible to move the player in this direction
        if (next_x,next_y) in self.warehouse.walls:
            return # impossible move
        if (next_x,next_y) in self.warehouse.boxes:
            if self.try_move_box( (next_x,next_y), (next_x+xy_offset[0],next_y+xy_offset[1]) ) == False:
                return # box next to the player could not be pushed
        # now, the cell next to the player must be empty
        # we still have to move the player
##        print 'let s move the player! '
        w = self.cells[(x,y)] # Label widget in the cell currently containing the player
        del self.cells[(x,y)]
        w.destroy()
        w = tk.Label(self.frame) #, image=self.image_dict['worker'])
        w.grid(row=next_y,column=next_x) # move it to the next cell
        self.cells[(next_x,next_y)] = w
        self.warehouse.worker = (next_x,next_y)
        # Test whether the appearance of the player need to change on the next cell
        if (next_x,next_y) in self.warehouse.targets:
            w['image'] = self.image_dict['worker_on_target']
        else:
            w['image'] = self.image_dict['worker']
        # update the cell where the player was
        if(x,y) in self.warehouse.targets:
            w = tk.Label(self.frame, image=self.image_dict['target'])
            w.grid(row=y,column=x)
            self.cells[(x,y)] = w      
        puzzle_solved = all(z in self.warehouse.targets for z in self.warehouse.boxes)
        if puzzle_solved:
            x,y = self.warehouse.worker
            w = self.cells[(x,y)] # Label widget in the cell currently containing the player
            del self.cells[(x,y)]
            w.destroy()
            w = tk.Label(self.frame, image=self.image_dict['smiley'])
            w.grid(row=y,column=x)
            self.cells[(x,y)] = w
        self.pack()
          

    def try_move_box(self, location, next_location):
        '''
        location and next_location are (x,y) tuples
        Move the box  from 'location' to 'next_location'
        Note that we assume that there is a wall around the warehouse!
        Return True if the box was moved, return False if the box could not be moved
        Update the position and the image of the Label widget for this box
        '''
        x, y = location
        next_x, next_y = next_location

        assert (x,y) in self.warehouse.boxes
        if (next_x, next_y) not in self.warehouse.walls and (next_x, next_y) not in self.warehouse.boxes:
            # can move the box!
            # clean cell (x,y)
            w = self.cells[(x,y)]
            del self.cells[(x,y)]
            w.destroy()
            # clean cell (next_x,next_y)
            if (next_x,next_y) in self.cells:
                assert (next_x,next_y) in self.warehouse.targets
                w = self.cells[(next_x,next_y)]
                del self.cells[(next_x,next_y)]
                w.destroy()
            # new Label for the moved box
            w = tk.Label(self.frame)
            if (next_x,next_y) in self.warehouse.targets:
                w['image'] = self.image_dict['box_on_target']
            else:
                w['image'] = self.image_dict['box']
            w.grid(row=next_y, column=next_x)
            self.cells[(next_x,next_y)] = w
            self.warehouse.boxes.remove((x,y))
            self.warehouse.boxes.append((next_x,next_y))
            # we don't have to update (x,y), this will be done while moving the player
            return True # move successful
        else:
            return False # box was blocked


if __name__ == "__main__":
    app = Application()
    app.bind_all("<Key>", app.key)
    app.mainloop()

# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + 
#                              CODE CEMETARY
# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + 
