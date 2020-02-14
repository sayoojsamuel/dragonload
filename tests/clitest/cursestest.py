#!/usr/bin/env python3

import curses
import time

#   stdscr = curses.initscr()
#
#   # InitiateScreen
#   curses.noecho()
#   curses.cbreak()
#   curses.curse_set(0)
#   stdscr.keypad(True)
#
#   stdscr.addstr(5, 5, "Hello!")
#   stdscr.refresh()
#   time.sleep(2)
#   # RollBack to default
#   curses.echo()
#   curses.nocbreak()
#   curses.curse_set(1)
#   stdscr.keypad(False)
#
#   curses.endwin()

menu = ['Join Room', 'Add Download Link', 'Start Download', 'Exit']

def getWindowCenter(stdscr, text=""):
    h, w = stdscr.getmaxyx()
    x = w//2 - len(text)//2
    y = h//2
    return y, x

def printMenu(stdscr, selected_row_idx):
    stdscr.clear()
    wy, wx = getWindowCenter(stdscr) # Return Screen Center

    for idx, row in enumerate(menu):
        x = wx - len(row)//2
        y = wy - len(menu) + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row = 0
    printMenu(stdscr, current_row)

    while 1:

        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_DOWN:
            current_row = (current_row+1)  % len(menu)
            print
        elif key == curses.KEY_UP:
            current_row = (current_row-1)  % len(menu)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.addstr("You are now in {}".format(menu[current_row]))
            stdscr.refresh()
            stdscr.getch()
            if current_row == menu.index('Exit'):
                break

        printMenu(stdscr, current_row)
        #stdscr.attron(curses.color_pair(1))
        #testText = "Hello World"
        #y, x = getWindowCenter(stdscr, testText)
        #stdscr.addstr(y, x, testText)
        #stdscr.attroff(curses.color_pair(1))
        #time.sleep(1)


   
curses.wrapper(main)
