import os
import sys
import time

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

def isTimestamp(str):
    if str.isnumeric():
        if int(str) > 99999:
            return True
        else:
            return False
    else:
        return False

class Commit:
    def __init__(self, line):
        self.line = line
        linesplit = line.split(' ')
        self.parentcode = linesplit[0]
        self.code = linesplit[1]
        self.timestamp = int(next(filter(isTimestamp, linesplit)))

    def timeSinceCommit(self):
        t = int(time.time())
        return (t - self.timestamp)

    def commitedWithinLast(self, t):
        return self.timeSinceCommit() < t

withinLast = input('How many hours back do you want to get data for? (Default is last 12 hours): ')

if withinLast == '' or withinLast == None:
    withinLast = 60 * 60 * 12
else:
    withinLast = 60 * 60 * int(withinLast)

commitsToInclude = []

for branch in branches:
    # print(f'Data for branch \'{branch}\':')
    # print()
    f = open(path + '/' + branch, "r")
    lines = f.read().splitlines()
    for line in lines:
        c = Commit(line)
        # print(f'Commit Code: {c.code}')
        # print(f'Time since commit: {c.timeSinceCommit()}')
        # print(f'Commited within last {withinLast}: {c.commitedWithinLast(withinLast)}')
        # print()
        if c.commitedWithinLast(withinLast):
            commitsToInclude.append(c)
        commitsToInclude = list(dict.fromkeys(commitsToInclude))

commitCodesToInclude = []
for commit in commitsToInclude:
    commitCodesToInclude.append(commit.code[0:8])

print(f'Result ({len(commitCodesToInclude)}):')
print(', '.join(commitCodesToInclude))


