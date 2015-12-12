#!/usr/bin/env python3

import requests, re
from bs4 import BeautifulSoup
from collections import OrderedDict

days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
compiled_re = re.compile(r"[0-9]{2}:[0-9]{2}-[0-9]{2}:[0-9]{2}")

class ManualError(Exception):
    def __init__(self, args):
        self.args = args
    def display(self):
        print(''.join(self.args))

def check_update(new_content):
    # return True if new update else False
    old = None
    try:
        old = open('routine.html', 'r')
        old_content = old.read()
        return bool(old_content == new_content)
    except FileNotFoundError:
        print("file doesnot exist")
        old = open('routine.html', 'w')
        old.write(new_content)

def extract_time(text):
    return compiled_re.findall(text)

def scrap_routine2(url):
    """
    returns a dictionary whose key is group number for routine as:
    Each value in dictionary is another dictionary whose key is day and value is list of loadshedding time
    ['1'] = {'Sunday' : [time1, time2], 'Monday' : [time1, time2], ....}
    and so on
    """
    # uses myrepublica's routine
    # store the result
    result = {}
    response = requests.get(url)
    # try:
    if response.status_code != 200:
        raise ManualError("error fetching, please check your connection perhaps...")
    else:
        # root extractor
        extractor = BeautifulSoup(response.content, "html.parser")
        # there are 2 tables in the site, first is of routine
        table = extractor.select('table')
        routine_table = table[0]
        routine_data = routine_table.find_all('tr')[1::]
        for group, tr in enumerate(routine_data):
            routine = OrderedDict()
            td_list = tr.find_all('td')
            days_index = 0
            for td in td_list:
                time_list = extract_time(td.get_text())
                if time_list:
                    routine[days[days_index]] = time_list
                    days_index += 1
            result[str(group+1)] = routine
    print(result)
    return result

def scrap_routine(url):
    """
    returns a dictionary whose key is group number for routine as:
    Each value in dictionary is another dictionary whose key is day and value is list of loadshedding time
    ['1'] = {'Sunday' : [time1, time2], 'Monday' : [time1, time2], ....}
    and so on
    """
    # store the result
    result = {}
    response = requests.get(url)
    # try:
    if response.status_code != 200:
        raise ManualError("error fetching, please check your connection perhaps...")
    else:
        # root extractor
        extractor = BeautifulSoup(response.content, "html.parser")
        # get the data <li>; here 7 in this html
        data = (extractor.select(".column-2")[0]).find_all(['li'])[1:]

        # iterate over li
        for group, li in enumerate(data):
            # get all the divs within li that is contain time information
            divs = li.find_all(['div'])

            # iterate over all the divs
            # every div is for a specific day
            # time separated by <br> tag
            day_index = 0
            routine = OrderedDict()
            for div in divs:
                # get the 
                time_list= [str(x) for x in div.contents if str(x)!='<br/>' ]
                routine[days[day_index]] = time_list
                day_index += 1
            result[str(group+1)] = routine

    # except ManualError as merr:
    #     merr.display()
    #     return {}
    return result

def write_xml(routine):
    output = open("routine.xml", "w")
    output.write('<?xml version="1.0" ?>\n')
    output.write('<Routine>\n')
    output.write('<Table>\n')
    for group in routine:
        output.write('<Group id="{0}">\n'.format(group))
        group_data = routine[group]
        for day in group_data:
            output.write('<{0}>\n'.format(day))
            for time in group_data[day]:
                splitted = time.split('-')
                output.write('<Time end="{0}" start="{1}"/>\n'.format(splitted[1], splitted[0]))
            output.write('</{0}>\n'.format(day))
        output.write('</Group>\n')

    output.write('</Table>\n')
    output.write('</Routine>\n')
    output.close()

def display_test(routine):
    for group in routine:
        group_data = routine[group]
        print(group)
        for day in group_data:
            print(day, group_data[day])
        print('-'*40)

def main():
    # check_new("hello")
    #url = "http://battigayo.com/schedule"
    url = "http://myrepublica.com/load-shedding.html"
    #routine = scrap_routine(url)
    routine = scrap_routine2(url)
    #display_test(routine)
    write_xml(routine)

if __name__=="__main__":
    main()

