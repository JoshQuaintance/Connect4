from colorama import init
from time import sleep
import sys
from os import system

init()

def print_at (y, x, s):
    print("\033[%d;%dH%s" % (y, x, s))

def main():
    system('cls')
    print('Hello')
    # sleep(1)
    print_at(1, 1, 'Hello World')
    # print('hello')

if __name__ == "__main__":
    main()