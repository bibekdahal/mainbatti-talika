from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
from ElementTree_Pretty import prettify
import xml.etree.ElementTree as ElemTree
from RoutineInput import *
from collections import deque

def PrintQueue(queue):
	for item in queue:
		print(item)

def CreateGroupList(schedule):
	queue = deque()
	for day in days:
		queue.append(schedule[day])

	queue_backup = queue
	inputid = int(schedule['id'])
	groups = [{}] * 7
	groups[inputid-1] = schedule

	for id in range(inputid+1,8):
		queue.rotate(1)
		routine = {}
		routine['id'] = str(id)
		for i in range(0,7):
			routine[days[i]] = queue[i]
		groups[id-1] = routine

	for id in range(inputid-1,0, -1):
		queue_backup.rotate(-1)
		routine = {}
		routine['id'] = str(id)
		for i in range(0,7):
			routine[days[i]] = queue_backup[i]
		groups[id-1] = routine

	return groups


def GenerateGroupTable(schedule):
	Table = Element("Table")
	Group = Element("Group")
	Group.attrib["id"] = schedule["id"]
	Table.append(Group)
	Day = [ Element(day) for day in days]

	for i in range(len(Day)):
		scheduletime = schedule[days[i]]
		for sch in scheduletime:
			time = Element("Time") 
			time.attrib["start"] = sch[0]
			time.attrib["end"] = sch[1]
			Day[i].append(time)
	Group.extend(Day)
	return Table

def main():
	schedule = InputRoutine()

	if schedule:
		root = Element('Routine')
		tree = ElementTree(root)
		grouplist = CreateGroupList(schedule)

		for group in grouplist:
			Table = GenerateGroupTable(group)
			root.append(Table)

		xml = prettify(root)
		with open("test.xml","w") as routine:
			for line in xml:
				routine.write(line)
				
if __name__=="__main__":
	main()