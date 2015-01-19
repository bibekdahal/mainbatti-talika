import xml.etree.ElementTree as ET
import curses

def GetTimeString(group, day, timeId):
    if not day in group:
        return "not found"
    times = group[day]
    if timeId >= len(times):
        return ""
    time = times[timeId]
    string = str(time["start"]["hr"]).zfill(2) + ":" + str(time["start"]["min"]).zfill(2) \
            + " - " + \
            str(time["end"]["hr"]).zfill(2) + ":" + str(time["end"]["min"]).zfill(2)
    return string

def ParseTimeStr(string):
    time = {}
    strings = string.split(':')
    time["hr"] = int(strings[0])
    if len(strings) == 2:
        time["min"] = int(strings[1])
    else:
        time["min"] = 0
    return time
    

class RoutineReader:
    def __init__(self):
        self.tables = []

    def ReadFile(self, filename):
        tree = ET.parse(filename)
        routineX = tree.getroot()
        if routineX.tag != 'Routine':
            return

        self.tables = []
        for tableX in routineX:
            if tableX.tag != 'Table':
                continue
            table = {}
            for groupX in tableX:
                if groupX.tag != 'Group' or not 'id' in groupX.attrib:
                    continue
                group = {}
                for dayX in groupX:
                    day = []
                    for timeX in dayX:
                        if timeX.tag != 'Time' or not 'start' in timeX.attrib or not 'end' in timeX.attrib:
                            continue
                        time = {}
                        time["start"] = ParseTimeStr(timeX.attrib['start'])
                        time["end"] = ParseTimeStr(timeX.attrib['end'])
                        day.append(time)
                    group[dayX.tag] = day
                table[int(groupX.attrib['id'])] = group
            self.tables.append(table)

    def GetRoutineAsString(self):
        tableId=1
        padding = 17
        string = ""
        for table in self.tables:
            string += ("Table #"+str(tableId)+":\n")
            string += ("Group".center(6) + "Sunday".center(padding) + "Monday".center(padding) + "Tuesday".center(padding) + \
                    "Wednesday".center(padding) + "Thursday".center(padding) + "Friday".center(padding) + "Saturday".center(padding))
            string += ("\n\n")
            for groupId, group in table.items():
                row = str(groupId).center(6)
                timeId = 0
                printTime = True
                while printTime:
                    row += \
                        GetTimeString(group, "Sunday", timeId).center(padding) + \
                        GetTimeString(group, "Monday", timeId).center(padding) + \
                        GetTimeString(group, "Tuesday", timeId).center(padding) + \
                        GetTimeString(group, "Wednesday", timeId).center(padding) + \
                        GetTimeString(group, "Thursday", timeId).center(padding) + \
                        GetTimeString(group, "Friday", timeId).center(padding) + \
                        GetTimeString(group, "Saturday", timeId).center(padding)
                    string += (row+"\n")
                    if row.find(':') == -1:
                        printTime = False
                    timeId += 1
                    row = " ".center(6)
            tableId += 1;
        return string

def scroll(screen, window, posX, posY):
    height, width = screen.getmaxyx()
    window.refresh(posY, posX, 0, 0, height-1, width-1)

def main(screen):
    reader = RoutineReader()
    reader.ReadFile('test.xml')

    string = reader.GetRoutineAsString()
    winwidth = 128
    winheight = string.count('\n')+1
    window = curses.newpad(winheight, winwidth)
    window.addstr(string)
    window.keypad(True)

    posX = 0
    posY = 0
    scroll(screen, window, posX, posY)
    
    while (True):
        event = window.getch()
        if event == ord('q'):
            break
        elif event == ord('l') or event == curses.KEY_RIGHT:
            height, width = screen.getmaxyx()
            if posX+1+width < winwidth:
                posX += 1
        elif event == ord('h') or event == curses.KEY_LEFT:
            height, width = screen.getmaxyx()
            if posX-1 >= 0:
                posX -= 1
        elif event == ord('k') or event == curses.KEY_UP:
            height, width = screen.getmaxyx()
            if posY-1 >= 0:
                posY -= 1
        elif event == ord('j') or event == curses.KEY_DOWN:
            height, width = screen.getmaxyx()
            if posY+1+height < winheight:
                posY += 1


        scroll(screen, window, posX, posY)
    
    
if __name__ == "__main__":
    curses.wrapper(main)
