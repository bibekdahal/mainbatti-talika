#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
import cairo
import signal
import datetime

import RoutineReader

def timediff(h1, m1, h2, m2):
    t1 = h1*60+m1
    t2 = h2*60+m2
    td = t1 - t2
    return int(td/60), td%60

def transparent_expose(widget, cr):
    cr.set_source_rgba(0.2, 0.2, 0.2, 0.4)
    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.paint()
    cr.set_operator(cairo.OPERATOR_OVER)

class DesktopWindow(Gtk.Window):
    def __init__(self, *args):
        Gtk.Window.__init__(self, *args)
        
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.set_keep_below(True)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)
        self.set_decorated(False)
        self.stick()
        
        screen = self.get_screen()
        rgba = screen.get_rgba_visual()
        self.set_visual(rgba)
        self.set_app_paintable(True)
        self.connect("draw", transparent_expose)
        self.set_events(Gdk.EventMask.FOCUS_CHANGE_MASK)
        self.connect("focus-out-event", self.lostFocus)

    def lostFocus(self, w, ww):
        self.set_keep_below(True)

    def Present(self):
        self.set_keep_above(True)
        self.present()

class TalikaGadget:
    def __init__(self):

        global reader
        reader = RoutineReader.RoutineReader()
        reader.ReadFile("test.xml");
       
        self.window = DesktopWindow()
        screen = self.window.get_screen()
        scr_w = screen.get_width()
        scr_h = screen.get_height()

        self.window.move(scr_w-300, 100)
        
        self.box = Gtk.HBox()
        self.window.add(self.box)
        
        self.label = Gtk.Label()
        self.box.add(self.label)
        
        text = "<b><i>12 minutes</i> remaining\nMainbatti-talika</b>"
        self.label.set_markup(text)
        self.label.set_justify(Gtk.Justification.CENTER)
        
        self.window.show_all()
        self.Refresh()

    def Refresh(self):
        times = reader.GetToday(4)
        now = datetime.datetime.now()

        string = "    <span size='x-large' foreground='#1155ff'>Mainbatti Talika</span>    \n"
        string += "<span foreground='#11ff55'>"
        
        donechecking = False
        timeid = -1
        inside = False
        for i in range(len(times)): 
            time = times[i];
            sh = time["start"]["hr"]
            sm = time["start"]["min"]
            eh = time["end"]["hr"]
            em = time["end"]["min"]
                
            string += RoutineReader.GetTime(sh, sm) + " - " + RoutineReader.GetTime(eh, em) 
            if i != len(times) - 1:
                string += "\n"

            if not donechecking:
                if (sh < now.hour or (sh == now.hour and sm <= now.minute)) \
                    and (eh > now.hour or (eh==now.hour and em >= now.minute)):
                    donechecking = True
                    timeid = i
                    inside = True
                else:
                    if now.hour < sh:
                        if timeid == -1 or times[timeid]["start"]["hr"] > sh:
                            timeid = i

        string += "</span>"

        time = times[timeid]
        if inside:
            hr, mn = timediff(time["end"]["hr"], time["end"]["min"], now.hour, now.minute)
            string += "\nPower comes after:\n" + RoutineReader.GetTime(hr, mn)
        else:
            hr, mn = timediff(time["start"]["hr"], time["start"]["min"], now.hour, now.minute)
            string += "\nPower goes in:\n" + RoutineReader.GetTime(hr, mn)


        self.label.set_markup("<b>"+string+"</b>");

        deltaseconds = 60-datetime.datetime.now().second
        GLib.timeout_add_seconds(deltaseconds, self.Refresh)  #Refresh every minute

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    instance = TalikaGadget()
    Gtk.main()
