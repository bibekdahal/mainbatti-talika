import xml.etree.ElementTree as ET
import CursesWindow
import sys
import datetime

GetNumber = CursesWindow.GetNumber

DaysList = [ "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday" ]

def TwoDigits(x):
    return GetNumber(x).rjust(2, GetNumber(0))

def GetTime(hr, mn):
    mnstr = ":" + TwoDigits(mn)
    if CursesWindow.Hour24:
        return TwoDigits(hr) + mnstr
    if hr > 12:
        return TwoDigits(hr-12) + mnstr + " PM"
    if hr == 12:
        return TwoDigits(hr) + mnstr + " PM"
    return TwoDigits(hr) + mnstr + " AM"

def GetTimeString(group, day, timeId):
    if not day in group:
        return "not found"
    times = group[day]
    if timeId >= len(times):
        return ""
    time = times[timeId]
    string = GetTime(time["start"]["hr"], time["start"]["min"]) \
            + " - " + \
            GetTime(time["end"]["hr"], time["end"]["min"]) 
    return string

def ParseTimeStr(string):
    time = {}
    strings = string.split(':')
    if (strings[0]!=''):
        time["hr"] = int(strings[0])
    else:
        time["hr"] = 0
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

    def GetDay(self, day, group):
        days = self.tables[0][group]
        return days[DaysList[day]]

    def GetRoutine(self):
        tableId=1
        padding = 17
        if not CursesWindow.Hour24:
            padding = 22
        strings = [["LoadShedding Schedule"]]
        for table in self.tables:
            strings.append([""])
            strings.append(["Table #"+GetNumber(tableId)+":"])

            headings = ["Group".center(6)]
            for day in DaysList:
                headings.append(day.center(padding))
            strings.append(headings)
            #strings.append([""])
            for groupId, group in table.items():
                temp = GetNumber(groupId)
                timeId = 0
                while True:
                    substr = [temp.center(6)]
                    for day in DaysList:
                        substr.append(GetTimeString(group, day, timeId).center(padding))
                    if not any(':' in string for string in substr):
                        strings.append([""])
                        break
                    strings.append(substr)
                    timeId += 1
                    temp = " "
            tableId += 1
        return strings

def main(filename, group = -1, nepali = False, twelveHr = False):
    if group > -1:
        CursesWindow.Group = group
    if nepali:
        CursesWindow.Language = CursesWindow.Nepali
    if twelveHr:
        CursesWindow.Hour24 = False

    reader = RoutineReader()
    reader.ReadFile(filename)

    strings = reader.GetRoutine()
    width = 126
    if not CursesWindow.Hour24:
        width = 161
    height = len(strings) + 1
    day = (datetime.datetime.today().weekday() + 1) % 7 + 1
    
    heads = []
    highlightCells = []
    groups = []
    for i in range(0, len(strings)):
        if any(':' in string for string in strings[i]) and len(strings[i]) > 1:
            highlightCells.append([i, day])
            if not strings[i][0].isspace():
                groups.append(i)
        elif any('Group' in string for string in strings[i]):
            heads.append(i);

    window = CursesWindow.CursesWindow(strings, width, height, highlightCells, heads, groups)
    if window.refresh:
        main(filename)
        
if __name__ == "__main__":
    filename = "test.xml"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    main(filename)
