############### file DnD.py  ###############################################################

'''Python wrapper for the tkDnD tk extension.'''

__autor__ = 'Hernani Aleman Ferraz'
__email__ = 'afhernani@gmail.com'
__apply__ = 'drag and drog'
__version__ = 0.1

import os
from platform import system
try:
    # Tkinter for Python 2.xx
    import Tkinter as tk
except ImportError:
    # Tkinter for Python 3.xx
    import tkinter as tk
 
if system() == 'Linux':
    os.environ['TKDND_LIBRARY'] = 'tkdnd2.8'
elif system() == 'Windows':
    os.environ['TKDND_LIBRARY'] = 'tkdnd2.8w'
else:
    print(f"no se ha definido la libreria en la plataforma: {system()}")

class DnD:
    def __init__(self, tkroot):
        if not getattr(tkroot, '_tkdnd_loaded', False):
               DnD._load_tkdnd(tkroot)
        # self._tkroot.tk.eval('package require tkdnd')
        self._tkroot = tkroot
        self.tk = tkroot.tk
        # make self an attribute of the parent window for easy access in child classes
        tkroot.dnd = self
        
    @staticmethod
    def _load_tkdnd(master):
       tkdndlib = os.environ.get('TKDND_LIBRARY')
       if tkdndlib:
           master.tk.eval('global auto_path; lappend auto_path {%s}' % tkdndlib)
       master.tk.eval('package require tkdnd')
       master._tkdnd_loaded = True
    
    def bindsource(self, widget, type=None, command=None, arguments=None, priority=None):
        '''Register widget as drag source; for details on type, command and arguments, see bindtarget().
        priority can be a value between 1 and 100, where 100 is the highest available priority (default: 50).
        If command is omitted, return the current binding for type; if both type and command are omitted,
        return a list of registered types for widget.'''
        command = self._generate_callback(command, arguments)
        tkcmd = self._generate_tkcommand('bindsource', widget, type, command, priority)
        res = self._tkroot.tk.eval(tkcmd)
        if type == None:
            res = res.split()
        return res
    
    def bindtarget(self, widget, type=None, sequence=None, command=None, arguments=None, priority=None):
        '''Register widget as drop target; type may be one of text/plain, text/uri-list, text/plain;charset=UTF-8
        (see the man page tkDND for details on other (platform specific) types);
        sequence may be one of '<Drag>', '<DragEnter>', '<DragLeave>', '<Drop>' or '<Ask>' ;
        command is the callback associated with the specified event, argument is an optional tuple of arguments
        that will be passed to the callback; possible arguments include: %A %a %b %C %c %D %d %L %m %T %t %W %X %x %Y %y
        (see the tkDND man page for details); priority may be a value in the range 1 to 100 ; if there are
        bindings for different types, the one with the priority value will be proceeded first (default: 50).
        If command is omitted, return the current binding for type, where sequence defaults to '<Drop>'.
        If both type and command are omitted, return a list of registered types for widget.'''
        command = self._generate_callback(command, arguments)
        tkcmd = self._generate_tkcommand('bindtarget', widget, type, sequence, command, priority)
        res = self._tkroot.tk.eval(tkcmd)
        if type == None:
            res = res.split()
        return res
    
    def clearsource(self, widget):
        '''Unregister widget as drag source.'''
        self._tkroot.tk.call('dnd', 'clearsource', widget)
    
    def cleartarget(self, widget):
        '''Unregister widget as drop target.'''
        self._tkroot.tk.call('dnd', 'cleartarget', widget)
    
    def drag(self, widget, actions=None, descriptions=None, cursorwindow=None, command=None, arguments=None):
        '''Initiate a drag operation with source widget.'''
        command = self._generate_callback(command, arguments)
        if actions:
            if actions[1:]:
                actions = '-actions {%s}' % ' '.join(actions)
            else:
                actions = '-actions %s' % actions[0]
        if descriptions:
            descriptions = ['{%s}'%i for i in descriptions]
            descriptions = '{%s}' % ' '.join(descriptions)
        if cursorwindow:
            cursorwindow = '-cursorwindow %s' % cursorwindow
        tkcmd = self._generate_tkcommand('drag', widget, actions, descriptions, cursorwindow, command)
        self._tkroot.tk.eval(tkcmd)
                
    def _generate_callback(self, command, arguments):
        '''Register command as tk callback with an optional list of arguments.'''
        cmd = None
        if command:
            cmd = self._tkroot._register(command)
            if arguments:
                cmd = '{%s %s}' % (cmd, ' '.join(arguments))
        return cmd
    
    def _generate_tkcommand(self, base, widget, *opts):
        '''Create the command string that will be passed to tk.'''
        tkcmd = 'dnd %s %s' % (base, widget)
        for i in opts:
            if i is not None:
                tkcmd += ' %s' % i
        return tkcmd


#############--demo code--########################################

def test():
    root = tk.Tk()
    dnd = DnD(root)
    tk.Label(root, text='Drop files from your file manager into the listbox').pack(side='top')
    l = tk.Listbox(root)
    l.pack(side='top', fill='both', expand=1)
    root.update()# may be necessary on unix
    # now make the listbox a drop target:
    
    def drag(action, actions, type, win, X, Y, x, y, data):
        return action
        
    def drag_enter(action, actions, type, win, X, Y, x, y, data):
        l.focus_force()
        return action
    
    def drop(action, actions, type, win, X, Y, x, y, data):
        files = data.split()
        #datos = str(data)
        print(str(data), action, type)
        #star = datos.find('{') + 1
        # end = datos.find('}')
        # r = datos[star:end]
        for f in files:
            l.insert('end',f)
    
    dnd.bindtarget(l, 'text/uri-list', '<Drag>', drag, ('%A', '%a', '%T', '%W', '%X', '%Y', '%x', '%y', '%D'))
    dnd.bindtarget(l, 'text/uri-list', '<DragEnter>', drag_enter, ('%A', '%a', '%T', '%W', '%X', '%Y', '%x', '%y', '%D'))
    dnd.bindtarget(l, 'text/uri-list', '<Drop>', drop, ('%A', '%a', '%T', '%W', '%X', '%Y', '%x', '%y','%D'))
    
    root.mainloop()

if __name__ == '__main__':
    test()

################  end of DnD.py  #######################################################