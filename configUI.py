#!/usr/bin/python3
from gi.repository import Gtk

import json
import sys, os

def LoadConfig():
    #load defaults from configuration file
    config = {}
    try:
        configstr = open("config.json").read()
        config = json.loads(configstr)
        if not "Group" in config:
            config["Group"] = 1
        if not "Language" in config:
            config["Language"] = "English"
        if not "Twelve-Hour" in config:
            config["Twelve-Hour"] = False
        if not "Auto-Update" in config:
            config["Auto-Update"] = True
    except:
        print("Couldn't load configuration file: config.json")
    return config

def SaveConfig(config):
    configstr = json.dumps(config, indent=4)
    open("config.json", "w").write(configstr)
 
def Nothing():
    pass

ChangeHandler = Nothing

class ConfigWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Mainbatti Talika Settings")
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_resizable(False)

        config = LoadConfig()

        grid = Gtk.Grid(row_homogeneous=True, column_homogeneous=True)
        grid.props.margin_top = 20
        grid.props.margin_right = 20
        grid.props.margin_bottom = 20
        self.add(grid)

        grid.attach(Gtk.Label("Group:"), 0, 0, 2, 1)
        spin = Gtk.SpinButton()
        spin.set_range(1, 7)
        spin.set_increments(1, 1)
        grid.attach(spin, 2, 0, 2, 1)
        self.group = spin
        self.group.set_value(config["Group"])

        grid.attach(Gtk.Label("Language:"), 0, 1, 2, 1)
        combo = Gtk.ComboBoxText()
        combo.append_text("English")
        combo.append_text("Nepali")
        combo.set_active(1)
        grid.attach(combo, 2, 1, 2, 1)
        self.lang = combo
        if config["Language"]=="Nepali":
            self.lang.set_active(1)
        else:
            self.lang.set_active(0)

        check = Gtk.CheckButton("12-Hour Format")
        grid.attach(check, 2, 2, 2, 1)
        self.hrformat = check
        self.hrformat.set_active(config["Twelve-Hour"])

        okButton = Gtk.Button("Apply")
        okButton.props.margin_top = 10
        okButton.set_can_default(True)
        grid.attach(okButton, 2, 3, 1, 1)
        closeButton = Gtk.Button("Close")
        closeButton.props.margin_top = 10
        grid.attach(closeButton, 3, 3, 1, 1)

        okButton.connect("clicked", self.Apply)
        closeButton.connect("clicked", self.Close)

        self.set_default(okButton)

    def Apply(self, w):
        config = {}
        config["Group"] = int(self.group.get_value())
        if self.lang.get_active() == 1:
            config["Language"] = "Nepali"
        else:
            config["Language"] = "English"
        config["Twelve-Hour"] = self.hrformat.get_active()
        SaveConfig(config)
        ChangeHandler()
        self.close()

    def Close(self, w):
        self.close()

def main():
    win = ConfigWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
