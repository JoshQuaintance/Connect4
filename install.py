from sys import argv
from os import system

# Get the arguments
modules = argv[1:]

def prettify(modules):
    ending_amount = len([x for x in modules if x == '[end]'])

    last_found_ending = 0

    for i in range(ending_amount):
        # ! TODO : GET THE ENDINGS AND ADD NEWLINES AFTER EVERY SINGLE ONE OF THEM
        # ! TODO : GET THE ENDINGS AND ADD NEWLINES AFTER EVERY SINGLE ONE OF THEM
        # ! TODO : GET THE ENDINGS AND ADD NEWLINES AFTER EVERY SINGLE ONE OF THEM
        # ! TODO : GET THE ENDINGS AND ADD NEWLINES AFTER EVERY SINGLE ONE OF THEM
        # ! TODO : GET THE ENDINGS AND ADD NEWLINES AFTER EVERY SINGLE ONE OF THEM
        # ! TODO : GET THE ENDINGS AND ADD NEWLINES AFTER EVERY SINGLE ONE OF THEM
        # ! TODO : GET THE ENDINGS AND ADD NEWLINES AFTER EVERY SINGLE ONE OF THEM
        # ! TODO : GET THE ENDINGS AND ADD NEWLINES AFTER EVERY SINGLE ONE OF THEM
        # ! TODO : GET THE ENDINGS AND ADD NEWLINES AFTER EVERY SINGLE ONE OF THEM
        current_ending_idx = ending_amount.index('[end]', last_found_ending)

        last_found_ending = current_ending_idx

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

    # Insert the new module
    content.insert(ending_idx, 'colorama')

    prettified = prettify(content)


write_modules()

# fout = open('./config.toml', 'w')

print(f'python -m pip install {" ".join(modules)}')
