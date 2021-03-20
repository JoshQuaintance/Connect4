import sys

from colorama import init
from termcolor import colored

# colorama initialization for windows
init()


def err(*values, sep: str = ' ', end: str = '\n', flush: bool = False):
    print(colored(values, 'red'), sep=sep, end=end, flush=flush)

def warn(*values, sep: str = ' ', end: str = '\n', flush: bool = False):
    print(colored(values, 'yellow'), sep=sep, end=end, flush=flush)

def info(*values, sep: str = ' ', end: str = '\n', flush: bool = False):
    print(colored(values, 'blue'), sep=sep, end=end, flush=flush)

def good(*values, sep: str = ' ', end: str = '\n', flush: bool = False):
    print(colored(values, 'green'), sep=sep, end=end, flush=flush)