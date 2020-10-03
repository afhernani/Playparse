# Playparse GUI tk
## lauch video and image archive with drag and drop.
## Autor: Hernani Aleman Ferraz
## email: afhernani@gmail.com / hotmail.com

# playparse.py
## rite: python playparse.py
## Drag and drop video or image to app area.-> open video file with ffplay or draw image into app area.

# use TkDnD lib.
### for linux: tkdnd2.8-linuz-x86_64
### for window tkdnd2.8-win32-x86_64
### use class DnD.py for drag and drop process from:
    
    https://sourceforge.net/projects/tkdnd/files/

    preinstalled Python already, and this is the path where Tcl library is installed. TkDnd lib will be loaded automatically while using Tk/Tcl lib.

    Set os.environ['TKDND_LIBRARY'] to the location of TkDnd2.x.dylib: Sample code:

    `if sys.platform == 'win32':
       if getattr(sys, 'frozen', False):
          os.environ['TKDND_LIBRARY'] = os.path.join(os.path.dirname(sys.executable), 'tkdnd2.8') `

    I got this working on both Windows (10) and OSX (10.11) by downloading:
    A) Tk extensions tkdnd2.8 from https://sourceforge.net/projects/tkdnd/
    B) Python wrapper TkinterDnD2 from https://sourceforge.net/projects/tkinterdnd/

    On OSX:
    1) Copy the tkdnd2.8 directory to /Library/Tcl
    2) Copy the TkinterDnD2 directory to /Library/Frameworks/Python.framework/Versions/.../lib/python/site-packages
    (Use the sudo command for copying files on OSX due to permissions.)

    On Windows:
    1) Copy the tkdnd2.8 directory to ...\Python\tcl
    2) Copy the TkinterDnD2 directory to ...\Python\Lib\site-packages

    And here's a simple test case based on python drag and drop explorer files to tkinter entry widget. The TkinterDnD2 download comes with much more robust examples.

        import sys
        if sys.version_info[0] == 2:
            from Tkinter import *
        else:
            from tkinter import *
        from TkinterDnD2 import *

        def drop(event):
            entry_sv.set(event.data)

        root = TkinterDnD.Tk()
        entry_sv = StringVar()
        entry_sv.set('Drop Here...')
        entry = Entry(root, textvar=entry_sv, width=80)
        entry.pack(fill=X, padx=10, pady=10)
        entry.drop_target_register(DND_FILES)
        entry.dnd_bind('<<Drop>>', drop)
        root.mainloop()

    Update: the above procedure works for Python 2 or 3.
