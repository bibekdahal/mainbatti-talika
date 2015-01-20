import re

days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

class InputError(Exception):
	def __init__(self, arg):
		self.args = arg
	def display(self):
		print(''.join(self.args))

#remove all  spaces within a string
def RemoveWhiteSpace(string):
	return ('' . join( re.sub(r'\s+', "", string) ) )

def IsTimeFormat(inputtime):
	inputtime = RemoveWhiteSpace(inputtime)
	time_re = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')
	return bool(time_re.match(inputtime))

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
			try:
				start = input("Enter start time [HH:MM] : ")
				end = input("Etner end time [HH:MM] : ")
				if not IsTimeFormat(start):
					raise InputError("Invalid time input")
				elif not IsTimeFormat(end):
					raise InputError("Invalid time input")
				else:
					time = [RemoveWhiteSpace(start), RemoveWhiteSpace(end)]
					routine[day].append(time)
				select = input("Add another?(y/n) : ")
				if select == 'n':
					fin = True
			except InputError as e:
				e.display()
				return {}
	return routine

def main():
	pass


if __name__=="__main__":
	main()