import os
import sys

if len(sys.argv) >= 2:
    basepath = sys.argv[1]
    directories = os.listdir(basepath)
else:
    basepath = None
    directories = os.listdir()

directories.sort()

path = basepath + '/.git/logs/refs'

refs = os.listdir(path)

if refs.__contains__('heads') & refs.__contains__('remotes'):
    reftype = input('Would you like data for heads or remotes? (H/r) ')
    if reftype.lower() == 'r':
        path += '/remotes'
        raise Exception('Sorry, this feature is not available right now. Please only use data from heads.')
    else:
        path += '/heads'
elif refs.__contains__('heads'):
    print('Fetching data for heads...')
    path += '/heads'
elif refs.__contains__('remotes'):
    print('Fetching data for remotes...')
    path += '/remotes'
    raise Exception('Sorry, this feature is not available right now. Please only use data from heads.')
else:
    raise Exception('Unrecognized file structure')

branches = os.listdir(path)

print(f'Gathering data from the following branches: {branches}')

for branch in branches:
    f = open(path + '/' + branch, "r")
    lines = f.read().splitlines()
    for line in lines:
        print(line.split(' '))
    print('========================================')