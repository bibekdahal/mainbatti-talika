# Mainbatti Talika

## About
Mainbatti Talika is a simple application to view loadshedding schedule on terminal. It is written in python and needs Python3 to run.

## Usage
Mainbatti Talika can be run from terminal by executing the python script "mainbatti-talika.py".

Simply run `mainbatti-talika.py` from a linux terminal to view the loadshedding schedule with default settings. For custom settings, you can provide additional parameters.

##### Optional Parameters
`mainbatti-talika.py [<filename>] [g<N>] [-nepali]/[--n] [-twelve]/[--12]`

*`filename`*
Specifies the XML file where the loadshedding schedule is stored. This file is read by the application and displayed in tabular format on the terminal.

*`g<N>`*
Specifies a group number. The routine of this particular group is highlighted.

*`-nepali`* or *`--n`*
Specifies that Nepali language should be used to display the time. Note that unicode must be supported by the terminal for this option to work.

*`-twelve`* or *`--12`*
Specifies that 12-hour format should be used to display the time.

###### Examples
`mainbatti-talika.py g4 -n --12`

This will display the schedule using nepali numerals and twelve hour time format. Schedule of Group-4 is highlighted

`mainbatti-talika.py routine.xml`

This will display the schedule described in file *`routine.xml`*.

#### Inside the application
Following commands are available when the application is running.
* Hit 't' to toggle the time format between 12-hour and 24-hour formats
* Hit 'n' to display the schedule in Nepali
* Hit 'e' to display the schedule in English
* Hit 'c' to toggle the background of terminal between transparent and opaque. This only works if terminal is currently using a transparent background
* Hit any of the number keys: '1', '2', ..., '7'  to change ground number. The schedule of that particular group is highlighted.
* Use the arrow keys or 'h', 'j', 'k', 'l' keys to scroll the window if all schedule is not visible

## Default Settings
The default settings are stored in JSON format in the file *`config.json`*.

Currently only following settings are supported:
* Group - The default group number
* Language - English/Nepali
* Twelve-Hour - Boolean value specifying whether or not to use the 12-hour format

Example config.json:
```
{
    "Group" : 4,
    "Language" : Nepali,
    "Twelve-Hour" : false
}
```
These settings can also be changed through the GUI python application *`configUI.py`*.

## GTK AppIndicator
An app-indicator for GNOME is also available. The python script *`mainbatti-indicator.py`* can be executed to start the indicator. In Ubuntu, the indicator may be set up to auto-start by adding this python script to the Startup Applications.

1. Open Dash
2. Search for Startup Applications
3. Click Add
4. Enter "Mainbatti Talika" for Name and browse and select "mainbatti-indicator.py" for command
5. Click Add
6. Log out and log in back to check if the app indicator works

