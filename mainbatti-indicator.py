#!/usr/bin/env python3
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator

import os
import subprocess
import RoutineReader
import signal


def OpenMainbattiTalika(w):
    subprocess.call(["gnome-terminal", "--command=python3 " + os.path.dirname(os.path.realpath(__file__)) + "/mainbatti-talika.py"])

def Quit(w):
    Gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    ind = appindicator.Indicator.new (
                          "example-simple-client",
                          "starred",
                          appindicator.IndicatorCategory.APPLICATION_STATUS)
    ind.set_status (appindicator.IndicatorStatus.ACTIVE)

    menu = Gtk.Menu()
    
    mitem = Gtk.MenuItem("Mainbatti-Talika")
    menu.append(mitem)
    mitem.connect("activate", OpenMainbattiTalika)
    mitem.show()
    
    mitem = Gtk.SeparatorMenuItem()
    menu.append(mitem)
    mitem.show()

    mitem = Gtk.MenuItem("Quit")
    mitem.connect("activate", Quit)
    menu.append(mitem)
    mitem.show()

    ind.set_menu(menu)

    Gtk.main()
