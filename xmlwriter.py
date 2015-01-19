from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
from ElementTree_Pretty import prettify
import xml.etree.ElementTree as ElemTree

days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def GenerateTable(id):
	Table = Element("Table")
	Group = Element("Group")
	Group.attrib["id"] = str(id)
	Table.append(Group)
	Day = [ Element(day) for day in days]

	for i in range(len(Day)):
		time = Element("Time")
		time.attrib["start"] = "12:00"
		time.attrib["end"] = "12:00"
		Day[i].append(time)
	Group.extend(Day)
	return Table



def main():
	root = Element('Routine')
	tree = ElementTree(root)

	#id = int(input("Enter group : "))

	Table = GenerateTable(1)
	root.append(Table)

	xml = prettify(root)
	#print(prettify(root))
	with open("test.xml","w") as routine:
		for line in xml:
			routine.write(line)

if __name__=="__main__":
	main()