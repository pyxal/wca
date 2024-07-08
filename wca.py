#!/bin/bash/python3

#
# WCA Championship competitor listing
#

# imports
from sys import argv
from requests import get
from urllib3 import disable_warnings, exceptions
from re import search as rxSearch
from datetime import date
from colorama import init as c_init, Fore as c, Style as c_s
from tabulate import tabulate
disable_warnings(exceptions.InsecureRequestWarning)
c_init()


# set year
year = str(date.today().year)

# sort argv
championship = 'DanishChampionship' + year
size = '333'
if len(argv) > 1:
    for arg in argv:
        if arg.isnumeric(): size = str(arg[0]*3)
        elif arg.isalpha():
            if arg.lower() in ['em', 'ec', 'euro']: championship = 'Euro' + year
            elif arg.lower() in ['wm', 'wc', 'worlds']: championship = 'WC' + year


#if championship == 'comListRequest':


# set legends arr
legends = [
    'Ciarán Beahan',
    'Feliks Zemdegs',
    'Kevin Hays',
    'Leo Borromeo',
    'Max Park',
    'Patrick Ponce',
    'Ruihang Xu',
    'Sebastian Weyer',
    'Tymon Kolasiński',
    'Yiheng Wang',
    'Yusheng Du'
]

# set yc arr
youCubers = [
    'Dylan Wang',
    'Milan Struyf'
]


# get source
pageSource = get('https://www.worldcubeassociation.org/competitions/' + championship + '/registrations/psych-sheet/' + size, verify=False).text.splitlines()

# get competition name
competitionName = ''
competitionNameRxPattern = r'for\s(.*?)(?=\s\|)'
for line in pageSource:
    if line.find('<title>') > -1:
        competitionName = rxSearch(competitionNameRxPattern, line)[0].strip().lstrip('for').strip().replace('&#39;', "'")
        break

# get competitors
competitorTable = [['#', 'Name', 'WCA ID', 'Citizen of', 'Average', 'WR', 'Single', 'WR']]
competitors = {'#':[], 'names':[], 'wcaids':[], 'countries':[], 'avgs':[], 'avgwrs':[], 'singles':[], 'singleswrs':[]}
competitorRxPattern = r'^([^()]+)'

# populate competitors arr
for i, line in enumerate(pageSource):
    
    if line.find('<td class="name">') > -1:
        competitors['#'].append(len(competitors['names'])+1)
        name = rxSearch(competitorRxPattern, pageSource[i][27:-5])[0].strip()
        if name not in legends and name not in youCubers: competitors['names'].append(name)
        elif name in legends: competitors['names'].append(f'{c.RED}{name}{c_s.RESET_ALL}')
        elif name in youCubers: competitors['names'].append(f'{c.GREEN}{name}{c_s.RESET_ALL}')
        #competitors['names'].append(name if name not in legends else f'{c.RED}{name}{c_s.RESET_ALL}')
    
    elif line.find('<td class="wca-id">') > -1:             competitors['wcaids'].append(pageSource[i+1][101:-11])
    elif line.find('<td class="country">') > -1:            competitors['countries'].append(pageSource[i][30:-5])
    elif line.find('<td class="average">') > -1:            competitors['avgs'].append(pageSource[i][30:-5])
    elif line.find('<td class="world-rank-average">') > -1: competitors['avgwrs'].append(pageSource[i][41:-5])
    elif line.find('<td class="single">') > -1:             competitors['singles'].append(pageSource[i][29:-5])
    elif line.find('<td class="world-rank-single">') > -1:  competitors['singleswrs'].append(pageSource[i][40:-5])

    #if len(competitors['#']) == 100: break


# populate table
for i, competitor in enumerate(competitors['names']):
    competitorTable.append([competitors['#'][i], competitors['names'][i], competitors['wcaids'][i], competitors['countries'][i], competitors['avgs'][i], competitors['avgwrs'][i], competitors['singles'][i], competitors['singleswrs'][i]])


# print competition
print(f'\n{competitionName}\n')

# print table
print(tabulate(competitorTable, headers='firstrow', tablefmt='fancy_grid'))
