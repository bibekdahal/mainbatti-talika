#!/usr/bin/env python3

import sys
import RoutineReader
import re

class ArgumentError(Exception):
	def __init__(self,arg):
		self.arg = arg
	def display(self):
		print(''.join(self.args))

group_re = re.compile(r'^g[1-7]$')
time_re = re.compile(r'^(-twelve)|(--12)$')
lang_re = re.compile(r'^(-nepali)|(--n)$')
file_re = re.compile(r'^[a-z]+.xml$')

def IsGroup(input):
	return bool(group_re.match(input))

def IsTime(input):
	return bool(time_re.match(input))

def IsNepali(input):
	return bool(lang_re.match(input))

def IsXML(input):
	return bool(file_re.match(input))

def ArgumentParser():
	arguments = sys.argv[1::]
	filename = None
	group = -1
	twelveHr = False
	nepali = False
	for arg in arguments:
		try:
			if IsGroup(arg):
				group = int(arg[1])
				print(group)
			elif IsTime(arg):
				twelveHr = True
				print(arg)
			elif IsNepali(arg):
				nepali = True
				print(arg)
			elif IsXML(arg):
				filename = arg
				print(arg)
			else:
				raise ArgumentError("invalid arguments ... cannot load :D")
		except ArgumentError as e:
			e.display()
			return
	
	try:
		if not filename:
			raise ArgumentError("Invalid filename ... cannot laod :D")
		else:
			RoutineReader.main(filename, group, nepali, twelveHr)
	except ArgumentError as e:
		e.display()



def main():
	#RoutineReader.main("test.xml")
	ArgumentParser()

if __name__=="__main__":
	main()