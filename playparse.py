#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from PIL import Image, ImageTk
# from dragmanager import DragManager
from DnD import DnD

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        image = 'logo.png'
        load = Image.open(image)
        self.render = ImageTk.PhotoImage(load)
        self.label = tk.Label(self, image=self.render)
        self.label.image = self.render
        self.label.pack(side="top")

        dnd = DnD(self.master)
        
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")
        
        self.master.update()# may be necessary on unix
        
        def drag(action, actions, type, win, X, Y, x, y, data):
            return action
        
        def drag_enter(action, actions, type, win, X, Y, x, y, data):
            self.label.focus_force()
            return action
        
        def drop(action, actions, type, win, X, Y, x, y, data):
            datos = str(data).encode('utf-8')
            print(datos)
            r = ''
            if '{' in datos:
                star = datos.find('{') + 1
                end = datos.find('}')
                print(star, end)
                r = datos[star:end]
            else:
                r = datos.split()[0]
            self.update_image(url=r)
                
                
        dnd.bindtarget(self.label, 'text/uri-list', '<Drag>', drag, 
                        ('%A', '%a', '%T', '%W', '%X', '%Y', '%x', '%y', '%D'))
        dnd.bindtarget(self.label, 'text/uri-list', '<DragEnter>', drag_enter, 
                        ('%A', '%a', '%T', '%W', '%X', '%Y', '%x', '%y', '%D'))
        dnd.bindtarget(self.label, 'text/uri-list', '<Drop>', drop, 
                        ('%A', '%a', '%T', '%W', '%X', '%Y', '%x', '%y','%D'))

    def say_hi(self):
        print("hi there, everyone!")
    
    extvd = ('.mp4', '.flv', '.avi', '.mpg', '.mkv', 
            '.webm', '.ts', '.mov', '.MP4', '.FLV',
            '.MPG', '.AVI', '.MKV', 'WEBM', '.MOV',
            '.TS', '.wmv', '.WMV')
    extim = ('.jpeg', '.jpg', '.png', '.gif')

    def update_image(self, url, *args):
        if url.endswith(self.extim):
            # esto es uma imagen
            load = Image.open(url)
            self.render = ImageTk.PhotoImage(load)
            #from copy import copy
            self.label.config(image=self.render)
        elif url.endswith(self.extvd):
            # aqui lanzamos la aplicacion
            from utility import lunch_ffplay
            lunch_ffplay(url)
        #self.label['image'] = self.render
        self.master.update_idletasks()


if __name__ == '__main__':
    root = tk.Tk()
    # root.iconbitmap('bily.ico')
    # root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='48pCrystal.png'))
    root.iconphoto(True, tk.PhotoImage(file='48pCrystal.png'))
    app = Application(master=root)
    app.mainloop()

