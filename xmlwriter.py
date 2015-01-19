from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
from ElementTree_Pretty import prettify
import xml.etree.ElementTree as ElemTree

days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

class InputError(Exception):
	def __init__(self, arg):
		self.args = arg
	def display(self):
		print(''.join(self.args))

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
			time.attrib["end"] = sch[1]
			time.attrib["start"] = sch[0]
			Day[i].append(time)
	Group.extend(Day)
	return Table

"""Returns a dict as:
	['id'] = ""
	['Sunday'] = [[1,2], [3,4]]
	['Monday'] = [[5,6]]
"""

def InputRoutine():
	routine = {}
	try:
		id = input("Which Group ? : ")
		if int(id)<1 or int(id) >7:
			raise InputError("Invalid Group ID")
		else:
			routine['id'] = id
	except InputError as e:
		e.display()
		return {}
	else: 
		print("yay")

	for day in days:
		routine[day] = []
		fin = False
		while not fin:
			print(day, ":")
			start = input("Enter start time : ")
			end = input("Etner end time : ")
			time = [start,end]
			routine[day].append(time)
			select = input("Add another?(y/n) : ")
			if select == 'n':
				fin = True
	return routine


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