import curses

nepaliDigits = [ '०', '१', '२', '३', '४', '५', '६', '७', '८', '९' ]

def Nepali(number):
    if number==0:
        return nepaliDigits[0]
    n = number
    text = '';
    while (n != 0):
        text = nepaliDigits[n%10] + text
        n = int(n/10)
    return text

def English(number):
    return str(number)

Language = English

def GetNumber(number):
    return Language(number)

Hour24 = True
TerminalColors = True
Group = -1

class CursesWindow:
    def __init__(self, strings, width, height, highlights, headrows, groups):
        self.strings = strings
        self.width = width
        self.height = height
        self.posX = 0
        self.posY = 0
        self.hlts = highlights
        self.heads = headrows
        self.groups = groups
        self.Language = English
        self.refresh = False
        curses.wrapper(self.main)

    def main(self, screen):
        global Language
        global Hour24
        global Group
        global TerminalColors

        curses.use_default_colors()
        back = curses.COLOR_BLACK
        if TerminalColors:
            back = -1
        
        curses.init_pair(1, curses.COLOR_YELLOW, back)
        curses.init_pair(2, -1, back)
        screen.bkgd(curses.color_pair(2))
        screen.clear()
        self.window = curses.newpad(self.height, self.width)
        self.window.bkgd(curses.color_pair(2))
#        curses.init_pair(2, curses.COLOR_GREEN, back)
        i = 0
        extras = 0
        for row in self.strings:
            j = 0
            for string in row:
                if i in self.groups:
                    if self.groups.index(i) == Group-1:
                        extras = curses.A_BOLD | curses.color_pair(1)
                    else:
                        extras = 0
                if [i,j] in self.hlts:
                    self.window.addstr(string, curses.color_pair(1) | extras)
                else:
                    if i in self.heads:
                        self.window.addstr(string, curses.A_BOLD | curses.A_REVERSE)
                    else:
                        self.window.addstr(string, extras)
                j += 1
            self.window.addstr('\n')
            i += 1

        self.window.keypad(True)
        self.screen = screen
    
        self.scroll()
        while (True):
            event = self.window.getch()
            if event == ord('q'):
                self.refresh = False
                break
            elif event == ord('n'):
                Language = Nepali
                self.refresh = True
                break
            elif event == ord('e'):
                Language = English
                self.refresh = True
                break
            elif event == ord('t'):
                Hour24 = not Hour24
                self.refresh = True
                break
            elif event == ord('c'):
                TerminalColors = not TerminalColors
                self.refresh = True
                break
            elif event >= ord('0') and event <= ord('9'):
                Group = event - ord('0')
                self.refresh = True
                break
            elif event == ord('l') or event == curses.KEY_RIGHT:
                height, width = self.screen.getmaxyx()
                if self.posX+1+width < self.width:
                    self.posX += 1
            elif event == ord('h') or event == curses.KEY_LEFT:
                height, width = self.screen.getmaxyx()
                if self.posX-1 >= 0:
                    self.posX -= 1
            elif event == ord('k') or event == curses.KEY_UP:
                height, width = self.screen.getmaxyx()
                if self.posY-1 >= 0:
                    self.posY -= 1
            elif event == ord('j') or event == curses.KEY_DOWN:
                height, width = self.screen.getmaxyx()
                if self.posY+1+height < self.height:
                    self.posY += 1
            
            self.scroll()
    
    def scroll(self):
        height, width = self.screen.getmaxyx()
        self.window.refresh(self.posY, self.posX, 0, 0, height-1, width-1)
    


