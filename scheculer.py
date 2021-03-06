#!/usr/bin/env python

## scheduler.py
# Class schedule generator

from itertools import *

import scraper

def conflicts(c1, c2):
    for cl1, cl2 in product(c1['classes'], c2['classes']):
        # See if the days collide
        if any(d1 == d2 for d1 in cl1['days'] for d2 in cl2['days']):
            t1, t2 = cl1['times'], cl2['times']
            # See if the times overlap
            # (start1 before end2 and end1 after start2)
            if t1[0] <= t2[1] and t1[1] >= t2[0]:
                return True

    return False


def print_schedules(all_courses, names):
    # Filter courses to those with ids in the names parameter (combination of
    # the departement and the course number).
    courses = \
        filter(lambda c: c['departement'] + c['number'] in names, all_courses)

    # Take one section of each course
    # (The iterators are turned into lists so that iterating over them doesn't
    # consume them)
    for possible in map(list, product(*sections)):
        # Make sure no pair conflicts
        if not any(conflicts(c1, c2) for c1, c2 in combinations(possible, 2)):
            for c in possible:
                print(c['id'], end=', ')
            print()


# main() function for executing the scraper locally
# TODO Remove this once the project is more stable
import sys
def main(argv):
    username = argv[0]
    password = argv[1]

    # TODO Figure out what terms are valid
    # (19 is Fall 2017)
    # (27 is Fall 2018)
    term = len(argv) > 2 and argv[2] or 27

    print('Retrieving courses')
    global all_courses
    all_courses = scrape_courses(username, password, term)

    print('Input desired courses (separated by newlines): ')
    desired = []
    while True:
        name = input().strip()
        if name:
            desired.append(name)
        else:
            break

    print('Possible schedules:')
    print_schedules(all_courses, desired)

if __name__ == '__main__':
    main(sys.argv[1:])

