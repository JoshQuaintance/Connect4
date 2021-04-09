#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from init import init
from menu import Menu

# ! Getch get arrow keys
# from getch import getch
    # if (getch() == '\033'):
    #     x = getch() + getch()
    #     'A' = Up -> 'D' = Left

def main():
    init()
    menu = Menu()
    menu.print_title()
    menu.print_main_menu()
    print()


if __name__ == '__main__':
    main()
