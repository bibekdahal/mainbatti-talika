#!/usr/bin/env python3
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator

import os
import subprocess
import RoutineReader
import signal
import configUI


window = Gtk.Window()
screen = window.get_screen()
parentPath = os.path.dirname(os.path.realpath(__file__))

def OpenMainbattiTalika(w):
    width = 125     # for 24-hr format display width = 160
    height = 26
    scr_w = screen.get_width()
    scr_h = screen.get_height()
    geomstr = str(width) + "x" + str(height) + "+" \
                + str(int(scr_w/2-width*4.28)) + "+" + str(int(scr_h/2 - height*10))

    subprocess.call(["gnome-terminal", "--working-directory="+parentPath, "--geometry="+geomstr, "--title=Mainbatti Talika", "--command=python3 " + os.path.dirname(os.path.realpath(__file__)) + "/mainbatti-talika.py"])

def Settings(w):
    configUI.main()

def Quit(w):
    Gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

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
    
    mitem = Gtk.SeparatorMenuItem()
    menu.append(mitem)

    mitem = Gtk.MenuItem("Quit")
    mitem.connect("activate", Quit)
    menu.append(mitem)

    menu.show_all()
    ind.set_menu(menu)

    Gtk.main()
