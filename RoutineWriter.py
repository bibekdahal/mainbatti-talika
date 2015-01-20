from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
from ElementTree_Pretty import prettify
import xml.etree.ElementTree as ElemTree
from RoutineInput import *

days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

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
	root = Element('Routine')
	tree = ElementTree(root)

	if schedule:
		Table = GenerateGroupTable(schedule)
		root.append(Table)
		xml = prettify(root)
		with open("test.xml","w") as routine:
			for line in xml:
				routine.write(line)
				
if __name__=="__main__":
	main()