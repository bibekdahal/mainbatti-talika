#!/usr/bin/env python3
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator

import os
import fcntl, sys
import subprocess

import RoutineReader
import RoutineUpdater
import signal
import configUI
import mainbatti_gadget


window = Gtk.Window()
screen = window.get_screen()
parentPath = os.path.dirname(os.path.realpath(__file__))

def update():
    try:
        RoutineUpdater.main()
        return True
    except:
        return False

def Update(w):
    u = update()

    if not u:
        dialog = Gtk.MessageDialog(window, 0, Gtk.MessageType.INFO,
                Gtk.ButtonsType.OK, "Couldn't update. Check your connection.")
        dialog.run()
        dialog.destroy()

def OpenMainbattiTalika(w):
    width = 125     # for 24-hr format display width = 160
    height = 26
    scr_w = screen.get_width()
    scr_h = screen.get_height()
    geomstr = str(width) + "x" + str(height) + "+" \
                + str(int(scr_w/2-width*4.28)) + "+" + str(int(scr_h/2 - height*10))

    subprocess.call(["gnome-terminal", "--working-directory="+parentPath, "--geometry="+geomstr, "--title=Mainbatti Talika", "--command=python3 " + os.path.dirname(os.path.realpath(__file__)) + "/mainbatti-talika.py"])

def SettingsChanged():
    if gadget:
        gadget.Refresh()

def Settings(w):
    configUI.ChangeHandler = SettingsChanged
    configUI.main()

def Quit(w):
    Gtk.main_quit()

def ShowGadget(w, i, d):
    if gadget:
        gadget.window.Present()

def GadgetToggle(w):
    global gadget

    # save the state as settings
    config = configUI.LoadConfig()
    config["Gadget"] = not config["Gadget"]
    configUI.SaveConfig(config)
    if w.get_active():
        gadget = mainbatti_gadget.TalikaGadget()
    else:
        gadget.window.close()
        del gadget

if __name__ == "__main__":
    # Don't run two instances
    pid_file = 'program.pid'
    fp = open(pid_file, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        # another instance is running
        sys.exit(0)

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    config = configUI.LoadConfig()
    if config["Auto-Update"]:
        update()

    os.chdir(parentPath)

    global gadget
    # load gadget according to settings
    if config["Gadget"]:
        gadget = mainbatti_gadget.TalikaGadget()
    else:
        gadget = None

    ind = appindicator.Indicator.new_with_path(
                          "Mainbatti-Talika",
                          "mainbatti",
                          appindicator.IndicatorCategory.APPLICATION_STATUS,
                          parentPath)
    ind.set_status(appindicator.IndicatorStatus.ACTIVE)

    menu = Gtk.Menu()
    
    mitem = Gtk.MenuItem("Mainbatti-Talika")
    menu.append(mitem)
    mitem.connect("activate", OpenMainbattiTalika)

    mitem = Gtk.MenuItem("Settings")
    menu.append(mitem)
    mitem.connect("activate", Settings)
 
    mitem = Gtk.MenuItem("Check for updates")
    menu.append(mitem)
    mitem.connect("activate", Update)   

    mitem = Gtk.SeparatorMenuItem()
    menu.append(mitem)

    mitem = Gtk.CheckMenuItem("Gadget")
    mitem.set_active(config["Gadget"])
    mitem.connect("toggled", GadgetToggle)
    menu.append(mitem)
    
    mitem = Gtk.SeparatorMenuItem()
    menu.append(mitem)

    mitem = Gtk.MenuItem("Quit")
    mitem.connect("activate", Quit)
    menu.append(mitem)

    menu.show_all()
    ind.set_menu(menu)

    ind.connect("scroll-event", ShowGadget)

    Gtk.main()
