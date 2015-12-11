#!/usr/bin/env python3

import sys, os
import RoutineReader
import RoutineUpdater
import re
import json

os.chdir(os.path.dirname(__file__))

class ArgumentError(Exception):
    def __init__(self,message, arg):
        self.message = message
        self.arg = arg
    def display(self):
        print(''.join(self.message), self.arg)

update_re = re.compile(r'^--update$')
group_re = re.compile(r'^(--group[1-7])|(-g[1-7])$')
time_re = re.compile(r'^(--twelve)|(-12)$')
lang_re = re.compile(r'^(--nepali)|(-n)$')
file_re = re.compile(r'^.+\.xml$')
help_re = re.compile(r'^(-h)|(--help)$')

def IsGroup(input):
    return bool(group_re.match(input))

def IsTime(input):
    return bool(time_re.match(input))

def IsNepali(input):
    return bool(lang_re.match(input))

def IsXML(input):
    return bool(file_re.match(input))

def IsHelp(input):
    return bool(help_re.match(input))

def IsUpdate(input):
    return bool(update_re.match(input))

def update():
    try:
        RoutineUpdater.main()
        print("Updated successfully")
    except:
        print("Couldn't update. Check your connection.")

def ArgumentParser():
    arguments = sys.argv[1::]
    filename = "routine.xml"

    group = -1
    twelveHr = False
    nepali = False
    autoupdate = True
    
    #load defaults from configuration file
    try:
        configstr = open("config.json").read()
        config = json.loads(configstr)
        if "Group" in config:
            group = config["Group"]
        if "Language" in config and config["Language"] == "Nepali":
            nepali = True
        if "Twelve-Hour" in config:
            twelveHr = config["Twelve-Hour"]
        if "Auto-Update" in config:
            autoupdate = config["Auto-Update"]
    except:
        print("Couldn't load configuration file: config.json")
    
    for arg in arguments:
        try:
            if IsUpdate(arg):
                update()
                return
            elif IsGroup(arg):
                #group = int(arg[1])
                group = ''.join(re.findall(r'\d+', arg))
                group = int(group)
                #print(group)
            elif IsTime(arg):
                twelveHr = True
                #print(arg)
            elif IsNepali(arg):
                nepali = True
                #print(arg)
            elif IsXML(arg):
                filename = arg
                #print(arg)
            elif IsHelp(arg):
                file = open("help.txt","r")
                print(file.read())
                file.close();
                return
            else:
                raise ArgumentError(":D cannot load... invalid argument : ", arg)
        except ArgumentError as e:
            e.display()
            return
        except IOError:
            print(" LOL file doesnt exist")
            return


    if autoupdate:
        update()

    try:
        if not filename:
            raise ArgumentError(":D cannot load... invlid filename : ", filename)
        else:
            try:
                file = open(filename, "r")
                file.close()
                RoutineReader.main(filename, group, nepali, twelveHr)
            except IOError:
                print(" LOL file doesnt exist")
            
    except ArgumentError as e:
        e.display()



def main():
    #RoutineReader.main("test.xml")
    ArgumentParser()

if __name__=="__main__":
    main()
