#!/usr/bin/env python3

import os
import shutil

path = os.path.dirname(os.path.abspath(__file__))


text = '\n\n# Added by mainbatti-indicator\n'
text += 'export PATH=\${PATH}:' + path + '\n'
os.system('bash -c \'grep -q -F "' + path + '" ~/.bashrc || echo "' + text + '" >> ~/.bashrc\'')

deskfile = path+"/mainbatti-indicator-template.desktop"
deskfile2 = path+"/mainbatti-indicator.desktop"

with open(deskfile,'r') as f:
    newlines = []
    for line in f.readlines():
        newlines.append(line.replace('<path>', path).replace('<icon>', path+"/mainbatti.png"))


with open(deskfile2, 'w') as f:
    for line in newlines:
        f.write(line)

finalpath = os.path.expanduser('~') + "/.config/autostart/"
if not os.path.exists(finalpath):
    os.makedirs(finalpath)

finalpath2 = os.path.expanduser('~') + "/.local/share/applications/"
if not os.path.exists(finalpath2):
    os.makedirs(finalpath2)

shutil.copyfile(deskfile2, finalpath+"mainbatti-indicator.desktop")
shutil.copyfile(deskfile2, finalpath2+"mainbatti-indicator.desktop")

if not os.fork():
    os.system('python3 "' + path+"/mainbatti-indicator.py" + '"')
