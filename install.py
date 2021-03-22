#!/usr/bin/env python3

from sys import argv
from os import system
import requests

# Get the arguments
modules = argv[1:]

def prettify(modules):
    ending_amount = len([x for x in modules if x == '[end]'])

    last_found_ending = 0

    for i in range(ending_amount):
        
        current_ending_idx = modules.index('[end]', last_found_ending + 2)
        
        if (len(modules) <= current_ending_idx + 1 or modules[current_ending_idx + 1] != ''):

            last_found_ending = current_ending_idx 
            modules.insert(current_ending_idx + 1, '')

    return modules
    

def write_modules():
    print('Installing modules and adding it to dependencies.toml')

    # Open the file to read, create one if it doesn't exit
    fin = open('./config.toml', 'r+')

    # Read the content
    content = fin.read().split('\n')

    # Get starting index
    start_idx = content.index('[modules]')

    # Get the modules_end
    ending_idx = content.index('[end]', start_idx)

    modules_area = content[start_idx + 1 : ending_idx]

    # Loop through every modules
    for module in modules:
        print()
        print(f'Checking pip if \'{ module }\' is a real package ...')

        # Go to pypi's api and check if the module exist
        response = requests.get(f'https://pypi.python.org/pypi/{module}/json')
        
        # If we the status code we got back is not 200
        if response.status_code != 200:
            print(f'The module \'{ module }\' does not exist in pip\'s database.')
            print('Make sure you check if your spelling is correct!')
            continue

        print('Module exist, continuing process ...')

        # If the module exist
        if (module in modules_area):
            # Inform user
            print(f'The module \'{ module }\' already exist in dependencies, ignoring...')
            continue

        # If the module doesn't exist in the dependencies
        else:
            content.insert(ending_idx, module)

    # Prettify the string
    prettified = prettify(content)

    # Join the string together
    formatted = '\n'.join(prettified)

    # file output
    fout = open('./config.toml', 'w')

    fout.write(formatted)



write_modules()


print(f'python -m pip install {" ".join(modules)}')
